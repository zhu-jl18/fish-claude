# ccc - Interactive Claude Code launcher with settings picker
# Lists settings* files in the current user's Claude config directory,
# then launches claude with --dangerously-skip-permissions using the selected file.
#
# Usage:  . scripts/ccc.ps1   (dot-source to get the function into your session)
#         ccc                  (then follow the prompts)

function ccc {
    $claudeDir = "$env:USERPROFILE\.claude"

    if (Test-Path $claudeDir) {
        $settingsFiles = Get-ChildItem -Path $claudeDir -Filter "settings*" -File

        if ($settingsFiles.Count -eq 0) {
            Write-Host "没有找到 settings 文件"
            return
        }

        Write-Host "选择配置文件:"
        for ($i = 0; $i -lt $settingsFiles.Count; $i++) {
            Write-Host "$($i + 1). $($settingsFiles[$i].Name)"
        }

        $choice = Read-Host "选择"

        if ($choice -match '^\d+$' -and [int]$choice -ge 1 -and [int]$choice -le $settingsFiles.Count) {
            $selected = $settingsFiles[[int]$choice - 1]
            Write-Host "执行: claude --dangerously-skip-permissions  --settings $claudeDir\$($selected.Name)"
            & claude --dangerously-skip-permissions --settings "$claudeDir\$($selected.Name)"
        }
        else {
            Write-Host "无效选择"
        }
    }
    else {
        Write-Host "$claudeDir 目录不存在"
    }
}
