// zine-card worker
// Serves docs/zine.svg from lingion/lingion@main. Reads on every request,
// 6h edge cache. Falls back to ?via=gh-proxy when raw.githubusercontent is flaky.

const REPO = "lingion/lingion";
const BRANCH = "main";
const PATH = "docs/zine.svg";
// gh-proxy (private mirror) — used only as fallback. Source path of the API
// endpoint to hit for fallback.
const GH_PROXY_RAW = (path) =>
  `https://gh.qdp.qzz.io/${REPO}/raw/${BRANCH}/${path}`;
// raw.githubusercontent.com — primary, fails in some networks.
const RAW_DIRECT = `https://raw.githubusercontent.com/${REPO}/${BRANCH}/${PATH}`;

const CACHE = {
  browser: "public, max-age=21600", // 6h
  cdn: "public, max-age=14400, s-maxage=14400", // 4h CDN, 6h browser
};

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, OPTIONS",
  "access-control-allow-headers": "*",
};

async function fetchWithTimeout(url, timeoutMs) {
  const c = new AbortController();
  const t = setTimeout(() => c.abort(), timeoutMs);
  try {
    return await fetch(url, { signal: c.signal });
  } finally {
    clearTimeout(t);
  }
}

async function fetchUpstream() {
  // Try direct first (3s). On any failure or non-200, fall back to mirror (5s).
  for (const [label, url, budget] of [
    ["direct", RAW_DIRECT, 3000],
    ["mirror", GH_PROXY_RAW(PATH), 5000],
  ]) {
    try {
      const r = await fetchWithTimeout(url, budget);
      if (r.ok) {
        return { response: r, source: label };
      }
    } catch (_) {
      // continue to next
    }
  }
  return null;
}

export default {
  async fetch(request) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS });
    }
    const url = new URL(request.url);
    if (url.pathname === "/" || url.pathname === "") {
      return new Response(
        JSON.stringify({
          ok: true,
          service: "zine-card",
          path: "/" + PATH,
        }),
        {
          status: 200,
          headers: { "content-type": "application/json", ...CORS },
        }
      );
    }
    if (url.pathname !== "/" + PATH && url.pathname !== "/zine.svg") {
      return new Response("not found", { status: 404, headers: CORS });
    }

    const got = await fetchUpstream();
    if (!got) {
      return new Response("upstream unreachable", {
        status: 502,
        headers: CORS,
      });
    }
    const body = await got.response.text();
    const headers = {
      ...CORS,
      "content-type": "image/svg+xml; charset=utf-8",
      "cache-control": CACHE.cdn,
      "x-zine-source": got.source,
    };
    return new Response(body, { status: 200, headers });
  },
};
