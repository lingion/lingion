# lingion

哈尔滨工程大学在读。

课表 app 有广告、AI 对话客户端移动端体验差、给 AI agent 画图的工具不够灵活——于是自己写了。

## 仓库

### [AIaW](https://github.com/lingion/AIaW) (fork · 235 commits ahead)
AI 对话客户端 [NitroRCr/AIaW](https://github.com/NitroRCr/AIaW) 的移动端原生 fork（Quasar + Vue 3 + Capacitor）。仓库大小 47 MB，TypeScript 主导。
- **iOS 落地**：添加完整 Xcode 工程（15 个 commit 一次性落）+ Capacitor iOS 兼容性硬化（10+ 个 fix commit）
- **原生能力**：`@capacitor/camera` 集成（带 retry dialog）、本地文件系统（mobile localfs native workflow）
- **Provider 接入**：Cerebras + MiniMax 一等公民支持（stream 中断 fallback、think block 提取与合并、模型列表失败时的手工输入兜底）
- **导出管线**：HTML / Markdown / TXT 双通道，含 chunked capacitor 写盘防大库 OOM
- **图片沙盒**：pivot-point pinch-zoom + 时间戳文件名 + SVG 按钮（避免 Material Icons 字体崩溃）
- **UI 系统**：自研 GlobalToast（swipe-to-dismiss、success/fail 配色、1.2s 时长）
- **代码重构**：DialogView 5 个 composable 拆分（2364→1250 行）
- 协议：GPL-3.0

### [plot-mcp-worker](https://github.com/lingion/plot-mcp-worker)
Cloudflare Workers 上的 MCP 图表引擎（105 commit，7 star）。TypeScript。
- **40+ 可视化工具**：函数绘图 / 多函数叠加 / 数据序列 / 子图网格 / 力分析图 / 电路图 / 3D 几何 / Venn 图 / 教学模板
- **CJK 字体管线**：opentype.js 文本转路径嵌入 SVG（GB2312 6763 字，PingFang SC → Heiti SC，bundle -36%），KV 外置字体
- **智能坐标轴**：niceTicks（1/2/2.5/5×10ⁿ）、π 模式自动识别、trig y-special、IQR 边界 clamp
- **断点检测**：sign-flip + 大 Δy 触发路径断开
- **4 阶段演进**：3A 多图层叠加 → 3B 误差棒 → 3C subplot 网格 → 3D 数据变换层（normalize / smooth / filter / rolling_average / downsample）
- **渲染**：SVG → resvg-wasm → PNG
- 协议：CC BY-NC-SA 4.0

### [sleepy](https://github.com/lingion/sleepy)
Material You 设计的纯净 Android 课表 app，21 个 release。Kotlin + Jetpack Compose，76 MB。
- **9 种教务协议直连导入**：金智（wisedu）/ 强智 5 变体（qz / qz_old / qz_crazy / qz_br / qz_with_node）/ 正方 3 变体（zf / zf_1 / zf_new）/ URP 2 变体 / 青果 / 北大 / 北师珠
- **多格式文本导入**：WakeUp JSON / WakeUp 分享文本 / ICS 日历 / CSV / HTML 表格 / 纯文本
- **三视图**：周视图（7 日横排）/ 网格视图（时间网格 + 课程色块）/ 今日视图
- **桌面小组件 4 类**：Today / TwoDay / WeekList / WeekGrid（Glance + RemoteViews 双渲染管线）
- **HSV 自定义调色盘**：自绘 SV 面板 + 色相条；HSL 黄金角（137.5°）自动配色作 fallback
- **节次编辑器**：手动模式 + 自动模式（每节时长 + 总节数 + 课间模板）
- **i18n**：简中 / 繁中 / 英 / 日 / 西
- 协议：GPL-3.0

### [wakeup-mod](https://github.com/lingion/wakeup-mod)
WakeUp 课程表 v6.1.06（com.suda.yzune.wakeupschedule）逆向修改，104 MB。
- **完整剥离 40,000+ SDK 类**：快手（com/kwad）/ 字节跳动（com/bytedance）/ 百度（com/baidu）/ 腾讯 Bugly（com/tencent/bugly）/ QQ（com/qq/e）/ 作业帮（com/zybang.*）等
- **删除 34 个 .so 原生库**：libttmplayer / libdpsdk / libMNN / libcronet / libkwad / libBugly 等 → 不含 32-bit-only 限制，兼容 Android 16 arm64
- **拍照搜题完整移除**：~100 个 smali + 相机 SDK 桥接 + 5 个作业帮 Activity + 2 个权限 Activity + manifest 引用 + 业务代码引用全清
- **广告关闭**：OooOOOO.smali 两个广告开关改为 return false（开屏 + 热启动）
- **上游切断**：AboutActivity 点击"版本"不再请求 API
- **APK 大小**：24 MB（去广告 + 去拍照）/ 27 MB（仅去广告）
- ⚠️ 仅供学习与个人使用

### [local-policy-agent](https://github.com/lingion/local-policy-agent)
NanoClaw 风格本地策略研究运行时（TypeScript，0.5 MB，43 commit）。
- **三阶段编排**：decision step → search → fetch → review → summarize
- **MCP-first / MCP-only** 后端：vendor 搜索 MCP worker
- **证据等级分类**：GOLD_STANDARD / SILVER_STANDARD / NOISE
- **两步收敛**：post_convergence_review → final_summary，避免无尽搜索循环
- **Golden Fixture 回归基线**
- 协议：GPL-3.0

### [HEU-keep](https://github.com/lingion/HEU-keep)
Keep 风格跑步打卡生成器（哈工程定制），JavaScript，15 MB，75 commit。
- **5 种样式** + 暗色 / 亮色模式
- **HEU 校园地图适配**：南体育场 / 军工操场 / 北体育场
- **实时数据编辑 + 预览**
- **字体优化**：Heiti SC 替代 PingFang SC，bundle -36%
- 自定义地图上传 + 恢复默认

### [qdp](https://github.com/lingion/qdp)
Qobuz 工具包，Python，196 MB，21 commit。
- **CLI + TUI** 双模式下载器
- **本地 Web 播放器**
- **跨平台**：macOS / Linux / Windows / Android (Termux) / WSL
- **一键安装**（curl pipe bash）

### [Dell-Precision-7740-OpenCore-EFI](https://github.com/lingion/Dell-Precision-7740-OpenCore-EFI)
Dell Precision 7740 黑苹果 OpenCore EFI，ASL，34 MB。
- 硬件：i7-9750H + AMD Radeon Pro WX7130 混合显卡共存
- S3 睡眠 / 4K 输出
- macOS Ventura 13.x
- 三码占位（使用前自行生成填入 `EFI/OC/config.plist` → PlatformInfo → Generic）

## 技术栈

Android (Kotlin / Jetpack Compose · Material You · Glance · RemoteViews) · TypeScript (Cloudflare Workers · MCP · Quasar · Vue 3 · Capacitor) · Python · APK 逆向 (smali · dexdump)

偶尔在 [blog.qdp.qzz.io](https://blog.qdp.qzz.io) 写东西。

---

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=lingion&show_icons=true&theme=default&hide_border=true&count_private=true" alt="GitHub Stats">
</p>
