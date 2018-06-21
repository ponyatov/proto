CWD		= $(CURDIR)
APP		= $(notdir $(CURDIR))
APP_LOW	= $(shell echo $(APP) | sed 's/\(.*\)/\L\1/')

SRC		= $(CWD)/src
OBJ		= $(CWD)/obj
BIN		= $(CWD)/bin

PACK	= io/github/ponyatov

MAIN	= app/src/main
JA		= $(MAIN)/java
RES		= $(MAIN)/res
LAYOUT	= $(RES)/layout
VALUES	= $(RES)/values

MANIFEST	= $(MAIN)/AndroidManifest.xml
JA_MAIN		= $(JA)/MainActivity.java
LA_MAIN 	= $(LAYOUT)/activity_main.xml

default: go

src: dirs Makefile $(MANIFEST) $(JA_MAIN) $(LA_MAIN)

dirs:
	mkdir -p $(JA) $(RES) $(LAYOUT) $(VALUES) $(SRC)/$(PACK) $(OBJ) $(BIN)

Makefile: ../Sample/Makefile
	cp $< $@
$(MANIFEST): ../Sample/$(MANIFEST) Makefile
	cat $< | sed "s/ponyatov\.sample/\Lponyatov.$(APP)/g" > $@
$(JA_MAIN): ../Sample/$(JA)/$(PACK)/sample/MainActivity.java Makefile
	cat $< | sed "s/ponyatov\.sample/\Lponyatov.$(APP)/g" > $@
$(LAYOUT)/activity_main.xml: ../Sample/$(LAYOUT)/activity_main.xml Makefile
	cat $< | sed "s/ponyatov\.sample/\Lponyatov.$(APP)/g" > $@

ADB		= $(HOME)/Android/Sdk/platform-tools/adb
SDK		= $(HOME)/Android/Sdk/build-tools/26.0.2
AAPT	= $(SDK)/aapt
AALIST	= $(AAPT) list 
JAR		= $(HOME)/Android/Sdk/platforms/android-9/android.jar
AAPACK	= $(AAPT) package -f -m -M $(MANIFEST) -S $(RES) -I $(JAR)

DEX		= $(HOME)/Android/Sdk/build-tools/26.0.2/dx
DEXDUMP	= $(HOME)/Android/Sdk/build-tools/26.0.2/dexdump

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
$(BIN)/$(APP_LOW).unaligned.apk: $(BIN)/classes.dex
	$(AAPACK) -F $@
	cp $< classes.dex && $(AAPT) add $@ classes.dex && rm classes.dex 

go: $(BIN)/$(APP_LOW).apk
	$(ADB) install $<
	
key: ../android.keystore
../android.keystore:
	keytool -genkeypair -validity 365 -keystore $@ -keyalg RSA -keysize 2048
