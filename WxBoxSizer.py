class WxBoxSizer:

    def __init__(self,name, type):
        self.features = []

        self.name = name
        self.type = type
        self.innerObj = []
        self.direction=""

    def addObjectName(self,obj_name):
        self.innerObj.append(obj_name)
        print obj_name,"Objname added to ", self.name

    def addFeature(self,feature):

        self.features.append(feature)