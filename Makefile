all: doxy stage_1.py.log

stage_1.py.log: stage_1.py.src stage_1.py
	python stage_1.py $< > $@ && tail $(TAIL) $@

doxy:
	rm -rf doc/html ; doxygen doxy.gen >/dev/null
