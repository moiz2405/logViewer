# load_env.ps1
# Reads .env file and sets environment variables for this PowerShell session

$envFile = ".env.local"

if (-Not (Test-Path $envFile)) {
    Write-Error "No .env file found in $(Get-Location)"
    exit 1
}

Get-Content $envFile | ForEach-Object {
    if ($_ -match "^\s*#") { return }   # skip comments
    if ($_ -match "^\s*$") { return }   # skip empty lines
    $name, $value = $_ -split "=", 2
    $name  = $name.Trim()
    $value = $value.Trim()

    # Remove surrounding quotes if present
    if ($value.StartsWith('"') -and $value.EndsWith('"')) {
        $value = $value.Substring(1, $value.Length - 2)
    }

    Set-Item -Path Env:$name -Value $value
    Write-Output "$name set."
}
