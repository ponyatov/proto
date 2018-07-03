build: r
	python $< vm.py
	
install: r

r: pypy2-v6.0.0-src/rpython/bin/rpython
	ln -fs $< $@
	
pypy2-v6.0.0-src/rpython/bin/rpython: pypy2-v6.0.0-src.zip 	
	unzip $< && touch $@

pypy2-v6.0.0-src.zip:
	wget -c https://bitbucket.org/pypy/pypy/downloads/pypy2-v6.0.0-src.zip
	