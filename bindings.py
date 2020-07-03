from math import floor
class Bindings:
    def __init__(self,win,can,cam,env,player):
        self.__pressed = dict()
        self.__win = win
        self.__can = can
        self.__cam = cam
        self.__env = env
        self.__player = player
    def start(self):
        self.__win.bind("<Button-1>",self.click)
        for char in [" ","q","d"]:
            self.__win.bind("<KeyPress-%s>" % char, self.press)
            self.__win.bind("<KeyRelease-%s>" % char, self.release)
            self.__pressed[char] = False
    def press(self,event):
        self.__pressed[event.char] = True
    def release(self,event):
        self.__pressed[event.char] = False
    def animate(self):
        if self.__pressed[' ']: self.__player.setJump()
        if self.__pressed['q']: self.__player.setGoLeft()
        if self.__pressed['d']: self.__player.setGoRight()
    def click(self,event):
        xClick = floor((event.x - int(self.__can['width'])//2)/self.__cam.getScale() + self.__cam.getPosx())
        yClick = floor(-(event.y - int(self.__can['height'])//2)/self.__cam.getScale() + self.__cam.getPosy())
        clickedBlockKey = str(xClick)+'-'+str(yClick)
        chunk = self.__env.getChunks()[str(floor(xClick/16))]
        try:
            clickedBlock = self.__player.getNeighbourBlocksDict()[clickedBlockKey]
            self.__can.delete(clickedBlock.getDisplayAdress())
            del(chunk.getBlocks()[clickedBlockKey])
            self.__player.updateChunkNeighbour()
        except:
            pass