import re
import glob
import webbrowser
from collections import defaultdict
import json

librarylist = []
libfilelist = []
classlist = []
linelist = []
objectlist = []
classObjectDic = defaultdict(list)
result = []

projet_path = "C:/ProjectSE"
library_file = open('C:/wxWidgets-3.0.2/include/wx/wx.h', 'r')
# test_file = open('C:/ProjectSE/wxRegitrationForm/WxRegitrationForm/WxRegitrationForm/FormReg.cpp', 'r')
# test_file = open('C:/ProjectSE/OpenCPN/src/AISTargetListDialog.cpp', 'r')
test_file = open('C:/ProjectSE/WxLoginForm/WxLoginForm/FormLogin.cpp', 'r')
file_path = 'C:/wxWidgets-3.0.2/include/'
header_file_path = 'C:/ProjectSE/OpenCPN/include/'
msw_path = 'C:/wxWidgets-3.0.2/include/wx/msw/'


def getLibraryFileName():
    count = 1
    for line in test_file:
        count = count + 1
        m = re.search('include ["<]wx[a-zA-Z0-9/]*.h[">]', line)
        if (m != None):
            print ("included header files")
            print(m.group(0))


def getHeaderfiles():
    for line in library_file:
        if line.strip() == '#if wxUSE_GUI':  # Or whatever test is needed
            break
    # Reads text until the end of the block:
    for line in library_file:  # This keeps reading the file
        if line.strip() == '//End':
            break
        m = re.search('include ["<]wx[a-zA-Z0-9/]*.h[">]', line)
        if (m != None):
            # print ("included header files")
            # print(m.group(0))
            libfilename = (m.group(0)).split(" ")[1]
            libfilename = libfilename[1:-1]
            libfilelist.append(libfilename)
            # print("Library file list")
            # print(libfilelist)


def readUIFile():
    getHeaderfiles()
    count = 0
    for item in libfilelist:
        fullpath = file_path + item
        fp = open(fullpath, 'r')
        for line in fp:
            m1 = re.search('class WXDLLIMPEXP_FWD_CORE [a-zA-Z0-9]*[:]{0,1}', line)
            if (m1 != None):
                classname = (m1.group(0)).split(" ")[2]
                if (classname in classlist):
                    count = count
                else:
                    # print (item,classname)
                    classlist.append(classname)
                    count = count + 1
            m2 = re.search('class WXDLLIMPEXP_CORE [a-zA-Z0-9]*[:]{0,1}', line)
            if (m2 != None):
                # print(item, m2.group())
                classname = (m2.group(0)).split(" ")[2]
                if (classname in classlist):
                    count = count
                else:
                    # print (item,classname)
                    classlist.append(classname)
                    count = count + 1
    for filename in glob.glob(msw_path + '*.h'):
        file = filename
        name = file.replace('\\', '/')
        # print(name)
        fp = open(name, 'r')
        for line in fp:
            m1 = re.search('class WXDLLIMPEXP_FWD_CORE [a-zA-Z0-9]*[:]{0,1}', line)
            if (m1 != None):
                classname = (m1.group(0)).split(" ")[2]
                if (classname in classlist):
                    count = count
                else:
                    # print (filename,classname)
                    classlist.append(classname)
                    count = count + 1
            m2 = re.search('class WXDLLIMPEXP_CORE [a-zA-Z0-9]*[:]{0,1}', line)
            if (m2 != None):
                # print(item, m2.group())
                classname = (m2.group(0)).split(" ")[2]
                if (classname in classlist):
                    count = count
                else:
                    # print (filename,classname)
                    classlist.append(classname)
                    count = count + 1
                    # print("Class list")
                    # print(classlist)


def readUserDefinedHeaderFiles():
    for filename in glob.glob(header_file_path + '*.h'):
        file = filename
        name = file.replace('\\', '/')
        # print(name)
        fp = open(name, 'r')
        for line in fp:
            m = re.search('class [a-zA-Z0-9]*: public wx[a-zA-Z]*', line)
            if (m != None):
                array1 = (m.group(0)).split(" ")
                classname = (array1[1]).replace(':', '')
                if (not (classname in classlist)):
                    classlist.append(classname)
                classname = array1[3]
                if (not (classname in classlist)):
                    classlist.append(classname)
                    # print(classlist)


def readHeaderfiles():
    # print(classlist)
    for line in test_file:
        m = re.search('include ["][a-zA-Z0-9/]*.h["]', line)
        if (m != None):
            arr = (m.group(0)).split(" ")
            filename = arr[1].replace('"', '')
            # path = 'C:/ProjectSE/wxRegitrationForm/WxRegitrationForm/WxRegitrationForm/' + filename
            path = 'C:/ProjectSE/WxLoginForm/WxLoginForm/' + filename
            # path = 'C:/ProjectSE/OpenCPN/include/' + filename
            hederfile = open(path, 'r')
            for eachline in hederfile:
                for x in classlist:
                    mystring = x + "[*]{0,1} [ ]*[a-zA-Z0-9_\\*]*"
                    m = re.search(mystring, eachline)
                    if (m != None):
                        # print(m.group())
                        objectname = (m.group()).split(" ")[1]
                        if (objectname is ''):
                            objectname = (m.group()).split(" ")[-1]
                            if (not (objectname is '')):
                                obj = objectname.replace('*', '')
                                if (not (obj is '')):
                                    if (not (obj in objectlist)):
                                        objectlist.append(obj)
                                    if (not ((x, obj) in classObjectDic.items())):
                                        classObjectDic[x].append(obj)

                        else:
                            objectname = (m.group()).split(" ")[1]
                            obj = objectname.replace('*', '')
                            if (not (obj is '')):
                                if (not (obj in objectlist)):
                                    objectlist.append(obj)
                                if (not ((x, obj) in classObjectDic.items())):
                                    classObjectDic[x].append(obj)


def getUIObjects():
    readUIFile()
    readUserDefinedHeaderFiles()
    readHeaderfiles()
    line_num = 0
    index = 0
    test_file.seek(0)
    for line in test_file:
        line_num = line_num + 1
        for x in classlist:
            mystring = x + "[*]{0,1} [ ]*[a-zA-Z0-9_\\*]*"
            m = re.search(mystring, line)
            if (m != None):
                # print(line_num, m.group())
                linelist.append(line_num)
                result.append([])
                result[index].append(line_num)
                result[index].append(x)
                objectname = (m.group()).split(" ")[1]
                if (objectname is ''):
                    objectname = (m.group()).split(" ")[-1]
                    if (not (objectname is '')):
                        obj = objectname.replace('*', '')
                        if (not (obj is '')):
                            result[index].append(obj)
                            if (not (obj in objectlist)):
                                objectlist.append(obj)
                            if (not ((x, obj) in classObjectDic.items())):
                                classObjectDic[x].append(obj)

                else:
                    objectname = (m.group()).split(" ")[1]
                    obj = objectname.replace('*', '')
                    if (not (obj is '')):
                        result[index].append(obj)
                        if (not (obj in objectlist)):
                            objectlist.append(obj)
                        if (not ((x, obj) in classObjectDic.items())):
                            classObjectDic[x].append(obj)
                index = index + 1
                # print(index)
    # print("Object list")
    # print(objectlist)
    # print("Line list")
    # print(linelist)
    # print("Dictionary")
    # print(classObjectDic)
    for index, (key, value) in enumerate(classObjectDic.items()):
        print(key, value)

    json.dump(classObjectDic, open("C:/ProjectSE/Parser/uifile.txt", 'w'))
    """for row in result:
        # Loop over columns.
        for column in row:
            print(column, end=" , ")
        print(end="\n")"""


def reverseDic(val):
    return next(key for key, value in classObjectDic.items() if value == val)


linevalueDic = []


def getUsedObjects():
    getUIObjects()
    test_file.seek(0)
    line_num = 1
    count = 0
    for line in test_file:
        for index, (key, value) in enumerate(classObjectDic.items()):
            list_of_elements = classObjectDic[key]
            for element in list_of_elements:
                if (line.find(element) != -1):
                    linevalueDic.append([])
                    linevalueDic[count].append(line_num)
                    linevalueDic[count].append(key)
                    linevalueDic[count].append(element)
                    count = count + 1

        line_num = line_num + 1
    for row in linevalueDic:
        # Loop over columns.
        for column in row:
            print(column, end," , ")
            print(end,"\n")

            highlightedlines = []

            def createHtmlfile():
                getUsedObjects()
                ishere = True
                f = open('C:/Users/Dinu/Desktop/FormLogin.html', 'a')
                msg1 = """<html>
    <head></head>
    <body><p>"""
                msg2 = """<br>"""
                msg3 = """</p></body>
    </html>"""
                msg4 = """<mark>"""
                msg5 = """</mark>"""
                f.write(msg1)
                test_file.seek(0)
                line_num = 1
                for line in test_file:
                    for x in objectlist:
                        if (line.find(x) != -1):
                            ishere = True
                            # print(line_num)
                            break
                        else:
                            ishere = False
                    if (ishere == True):
                        highlightedlines.append(line_num)
                        f.write(msg2 + str(line_num) + msg4 + line + msg5)
                    else:
                        f.write(msg2 + str(line_num) + line)
                    line_num = line_num + 1
                f.write(msg3)
                f.close()
                # webbrowser.open_new_tab('C:/ProjectSE/OpenCPN/src/toolbar.html')

            # getUsedObjects()
            # readUserDefinedHeaderFiles()
            #createHtmlfile()
            # getUIClassName(
getUIObjects()
            # createHtmlfile()
            # highlightFile()
