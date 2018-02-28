LATEXMK_OPTIONS=pdflatex -interaction=nonstopmode -synctex=1 %O %S

.PHONY: all clean

all: cr.pdf 

%.pdf: %.tex
	latexmk -pdf -pdflatex="$(LATEXMK_OPTIONS)" -use-make $<

clean:
	latexmk -CA
