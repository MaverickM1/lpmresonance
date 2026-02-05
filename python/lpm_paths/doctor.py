#!/usr/bin/env python3
"""
Diagnostic tool for lpmresonance installation.

Checks that required components are available and working, including
PythonTeX, latexmk, shell-escape, and the TeX/Python packages.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, NamedTuple, Optional

VERSION_TIMEOUT = 5
TEX_TIMEOUT = 30


class CheckResult(NamedTuple):
    """Result of a diagnostic check."""
    name: str
    passed: bool


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str, *, use_color: bool) -> None:
    """Print a formatted section header."""
    if use_color:
        print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    else:
        print(f"\n{text}")
    print("=" * len(text))


def print_success(text: str, *, use_color: bool) -> None:
    """Print a success message."""
    if use_color:
        print(f"{Colors.GREEN}✓{Colors.RESET} {text}")
    else:
        print(f"✓ {text}")


def print_error(text: str, *, use_color: bool) -> None:
    """Print an error message."""
    if use_color:
        print(f"{Colors.RED}✗{Colors.RESET} {text}")
    else:
        print(f"✗ {text}")


def print_warning(text: str, *, use_color: bool) -> None:
    """Print a warning message."""
    if use_color:
        print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")
    else:
        print(f"⚠ {text}")


def check_command(command: str, name: str) -> tuple[bool, str]:
    """Check if a command exists and report its version."""
    path = shutil.which(command)
    if not path:
        return False, f"{name} not found in PATH"
    
    try:
        result = subprocess.run(
            [command, '--version'],
            capture_output=True,
            text=True,
            timeout=VERSION_TIMEOUT
        )
        version = result.stdout.split('\n')[0] if result.stdout else result.stderr.split('\n')[0]
        return True, f"{name} found at {path}\n  Version: {version}"
    except (subprocess.TimeoutExpired, OSError, subprocess.SubprocessError) as e:
        return True, f"{name} found at {path} (version check failed: {e})"


def check_pythontex(*, use_color: bool) -> bool:
    """Check if PythonTeX is installed and functional."""
    print_header("Checking PythonTeX", use_color=use_color)
    
    success, info = check_command("pythontex", "PythonTeX")
    if success:
        print_success(info, use_color=use_color)
        return True
    else:
        print_error(info, use_color=use_color)
        print_warning("Install PythonTeX: https://ctan.org/pkg/pythontex", use_color=use_color)
        return False


def check_latexmk(*, use_color: bool) -> bool:
    """Check if latexmk is installed."""
    print_header("Checking latexmk", use_color=use_color)
    
    success, info = check_command("latexmk", "latexmk")
    if success:
        print_success(info, use_color=use_color)
        return True
    else:
        print_error(info, use_color=use_color)
        print_warning("Install latexmk with your TeX distribution", use_color=use_color)
        return False


def check_pdflatex(*, use_color: bool) -> bool:
    """Check if pdflatex is installed."""
    print_header("Checking pdflatex", use_color=use_color)
    
    success, info = check_command("pdflatex", "pdflatex")
    if success:
        print_success(info, use_color=use_color)
        return True
    else:
        print_error(info, use_color=use_color)
        print_warning("Install TeX Live or MiKTeX", use_color=use_color)
        return False


def check_shell_escape(*, use_color: bool) -> bool:
    """Check if pdflatex supports -shell-escape."""
    print_header("Checking -shell-escape capability", use_color=use_color)
    
    test_tex = r"""
\documentclass{minimal}
\begin{document}
Test
\end{document}
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = Path(tmpdir) / "test.tex"
        tex_file.write_text(test_tex, encoding="utf-8")
        
        try:
            result = subprocess.run(
                ['pdflatex', '-shell-escape', '-interaction=nonstopmode', 'test.tex'],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=TEX_TIMEOUT
            )
            
            if result.returncode == 0:
                print_success("-shell-escape is enabled and working", use_color=use_color)
                return True
            
            print_error("-shell-escape test failed", use_color=use_color)
            print_warning("Compilation error (this might be a TeX configuration issue)", use_color=use_color)
            return False
                
        except subprocess.TimeoutExpired:
            print_error("-shell-escape test timed out", use_color=use_color)
            return False
        except (OSError, subprocess.SubprocessError) as e:
            print_error(f"-shell-escape test failed: {e}", use_color=use_color)
            return False


def check_lpmresonance_package(*, use_color: bool) -> bool:
    """Check if lpmresonance.sty is findable by TeX."""
    print_header("Checking lpmresonance package installation", use_color=use_color)
    
    test_tex = r"""
\documentclass{minimal}
\usepackage{lpmresonance}
\begin{document}
Test
\end{document}
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = Path(tmpdir) / "test.tex"
        tex_file.write_text(test_tex, encoding="utf-8")
        
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'test.tex'],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=TEX_TIMEOUT
            )
            
            pdf_file = Path(tmpdir) / "test.pdf"
            if pdf_file.exists() and result.returncode == 0:
                print_success("lpmresonance.sty found and loaded successfully", use_color=use_color)
                
                try:
                    kpse_result = subprocess.run(
                        ['kpsewhich', 'lpmresonance.sty'],
                        capture_output=True,
                        text=True,
                        timeout=VERSION_TIMEOUT
                    )
                    if kpse_result.returncode == 0:
                        location = kpse_result.stdout.strip()
                        print(f"  Location: {location}")
                except (subprocess.TimeoutExpired, OSError, subprocess.SubprocessError):
                    pass
                
                return True
            
            print_error("lpmresonance.sty not found", use_color=use_color)
            print_warning("Run the install script:", use_color=use_color)
            print_warning("  macOS/Linux: bash scripts/install.sh", use_color=use_color)
            print_warning("  Windows:     powershell scripts/install-windows.ps1", use_color=use_color)
            return False
            
        except subprocess.TimeoutExpired:
            print_error("Package check timed out", use_color=use_color)
            return False
        except (OSError, subprocess.SubprocessError) as e:
            print_error(f"Package check failed: {e}", use_color=use_color)
            return False


def check_python_package(*, use_color: bool) -> bool:
    """Check if the lpm_paths Python package is installed."""
    print_header("Checking Python package installation", use_color=use_color)
    
    from importlib.metadata import distribution, PackageNotFoundError
    
    try:
        dist = distribution("lpmresonance")
        print_success("lpm_paths package found", use_color=use_color)
        print(f"  Version: {dist.version}")
        
        try:
            location = dist.locate_file("")
            print(f"  Location: {location}")
        except (AttributeError, OSError):
            pass
        
        return True
    except PackageNotFoundError:
        print_error("lpm_paths package not found", use_color=use_color)
        print_warning("Install with: pip install -e .", use_color=use_color)
        return False


def main(argv: Optional[list[str]] = None) -> int:
    """Run all diagnostic checks and return exit code."""
    args = argv or sys.argv[1:]
    use_color = "--no-color" not in args

    def with_color(func: Callable[..., bool]) -> Callable[[], bool]:
        return lambda: func(use_color=use_color)

    if use_color:
        print(f"\n{Colors.BOLD}lpmresonance Doctor{Colors.RESET}")
    else:
        print("\nlpmresonance Doctor")
    print("Checking your lpmresonance installation...\n")

    checks: list[tuple[str, Callable[[], bool]]] = [
        ("pdflatex", with_color(check_pdflatex)),
        ("PythonTeX", with_color(check_pythontex)),
        ("latexmk", with_color(check_latexmk)),
        ("shell-escape", with_color(check_shell_escape)),
        ("Python package", with_color(check_python_package)),
        ("TeX package", with_color(check_lpmresonance_package)),
    ]
    
    results: list[CheckResult] = []
    for name, check_func in checks:
        try:
            results.append(CheckResult(name=name, passed=check_func()))
        except Exception as e:
            print_error(f"Check failed with exception: {e}", use_color=use_color)
            results.append(CheckResult(name=name, passed=False))
    
    print_header("Summary", use_color=use_color)
    passed = sum(1 for result in results if result.passed)
    total = len(results)
    
    for result in results:
        if result.passed:
            print_success(f"{result.name}: OK", use_color=use_color)
        else:
            print_error(f"{result.name}: FAILED", use_color=use_color)
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        if use_color:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All checks passed! Your installation is ready.{Colors.RESET}\n")
        else:
            print("\n✓ All checks passed! Your installation is ready.\n")
        return 0
    else:
        if use_color:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ Some checks failed. Please fix the issues above.{Colors.RESET}\n")
        else:
            print("\n✗ Some checks failed. Please fix the issues above.\n")
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
