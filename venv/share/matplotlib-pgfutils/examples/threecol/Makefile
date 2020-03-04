default: threecol.pdf

threecol.pdf: threecol.tex single.pypgf double.pypgf triple.pypgf
	xelatex threecol

%.pypgf: %.py pgfutils.cfg
	python3 $<

.PHONY: clean

clean:
	rm -f threecol.{aux,log,pdf}
	rm -f {single,double,triple}.pypgf
