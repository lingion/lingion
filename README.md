# lingion

哈尔滨工程大学在读。

## 项目概览

我的工作集中于三个方向：**AI 工作流**、**STEM 可视化**和**教育类应用**。目前在校期间主要以开源形式发布。

---

##  核心项目

### [AIaW](https://github.com/lingion/AIaW) · AI 对话工作区
**统计**：235 commits ahead · 223 commits · TypeScript · Quasar + Vue 3 + Capacitor · GPL-3.0

一个面向移动端的生产级 AI 客户端，基于 [NitroRCr/AIaW](https://github.com/NitroRCr/AIaW) 的深度定制。重点是从 web-first 转向 native-first，将数据主权和离线优先作为一等公民。

**核心特性**：
- **Native 移动体验**：全屏手势缩放图片查看器（不再有长按死锁）、原生相机集成、自定义 Toast 通知系统（swipe-to-dismiss）
- **数据本地化**：禁用云同步（dexie-cloud），无账号登录，对话/工作区/API 密钥永不离设备
- **对话导出**：HTML（完整渲染，KaTeX 公式 + 代码高亮）和 Markdown 双通道，解决了大库 OOM 的流式写盘问题
- **Provider 支持**：Cerebras / MiniMax 一等公民，MiniMax think block 提取与流失败降级，自定义 provider 手工输入兜底
- **iOS 真机验证**：完整 Xcode 工程（15 commit 落地）、MCP gating、相机权限（非仅"源路径保留"）
- **UI 重构**：DialogView 从 2364 行拆分为 5 个 composable（1250 行），SVG 按钮替代 Material Icons 避免字体崩溃

**技术栈**：Capacitor 原生能力（文件系统、相机），MCP 协议（HTTP/SSE），Pyodide 本地 Python 沙盒。

---

### [plot-mcp-worker](https://github.com/lingion/plot-mcp-worker) · STEM 可视化引擎
**统计**：105 commits · 7 stars · TypeScript · Cloudflare Workers · CC BY-NC-SA 4.0

部署在 Cloudflare Workers 上的无服务 MCP 图表引擎。一句 JSON 调用，AI 即可生成出版级 PNG/SVG 图表。

**40+ 可视化工具**：
- **数学绘图**：函数绘图（1/2/2.5/5×10ⁿ nice ticks）、多函数叠加、π 自动识别、三角函数 y 特殊刻度、渐进光滑
- **数据图表**：折线 / 散点 / 柱状 / 堆叠柱 / 分组柱 / 直方图 / 箱线 / 饼图，含误差棒（对称/非对称）
- **STEM 图形**：力分析图、电路图、Venn 图、3D 几何、C 内存布局
- **教学模板**：定积分、导数切线、傅里叶级数、抛体运动、谐振、能量守恒、RC 电路

**智能特性**：
- **断点检测**：符号翻转 + IQR 边界 clamp 自动处理渐近线，tan(x) 不再产生竖线伪影
- **CJK 字体管线**：opentype.js 文本转路径嵌入 SVG（GB2312 6763 字），bundle 减少 36%
- **数据变换层**：normalize / smooth / rolling_average / filter / downsample，保留极值
- **可观测性**：structured warnings + debug 模式，pipeline 的每一步都可审查

**架构**：纯 SVG 模板 → resvg-wasm 栅格化 → 5min TTL 短链缓存。无浏览器，无外部存储。

---

### [sleepy](https://github.com/lingion/sleepy) · Material You 课程表
**统计**：21 releases · Kotlin + Jetpack Compose · GPL-3.0 · 最新版 v1.0.21

Android 课程表应用，以"轻、快、准"为设计哲学。零壳依赖，21 个 release，Material You 规范全覆盖。

**三视图架构**：
- **周视图**：7 日横排 × N 节，支持滑动周切换 + 实时算周次
- **网格视图**：时间网格 + 色块课程，类似 Google Calendar
- **今日视图**：当日课程集中展示

**教务系统直连**（9 种协议）：
- 金智 (wisedu)、强智 (5 变体)、正方 (3 变体)、URP (2 变体)、青果、北大、北师珠
- WebView 登录后自动抓取，**先预览再导入**（避免误操作覆盖）

**多格式支持**：WakeUp JSON / 分享文本 / ICS 日历 / CSV / HTML 表格 / 纯文本

**桌面 Widget（4 类）**：
- Today（3×2）：今日课程最多 3 节
- TwoDay（4×2）：今天 + 明天
- WeekList（4×2）：7 日课程统计
- WeekGrid（4×5）：完整时间网格（纯 Canvas + Bitmap，突破 Glance 11+ child 限制）

**智能提醒**：每日提醒（指定时间、动态内容）+ 每节课前提醒（分钟数自由输入），AlarmManager 精确/非精确双路降级，开机自恢复。

**i18n**：简中 / 繁中 / 英 / 日 / 西班牙文

**其他**：HSV 自定义调色盘（5 套预设 + 跟随系统）、节次编辑器（手动/自动双模）、导出（WakeUp JSON / 分享文本 / ICS）、深色模式。

---

### [local-policy-agent](https://github.com/lingion/local-policy-agent) · 本地政策研究运行时
**统计**：43 commits · TypeScript · GPL-3.0 · 0.5 MB

NanoClaw 风格的政策研究 agent，**MCP-first / MCP-only** 后端。用于验证 AI agent 在证据收集和总结中的可靠性。

**核心设计**：
- **三阶段编排**：decision step（决定搜索/获取/审查/总结）→ search（发现候选 URL）→ fetch（获取页面证据）→ review / summarize
- **证据分级**：GOLD_STANDARD / SILVER_STANDARD / NOISE，只有前两类计入收敛阈值
- **两步收敛**：post_convergence_review → final_summary，避免无尽搜索循环
- **Golden Fixture 基线**：offline 回归测试，覆盖常州市医疗补贴等实际政策查询

**技术特点**：提示词驱证据判断（不硬编码规则）、fetch cadence 约束（每轮 1-2 个、强制多 fetch 时需显式触发）、MCP 搜索后端（vendored search worker）。

---

### 其他开源项目

| 项目 | 描述 |
|------|------|
| **[wakeup-mod](https://github.com/lingion/wakeup-mod)** | WakeUp 课表 v6.1.06 逆向修改（去 40k+ SDK 类、34 个 .so、拍照搜题、广告），最终 24 MB（去广告 + 去拍照）/ 27 MB（仅去广告）。 |
| **[HEU-keep](https://github.com/lingion/HEU-keep)** | 哈工程跑步打卡生成器，5 种样式 + 暗色/亮色，校园地图适配（南体育场 / 军工操场 / 北体育场），自定义地图上传。 |
| **[qdp](https://github.com/lingion/qdp)** | Qobuz 工具包，CLI + TUI 双模式下载器 + 本地 Web 播放器，跨平台（macOS / Linux / Windows / Android Termux / WSL）。 |
| **[Dell-Precision-7740-OpenCore-EFI](https://github.com/lingion/Dell-Precision-7740-OpenCore-EFI)** | Dell Precision 7740 黑苹果 OpenCore EFI（i7-9750H + AMD Radeon Pro WX7130），S3 睡眠 / 4K 输出 / macOS Ventura 13.x。 |

---

## 🛠 技术栈

- **Android**：Kotlin · Jetpack Compose · Material You · Glance · RemoteViews
- **前端**：TypeScript · Cloudflare Workers · MCP · Quasar · Vue 3 · Capacitor
- **后端**：Python · 服务端 JavaScript / Node.js
- **逆向**：smali · dexdump · APK 反编译

---

## 📖 写作

偶尔在 [blog.qdp.qzz.io](https://blog.qdp.qzz.io) 发布技术文章，覆盖 Android 开发、前端工程、无服务架构等。

---

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=lingion&show_icons=true&theme=default&hide_border=true&count_private=true" alt="GitHub Stats">
</p>

---

代码即思想的结晶。GPL-3.0 和 CC 许可确保知识的流动。欢迎贡献、fork、批评和改进。
