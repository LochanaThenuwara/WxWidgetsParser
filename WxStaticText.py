import WxObjects

class WxStaticText(WxObjects.WxObjects):
    def __init__(self,name, type):
        self.name = name
        self.type = type

        self.wxT=None
        self.wxID = ""
        self.wxString=""
        self.wxSize=[]
        self.wxPoint=[]

        self.innerObj = []