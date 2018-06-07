all: doxy proto.py.log

proto.py.log: proto.py.src proto.py
	python proto.py $< > $@ && tail $(TAIL) $@

doxy:
	rm -rf doc/html ; doxygen doxy.gen
