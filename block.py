import tkinter as Tk
from PIL import Image

class block:
    def __init__(self,env,x,y):
        self._x = x
        self._y = y
        self._env = env
        self._color = 'black'
        self._displayAdress = ''
        self._type = 'opaque'
        self._name = 'block'
    def getEnv(self): return self._env
    def getx(self): return self._x
    def gety(self): return self._y
    def getColor(self): return self._color
    def getDisplayAdress(self): return self._displayAdress
    def setDisplayAdress(self,adress): self._displayAdress = adress
    def getType(self): return self._type
    def getName(self): return self._name
class dirt(block):
    def __init__(self,env,x,y):
        block.__init__(self,env,x,y)
        self._color = '#834436'
        self._type = 'opaque'
        self._name = 'dirt'
        self._texture = env.getTextures().getDict()['dirt']
    def getImg(self): return self._texture.getImg()
    def getName(self): return self._name
class grass(block):
    def __init__(self,env,x,y):
        block.__init__(self,env,x,y)
        self._color = '#834436'
        self._type = 'opaque'
        self._name = 'grass'
        self._texture = env.getTextures().getDict()['grass']
    def getImg(self): return self._texture.getImg()
class rock(block):
    def __init__(self,env,x,y):
        block.__init__(self,env,x,y)
        self._color = '#B1B1B1'
        self._type = 'opaque'
        self._name = 'rock'
        self._texture = env.getTextures().getDict()['rock']
    def getImg(self): return self._texture.getImg()
class water(block):
    def __init__(self,env,x,y):
        block.__init__(self,env,x,y)
        self._color = '#0670FF'
        self._type = 'fluid'
        self._name = 'water'
        self._texture = env.getTextures().getDict()['water']
    def getImg(self): return self._texture.getImg()
class sand(block):
    def __init__(self,env,x,y):
        block.__init__(self,env,x,y)
        self._color = '#E8DE75'
        self._type = 'opaque'
        self._name = 'sand'
        self._texture = env.getTextures().getDict()['sand']
    def getImg(self): return self._texture.getImg()
class wood(block):
    def __init__(self,env,x,y):
        block.__init__(self,env,x,y)
        self._color = '#FFFFFF'
        self._type = 'opaque'
        self._name = 'wood'
        self._texture = env.getTextures().getDict()['wood']
    def getImg(self): return self._texture.getImg()
class leaf(block):
    def __init__(self,env,x,y):
        block.__init__(self,env,x,y)
        self._color = '#FFFFFF'
        self._type = 'opaque'
        self._name = 'leaf'
        self._texture = env.getTextures().getDict()['leaf']
    def getImg(self): return self._texture.getImg()
class redFlower(block):
    def __init__(self,env,x,y):
        block.__init__(self,env,x,y)
        self._color = '#FFFFFF'
        self._type = 'none'
        self._name = 'redFlower'
        self._texture = env.getTextures().getDict()['redFlower']
    def getImg(self): return self._texture.getImg()
class snowyGrass(block):
    def __init__(self,env,x,y):
        block.__init__(self,env,x,y)
        self._color = '#FFFFFF'
        self._type = 'opaque'
        self._name = 'snowyGrass'
        self._texture = env.getTextures().getDict()['snowyGrass']
    def getImg(self): return self._texture.getImg()