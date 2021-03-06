import block as bl
from random import randint
import rendering as re
from math import sin,pi,floor

## ---------------------- ##
##|       CLASSES        |##
## ---------------------- ##
class Environment:
    ## Here we : 
    # - initiate the environment, 
    # - define biome suite, 
    # - define biomes lengths
    # - define chunks biomes
    def __init__(self,textures):                                                    ## --- Update when adding a biome
        self.__biomes = ['plain','mountain','forest','ocean']                       ## --- Update when adding a biome
        self.__biomesLen = {'plain':4,'mountain':2,'forest':5,'ocean':3}            ## --- Update when adding a biome
        self.__chunks = dict()
        self.__biomesSuite = {'left':-1,'right':0}
        self.__chunksBiomes = {'left':-1,'right':0}
        self.__textures = textures
        self.__seed = '274879613145787'
        self.__oceanSurfaceAltitude = 20
        self.__snowAltitude = 40
        self.__maxHeight = 126
        self.__dayAndNightCycleDuration = 256
        self.__biomesTransitionConstraints = {
            'ocean-plain':self.__oceanSurfaceAltitude+2,
            'ocean-forest':self.__oceanSurfaceAltitude+2,
            'ocean-mountain':self.__oceanSurfaceAltitude+2,
            'plain-ocean':self.__oceanSurfaceAltitude+2,
            'forest-ocean':self.__oceanSurfaceAltitude+2,
            'mountain-ocean':self.__oceanSurfaceAltitude+2
            }

    ## Here we get some useful values
    def getDayAndNightCyclesDuration(self): return self.__dayAndNightCycleDuration
    def getSnowAltitude(self): return self.__snowAltitude
    def getBiomesTransitionsConstraints(self): return self.__biomesTransitionConstraints
    def getChunksBiomes(self): return self.__chunksBiomes
    def getOceanSurfaceAltitude(self): return self.__oceanSurfaceAltitude
    def getSeed(self):return self.__seed
    def getTextures(self): return self.__textures
    def getMaxHeight(self): return self.__maxHeight
    def getChunks(self): return self.__chunks
    
    # Here we create the biome suite
    def increaseBiomeSuite(self):
        # Procedural generation of the biome suite
        bMax = len(self.__biomes)
        sMax = len(self.__seed)
        bLeft = self.__biomesSuite['left']
        bRight = self.__biomesSuite['right']
        newBiomeRight = self.__biomes[int(self.__seed[bRight%sMax])%bMax]
        newBiomeLeft = self.__biomes[int(self.__seed[(bLeft-1)%sMax])%bMax]
        self.__biomesSuite['left'] = bLeft - 1
        self.__biomesSuite['right'] = bRight + 1
        leftChunkNumber = self.__chunksBiomes['left']
        rightChunkNumber = self.__chunksBiomes['right']
        for chunkNumber in range(leftChunkNumber,leftChunkNumber - self.__biomesLen[newBiomeLeft],-1):
            self.__chunksBiomes[str(chunkNumber)] = newBiomeLeft
        self.__chunksBiomes['left'] = chunkNumber-1
        for chunkNumber in range(rightChunkNumber,rightChunkNumber + self.__biomesLen[newBiomeRight]):
            self.__chunksBiomes[str(chunkNumber)] = newBiomeRight
        self.__chunksBiomes['right'] = chunkNumber+1

    ## Here we create a chunk
    def createChunk(self,n):
        chunk = Chunk(self,n)
        self.__chunks[str(n)] = chunk

class Chunk:
    def __init__(self,env,n):         # 1 chunk = 16 blocks
        self.__env = env
        self.__blocks = dict()
        self.__active = False
        self.__chunkNumber = n

        # Assign a biome
        while not str(n) in self.__env.getChunksBiomes().keys():
            self.__env.increaseBiomeSuite()
        self.__biome = self.__env.getChunksBiomes()[str(n)]

        self.__Y1 = 0
        self.__Y2 = 0
        self.__y0 = int(self.__env.getSeed())/10**len(self.__env.getSeed())
        self.buildTerrain(n)
    
    ## Here we get some useful values
    def getChunkNumber(self): return self.__chunkNumber
    def getY1(self): return self.__Y1
    def getY2(self): return self.__Y2
    def getBlocks(self): return self.__blocks
    def getEnv(self): return self.__env
    def isActive(self): return self.__active
    ## Here we display or erase chunk rendering
    def activate(self): 
        self.__active = True
    def disactivate(self): self.__active = False

    ## Chunk generation method                                          ## --- Update when adding a biome
    def buildTerrain(self,n):
        # Creating a plain
        if self.__biome == 'plain':
            offset = 20
            mountainHeightCoefficient = 4
            self.__params = {'offset':offset,'mountainHeightCoefficient':mountainHeightCoefficient,'snowAltitude':40}
            self.computeBorders()
            self.buildTerrain_plain()
        # Creating a forest
        if self.__biome == 'forest':
            offset = 20
            mountainHeightCoefficient = 4
            self.__params = {'offset':offset,'mountainHeightCoefficient':mountainHeightCoefficient,'snowAltitude':40}
            self.computeBorders()
            self.buildTerrain_forest()
        # Creating a mountain
        if self.__biome == 'mountain':
            offset = 30
            mountainHeightCoefficient = 30
            self.__params = {'offset':offset,'mountainHeightCoefficient':mountainHeightCoefficient,'snowAltitude':40}
            self.computeBorders()
            self.buildTerrain_mountain()
        # Creating an ocean
        if self.__biome == 'ocean':
            offset = 10
            mountainHeightCoefficient = 10
            self.__params = {'offset':offset,'mountainHeightCoefficient':mountainHeightCoefficient,'snowAltitude':40,'surfaceAltitude':20}
            self.computeBorders()
            self.buildTerrain_ocean()
    def computeBorders(self):
        n = self.__chunkNumber
        self.__X1 = 16*n
        self.__X2 = 16*(n+1)
        # Building from left ?
        if str(n-1) in self.__env.getChunks().keys():
            # Left continuity
            self.__Y1 = self.__env.getChunks()[str(n-1)].getY2()    
            # Check if biome suite is big enought
            if str(n+1) in self.__env.getChunksBiomes().keys():
                pass
            else:
                while not str(n+1) in self.__env.getChunksBiomes().keys():
                    self.__env.increaseBiomeSuite()
                    
            # Check if the biome transition is constrained and apply constraint
            rightTransition = self.__biome + '-' + self.__env.getChunksBiomes()[str(n+1)]
            if rightTransition in self.__env.getBiomesTransitionsConstraints().keys():
                self.__Y2 = self.__env.getBiomesTransitionsConstraints()[rightTransition]
            else:
                self.__Y2 = self.__params['offset'] + self.__params['mountainHeightCoefficient']*chaotic(self.__y0,n+1)
        # Building from right ?
        elif str(n+1) in self.__env.getChunks().keys():
            # Right continuity
            self.__Y2 = self.__env.getChunks()[str(n+1)].getY1() 
            # Check if biome suite is big enought
            if str(n-1) in self.__env.getChunksBiomes().keys():
                pass
            else:
                while not str(n-1) in self.__env.getChunksBiomes().keys():
                    self.__env.increaseBiomeSuite() 
                    
            # Check if the biome transition is constrained and apply constraint 
            leftTransition =  self.__env.getChunksBiomes()[str(n-1)] + '-' +self.__biome
            if leftTransition in self.__env.getBiomesTransitionsConstraints().keys():
                self.__Y1 = self.__env.getBiomesTransitionsConstraints()[leftTransition]
            else:
                self.__Y1 = self.__params['offset'] + self.__params['mountainHeightCoefficient']*chaotic(self.__y0,n)
        # First built chunk ?
        else:
            self.__Y1 = self.__params['offset'] + self.__params['mountainHeightCoefficient']*chaotic(self.__y0,n)
            self.__Y2 = self.__params['offset'] + self.__params['mountainHeightCoefficient']*chaotic(self.__y0,n+1)
        
    ## Biomes detailed generation                                       ## --- Update when adding a biome
    def buildTerrain_plain(self):
        
        for X in range(self.__X1,self.__X2):
            for Y in range(self.__env.getMaxHeight()):
                earthFloor = floor(interpolation(self.__X1,self.__Y1,self.__X2,self.__Y2,X))
                if Y == earthFloor and Y< self.__params['snowAltitude']:
                    block = bl.grass(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y == earthFloor and Y>= self.__params['snowAltitude']:
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
            X = 16*self.__chunkNumber+randint(0,15)
            Y = floor(interpolation(self.__X1,self.__Y1,self.__X2,self.__Y2,X))+1
            self.createFlower(X,Y)
    def buildTerrain_forest(self):
        
        for X in range(self.__X1,self.__X2):
            for Y in range(self.__env.getMaxHeight()):
                earthFloor = floor(interpolation(self.__X1,self.__Y1,self.__X2,self.__Y2,X))
                if Y == earthFloor and Y>= self.__params['snowAltitude']:
                    block = bl.snowyGrass(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y == earthFloor and Y< self.__params['snowAltitude']:
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
            X = 16*self.__chunkNumber+randint(0,15)
            Y = floor(interpolation(self.__X1,self.__Y1,self.__X2,self.__Y2,X))
            self.createTree(X,Y)
    def buildTerrain_mountain(self):
        
        for X in range(self.__X1,self.__X2):
            for Y in range(self.__env.getMaxHeight()):
                earthFloor = floor(interpolation(self.__X1,self.__Y1,self.__X2,self.__Y2,X))
                if Y == earthFloor and Y>= self.__params['snowAltitude']:
                    block = bl.snowyGrass(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y == earthFloor and Y< self.__params['snowAltitude']:
                    block = bl.dirt(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y< earthFloor:
                    block = bl.rock(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                else:
                    pass
    def buildTerrain_ocean(self):
        for X in range(self.__X1,self.__X2):
            for Y in range(self.__env.getMaxHeight()):
                earthFloor = floor(interpolation(self.__X1,self.__Y1,self.__X2,self.__Y2,X))
                if Y > earthFloor and Y <= self.__env.getOceanSurfaceAltitude():
                    block = bl.water(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y <= earthFloor and Y > earthFloor-2 and Y>= self.__env.getSnowAltitude():
                    block = bl.snowyGrass(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y <= earthFloor and Y > earthFloor-2 and Y< self.__env.getSnowAltitude() and Y> self.__env.getOceanSurfaceAltitude():
                    block = bl.sand(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y <= earthFloor and Y > earthFloor-2 and Y< self.__env.getSnowAltitude() :
                    block = bl.sand(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                elif Y<= earthFloor-2:
                    block = bl.rock(self.__env,X,Y)
                    self.__blocks[str(X)+'-'+str(Y)] = block
                else:
                    pass
    
    # Section where we create environment objects
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
                        if floor(i/16) == self.__chunkNumber:
                            block = bl.leaf(self.__env,i,j)
                            self.__blocks[str(i)+'-'+str(j)] = block
    def createFlower(self,flowerPosx,flowerPosy):
        flowerPosKey = str(flowerPosx)+'-'+str(flowerPosy)
        underFlowerPosKey = str(flowerPosx)+'-'+str(flowerPosy-1)
        if flowerPosKey not in self.getBlocks().keys() and self.getBlocks()[underFlowerPosKey].getName() == 'grass':
            block = bl.redFlower(self.__env,flowerPosx,flowerPosy)
            self.__blocks[flowerPosKey] = block

## ---------------------- ##
##| ADDITIONAL FUNCTIONS |##
## ---------------------- ##

## Here we define useful functions for terrain height generation
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

# Here we interpolate between control points
def interpolation(x1,y1,x2,y2,x):
        y1p = 0
        y2p = 0
        a =  -(2*y1 - 2*y2 - x1*y1p - x1*y2p + x2*y1p + x2*y2p)/((x1 - x2)*(x1**2 - 2*x1*x2 + x2**2))
        b = -(x1**2*(y1p) + 2*x1**2*(y2p) - 2*x2**2*(y1p) - x2**2*(y2p) - 3*x1*(y1) + 3*x1*(y2) - 3*x2*(y1) + 3*x2*(y2) + x1*x2*(y1p) - x1*x2*(y2p))/((x1 - x2)*(x1**2 - 2*x1*x2 + x2**2))
        c = (x1**3*(y2p) - x2**3*(y1p) - 6*x1*x2*(y1) + 6*x1*x2*(y2) - x1*x2**2*(y1p) + 2*x1**2*x2*(y1p) - 2*x1*x2**2*(y2p) + x1**2*x2*(y2p))/((x1 - x2)*(x1**2 - 2*x1*x2 + x2**2))
        d = (x1**3*(y2) - x2**3*(y1) + 3*x1*x2**2*(y1) - 3*x1**2*x2*(y2) + x1*x2**3*(y1p) - x1**3*x2*(y2p) - x1**2*x2**2*(y1p) + x1**2*x2**2*(y2p))/((x1 - x2)*(x1**2 - 2*x1*x2 + x2**2))
        y = a*x**3 + b*x**2 + c*x + d
        return y