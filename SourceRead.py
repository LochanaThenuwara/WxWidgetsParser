import re
import WxObjects
import jsonpickle
import simplejson
import dicttoxml
import WxButton


type1={"panel"}
type2={"button","m_cb"}

objects={"panel":"wxPanel","m_cb":"wxCheckBox","button1":"wxButton","button2":"wxButton"}
foundObjects=[]

Mappings={"wxButton":"button","wxPanel":"div"}


# wx_file= open('C:/ProjectSE/WxTest/WxTest/button.cpp','r')
wx_file= open('C:/ProjectSE/wxCheckBox/wxCheckBox/checkbox.cpp','r')

def getUIobjName():

    for line in wx_file:

        for obj, type in objects.iteritems():

            searchStr = obj+" "+"="+" "+"new"

            if searchStr in line:
                print line
                parameters = getType1Obj(line)
                print parameters[0],"+_+_+_+_"

                if type=="wxButton":
                    obj = WxButton.WxButton(obj, type)

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




                else:
                    obj= WxObjects.WxObjects(obj,type)
                    for i in range(1, len(parameters)):
                        obj.addFeature(parameters[i])
                        print parameters[i], "feature", i



                foundObjects.append(obj)
                print obj.name," Object found in the code"





                if parameters[0] in type1:
                    for x in foundObjects:
                        if x.name == parameters[0]:
                            x.addObject(obj)
                            # x.addObject(obj)
                            print len(x.innerObj),"--------------------"
                            convertToXml(x)



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