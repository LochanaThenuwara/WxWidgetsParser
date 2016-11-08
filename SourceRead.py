import re
import WxObjects
import jsonpickle
import simplejson
import dicttoxml


type1={"panel"}
type2={"button","m_cb"}

objects={"panel":"wxPanel","button1":"wxButoon","m_cb":"wxCheckBox","button2":"wxButoon"}
foundObjects=[]

Mappings={"wxButton":"button","wxPanel":"div"}


wx_file= open('C:/ProjectSE/WxTest/WxTest/button.cpp','r')
# wx_file= open('C:/ProjectSE/wxCheckBox/wxCheckBox/checkbox.cpp','r')

def getUIobjName():

    for line in wx_file:

        for obj, type in objects.iteritems():

            searchStr = obj+" "+"="+" "+"new"

            if searchStr in line:
                print line
                obj=WxObjects.WxObjects(obj,type)
                foundObjects.append(obj)
                print obj.name," Object found in the code"

                parameters=getType1Obj(line)
                print len(parameters)

                for i in range(1,len(parameters)):
                    obj.addFeature(parameters[i])
                    print parameters[i], "feature",i

                if parameters[0] in type1:
                    for x in foundObjects:
                        if x.name == parameters[0]:
                            x.addObject(obj)
                            # x.addObject(obj)
                            print len(x.innerObj),"--------------------"
                            xtojson=jsonpickle.dumps(x)
                            xjsonObj=simplejson.loads(xtojson)
                            print xjsonObj, "******************"

                            type1xml = dicttoxml.dicttoxml(xjsonObj)
                            print "Type1 object xml :"
                            print(type1xml), "yeeeeeeeeeeeeeeeeeeeeesss"

                            xmlFile = open("ui.xml", "w")

                            xmlFile.write(type1xml)



                # tojsonObj = jsonpickle.dumps(obj)
                # jsonObj = simplejson.loads(tojsonObj)
                # print jsonObj,"******************"
                # print "object xml :"
                # xml = dicttoxml.dicttoxml(jsonObj)
                # print(xml),"yeeeeeeeeeeeeeeeeeeeeesss"


def getType1Obj(line):
    pattern=re.compile(r'\((.*)\)')

    match = re.search(pattern, line)

    print match.group()

    a=match.group(1).split(", ")

    if a[0] in type1:
        print a[0], " is the type1 obj found"
    return a



getUIobjName()