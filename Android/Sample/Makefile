CWD		= $(CURDIR)
APP		= $(notdir $(CURDIR))

PACK	= io/github/ponyatov

MAIN	= app/src/main
JA		= $(MAIN)/java
RES		= $(MAIN)/res
LAYOUT	= $(RES)/layout
VALUES	= $(RES)/values

MANIFEST	= $(MAIN)/AndroidManifest.xml

JA_MAIN	= $(JA)/MainActivity.java

A: dirs Makefile $(MANIFEST) $(JA_MAIN)

dirs:
	mkdir -p app app/src app/src/main $(JA) $(RES) $(LAYOUT) $(VALUES)

Makefile: ../Sample/Makefile
	cp $< $@
$(MANIFEST): ../Sample/$(MANIFEST) Makefile
	cat $< | sed "s/ponyatov\.sample/\Lponyatov.$(APP)/g" > $@
$(JA_MAIN): ../Sample/$(JA)/$(PACK)/sample/MainActivity.java Makefile
	cat $< | sed "s/ponyatov\.sample/\Lponyatov.$(APP)/g" > $@
	