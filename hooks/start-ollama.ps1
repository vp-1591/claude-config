if (-not (Get-Process ollama -ErrorAction SilentlyContinue)) {
    Start-Process ollama -ArgumentList 'serve' -WindowStyle Hidden
}
exit 0