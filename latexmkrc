# latexmkrc for lpmresonance (repository root)
# Configures automatic compilation with PythonTeX support

# Set TEXINPUTS to find package files
$ENV{"TEXINPUTS"} = "tex/latex/lpmres:" . ($ENV{"TEXINPUTS"} // "");

# Use pdflatex with -shell-escape for minted and PythonTeX
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -shell-escape %O %S';

# PythonTeX configuration - standard approach from PythonTeX documentation
# Find python3 executable
my $python_exe = 'python3';
for my $try_path ('/usr/local/bin/python3', '/Library/Frameworks/Python.framework/Versions/3.14/bin/python3') {
    if (-e $try_path) {
        $python_exe = $try_path;
        last;
    }
}

# Custom dependency: when .pytxcode changes, run pythontex
add_cus_dep('pytxcode', 'tex', 0, 'run_pythontex');

sub run_pythontex {
    my $base = shift;
    return system($python_exe, '/Library/TeX/texbin/pythontex',
                  '--interpreter', "python:$python_exe", "$base");
}

# Clean up
$clean_ext .= ' %R.pytxcode pythontex-files-%R';
$max_repeat = 5;
