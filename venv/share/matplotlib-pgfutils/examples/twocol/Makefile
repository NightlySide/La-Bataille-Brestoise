default: twocol.pdf

twocol.pdf: twocol.tex single.pypgf double.pypgf
	xelatex twocol

%.pypgf: %.py pgfutils.cfg
	python3 $?

.PHONY: clean

clean:
	rm -f twocol.{aux,log,pdf}
	rm -f {single,double}.pypgf
