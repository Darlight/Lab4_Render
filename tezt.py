"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

tezt.py
Proposito: Un framebuffer simple para pintar un punto con modificaciones simples como:
- Cambiar de color de los puntos
- Crear un punto
- Modificaciones del tamaño de la venta principal
"""
#struc pack
# wikipedia bmp file format
import struct
from collections import namedtuple
from obj import Obj, Texture
from math_functions import *

V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])
#opcion = 0
def char(c):
    # un char que vale un caracter de tipo string
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    #convierte el numero de posicion de pixel a 2 bytes
    return struct.pack('=h', c)

def dword(c):
    #4 bytes de la estructura de un framebuffer
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])

#Colores como constantes
GREEN = color(0, 255, 0)
RED = color(255, 0, 0)
BLUE = color(0, 0, 255)
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255) 

class Render(object):
    def __init__(self):
        #Tamanio del bitmap
        self.framebuffer = []
        self.color = WHITE
        self.bg_color = BLACK
        self.xPort = 0
        self.yPort = 0
        self.glCreateWindow()
    
    #Basicamente __init__ ^ hace esta funcion, asi que cree esta funcion por estética
    def glInit(self):
        return "Bitmap creado... \n"

    def point(self, x, y):
        self.framebuffer[y][x] = self.color

    def glCreateWindow(self, width=800, height=600):
        self.windowWidth = width
        self.windowHeight = height
        self.glClear()
        self.glViewPort(self.xPort, self.yPort, width, height)

    def glViewPort(self, x, y, width, height):
        self.xPort = x
        self.yPort = y
        self.viewPortWidth = width
        self.viewPortHeight = height

    def glClear(self):
        self.framebuffer = [
            [self.bg_color for x in range(self.windowWidth)] for y in range(self.windowHeight)
        ]

    def glClearColor(self, r=0, g=0, b=0):
        self.bg_color = color(r,g,b)

    def glVertex(self, x, y):
        #Formula sacada de:
        # https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml
        newX = round((x + 1)*(self.viewPortWidth/2) + self.xPort)
        newY = round((y + 1)*(self.viewPortHeight/2) + self.yPort)
        #funcion point para optimar
        self.point(newX,newY)

    def glColor(self, r=0, g=0, b=0):
        #self.framebuffer[self.yPort][self.xPort] = color(r,g,b)
        #Cambiar los valores de 0-255 a 0-1
        self.color = color(r,g,b)

    def glLine(self, placement, ycardinal = False):
        #variables condicionales y misma formula del vertex
        position = ((placement + 1) * (self.viewPortHeight/2) + self.yPort) if ycardinal else ((placement+1) * (self.viewPortWidth/2) + self.xPort)
        return round(position)

    
    def Line(self,x1,y1,x2,y2):
        #Da error con multiples puntos y salen del index si los metemeos a glLine
       # x1 = self.glLine(x1)
       # x2 = self.glLine(x2)
       # y1 = self.glLine(y1,True)
       # y2 = self.glLine(y2,True)
    
        #El steep es la direccion de la recta
        steep = abs(y2 - y1) > abs(x2 - x1)

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        #Es una resta con el punto original para determinar su coordenada
        offset = 0
        #El limite de la pendiente
        threshold = dx

        y = y1
        for x in range(x1, x2 + 1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)
            
            offset += dy*2

            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += dx*2

    def triangle(self, A, B, C):
        if A.y > B.y:
           A, B = B, A
        if A.y > C.y:
         A, C = C, A
        if B.y > C.y:
            B, C = C, B

        dx_ac = C.x - A.x
        dy_ac = C.y - A.y
        if dy_ac == 0:
            return
        mi_ac = dx_ac/dy_ac

        dx_ab = B.x - A.x
        dy_ab = B.y - A.y
        if dy_ab != 0:
            mi_ab = dx_ab/dy_ab

            for y in range(A.y, B.y + 1):
                xi = round(A.x - mi_ac * (A.y - y))
                xf = round(A.x - mi_ab * (A.y - y))

                if xi > xf:
                    xi, xf = xf, xi
                for x in range(xi, xf + 1):
                    self.point(x, y)

        dx_bc = C.x - B.x
        dy_bc = C.y - B.y
        if dy_bc:
            mi_bc = dx_bc/dy_bc

            for y in range(B.y, C.y + 1):
                xi = round(A.x - mi_ac * (A.y - y))
                xf = round(B.x - mi_bc * (B.y - y))

                if xi > xf:
                    xi, xf = xf, xi
                for x in range(xi, xf + 1):
                    self.point(x, y)

    def drawPolygon(self, points):
        iterations = len(points)
        for i in range(iterations):
            v0 = points[i]
            v1 = points[(i+1)%iterations]
            self.Line(v0[0], v0[1], v1[0], v1[1]) 

    def inundation_left(self, x, y, color1, color2):
        current_color = self.framebuffer[y][x]
        if (current_color != color1 and current_color != color2):
            self.point(x,y)
            #self.inundation(x+1,y,color1,color2)
            self.inundation_left(x,y+1,color1,color2)
            self.inundation_left(x-1,y,color1,color2)
            self.inundation_left(x,y-1,color1,color2)
    
    def inundation_right(self, x, y, color1, color2):
        current_color = self.framebuffer[y][x]
        if (current_color != color1 and current_color != color2):
            self.point(x,y)
            self.inundation_right(x+1,y,color1,color2)
            self.inundation_right(x,y+1,color1,color2)
            #self.inundation(x-1,y,color1,color2)
            self.inundation_right(x,y-1,color1,color2)

    def load(self, filename, translate=[0,0], scale=[1,1]):
        model = Obj(filename)

        for face in model.faces:
            vcount = len(face)
            for j in range(vcount):
             vi1 = face[j][0] - 1
             vi2 = face[(j+1) % vcount][0] - 1 

            v1 = model.vertices[vi1]
            v2 = model.vertices[vi2]
            #x1 = round((v1[0] *scale[0]) + translate[0])
            x1 = round((v1[0] + translate[0]) * scale[0])
            y1 = round((v1[1] + translate[1]) * scale[1])
            x2 = round((v2[0] + translate[0]) * scale[0])
            y2 = round((v2[1] + translate[1]) * scale[1])

            self.Line(x1,y1, x2, y2)
            
    def glFinish(self, filename):
        f = open(filename, 'bw')
        # file header
        f.write(char('B'))
        f.write(char('M'))

        f.write(dword(14 + 40 + self.windowWidth * self.windowHeight * 3))

        f.write(dword(0))

        f.write(dword(14 + 40))

        # image header 
        f.write(dword(40))
        f.write(dword(self.windowWidth))
        f.write(dword(self.windowHeight))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.windowWidth * self.windowHeight * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # pixel data

        #ESTA COSA ERA MI ERROR, HABIA COLOCADO MAL LAS COORDENADAS 
        for x in range(self.windowHeight):
            for y in range(self.windowWidth):
                f.write(self.framebuffer[x][y])
        f.close()
"""
    def inundation(self, x, y, color1, color2):
        current_color = self.framebuffer[y][x]
        if (current_color != color1 and current_color != color2):
            self.point(x,y)
            #self.inundation(x+1,y,color1,color2)
            self.inundation(x,y+1,color1,color2)
            self.inundation(x-1,y,color1,color2)
            self.inundation(x,y-1,color1,color2)
"""




#bitmap es el producto final, debo hacer un  menu completo 
# 128, 64


"""
    def Line(self,x0,y0,x1,y1):
        #self.x0 = x0
        #self.x1 = x1
        #self.y0 = y0
        #self.y1 = y1
        #dy = abs(y1 - y0)
        #dx = abs(x1 - x0)
        #dy > dx
        
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        offset  = 0
        
        threshold = dx 
       
        y = y0
        # y = y1 - m * (x1 - x)
        for x in range(x0, x1):

            #self.point(self.y,self.x)
            
            if steep:
                 #render.point(round(x), round(y))
                self.point(y, x)

            else:
                #render.point(x), round(y))
                self.point(x,y)
                
            offset += dy * 2
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += dx * 2
"""