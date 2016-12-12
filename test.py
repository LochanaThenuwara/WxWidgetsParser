import re
import json
import NewSourceRead.events

for key, value in NewSourceRead.events.iteritems():
    print key,value


#
# wx_file=open("C:/ProjectSE/Parser/AISTargetListDialog.cpp","r")
# out_file=open("C:/ProjectSE/Parser/yes.txt","w")
#
# data = wx_file.read().replace('\n', '')
# out_file.write(data)
