all: S0.py.log doxy 

S0.py.log: S0.py.src S0.py
	python S0.py $< > $@ && tail $(TAIL) $@

doxy:
	rm -rf doc/html ; doxygen doxy.gen >/dev/null
