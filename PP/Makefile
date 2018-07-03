## build VM
build: r
	python $< vm.py
	
## install PyPy
install: r

RPYTHON = pypy2-v6.0.0-src/rpython/bin/rpython

r: $(RPYTHON)
	ln -fs $< $@
	
$(RPYTHON): pypy2-v6.0.0-src.zip 	
	unzip $< && touch $@

pypy2-v6.0.0-src.zip:
	wget -c https://bitbucket.org/pypy/pypy/downloads/pypy2-v6.0.0-src.zip

## build & install PyPy into your system
pypy: /usr/local/bin/pypy
/usr/local/bin/pypy: $(RPYTHON)
	cd pypy2-v6.0.0-src/pypy/goal ;\
	python ../../rpython/bin/rpython -O2 targetpypystandalone
#	sudo pip install pycparser ;\
