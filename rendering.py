import tkinter as Tk
from math import floor
import numpy as np
from PIL import Image,ImageTk

class Texture:
    def __init__(self,path):
        self._img = Tk.PhotoImage(file=path)
    def getImg(self): return self._img
class Textures:
    def __init__(self):
        dirt = Texture('.\\Textures\\dirt.gif')
        rock = Texture('.\\Textures\\rock.gif')
        water = Texture('.\\Textures\\water.gif')
        grass = Texture('.\\Textures\\grass.gif')
        snowyGrass = Texture('.\\Textures\\snowyGrass.gif')
        sand = Texture('.\\Textures\\sand.gif')
        wood = Texture('.\\Textures\\wood.gif')
        leaf = Texture('.\\Textures\\leaf.gif')
        redFlower = Texture('.\\Textures\\redFlower.gif')
        self.__textures = {'dirt':dirt,'rock':rock,'water':water,'grass':grass,'sand':sand,'wood':wood,'leaf':leaf,'redFlower':redFlower,'snowyGrass':snowyGrass}
    def getDict(self): return self.__textures
class Camera:
    def __init__(self,can,env):
        self.__height = int(can['height'])
        self.__width = int(can['width'])
        self.__can = can
        self.__env = env
        self.__posx = 8
        self.__posy = 25
        self.__chunkNumber = floor(self.__posx/16)
        self.__scale = 40
        self.__renderingDistanceInChunks = 2
        self.__moveVertical = 8
        self.__moveHorizontal = 16
    def getScale(self): return self.__scale
    def getPosx(self): return self.__posx
    def getPosy(self): return self.__posy
    def moveVertical(self,v): self.__posy += v
    def moveHorizontal(self,h): self.__posx -= h
    def position2pixel(self,x,y):
        xc = self.__posx
        yc = self.__posy
        xr = x-xc
        yr = y-yc
        px = self.__width//2 + xr*self.__scale
        py = self.__height//2 - yr*self.__scale
        return (px,py)
    def displayBlock(self,block):
        x = block.getx()
        y = block.gety()
        (px1,py1) = self.position2pixel(x,y)
        
        self.__can.delete(block.getDisplayAdress())
        try:
            img = block.getImg()
            adress = self.__can.create_image(px1+self.__scale//2,py1-self.__scale//2,image=img)
            
        except:
            px2 = px1 + self.__scale
            py2 = py1 - self.__scale
            adress = self.__can.create_rectangle(px1,py1,px2,py2,fill=block.getColor())
        block.setDisplayAdress(adress)
    def displayChunk(self,chunk):
        chunk.activate()
        for blk in chunk.getBlocks().items():
            self.displayBlock(blk[1])
    def eraseChunk(self,chunk):
        chunk.disactivate()
        for blk in chunk.getBlocks().items():
            self.__can.delete(blk[1].getDisplayAdress())
    def displayPlayer(self,player):
        x1 = player.getPosx() - 0.25
        y1 = player.getPosy() -0.9
        x2 = x1 + 0.5
        y2 = y1 + 1.8
        (px1,py1) = self.position2pixel(x1,y1)
        (px2,py2) = self.position2pixel(x2,y2)
        displayAdress = self.__can.create_rectangle(px1,py1,px2,py2,fill='black')
        player.setDisplayAdress(displayAdress)
    def displayEnv(self,env):
        for chunk in env.getChunks().items():
            self.displayChunk(chunk[1])
    def movePlayer(self,player,dx,dy):
        self.__can.move(player.getDisplayAdress(),dx*self.__scale,-dy*self.__scale)
        self.__can.tag_raise(player.getDisplayAdress())
    def bind(self,player,env):
        playerPosx = player.getPosx()
        camPosx = self.__posx
        playerPosy = player.getPosy()
        camPosy = self.__posy
        diffx = playerPosx-camPosx
        diffy = playerPosy-camPosy
        if diffx > 10:
            self.moveHorizontal(-20)
            self.displayEnv(env)
            self.__can.delete(player.getDisplayAdress())
            self.displayPlayer(player)
        elif diffx < -10:
            self.moveHorizontal(20)
            self.displayEnv(env)
            self.__can.delete(player.getDisplayAdress())
            self.displayPlayer(player)
        else: pass

        if diffy > 8:
            self.moveVertical(8)
            self.displayEnv(env)
            self.__can.delete(player.getDisplayAdress())
            self.displayPlayer(player)
        elif diffy < -8:
            self.moveVertical(-8)
            self.displayEnv(env)
            self.__can.delete(player.getDisplayAdress())
            self.displayPlayer(player)
        else: pass     
    def updateChunkRendeering(self,player):
        playerChunk = player.getChunkNumber()
        for chunk in self.__env.getChunks().items():
            self.eraseChunk(chunk[1])
        for n in range(-self.__renderingDistanceInChunks+playerChunk,self.__renderingDistanceInChunks+playerChunk):
            try :
                self.displayChunk(self.__env.getChunks()[str(n)])
            except:
                self.__env.createChunk(n)
                self.displayChunk(self.__env.getChunks()[str(n)])
            

def skyColor(time,w,h):
    size = (100,100)
    img = Image.new('RGB', size)
    upColor = [[0,0,0],[0,7,107],[0,65,163],[0,7,107]]
    downColor = [[0,0,0],[250,196,0],[150, 192, 255],[250,196,0]]

    if time < 50:
        Cu1 = upColor[0]
        Cu2 = upColor[1]
        Cd1 = downColor[0]
        Cd2 = downColor[1]
        alpha = (time-0)/50
    elif time < 100:
        Cu1 = upColor[1]
        Cu2 = upColor[2]
        Cd1 = downColor[1]
        Cd2 = downColor[2]
        alpha = (time-50)/50
    elif time < 150:
        Cu1 = upColor[2]
        Cu2 = upColor[3]
        Cd1 = downColor[2]
        Cd2 = downColor[3]
        alpha = (time-100)/50
    else:
        Cu1 = upColor[3]
        Cu2 = upColor[0]
        Cd1 = downColor[3]
        Cd2 = downColor[0]
        alpha = (time-150)/50

    R = np.linspace(Cu1[0]+(Cu2[0]-Cu1[0])*alpha,Cd1[0]+(Cd2[0]-Cd1[0])*alpha,100)
    G = np.linspace(Cu1[1]+(Cu2[1]-Cu1[1])*alpha,Cd1[1]+(Cd2[1]-Cd1[1])*alpha,100)
    B = np.linspace(Cu1[2]+(Cu2[2]-Cu1[2])*alpha,Cd1[2]+(Cd2[2]-Cd1[2])*alpha,100)
    for i in range(100):
        for j in range(100):
            color = (int(R[j]),int(G[j]),int(B[j]))
            img.putpixel((i,j),color)
    img = img.resize((w*2,h*2))
    img.save('.\\skies\\sky-'+str(int(time))+'.gif', "GIF")
    

