import block as bl
from random import randint
import rendering as re
from math import sin,pi,floor
import numpy as np
class Environment:
    def __init__(self,textures):
        self.__chunks = dict()
        self.__textures = textures
        self.__seed = '164879613145787'
    def getSeed(self):return self.__seed
    def getTextures(self): return self.__textures
    def getMaxHeight(self): return 126
    def getChunks(self): return self.__chunks
    def createChunk(self,n):
        chunk = Chunk(self,n)
        self.__chunks[str(n)] = chunk



class Chunk:
    def __init__(self,env,n):         # 1 chunk = 16 blocks, max height = 256
        self.__env = env
        self.__blocks = dict()
        self.__active = True
        self.__chunkNumber = n
        biomeRandom = randint(0,3)
        if biomeRandom == 0 :self.__biome = 'forest'
        elif biomeRandom == 1 : self.__biome = 'plain'
        elif biomeRandom == 2 : self.__biome = 'mountain'
        elif biomeRandom == 3 : self.__biome = 'ocean'
        else: pass
        self.__Y1 = 0
        self.__Y2 = 0
        self.__y0 = int(self.__env.getSeed())/10**15
        self.buildTerrain(n)
        
    def getY1(self): return self.__Y1
    def getY2(self): return self.__Y2
    def buildTerrain(self,n):
        if str(n+1) in self.__env.getChunks().keys():
            YConstraint = self.__env.getChunks()[str(n+1)].getY1()
            buildFrom = 'Right'
        elif str(n-1) in self.__env.getChunks().keys():
            YConstraint = self.__env.getChunks()[str(n-1)].getY2()
            buildFrom = 'Left'
        else:
            YConstraint = 'None'
            buildFrom = 'Left'

        if self.__biome == 'plain':
            offset = 20
            mountainHeightCoefficient = 4
            params = {'offset':offset,'mountainHeightCoefficient':mountainHeightCoefficient,'snowAltitude':40}
            self.buildTerrain_plain(params,buildFrom,YConstraint)
        if self.__biome == 'forest':
            offset = 20
            mountainHeightCoefficient = 4
            params = {'offset':offset,'mountainHeightCoefficient':mountainHeightCoefficient,'snowAltitude':40}
            self.buildTerrain_forest(params,buildFrom,YConstraint)
        if self.__biome == 'mountain':
            offset = 30
            mountainHeightCoefficient = 30
            params = {'offset':offset,'mountainHeightCoefficient':mountainHeightCoefficient,'snowAltitude':40}
            self.buildTerrain_mountain(params,buildFrom,YConstraint)
        if self.__biome == 'ocean':
            offset = 10
            mountainHeightCoefficient = 10
            params = {'offset':offset,'mountainHeightCoefficient':mountainHeightCoefficient,'snowAltitude':40,'surfaceAltitude':20}
            self.buildTerrain_ocean(params,buildFrom,YConstraint)
        
    def buildTerrain_plain(self,params,buildFrom,YConstraint):
        n = self.__chunkNumber
        X1 = 16*n
        X2 = 16*(n+1)
        if buildFrom == 'Left':
            if YConstraint == 'None':
                Y1 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n)
                Y2 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n+1)
            else:
                Y1 = YConstraint
                Y2 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n+1)
        else:
            Y2 = YConstraint
            Y1 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n-1)
        self.__Y1 = Y1
        self.__Y2 = Y2
        for X in range(X1,X2):
            for Y in range(self.__env.getMaxHeight()):
                earthFloor = floor(interpolation(X1,Y1,X2,Y2,X))
                if Y == earthFloor and Y< params['snowAltitude']:
                    block = bl.grass(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y == earthFloor and Y>= params['snowAltitude']:
                    block = bl.snowyGrass(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y< earthFloor and Y> earthFloor - 4:
                    block = bl.dirt(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y <= earthFloor - 4:
                    block = bl.rock(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                else: pass
        numberOfFlowers = randint(1,10)
        for f in range(numberOfFlowers):
            X = 16*n+randint(0,15)
            Y = floor(interpolation(X1,Y1,X2,Y2,X))+1
            self.createFlower(X,Y)
    def buildTerrain_forest(self,params,buildFrom,YConstraint):
        n = self.__chunkNumber
        X1 = 16*n
        X2 = 16*(n+1)
        if buildFrom == 'Left':
            if YConstraint == 'None':
                Y1 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n)
                Y2 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n+1)
            else:
                Y1 = YConstraint
                Y2 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n+1)
        else:
            Y2 = YConstraint
            Y1 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n-1)
        self.__Y1 = Y1
        self.__Y2 = Y2
        for X in range(X1,X2):
            for Y in range(self.__env.getMaxHeight()):
                earthFloor = floor(interpolation(X1,Y1,X2,Y2,X))
                if Y == earthFloor and Y>= params['snowAltitude']:
                    block = bl.snowyGrass(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y == earthFloor and Y< params['snowAltitude']:
                    block = bl.grass(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y< earthFloor and Y> earthFloor - 4:
                    block = bl.dirt(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y <= earthFloor - 4:
                    block = bl.rock(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                else: pass
                    
        numberOfTrees = randint(5,10)
        for f in range(numberOfTrees):
            X = 16*n+randint(0,15)
            Y = floor(interpolation(X1,Y1,X2,Y2,X))
            self.createTree(X,Y)
    def buildTerrain_mountain(self,params,buildFrom,YConstraint):
        n = self.__chunkNumber
        X1 = 16*n
        X2 = 16*(n+1)
        if buildFrom == 'Left':
            if YConstraint == 'None':
                Y1 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n)
                Y2 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n+1)
            else:
                Y1 = YConstraint
                Y2 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n+1)
        else:
            Y2 = YConstraint
            Y1 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n-1)
        self.__Y1 = Y1
        self.__Y2 = Y2
        for X in range(X1,X2):
            for Y in range(self.__env.getMaxHeight()):
                earthFloor = floor(interpolation(X1,Y1,X2,Y2,X))
                if Y == earthFloor and Y>= params['snowAltitude']:
                    block = bl.snowyGrass(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y == earthFloor and Y< params['snowAltitude']:
                    block = bl.dirt(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y< earthFloor:
                    block = bl.rock(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                else:
                    pass
    def buildTerrain_ocean(self,params,buildFrom,YConstraint):
        n = self.__chunkNumber
        X1 = 16*n
        X2 = 16*(n+1)
        if buildFrom == 'Left':
            if YConstraint == 'None':
                Y1 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n)
                Y2 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n+1)
            else:
                Y1 = YConstraint
                Y2 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n+1)
        else:
            Y2 = YConstraint
            Y1 = params['offset'] + params['mountainHeightCoefficient']*chaotic(self.__y0,n-1)
        self.__Y1 = Y1
        self.__Y2 = Y2
        for X in range(X1,X2):
            for Y in range(self.__env.getMaxHeight()):
                earthFloor = floor(interpolation(X1,Y1,X2,Y2,X))
                if Y > earthFloor and Y <= params['surfaceAltitude']:
                    block = bl.water(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y <= earthFloor and Y > earthFloor-2 and Y>= params['snowAltitude']:
                    block = bl.snowyGrass(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y <= earthFloor and Y > earthFloor-2 and Y< params['snowAltitude'] and Y> params['surfaceAltitude']:
                    block = bl.grass(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y <= earthFloor and Y > earthFloor-2 and Y< params['snowAltitude'] and Y< params['surfaceAltitude']:
                    block = bl.sand(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y<= earthFloor-2:
                    block = bl.rock(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                else:
                    pass
    
    def getBlocks(self): return self.__blocks
    def getEnv(self): return self.__env
    def activate(self): 
        self.__active = True
    def disactivate(self): self.__active = False
    
    def createTree(self,rootPosx,rootPosy):
        truncHeight = randint(2,4)
        truncPosKey = str(rootPosx)+'-'+str(rootPosy+1)
        if truncPosKey not in self.getBlocks().keys():
            if self.getBlocks()[str(rootPosx)+'-'+str(rootPosy)].getName() == 'grass' or self.getBlocks()[str(rootPosx)+'-'+str(rootPosy)].getName() == 'dirt':
                for j in range(rootPosy+1,rootPosy+1+truncHeight):
                    block = bl.wood(self.__env,rootPosx,j)
                    self.__blocks[str(rootPosx)+'-'+str(j)] = block
                for j in range(rootPosy+1+truncHeight,rootPosy+1+truncHeight+randint(2,4)):
                    for i in range(rootPosx-randint(1,2),rootPosx+randint(1,2)):
                        block = bl.leaf(self.__env,i,j)
                        self.__blocks[str(i)+'-'+str(j)] = block
    
    def createFlower(self,flowerPosx,flowerPosy):
        flowerPosKey = str(flowerPosx)+'-'+str(flowerPosy)
        underFlowerPosKey = str(flowerPosx)+'-'+str(flowerPosy-1)
        if flowerPosKey not in self.getBlocks().keys() and self.getBlocks()[underFlowerPosKey].getName() == 'grass':
            block = bl.redFlower(self.__env,flowerPosx,flowerPosy)
            self.__blocks[flowerPosKey] = block
    
def chaotic(y0,n):
    if n<0:
        n = -n+5
    for i in range(n):
        y1 = y0
        if y1<0.33:
            y0 = 1 - y1/0.33
        elif y1<0.66:
            y0 = (y1-0.33)/0.33
        else:
            y0 = 1-(y1-0.66)/0.34
    return y0
def interpolation(x1,y1,x2,y2,x):
        y1p = 0
        y2p = 0
        a =  -(2*y1 - 2*y2 - x1*y1p - x1*y2p + x2*y1p + x2*y2p)/((x1 - x2)*(x1**2 - 2*x1*x2 + x2**2))
        b = -(x1**2*(y1p) + 2*x1**2*(y2p) - 2*x2**2*(y1p) - x2**2*(y2p) - 3*x1*(y1) + 3*x1*(y2) - 3*x2*(y1) + 3*x2*(y2) + x1*x2*(y1p) - x1*x2*(y2p))/((x1 - x2)*(x1**2 - 2*x1*x2 + x2**2))
        c = (x1**3*(y2p) - x2**3*(y1p) - 6*x1*x2*(y1) + 6*x1*x2*(y2) - x1*x2**2*(y1p) + 2*x1**2*x2*(y1p) - 2*x1*x2**2*(y2p) + x1**2*x2*(y2p))/((x1 - x2)*(x1**2 - 2*x1*x2 + x2**2))
        d = (x1**3*(y2) - x2**3*(y1) + 3*x1*x2**2*(y1) - 3*x1**2*x2*(y2) + x1*x2**3*(y1p) - x1**3*x2*(y2p) - x1**2*x2**2*(y1p) + x1**2*x2**2*(y2p))/((x1 - x2)*(x1**2 - 2*x1*x2 + x2**2))
        y = a*x**3 + b*x**2 + c*x + d
        return y