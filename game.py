import tkinter as Tk
import rendering as re
import environment as en
import player as pl
import bindings as bi
import time
import ctypes
user32 = ctypes.windll.user32



class Game:
    def __init__(self):
        self.__win = Tk.Tk()
        height = user32.GetSystemMetrics(1)
        width = user32.GetSystemMetrics(0)
        self.__can = Tk.Canvas(self.__win,height=height,width = width,background = '#9FDBFE')
        self.__textures = re.Textures()
        self.__env = en.Environment(self.__textures)
        
        self.__cam = re.Camera(self.__can,self.__env)
        self.__player = pl.Player('Sobs',self.__cam,self.__env)
        self.__bin = bi.Bindings(self.__win,self.__can,self.__cam,self.__env,self.__player)
        
    def start(self):
        
        self.__can.pack()
        self.__cam.displayEnv(self.__env)
        self.__cam.displayPlayer(self.__player)
        self.__bin.start()
        self.__cam.updateChunkRendeering(self.__player)
        self.__player.updateChunkNeighbour()
        

    def run(self):
        while True:
            t1 = time.perf_counter()
            time.sleep(1/70)
            ## The player does its controls
            self.__player.bind()  
            ## The bindings do their stuffs                      
            self.__bin.animate()                        
            t2=time.perf_counter()
             ## Running time
            dt = t2-t1                                 

            ## Moving player
            self.__player.setVx(self.__player.getVx() + self.__player.getAx()*dt)
            self.__player.setVy(self.__player.getVy() + self.__player.getAy()*dt)
            self.__player.setDx(self.__player.getVx()*dt)
            self.__player.setDy(self.__player.getVy()*dt)
            self.__player.move(self.__player.getDx(),self.__player.getDy())
            ## The camera does its controls
            self.__cam.bind(self.__player,self.__env)   
            ## Updating the window
            self.__win.update()
            
        

    

    