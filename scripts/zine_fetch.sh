#!/bin/bash
# zine_fetch.sh — fetch all data the zine card needs, write to ./out/zine.json.
# Run from repo root (CI: actions/checkout). Requires GH_TOKEN with public-repo read.
set -euo pipefail

OUT_DIR="${OUT_DIR:-out}"
mkdir -p "$OUT_DIR"

# 1. Calendar + canonical totals + repos-with-contributed-commits, one GraphQL call.
gh api graphql -f query='query{ user(login:"lingion"){
  createdAt
  contributionsCollection{
    totalCommitContributions
    totalPullRequestContributions
    totalIssueContributions
    commitContributionsByRepository(maxRepositories:100){
      repository{ nameWithOwner }
    }
    contributionCalendar{
      totalContributions
      weeks{ contributionDays{ date contributionCount color } }
    }
  }
}}' > "$OUT_DIR/graphql.json"

# 2. Stars across lingion's own non-fork repos (separate call so the calendar query stays small).
gh api graphql -f query='query{ user(login:"lingion"){
  repositories(first:100,ownerAffiliations:OWNER,isFork:false){
    nodes{ stargazerCount }
  }
}}' > "$OUT_DIR/stars.json"

# 3. Aggregate into the flat shape render_zine.py expects.
python3 - <<'PY' > "$OUT_DIR/zine.json"
import json
g = json.load(open("out/graphql.json"))
s = json.load(open("out/stars.json"))
u = g["data"]["user"]
cc = u["contributionsCollection"]
repos = cc["commitContributionsByRepository"]
stars = sum(n["stargazerCount"] for n in s["data"]["user"]["repositories"]["nodes"])
out = {
    "user": {"createdAt": u["createdAt"]},
    "calendar": cc["contributionCalendar"],
    "totals": {
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "issues": cc["totalIssueContributions"],
        # Repos contributed = distinct non-empty entries from the contributions API.
        # This includes private ones the user has access to, matching the GitHub profile ring.
        "repos": len([r for r in repos if r.get("repository")]),
    },
    "stars": stars,
}
print(json.dumps(out))
PY

echo "zine.json: total=$(python3 -c "import json;print(json.load(open('out/zine.json'))['calendar']['totalContributions'])") commits=$(python3 -c "import json;print(json.load(open('out/zine.json'))['totals']['commits'])") stars=$(python3 -c "import json;print(json.load(open('out/zine.json'))['stars'])")"
