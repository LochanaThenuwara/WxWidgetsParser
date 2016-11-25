import WxObjects

class WxCheckBox(WxObjects.WxObjects):
    def __init__(self,name, type):
        self.name = name
        self.type = type

        self.wxT=None
        self.wxID = ""
        self.wxPoint=[]

        self.innerObj = []