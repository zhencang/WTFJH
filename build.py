#!/usr/bin/env python
from os import listdir
import string
import random
import os
import sys
makeFileString=""
PathList=["./Hooks/APIHooks/","./Hooks/SDKHooks"]
global toggleString
toggleString="void GlobalInit(){\n"
MakeFileListString="_FILES = Tweak.xm CompileDefines.xm"
def ModuleIter(Path):
	List=listdir(Path)
	for x in List:
		if(x.endswith(".xm")==False):
			print x+" "+"Not A Theos Code File"
		else:
			componentList=x.split(".")
			componentName=""
			i=0
			while i<len(componentList[i])-1:#ModuleName
				componentName+=componentList[i]
				i+=1
			global toggleString
			toggleString+="extern  void init_"+componentName+"_hook();\n"
			toggleString+="init_"+componentName+"_hook();\n";
def toggleModule():
	for x in PathList:
		ModuleIter(x)
	global toggleString
	toggleString+="}\n"
	os.system("touch"+" "+"./CompileDefines.xm")
	fileHandle=open("./CompileDefines.xm","w")
	fileHandle.flush()
	fileHandle.write(toggleString)
	fileHandle.close() 

def MakeFileIter(Path):
		FileList=listdir(Path)
		for x in FileList:
			if(x.endswith(".mm")==False and x.endswith(".m")==False and x.endswith(".xm")==False):
				print "AAA"
			else:	
				string=" "+Path+x
				MakeFileListString+=string



def subModuleList():
	for x in PathList:
		MakeFileIter(x)
def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
	#Thanks to http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
	return ''.join(random.choice(chars) for _ in range(size))
randomTweakName=id_generator()#Generate Random Name To Help Bypass Detection
#os.remove("./Makefile")
toggleModule()
if (os.path.exists("theos")==False):
	print "Theos Link Doesn't Exist,Creating"
	if(os.environ.get('THEOS')!=None):
		os.system("ln -s $THEOS theos")
	else:
		print "$THEOS ENV Not Set"
		sys.exit(255)
else:
	print "Theos Link Exists at"+os.getcwd()+"/theos"+",Building"
makeFileString+="include theos/makefiles/common.mk\n"
makeFileString+="export ARCHS = armv7 armv7s arm64\n"
makeFileString+="export TARGET = iphone:clang:7.0:7.0\n"
makeFileString+="TWEAK_NAME = "+randomTweakName+"\n"
makeFileString+=randomTweakName+MakeFileListString+"\n"
makeFileString+="ADDITIONAL_CCFLAGS  = -Qunused-arguments\n"
makeFileString+="ADDITIONAL_LDFLAGS  = -Wl,-segalign,4000\n"
makeFileString+=randomTweakName+"_LIBRARIES = sqlite3 substrate\n"
makeFileString+="include $(THEOS_MAKE_PATH)/tweak.mk\n"
makeFileString+="after-install::\n"
makeFileString+="	install.exec \"killall -9 SpringBoard\""
#print makeFileString
fileHandle = open('Makefile','w')
fileHandle.flush() 
fileHandle.write(makeFileString)
fileHandle.close() 
os.system("cp ./WTFJH.plist ./"+randomTweakName+".plist")
os.system("make clean")
os.system("make package")
os.system("rm ./"+randomTweakName+".plist")

