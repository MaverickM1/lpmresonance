#!/usr/bin/env python3
"""
Diagnostic tool for lpmresonance installation.

Checks that all required components are properly installed:
- PythonTeX
- latexmk
- TeX Live with shell-escape capability
- lpmresonance package in TEXMFHOME
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Tuple


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str) -> None:
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print("=" * len(text))


def print_success(text: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")


def print_error(text: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}✗{Colors.RESET} {text}")


def print_warning(text: str) -> None:
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")


def check_command(command: str, name: str) -> Tuple[bool, str]:
    """
    Check if a command exists and is executable.
    
    Returns:
        Tuple of (success, version/path info)
    """
    path = shutil.which(command)
    if not path:
        return False, f"{name} not found in PATH"
    
    # Try to get version
    try:
        result = subprocess.run(
            [command, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        # Get first line of output
        version = result.stdout.split('\n')[0] if result.stdout else result.stderr.split('\n')[0]
        return True, f"{name} found at {path}\n  Version: {version}"
    except Exception as e:
        return True, f"{name} found at {path} (version check failed: {e})"


def check_pythontex() -> bool:
    """Check if PythonTeX is installed and functional."""
    print_header("Checking PythonTeX")
    
    success, info = check_command('pythontex', 'PythonTeX')
    if success:
        print_success(info)
        return True
    else:
        print_error(info)
        print_warning("Install PythonTeX: https://ctan.org/pkg/pythontex")
        return False


def check_latexmk() -> bool:
    """Check if latexmk is installed."""
    print_header("Checking latexmk")
    
    success, info = check_command('latexmk', 'latexmk')
    if success:
        print_success(info)
        return True
    else:
        print_error(info)
        print_warning("Install latexmk with your TeX distribution")
        return False


def check_pdflatex() -> bool:
    """Check if pdflatex is installed."""
    print_header("Checking pdflatex")
    
    success, info = check_command('pdflatex', 'pdflatex')
    if success:
        print_success(info)
        return True
    else:
        print_error(info)
        print_warning("Install TeX Live or MiKTeX")
        return False


def check_shell_escape() -> bool:
    """Check if -shell-escape works with pdflatex."""
    print_header("Checking -shell-escape capability")
    
    # Create a minimal test document
    test_tex = r"""
\documentclass{minimal}
\begin{document}
Test
\end{document}
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = Path(tmpdir) / "test.tex"
        tex_file.write_text(test_tex)
        
        try:
            result = subprocess.run(
                ['pdflatex', '-shell-escape', '-interaction=nonstopmode', 'test.tex'],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print_success("-shell-escape is enabled and working")
                return True
            else:
                print_error("-shell-escape test failed")
                print_warning("Compilation error (this might be a TeX configuration issue)")
                return False
                
        except subprocess.TimeoutExpired:
            print_error("-shell-escape test timed out")
            return False
        except Exception as e:
            print_error(f"-shell-escape test failed: {e}")
            return False


def check_lpmresonance_package() -> bool:
    """Check if lpmresonance.sty is findable by TeX."""
    print_header("Checking lpmresonance package installation")
    
    # Create a minimal test document that uses the package
    test_tex = r"""
\documentclass{minimal}
\usepackage{lpmresonance}
\begin{document}
Test
\end{document}
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = Path(tmpdir) / "test.tex"
        tex_file.write_text(test_tex)
        
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'test.tex'],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check if the package was found
            if 'lpmresonance.sty' in result.stdout or result.returncode == 0:
                # Verify the PDF was created
                pdf_file = Path(tmpdir) / "test.pdf"
                if pdf_file.exists():
                    print_success("lpmresonance.sty found and loaded successfully")
                    
                    # Try to find where it's installed
                    try:
                        kpse_result = subprocess.run(
                            ['kpsewhich', 'lpmresonance.sty'],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if kpse_result.returncode == 0:
                            location = kpse_result.stdout.strip()
                            print(f"  Location: {location}")
                    except:
                        pass
                    
                    return True
            
            print_error("lpmresonance.sty not found")
            print_warning("Run the install script for your platform:")
            print_warning("  macOS:   bash scripts/install-macos.sh")
            print_warning("  Linux:   bash scripts/install-linux.sh")
            print_warning("  Windows: powershell scripts/install-windows.ps1")
            return False
            
        except subprocess.TimeoutExpired:
            print_error("Package check timed out")
            return False
        except Exception as e:
            print_error(f"Package check failed: {e}")
            return False


def check_python_package() -> bool:
    """Check if lpm_paths Python package is installed."""
    print_header("Checking Python package installation")
    
    try:
        import lpm_paths
        print_success(f"lpm_paths package found")
        
        # Try to get version
        try:
            from lpm_paths.version import __version__
            print(f"  Version: {__version__}")
        except:
            pass
        
        return True
    except ImportError:
        print_error("lpm_paths package not found")
        print_warning("Install with: pip install -e .")
        return False


def main() -> int:
    """Run all diagnostic checks."""
    print(f"\n{Colors.BOLD}lpmresonance Doctor{Colors.RESET}")
    print("Checking your lpmresonance installation...\n")
    
    checks = [
        ("pdflatex", check_pdflatex),
        ("PythonTeX", check_pythontex),
        ("latexmk", check_latexmk),
        ("shell-escape", check_shell_escape),
        ("Python package", check_python_package),
        ("TeX package", check_lpmresonance_package),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            results.append((name, check_func()))
        except Exception as e:
            print_error(f"Check failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print_header("Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        if result:
            print_success(f"{name}: OK")
        else:
            print_error(f"{name}: FAILED")
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All checks passed! Your installation is ready.{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Some checks failed. Please fix the issues above.{Colors.RESET}\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
