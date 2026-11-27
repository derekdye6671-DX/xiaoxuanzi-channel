param([ValidateSet('preview','render')][string]$Mode='preview')
$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$nodeFolder='D:\Tools\nodejs\node-v24.22.3-win-x64'
$nodeExecutable=Join-Path $nodeFolder 'node.exe'
if (-not (Test-Path -LiteralPath $nodeExecutable)) { throw '没有找到已安装的 Node.js，请让 Codex 检查依赖目录。' }
$launcher=Join-Path $env:USERPROFILE '.codex\skills\hyperframes\scripts\plugin-cli.mjs'
if (-not (Test-Path -LiteralPath $launcher)) { throw '没有找到 HyperFrames 技能，请让 Codex 检查安装。' }
$env:Path=$nodeFolder+';'+$env:Path
$env:npm_config_cache='D:\Tools\npm-cache'
$env:HYPERFRAMES_NO_TELEMETRY='1'
$env:DO_NOT_TRACK='1'
$env:HYPERFRAMES_FFMPEG_PATH='D:\Tools\ffmpeg\ffmpeg-9.1-essentials_build\bin\ffmpeg.exe'
$env:HYPERFRAMES_FFPROBE_PATH='D:\Tools\ffmpeg\ffmpeg-9.1-essentials_build\bin\ffprobe.exe'
if ($Mode -eq 'preview') {
    & $nodeExecutable $launcher --cli-version 0.9.102 preview --background --port 3017
} else {
    $filename='renders/片头-'+(Get-Date -Format 'yyyyMMdd-HHmmss')+'.mp4'
    & $nodeExecutable $launcher --cli-version 0.9.102 check
    if ($LASTEXITCODE -ne 0) { throw '画面检查未通过，停止导出，请把错误交给 Codex。' }
    & $nodeExecutable $launcher --cli-version 0.9.102 render --quality delivery --fps 30 --output $filename
}
if ($LASTEXITCODE -ne 0) { throw '执行失败，请把窗口中的错误交给 Codex。' }
