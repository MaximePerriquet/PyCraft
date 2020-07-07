import tkinter as Tk
import rendering as re
import environment as en
import player as pl
import bindings as bi
import time
import ctypes
from PIL import Image,ImageTk
from math import floor
user32 = ctypes.windll.user32


## ---------------------- ##
##|       CLASSES        |##
## ---------------------- ##
class Game:
    def __init__(self):
        print('~~~~~~~~~  INITIALIZING PYCRAFT  ~~~~~~~~~')
        self.__win = Tk.Tk()
        self.__win.protocol("WM_DELETE_WINDOW", self.close_window)
        self.__height = user32.GetSystemMetrics(1)
        self.__width = user32.GetSystemMetrics(0)
        self.__can = Tk.Canvas(self.__win,height=self.__height,width = self.__width,background = '#9FDBFE') 
        print('Creating textures ...')
        self.__textures = re.Textures()
        print('Creating environment ...')
        self.__env = en.Environment(self.__textures)
        print('Creating camera ...')
        self.__cam = re.Camera(self.__can,self.__env)
        print('Creating player ...')
        self.__player = pl.Player('Sobs',self.__cam,self.__env)
        print('Setting controls ...')
        self.__bin = bi.Bindings(self.__win,self.__can,self.__cam,self.__env,self.__player)
        self.__startTime = 90
        
    def start(self):
        print('~~~~~~~~~  STARTING PYCRAFT  ~~~~~~~~~')
        self.__can.pack()
        print('Displaying environment ...')
        self.__cam.displayEnv(self.__env)
        print('Displaying player ...')
        self.__cam.displayPlayer(self.__player)
        self.__bin.start()
        self.__cam.updateChunkRendeering(self.__player)
        self.__player.updateChunkNeighbour()
        self.__skyUpdate = 2
        self.__skies = dict()
        self.__brightnesses = dict()
        print('Successfully started !')
        
    def run(self): 
        self.__running = True
        print('~~~~~~~~~  RUNNING PYCRAFT  ~~~~~~~~~')
        while self.__running:
            
            t1 = time.perf_counter() + self.__startTime
            time.sleep(1/70)
            ## The player does its controls
            self.__player.bind()  
            ## The bindings do their stuffs                      
            self.__bin.animate()                        
            t2=time.perf_counter() + self.__startTime
             ## Running time
            dt = t2-t1                                 

            ## Moving player
            self.__player.setVx(self.__player.getVx() + self.__player.getAx()*dt)
            self.__player.setVy(self.__player.getVy() + self.__player.getAy()*dt)
            self.__player.setDx(self.__player.getVx()*dt)
            self.__player.setDy(self.__player.getVy()*dt)
            self.__player.move(self.__player.getDx(),self.__player.getDy())
            ## The camera does its controls
            self.__cam.bind(self.__player,self.__env,t1,t2)   
            ## Updating the window
            
            self.__win.update()
            
    def close_window(self):
        self.__running = False
        print('~~~~~~~~~  CLOSING PYCRAFT  ~~~~~~~~~')

    

    