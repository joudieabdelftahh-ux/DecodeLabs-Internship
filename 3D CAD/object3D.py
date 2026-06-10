from matrix_function import *
import pygame as pg
import sys



class object3D:
    def __init__(self,render,):
        self.render= render
        self.vertexes=np.array([(0,0,0,1),(0,1,0,1),(1,1,0,1),(1,0,0,1),(0,0,1,1),(0,1,1,1),(1,1,1,1),(1,0,1,1)])
        self.faces=np.array([(0,1,2,3),(4,5,6,7),(0,4,5,1),(2,3,7,6),(1,2,6,5),(0,3,7,4)])

        self.font=pg.font.SysFont('Arial',30,bold=True)
        self.color_faces=[(pg.Color('blue'),face)for face in self.faces]
        self.movment_flag,self.draw_vertexes= True, False
        self.label=''



    def draw(self):
        self.screen_projection()
        self.movment()#take alook here

    def movment(self):
        if self.movment_flag:
            self.rotate_x(-(pg.time.get_ticks()%0.005))
            self.rotate_y(-(pg.time.get_ticks()%0.005))
            self.rotate_z(-(pg.time.get_ticks()%0.005))

    def screen_projection(self):
        vertexes=self.vertexes @ self.render.camera.camera_matrix()
        vertexes=vertexes @ self.render.projection.projection_matrix
        vertexes/=vertexes[:,-1].reshape(-1,1)
        vertexes[(vertexes>2) | (vertexes<-2)] = 0
        vertexes=vertexes @ self.render.projection.to_screen_matrix
        vertexes=vertexes[:,:2]

        for index, (color, face) in enumerate(self.color_faces):
            polygon = vertexes[face]
            if  (polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
               pg.draw.polygon(self.render.screen, color, polygon, 2)
            
            if self.label:
               text = self.font.render(self.label[index], True, pg.Color('red'))
               self.render.screen.blit(text, polygon[-2]) 
        for vertix in vertexes:
                if not np.any((vertix == self.render.H_WIDTH) | (vertix == self.render.H_HEIGHT)):
                   pg.draw.circle(self.render.screen,pg.Color('white'),vertix.astype(int),2)


    def translate(self,pos):
        self.vertexes=self.vertexes @ translate(pos)
    def scale (self,scale_to):
        self.vertexes=self.vertexes @ scale(scale_to)
    def rotate_x(self, angle):
        self.vertexes=self.vertexes @ rotate_x (angle)
    def rotate_y(self, angle):
        self.vertexes=self.vertexes @ rotate_y (angle)
    def rotate_z(self, angle):
        self.vertexes=self.vertexes @ rotate_z (angle)
        #object