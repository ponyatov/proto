CWD		= $(CURDIR)
APP		= $(notdir $(CURDIR))
APP_LOW	= $(shell echo $(APP) | sed 's/\(.*\)/\L\1/')

SRC		= $(CWD)/src
OBJ		= $(CWD)/obj

PACK	= io/github/ponyatov

MAIN	= app/src/main
JA		= $(MAIN)/java
RES		= $(MAIN)/res
LAYOUT	= $(RES)/layout
VALUES	= $(RES)/values

MANIFEST	= $(MAIN)/AndroidManifest.xml
JA_MAIN		= $(JA)/MainActivity.java
LA_MAIN 	= $(LAYOUT)/activity_main.xml

default: dirs build

src: dirs Makefile $(MANIFEST) $(JA_MAIN) $(LA_MAIN)

dirs:
	mkdir -p $(JA) $(RES) $(LAYOUT) $(VALUES) $(SRC)/$(PACK) $(OBJ)

Makefile: ../Sample/Makefile
	cp $< $@
$(MANIFEST): ../Sample/$(MANIFEST) Makefile
	cat $< | sed "s/ponyatov\.sample/\Lponyatov.$(APP)/g" > $@
$(JA_MAIN): ../Sample/$(JA)/$(PACK)/sample/MainActivity.java Makefile
	cat $< | sed "s/ponyatov\.sample/\Lponyatov.$(APP)/g" > $@
$(LAYOUT)/activity_main.xml: ../Sample/$(LAYOUT)/activity_main.xml Makefile
	cat $< | sed "s/ponyatov\.sample/\Lponyatov.$(APP)/g" > $@

AAPT	= $(HOME)/Android/Sdk/build-tools/26.0.2/aapt
JAR		= $(HOME)/Android/Sdk/platforms/android-9/android.jar

build:
#	$(AAPT) package -f -m -J $(SRC) -M $(MANIFEST) -S $(RES) -I $(JAR)
	javac -d obj -classpath src -bootclasspath $(JAR) \
	$(SRC)/$(PACK)/$(APP_LOW)/*.java

