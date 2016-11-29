import re
import WxObjects
import jsonpickle
import simplejson
import dicttoxml
import WxButton
import WxCheckBox
import WxStaticText
import WxTextCtrl
import WxBoxSizer

sizers={"vbox":None,"hbox1":None,"hbox2":None,"hbox3":None}
type1={"panel":None}
type2={"button1","button2S","m_cb"}


objects={"panel":"wxPanel","m_cb":"wxCheckBox","button1":"wxButton","button2":"wxButton",
         "m_usernameLabel":"wxStaticText","m_usernameEntry":"wxTextCtrl","m_passwordLabel":"wxStaticText",
         "m_passwordEntry":"wxTextCtrl","m_buttonLogin":"wxButton","m_buttonQuit":"wxButton","vbox":"wxBoxSizer","hbox1":"wxBoxSizer","hbox2":"wxBoxSizer",
         "hbox3": "wxBoxSizer"}
foundObjects=[]

Mappings={"wxButton":"button","wxPanel":"div"}


# wx_file= open('C:/ProjectSE/WxTest/WxTest/button.cpp','r')
# wx_file= open('C:/ProjectSE/wxCheckBox/wxCheckBox/checkbox.cpp','r')
wx_file= open('C:/ProjectSE/WxLoginForm/WxLoginForm/FormLogin.cpp','r')

def getUIobjName():
    normal = True

    for line in wx_file:

        for obj, type in objects.iteritems():

            searchStr = obj+" "+"="+" "+"new"
            sizerStr="->Add("+obj


            if (searchStr in line):

                if type=="wxBoxSizer":
                    pattern = re.compile(r'\((.*)\)')

                    match = re.search(pattern, line)

                    print match.group()
                    parameters=match.group()
                    print parameters

                else:
                    print line
                    parameters = getType1Obj(line)
                    print type, "+_+_+_+_"



                if type=="wxButton":
                    obj = WxButton.WxButton(obj, type)
                    obj.panel=parameters[0]
                    for i in range(1, len(parameters)):


                        if "wxT"in parameters[i]:
                            word =re.findall('"([^"]*)"', parameters[i])
                            obj.wxT=word[0]

                        elif "wxPoint"in parameters[i]:
                            pattern = re.compile(r'\((.*)\)')
                            match = re.search(pattern, parameters[i])
                            print match.group()
                            a = match.group(1).split(",")
                            obj.wxPoint=[a]

                        elif "wxID" in parameters[i]:
                            obj.wxID=parameters[i].split("_")[1]
                            print obj.wxID

                if type=="wxBoxSizer":
                    objName=obj
                    obj = WxBoxSizer.WxBoxSizer(objName, type)

                    if "wxHORIZONTAL"in parameters:
                        obj.direction="wxHORIZONTAL"
                    elif "wxVERTICAL"in parameters:
                        obj.direction="wxVERTICAL"

                    sizers[objName]=obj


                elif type=="wxCheckBox":
                    obj = WxCheckBox.WxCheckBox(obj, type)
                    obj.panel = parameters[0]

                    for i in range(1, len(parameters)):
                        if "wxT"in parameters[i]:
                            word =re.findall('"([^"]*)"', parameters[i])
                            obj.wxT=word[0]

                        elif "wxPoint"in parameters[i]:
                            pattern = re.compile(r'\((.*)\)')
                            match = re.search(pattern, parameters[i])
                            print match.group()
                            a = match.group(1).split(",")
                            obj.wxPoint=[a]

                        elif "wxID" in parameters[i]:
                            obj.wxID=parameters[i].split("_")[1]
                            print obj.wxID

                elif type=="wxStaticText":
                    obj = WxStaticText.WxStaticText(obj, type)
                    obj.panel = parameters[0]

                    for i in range(1, len(parameters)):
                        if "wxT"in parameters[i]:
                            word =re.findall('"([^"]*)"', parameters[i])
                            obj.wxT=word[0]

                        elif "wxPoint"in parameters[i]:
                            pattern = re.compile(r'\((.*)\)')
                            match = re.search(pattern, parameters[i])
                            print match.group()
                            a = match.group(1).split(",")
                            obj.wxPoint=[a]

                        elif "wxID" in parameters[i]:
                            obj.wxID=parameters[i].split("_")[1]
                            # print obj.wxID

                        elif "wxString" in parameters[i]:
                            word = re.findall('"([^"]*)"', parameters[i])
                            obj.wxString = word[0]

                        elif "wxSize" in parameters[i]:
                            pattern = re.compile(r'\((.*)\)')
                            match = re.search(pattern, parameters[i])
                            print match.group()
                            a = match.group(1).split(",")
                            obj.wxSize = [a]

                elif type=="wxTextCtrl":
                    obj = WxTextCtrl.WxTextCtrl(obj, type)
                    obj.panel = parameters[0]

                    for i in range(1, len(parameters)):
                        if "wxT("in parameters[i]:
                            word =re.findall('"([^"]*)"', parameters[i])
                            obj.wxT=word[0]

                        elif "wxPoint"in parameters[i]:
                            pattern = re.compile(r'\((.*)\)')
                            match = re.search(pattern, parameters[i])
                            # print match.group()
                            a = match.group(1).split(",")
                            obj.wxPoint=[a]

                        elif "wxID" in parameters[i]:
                            obj.wxID=parameters[i].split("_")[1]
                            # print obj.wxID

                        elif "DefaultPosition" in parameters[i]:
                            obj.wxPoint = [-1,-1]

                        elif "DefaultSize" in parameters[i]:
                            obj.wxSize = [-1,-1]

                        elif "wxTE" in parameters[i]:
                            obj.wxTE = parameters[i].split("_")[1]
                            # print obj.wxTE,"wxTE.........................."


                elif type=="wxPanel":
                    obj= WxObjects.WxObjects(obj,type)

                    type1[obj.name]=obj

                    for i in range(1, len(parameters)):
                        obj.addFeature(parameters[i])
                        print parameters[i], "feature", i

                foundObjects.append(obj)
                print obj.name," Object found in the code"

                # if parameters[0] in type1:
                #     for x in foundObjects:
                #         if x.name == parameters[0]:
                #             x.addObject(obj)
                #             # x.addObject(obj)
                #             print len(x.innerObj),"--------------------"
                #             convertToXml(x)
            elif (sizerStr in line):
                sizer = line.split("->")[0].split()[0]
                print "---------------------****************--------------------", obj

                if sizers.has_key(sizer):
                    print "---------------------chanaka--------------------", sizers[sizer]
                    sizerObj = sizers[sizer]

                    for x in foundObjects:
                        if x.name==obj:
                            sizers[sizer].addObject(x)

        for panels,panelObj in type1.iteritems():

            if panels+"->SetSizer" in line:
                normal=False
                m = re.search(r"\(([A-Za-z0-9_]+)\)", line)
                boxs=m.group(1)
                panelObj.addObject(sizers[boxs]);

    if normal:
        for wxObj in foundObjects:

            if wxObj.name in type2:
                print wxObj.type, "ttttttttttttttttttttttt"
                panelObj.addObject(wxObj);



    for panels, panelObj in type1.iteritems():
        convertToXml(panelObj)

def getType1Obj(line):
    pattern=re.compile(r'\((.*)\)')

    match = re.search(pattern, line)

    print match.group()

    a=match.group(1).split(", ")

    if a[0] in type1:
        print a[0], " is the type1 obj found"
    return a


def convertToXml(x):
    xtojson = jsonpickle.dumps(x)
    xjsonObj = simplejson.loads(xtojson)
    print xjsonObj, "******************"

    type1xml = dicttoxml.dicttoxml(xjsonObj)
    print "Type1 object xml :"
    print(type1xml)

    # xmlFile = open("C:\wamp\www\ui.xml", "w")
    xmlFile = open("C:\wamp\www\BootstrapConverter\ui.xml", "w")

    xmlFile.write(type1xml)


getUIobjName()