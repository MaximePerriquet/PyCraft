import tkinter as Tk
from math import floor
import numpy as np
from PIL import Image,ImageTk

## ---------------------- ##
##|       CLASSES        |##
## ---------------------- ##
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
        self.__scale = 40 # Block rendering size - DO NOT CHANGE WITHOUT RESIZE TEXTURES

        # Camera position when starting
        self.__posx = 8
        self.__posy = 25
        self.__chunkNumber = floor(self.__posx/16)
        
        # Options
        self.__renderingDistanceInChunks = 2
        self.__moveVertical = 8
        self.__moveHorizontal = 16
        self.__skyUpdateTime = 1
        self.__horzCamFollowing = 5
        self.__vertCamFollowing = 5

        # Data sets
        self.__skies = dict()
        self.__brightnesses = dict()
        
        # skyRendering initialization
        self.computeAndLoadImages()
        backgroundImage = self.__skies['sky-0']
        brightnessImage = self.__brightnesses['br-0']
        self.__sky = self.__can.create_image(self.__width//2,self.__height//2,image=backgroundImage)
        self.__brightness = self.__can.create_image(self.__width//2,self.__height//2,image=brightnessImage)
    
    # Get useful values
    def getScale(self): return self.__scale
    def getPosx(self): return self.__posx
    def getPosy(self): return self.__posy

    # Convert a frame position into canvas position
    def position2pixel(self,x,y):
        xc = self.__posx
        yc = self.__posy
        xr = x-xc
        yr = y-yc
        px = self.__width//2 + xr*self.__scale
        py = self.__height//2 - yr*self.__scale
        return (px,py)
    
    # Display stuff
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

    # Move stuff
    def moveBlock(self,block,dx,dy):
        self.__can.move(block.getDisplayAdress(),dx*self.__scale,-dy*self.__scale)
    def moveChunk(self,chunk,dx,dy):
        for blk in chunk.getBlocks().items():
            self.moveBlock(blk[1],dx,dy)
    def movePlayer(self,player,dx,dy):
        self.__can.move(player.getDisplayAdress(),dx*self.__scale,-dy*self.__scale)
        self.__can.tag_raise(player.getDisplayAdress())
    def moveEnv(self,dx,dy):
        for chunk in self.__env.getChunks().items():
            self.moveChunk(chunk[1],dx,dy)
    
    # Chunk rendering methods
    def eraseChunk(self,chunk):
        chunk.disactivate()
        for blk in chunk.getBlocks().items():
            self.__can.delete(blk[1].getDisplayAdress())
    def updateChunkRendeering(self,player):
        playerChunk = player.getChunkNumber()
        for chunk in self.__env.getChunks().items():
            if abs(chunk[1].getChunkNumber() - playerChunk) > self.__renderingDistanceInChunks:
                self.eraseChunk(chunk[1])
        for n in range(-self.__renderingDistanceInChunks+playerChunk,self.__renderingDistanceInChunks+playerChunk):
            if str(n) in self.__env.getChunks().keys():
                if not self.__env.getChunks()[str(n)].isActive(): 
                    self.displayChunk(self.__env.getChunks()[str(n)])
            else:
                self.__env.createChunk(n)
                self.displayChunk(self.__env.getChunks()[str(n)])
    
    # Sky and brightness 
    def computeAndLoadImages(self):
        print('     Creating and loading skies...')
        T = self.__env.getDayAndNightCyclesDuration()
        for t in range(0,T,self.__skyUpdateTime):
            try:
                self.__skies['sky-'+str(t)] = Tk.PhotoImage(file=".\\skies\\sky-"+str(int(t))+".gif")
            except:
                skyColor(t,self.__width,self.__height,T)
                self.__skies['sky-'+str(t)] = Tk.PhotoImage(file=".\\skies\\sky-"+str(int(t))+".gif")
        print('     Creating and loading brightnesses...')
        for t in range(0,T,self.__skyUpdateTime):
            try:
                self.__brightnesses['br-'+str(t)] = Tk.PhotoImage(file=".\\brightnesses\\br-"+str(int(t))+".png")
            except:
                brightness(t,self.__width,self.__height,T)
                self.__brightnesses['br-'+str(t)] = Tk.PhotoImage(file=".\\brightnesses\\br-"+str(int(t))+".png")
    def updateSkyAndBrightnessRendering(self,t1,t2):
        if floor(t1/self.__skyUpdateTime) == floor(t2/self.__skyUpdateTime) -1:
            self.__can.delete(self.__sky)
            self.__can.delete(self.__brightness)
            T = self.__env.getDayAndNightCyclesDuration()
            backgroundImage = self.__skies['sky-'+str(int(t2%T))]
            brightnessImage = self.__brightnesses['br-'+str(int(t2%T))]
            self.__sky = self.__can.create_image(self.__width//2,self.__height//2,image=backgroundImage)
            self.__brightness = self.__can.create_image(self.__width//2,self.__height//2,image=brightnessImage)
            self.reorder()
    
    # Set all stuff on the good plane
    def reorder(self):
        self.__can.tag_lower(self.__sky)
        self.__can.tag_raise(self.__brightness)

    # Camera function call
    def bind(self,player,env,t1,t2):
        playerPosx = player.getPosx()
        camPosx = self.__posx
        playerPosy = player.getPosy()
        camPosy = self.__posy
        diffx = playerPosx-camPosx
        diffy = playerPosy-camPosy
        if (diffx/self.__horzCamFollowing)**2 + (diffy/self.__vertCamFollowing)**2 > 1:
            self.moveEnv(-diffx,-diffy)
            self.__posx += diffx
            self.__posy += diffy
            self.__can.delete(player.getDisplayAdress())
            self.displayPlayer(player)
        self.updateSkyAndBrightnessRendering(t1,t2)  
    
## ---------------------- ##
##| ADDITIONAL FUNCTIONS |##
## ---------------------- ##
# Create the sky images
def skyColor(time,w,h,dayAndNightCycleTime):
    T = dayAndNightCycleTime
    transitionTime = dayAndNightCycleTime//6
    size = (100,100)
    img = Image.new('RGB', size)
    upColor = [[0,0,0],[0,7,107],[0,65,163],[0,7,107]]
    downColor = [[0,0,0],[250,196,0],[150, 192, 255],[250,196,0]]
    
    if time < T//4 - transitionTime//2:
        Cu1 = upColor[0]
        Cu2 = upColor[1]
        Cd1 = downColor[0]
        Cd2 = downColor[1]
        alpha = 0
    elif time < T//4:
        Cu1 = upColor[0]
        Cu2 = upColor[1]
        Cd1 = downColor[0]
        Cd2 = downColor[1]
        alpha = (time-(T//4 - transitionTime//2))/(transitionTime//2)
    elif time < T//4 + transitionTime//2:
        Cu1 = upColor[1]
        Cu2 = upColor[2]
        Cd1 = downColor[1]
        Cd2 = downColor[2]
        alpha = (time-T//4)/(transitionTime//2)
    elif time < 3*T//4 - transitionTime//2:
        Cu1 = upColor[2]
        Cu2 = upColor[2]
        Cd1 = downColor[2]
        Cd2 = downColor[2]
        alpha = 0
    elif time < 3*T//4:
        Cu1 = upColor[2]
        Cu2 = upColor[3]
        Cd1 = downColor[2]
        Cd2 = downColor[3]
        alpha = (time-(3*T//4 - transitionTime//2))/(transitionTime//2)
    elif time < 3*T//4 + transitionTime//2:
        Cu1 = upColor[3]
        Cu2 = upColor[0]
        Cd1 = downColor[3]
        Cd2 = downColor[0]
        alpha = (time-3*T//4)/(transitionTime//2)
    else:
        Cu1 = upColor[0]
        Cu2 = upColor[0]
        Cd1 = downColor[0]
        Cd2 = downColor[0]
        alpha = 1

    R = np.linspace(Cu1[0]+(Cu2[0]-Cu1[0])*alpha,Cd1[0]+(Cd2[0]-Cd1[0])*alpha,100)
    G = np.linspace(Cu1[1]+(Cu2[1]-Cu1[1])*alpha,Cd1[1]+(Cd2[1]-Cd1[1])*alpha,100)
    B = np.linspace(Cu1[2]+(Cu2[2]-Cu1[2])*alpha,Cd1[2]+(Cd2[2]-Cd1[2])*alpha,100)
    for i in range(100):
        for j in range(100):
            color = (int(R[j]),int(G[j]),int(B[j]))
            img.putpixel((i,j),color)
    img = img.resize((w*2,h*2))
    img.save('.\\skies\\sky-'+str(int(time))+'.gif', "GIF")
    
# Create the brightness images
def brightness(time,w,h,dayAndNightCycleTime):
    T = dayAndNightCycleTime
    transitionTime = dayAndNightCycleTime//6
    size = (w,h)
    maxOpacity = 200
    if time <T//4 - transitionTime//2:
        transparency = maxOpacity
    elif time < T//4 + transitionTime//2:
        transparency = int(-(time-(T//4 - transitionTime//2))/transitionTime*maxOpacity+maxOpacity)
    elif time < 3*T//4 - transitionTime//2:
        transparency = 0
    elif time < 3*T//4 + transitionTime//2:
        transparency = int((time-(3*T//4 - transitionTime//2))/transitionTime*maxOpacity)
    else:
        transparency = maxOpacity
    print(transparency)
    img = Image.new('RGBA', size,(0,0,0,transparency))
    img.save('.\\brightnesses\\br-'+str(int(time))+'.png', "PNG")
    
