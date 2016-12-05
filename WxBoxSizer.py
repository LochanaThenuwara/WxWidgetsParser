class WxBoxSizer:

    def __init__(self,name, type):
        self.features = []

        self.name = name
        self.type = type
        self.innerObj = []
        self.direction=""

    def addObject(self,obj):
        self.innerObj.append(obj)
        print obj.name,"Obj---- added to ", self.name

    def addFeature(self,feature):

        self.features.append(feature)