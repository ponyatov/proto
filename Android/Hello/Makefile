CWD		= $(CURDIR)
APP		= $(notdir $(CURDIR))
APP_LOW	= $(shell echo $(APP) | sed 's/\(.*\)/\L\1/')

SRC		= $(CWD)/src
OBJ		= $(CWD)/obj
BIN		= $(CWD)/bin

PACK	= io/github/ponyatov
PACKDOT = $(PACK)/$(APP_LOW)

MAIN	= app/src/main
JA		= $(MAIN)/java
RES		= $(MAIN)/res
LAYOUT	= $(RES)/layout
VALUES	= $(RES)/values

MANIFEST	= $(MAIN)/AndroidManifest.xml
JA_MAIN		= $(JA)/$(PACKDOT)/MainActivity.java
LA_MAIN 	= $(LAYOUT)/activity_main.xml

default: build

src: dirs Makefile $(MANIFEST) $(JA_MAIN) $(LA_MAIN)

dirs:
	mkdir -p $(JA) $(RES) $(LAYOUT) $(VALUES) $(SRC)/$(PACK) $(JA)/$(PACKDOT) \
				$(OBJ) $(BIN) 

Makefile: ../Sample/Makefile
	cp $< $@
$(MANIFEST): ../Sample/$(MANIFEST) Makefile
	cat $< | sed "s/ponyatov\.sample/\Lponyatov.$(APP)/g" > $@
$(JA_MAIN): ../Sample/$(JA)/io/github/ponyatov/sample/MainActivity.java Makefile
	cat $< | sed "s/ponyatov\.sample/\Lponyatov.$(APP)/g" > $@
$(LAYOUT)/activity_main.xml: ../Sample/$(LAYOUT)/activity_main.xml Makefile
	cat $< | sed "s/ponyatov\.sample/\Lponyatov.$(APP)/g" > $@

# tools

SDK		= $(HOME)/Android/Sdk/build-tools/26.0.2
JAR		= $(HOME)/Android/Sdk/platforms/android-9/android.jar
ADB		= $(HOME)/Android/Sdk/platform-tools/adb
DEX		= $(HOME)/Android/Sdk/build-tools/26.0.2/dx
DEXDUMP	= $(HOME)/Android/Sdk/build-tools/26.0.2/dexdump
AAPT	= $(SDK)/aapt
AAPACK	= $(AAPT) package -f -m -M $(MANIFEST) -S $(RES) -I $(JAR)
AALIST	= $(AAPT) list
SIGNER	= $(SDK)/apksigner

build: R class dex apk
R:
	$(AAPACK) -J $(SRC) 
class:
	javac -d obj -classpath src -bootclasspath $(JAR) \
	$(SRC)/$(PACK)/$(APP_LOW)/*.java
dex:
	$(DEX) --dex --output=$(BIN)/classes.dex $(OBJ)
apk: $(BIN)/$(APP_LOW).apk
$(BIN)/$(APP_LOW).apk: $(BIN)/$(APP_LOW).unaligned.apk
	$(SDK)/zipalign -f 4 $< $@ ; echo ; $(AALIST) $@
$(BIN)/$(APP_LOW).unaligned.apk: $(BIN)/classes.dex key
	$(AAPACK) -F $@
	cp $< classes.dex && $(AAPT) add $@ classes.dex && rm classes.dex
	cat ../debug.passwd | $(SIGNER) sign --ks ../debug.keystore $@

go: $(BIN)/$(APP_LOW).apk
	$(ADB) install -r $<
	
key: ../debug.keystore ../debug.passwd
../debug.keystore:
	keytool -genkeypair -validity 365 -keystore $@ -keyalg RSA -keysize 2048
