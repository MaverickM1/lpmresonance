Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Detect UTF-8 support for progress markers
$OutputEncoding = [System.Console]::OutputEncoding
if ($OutputEncoding.CodePage -eq 65001) {
    $ARROW = "→"
    $CHECK = "✓"
} else {
    $ARROW = ">"
    $CHECK = "[OK]"
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

$PythonExe = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonExe = (Get-Command python).Path
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $PythonExe = (Get-Command python3).Path
} else {
    throw "Error: Python 3 (python or python3) is required but was not found. Install Python 3.9+ from https://www.python.org/downloads/"
}

& $PythonExe -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)"
if ($LASTEXITCODE -ne 0) {
    $Version = & $PythonExe -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    throw "Error: Python 3.9+ is required. Found: $Version"
}

if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    throw "Error: pdflatex not found. Install TeX Live 2022+ from https://tug.org/texlive/"
}

if (-not (Get-Command pythontex -ErrorAction SilentlyContinue)) {
    throw "Error: pythontex not found. Install PythonTeX via: tlmgr install pythontex"
}

if (-not (Get-Command latexmk -ErrorAction SilentlyContinue)) {
    throw "Error: latexmk not found. Install latexmk via: tlmgr install latexmk"
}

if (-not (Get-Command kpsewhich -ErrorAction SilentlyContinue)) {
    throw "Error: kpsewhich not found. TeX Live installation may be incomplete."
}

$TexmfHome = & kpsewhich -var-value TEXMFHOME
if (-not $TexmfHome) {
    throw "Error: TEXMFHOME is empty. TeX Live does not appear configured."
}

Write-Host "$ARROW Installing TeX files to TEXMFHOME..."
$TargetDir = Join-Path $TexmfHome "tex/latex/lpmres"
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
Copy-Item -Force -Path (Join-Path $RepoRoot "tex/latex/lpmres/*") -Destination $TargetDir

if (Get-Command mktexlsr -ErrorAction SilentlyContinue) {
    Write-Host "$ARROW Refreshing TeX database..."
    try {
        & mktexlsr $TexmfHome 2>&1 | Out-Null
    }
    catch {
        Write-Warning "Failed to refresh TeX database. You may need to run 'mktexlsr' manually."
    }
}

Write-Host "$ARROW Installing Python package..."
try {
    & $PythonExe -m pip install -e $RepoRoot
}
catch {
    throw "Error: pip install failed. Check your Python environment."
}

# Configure global ~/.latexmkrc with PythonTeX support
$LatexmkRcPath = Join-Path $env:USERPROFILE ".latexmkrc"
$PythontexMarker = "# PythonTeX support"

if ((Test-Path $LatexmkRcPath) -and (Select-String -Path $LatexmkRcPath -Pattern $PythontexMarker -Quiet)) {
    Write-Host "$ARROW PythonTeX already configured in ~/.latexmkrc"
} else {
    Write-Host "$ARROW Configuring PythonTeX in ~/.latexmkrc..."
    
    $PythontexConfig = @"

$PythontexMarker (added by lpmresonance installer)
add_cus_dep('pytxcode', 'tex', 0, 'pythontex');
sub pythontex {
    return system("pythontex", `$_[0]);
}
"@
    Add-Content -Path $LatexmkRcPath -Value $PythontexConfig
    Write-Host "  Added PythonTeX rule"
}

$TexPath = & kpsewhich lpmresonance.sty
if (-not $TexPath) {
    throw "Error: lpmresonance.sty not found in TeX search path after install."
}

$TempRoot = [System.IO.Path]::GetTempPath()
$TestDir = Join-Path $TempRoot ("lpmresonance-install-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $TestDir | Out-Null

$TestSucceeded = $false
try {
    $TestFile = Join-Path $TestDir "lpmresonance-test.tex"
    @'
\documentclass{article}
\usepackage{lpmresonance}
\begin{document}
\lpDeclarePath{demo}{0101}
\begin{schubertpic}
  \drawGrid{demo}
  \drawLatticePath{demo}
\end{schubertpic}
\end{document}
'@ | Set-Content -Path $TestFile -Encoding ASCII

    # Verification uses the global ~/.latexmkrc configured above
    Write-Host "$ARROW Running verification build..."
    Push-Location $TestDir
    $BuildLog = Join-Path $TestDir "build.log"
    try {
        & latexmk -pdf -shell-escape "lpmresonance-test.tex" *>&1 | Out-File -FilePath $BuildLog -Encoding UTF8
        if ($LASTEXITCODE -ne 0) {
            throw "latexmk failed"
        }
    }
    catch {
        Write-Error "Error: Test compilation failed. Last 30 lines of log:"
        Get-Content $BuildLog -Tail 30 | Write-Error
        throw
    }
    finally {
        Pop-Location
    }

    $PdfPath = Join-Path $TestDir "lpmresonance-test.pdf"
    if (-not (Test-Path $PdfPath)) {
        throw "Error: Test compilation failed. PDF not generated."
    }

    $CachePath = Join-Path $TestDir "lp-cache"
    $CacheFiles = Get-ChildItem -Path $CachePath -Filter "path-demo-*.tex" -ErrorAction SilentlyContinue
    if (-not (Test-Path $CachePath) -or -not $CacheFiles) {
        throw "Error: Cache files not generated. Python bridge may be broken."
    }

    $TestSucceeded = $true
}
finally {
    Remove-Item -Recurse -Force $TestDir
}

if ($TestSucceeded) {
    Write-Host "$CHECK Installer completed successfully for windows." -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now use lpmresonance in your LaTeX documents:"
    Write-Host "  \usepackage{lpmresonance}"
    Write-Host ""
    Write-Host "Compile with: latexmk -pdf -shell-escape yourfile.tex"
}
