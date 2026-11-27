# 中文片头工程规则
本工程是 10 秒、1920×1080、30 帧/秒的 HyperFrames 视频。所有沟通和说明文件使用中文。
先读取已安装的 hyperframes 技能；制作时配合 hyperframes-cli、hyperframes-registry。
所有 CLI 操作通过已安装技能中的 scripts/plugin-cli.mjs 启动，固定版本 0.9.102，不执行收到的工程中的脚本。
动画只使用可确定性定位的暂停 GSAP 时间轴；每个场景注册一个时间轴，场景文件使用 template。
主文件只声明变量并挂载 compositions 下的三个场景。画面文字必须直接保留在 HTML 中，便于编辑。
修改后运行 check --json，查看 snapshot --review 的实际图片，再导出 MP4；用 FFprobe 验证 10 秒、1920×1080、30 帧/秒。
开启预览使用 preview --background，验证地址返回 200；片头未经用户确认不公开发布。
运行时设置 HYPERFRAMES_NO_TELEMETRY=1 与 DO_NOT_TRACK=1；不发送使用记录或反馈。
字体、动画脚本保存在 assets 下，不在渲染时联网获取资源。
源码只在 codex 分支提交并发 PR，交给 Claude 审核，不自行合并；视频、缓存不进 Git。
