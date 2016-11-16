class WxObjects:

    def __init__(self,name, type):
        self.features = []

        self.name = name
        self.type = type
        self.innerObj = []

    def addObject(self,type2obj):
        self.innerObj.append(type2obj)
        print type2obj.name,"Obj added to ", self.name

    def addFeature(self,feature):

        self.features.append(feature)