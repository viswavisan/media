

import os
supportfilesfolder='D:/media/stored/'
py='SDK.py'

cmd='pyinstaller --onefile '
for file in os.listdir(supportfilesfolder):cmd+='--add-data="'+supportfilesfolder+file+';stored" '
cmd+=py
print(cmd)
#os.system(cmd)


