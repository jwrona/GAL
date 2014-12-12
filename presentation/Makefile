SOURCE = presentation

latex: $(SOURCE).tex
	latex $(SOURCE).tex
	latex $(SOURCE).tex #double compilation because of references
	dvipdf $(SOURCE).dvi

clean:
	rm $(SOURCE).{aux,log,out,toc,dvi,nav,snm}
