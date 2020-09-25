from xml.dom import minidom
import os

class AppSetting:

    Config={}
    Root=""

    def __init__(self,PathRoot=""):
        self.Root = PathRoot
        xmlConfig = self.getFile()
        for elem in xmlConfig.getElementsByTagName('item'):
            self.Config.update({elem.attributes['name'].value:elem.firstChild.data})

    def getFile(self):
        __file__="app/appsetting/configWS.xml"
        return minidom.parse(os.path.abspath(__file__))
    
    def getElem(self, name):
        if(name!=None):
            return self.Config[name]
        return None
    
    def getConfig(self):
        return self.Config

    def getRoot(self):
        return self.Root
    