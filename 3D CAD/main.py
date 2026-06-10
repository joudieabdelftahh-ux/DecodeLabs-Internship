import pygame as pg
from object3D import *
from camera import *
from projection import *



class softwarerender:

   def __init__(self):
      pg.init()
      self.RES=self.WIDTH, self.HEIGHT=1600,900
      self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
      self.FPS=60
      self.screen= pg.display.set_mode(self.RES)
      self.clock=pg.time.Clock()
      self.createobject()

   def createobject(self):
        self.camera = camera(self, [-10,10,-38])
        self.projection=projection(self)
        self.object=object3D(self)
        self.object.scale(6)
        self.object.translate([0.3,1,0.3])
        self.object.rotate_y(math.pi/6)

   def draw(self):
         self.screen.fill(pg.Color('black'))
         self.object.draw()


   def run(self):
       while True:
         self.draw()
         self.camera.control()
         [exit() for i in pg.event.get() if i.type==pg.QUIT]
         pg.display.set_caption(str(self.clock.get_fps()))
         pg.display.flip()
         self.clock.tick(self.FPS)



if __name__ =='__main__':
   app = softwarerender()
   app.run()
#main