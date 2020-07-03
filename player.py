from math import floor,exp
class Player:
    def __init__(self,name,cam,env):
        self.__name = name
        self.__cam = cam
        self.__env = env
        self.__posx = 0.5
        self.__posy = 30.5
        self.__dx = 0
        self.__dy = 0
        self.__chunkNumber = floor(floor(self.__posx)/16)
        self.__vx = 0
        self.__vy = 0
        self.__ax = 0
        self.__ay = 0
        self.__mass = 50
        self.__walkingVelocity = 5
        self.__inJumpWalkingVelocity = 0.1
        self.__jumpVelocity = 5
        self.__displayAdress = ''
        self.__canJump = False
        self.__canGoLeft = True
        self.__canGoRight = True
        self.__inWater = False
        self.__inWaterDampingFactor = 0.9
        self.__swimmingVelocity = 1
        self.__neighbourBlocksDict = dict()
    def setJump(self):
        if not self.__inWater:
            self.__vy += self.__jumpVelocity*self.__canJump
            self.__canJump = False
        else:
            self.__vy = self.__jumpVelocity*self.__inWaterDampingFactor
            self.__canJump = False
    def setGoRight(self):
        if not self.__inWater:
            self.__vx = self.__walkingVelocity*self.__canGoRight
        else:
            self.__vx = self.__swimmingVelocity*self.__canGoRight
        self.__canGoLeft = True
    def setGoLeft(self):
        if not self.__inWater:
            self.__vx = -self.__walkingVelocity*self.__canGoLeft
        else:
            self.__vx = -self.__swimmingVelocity*self.__canGoLeft*self.__inWaterDampingFactor
        self.__canGoRight = True
    def stopVelocity(self,coeffx,coeffy):
        self.__vx = self.__vx*coeffx
        self.__vy = self.__vy*coeffy
    def getVx(self): return self.__vx
    def getVy(self): return self.__vy
    def getAx(self): return self.__ax
    def getAy(self): return self.__ay
    def getMass(self): return self.__mass
    def getPosx(self): return self.__posx
    def getPosy(self): return self.__posy
    def setDx(self,dx): self.__dx = dx
    def setDy(self,dy): self.__dy = dy
    def setVx(self,vx): self.__vx = vx
    def setVy(self,vy): self.__vy = vy
    def getDx(self): return self.__dx
    def getDy(self): return self.__dy
    def getChunkNumber(self): return self.__chunkNumber
    def updateChunkNeighbour(self):
        playerChunkNumber = self.__chunkNumber
        playerChunkKey = str(playerChunkNumber)
        playerChunk = self.__env.getChunks()[playerChunkKey]

        rightChunkNumber = playerChunkNumber + 1
        rightChunk = self.__env.getChunks()[str(rightChunkNumber)]
        leftChunkNumber = playerChunkNumber - 1
        leftChunk = self.__env.getChunks()[str(leftChunkNumber)]

        rightChunkBlocksDict = rightChunk.getBlocks()
        leftChunkBlocksDict = leftChunk.getBlocks()
        playerChunkBlocksDict = playerChunk.getBlocks()

        self.__neighbourBlocksDict = dict()
        self.__neighbourBlocksDict.update(leftChunkBlocksDict)
        self.__neighbourBlocksDict.update(rightChunkBlocksDict)
        self.__neighbourBlocksDict.update(playerChunkBlocksDict)
    def getNeighbourBlocksDict(self): return self.__neighbourBlocksDict
    def getDisplayAdress(self): return self.__displayAdress
    def setDisplayAdress(self,displayAdress): self.__displayAdress = displayAdress
    def move(self,dx,dy):
        self.__posx += dx
        self.__posy += dy
        newChunkNumber = floor(self.__posx/16)
        if newChunkNumber != self.__chunkNumber:
            self.__chunkNumber = newChunkNumber
            self.__cam.updateChunkRendeering(self)
            self.updateChunkNeighbour()
        self.__cam.movePlayer(self,dx,dy)
    def bind(self):
        
        playerFootBlock = [floor(self.__posx),floor(self.__posy-0.5)]
        playerFootBlockKey = str((str(playerFootBlock[0])+'-'+str(playerFootBlock[1])))

        rightBlock1 = [floor(self.__posx)+1,floor(self.__posy-0.85)]
        rightBlock2 = [floor(self.__posx)+1,floor(self.__posy)]
        rightBlock3 = [floor(self.__posx)+1,floor(self.__posy+0.85)]
        rightBlock1Key = str(str(rightBlock1[0])+'-'+str(rightBlock1[1]))
        rightBlock2Key = str(str(rightBlock2[0])+'-'+str(rightBlock2[1]))
        rightBlock3Key = str(str(rightBlock3[0])+'-'+str(rightBlock3[1]))

        leftBlock1 = [floor(self.__posx)-1,floor(self.__posy-0.85)]
        leftBlock2 = [floor(self.__posx)-1,floor(self.__posy)]
        leftBlock3 = [floor(self.__posx)-1,floor(self.__posy+0.85)]
        leftBloc1kKey = str(str(leftBlock1[0])+'-'+str(leftBlock1[1]))
        leftBloc2kKey = str(str(leftBlock2[0])+'-'+str(leftBlock2[1]))
        leftBloc3kKey = str(str(leftBlock3[0])+'-'+str(leftBlock3[1]))

        bottomBlock = [floor(self.__posx),floor(self.__posy-0.9)]
        bottomBlockKey = str(str(bottomBlock[0])+'-'+str(bottomBlock[1]))

        topBlock = [floor(self.__posx),floor(self.__posy+0.9)]
        topBlockKey = str(str(topBlock[0])+'-'+str(topBlock[1]))
        
        ## deal with vertical collision
        if bottomBlockKey in self.__neighbourBlocksDict.keys():
            bottomBlock = self.__neighbourBlocksDict[bottomBlockKey]
            minPosy = bottomBlock.gety()+1.9
            if self.__posy < minPosy and bottomBlock.getType() == 'opaque':
                self.move(0,minPosy - self.__posy)
                self.__vy = 0
                self.__ay = 0
                self.__vx = self.__vx*0.5
                self.__canJump = True
        else:
            self.__ax = 0
            self.__ay = -9.81
            self.__canJump = False

        ## deal with head collision
        if topBlockKey in self.__neighbourBlocksDict.keys():
            topBlock = self.__neighbourBlocksDict[topBlockKey]
            maxPosy = topBlock.gety()-0.9
            if self.__posy > maxPosy and topBlock.getType() == 'opaque':
                self.move(0,maxPosy - self.__posy)
                self.__vy = 0
                self.__ay = 0

        ## deal with horizontal collisions
        leftBlocked = False
        if leftBloc1kKey in self.__neighbourBlocksDict.keys():
            if self.__neighbourBlocksDict[leftBloc1kKey].getType() == 'opaque':
                leftBlocked = True
        if leftBloc2kKey in self.__neighbourBlocksDict.keys():
            if self.__neighbourBlocksDict[leftBloc2kKey].getType() == 'opaque':
                leftBlocked = True
        if leftBloc3kKey in self.__neighbourBlocksDict.keys():
            if self.__neighbourBlocksDict[leftBloc3kKey].getType() == 'opaque':
                leftBlocked = True
        if leftBlocked:
            minPosx = floor(self.__posx)+0.25
            if self.__posx < minPosx:
                self.move(minPosx - self.__posx,0)
                self.__vx = 0
                self.__canGoLeft = False
        else:
            self.__canGoLeft = True


        rightBlocked = False
        if rightBlock1Key in self.__neighbourBlocksDict.keys():
            if self.__neighbourBlocksDict[rightBlock1Key].getType() == 'opaque':
                rightBlocked = True
        if rightBlock2Key in self.__neighbourBlocksDict.keys():
            if self.__neighbourBlocksDict[rightBlock2Key].getType() == 'opaque':
                rightBlocked = True
        if rightBlock3Key in self.__neighbourBlocksDict.keys():
            if self.__neighbourBlocksDict[rightBlock3Key].getType() == 'opaque':
                rightBlocked = True
        if rightBlocked:
            maxPosx = floor(self.__posx)+0.75
            if self.__posx > maxPosx:
                self.move(maxPosx - self.__posx,0)
                self.__vx = 0
                self.__canGoRight = False
        else:
            self.__canGoRight = True

        
        ## Deal with water 
        self.__inWater = False
        if playerFootBlockKey in self.__neighbourBlocksDict.keys():
            if self.__neighbourBlocksDict[playerFootBlockKey].getType() == 'fluid':
                self.__inWater = True
        if bottomBlockKey in self.__neighbourBlocksDict.keys():
            if self.__neighbourBlocksDict[bottomBlockKey].getType() == 'fluid':
                self.__inWater = True
        if self.__inWater:
            self.__vx = self.__inWaterDampingFactor*self.__vx
            self.__vy = self.__inWaterDampingFactor*self.__vy
            self.__ay = -9.81*self.__inWaterDampingFactor
            self.__inWater = True
        
        
        
            




        

        

        
        
