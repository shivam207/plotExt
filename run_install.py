#!/usr/bin python
import os
os.chmod("./packages/install_Local",0777)
os.system("./packages/install_Local")
f=file("plotExt.py","w")
f.write("#!/usr/bin python\nimport os\nos.system('python ./src/mainGui.py')")
f.close()
os.chmod("plotExt.py",0777)
try:
	os.system('gvfs-set-attribute -t string plotExt.py metadata::custom-icon file://'+os.path.abspath('src/icon.png')+'; sleep 3; xte "key F5"')
except:
	pass
