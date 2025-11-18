$ENV{"TEXINPUTS"} = join(':', 'tex/latex/lpmres', $ENV{"TEXINPUTS"} // '');

$force_mode = 1;

$pdflatex  = 'pdflatex -interaction=nonstopmode -shell-escape %O %S';

my $pythontex_cmd = 'PATH=' . $ENV{'PWD'} . '/.local/bin:$PATH /usr/local/bin/python3 /Library/TeX/texbin/pythontex';

add_cus_dep('pytxcode','tex',0,'pythontex');
sub pythontex { return system("$pythontex_cmd \"$_[0]\""); }

$clean_ext .= ' %R.pytxcode %R.pytxmcr pythontex-files-%R';
