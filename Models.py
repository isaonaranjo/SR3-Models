# Maria Isabel Ortiz Naranjo
# Graficas por computadora
# SR3 - MODELOS
# 18176
# Basado en codigo proporcionado en clase por Dennis 

import struct
from Obj import Obj

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])

NEGRO = color(0,0,0)
BLANCO = color(255,255,255)


class Render(object):

    def __init__(self):
        self.framebuffer = []
        self.color = BLANCO
        self.bg_color = NEGRO
        self.xPort = 0
        self.yPort = 0
        self.glCreateWindow(1,1)

    # función glInit() 
    def glInit(self):
        pass

    # función glCreateWindow(width, height) 
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0, 0, width, height)

    # función glViewPort(x, y, width, height)
    def glViewport(self, x, y, width, height):
        self.xViewPort = x
        self.yViewPort = y
        self.viewPortWidth = width
        self.viewPortHeight = height

    # función glClear() 
    def glClear(self):
        self.framebuffer = [[NEGRO for x in range(self.width)] for y in range(self.height)]


    # funcion glLine
    def glLine(self, x0, y0, x1, y1):
        x0 = round(( x0 + 1) * (self.viewPortWidth / 2 ) + self.xViewPort)
        x1 = round(( x1 + 1) * (self.viewPortWidth / 2 ) + self.xViewPort)
        y0 = round(( y0 + 1) * (self.viewPortHeight / 2 ) + self.yViewPort)
        y1 = round(( y1 + 1) * (self.viewPortHeight / 2 ) + self.yViewPort)

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        offset = 0 
        limit = 0.5
        
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glVertex_coord(y, x)
            else:
                self.glVertex_coord(x, y)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    # Funcion de las coordenadas
    def glLine_coord(self, x0, y0, x1, y1): 
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        
        try:
            m = dy/dx
        except ZeroDivisionError:
            pass
        else:
            y = y0

            for x in range(x0, x1 + 1):
                if steep:
                    self.glVertex_coord(y, x)
                else:
                    self.glVertex_coord(x, y)

                offset += m
                if offset >= limit:
                    y += 1 if y0 < y1 else -1
                    limit += 1

    def glClearColor(self, r, g, b):
        self.clear_color = color(r,g,b)

    def glColor(self, r=0.5, g=0.5, b=0.5):
        self.curr_color = color(r,g,b)

    def glVertex(self, x, y):
        pixelX = ( x + 1) * (self.viewPortWidth / 2 ) + self.xViewPort
        pixelY = ( y + 1) * (self.viewPortHeight / 2 ) + self.yViewPort
        try:
            self.framebuffer[round(pixelY)][round(pixelX)] = self.curr_color
        except:
            pass

    def glVertex_coord(self, x, y):
        try:
            self.framebuffer[y][x] = self.curr_color
        except:
            pass

    def glFinish(self, filename):
        f = open(filename, 'bw')
        f.write(bytes('B'.encode('ascii')))
        f.write(bytes('M'.encode('ascii')))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[y][x])

        f.close()

    def display(self, filename='out.bmp'):

        self.glFinish(filename)

        try:
            from wand.image import Image
            from wand.display import display

            with Image(filename=filename) as image:
                display(image)
        except ImportError:
            pass  # do nothing if no wand is installed


    def drawPoligono(self, points):
        count = len(points)

        for i in range(count):
            v0 = points[i]
            v1 = points[(i+1)%count]
            self.glLine_coord(v0[0], v0[1], v1[0], v1[1])

    # Funcion tomada del blog citado arriba, pagina 35
    def Inundacion(self, x, y, r, g, b):
        color1 = color(1, 1, 1)
        color2 = color(r, g, b)
        punto = self.framebuffer[y][x]

        if (punto != color1 and punto != color2):
            self.glColor(r, g, b)
            self.glVertex_coord(x,y)

            self.Inundacion(x+1, y, r, g, b)
            self.Inundacion(x, y+1, r, g, b)
            #self.Inundacion(x-1, y, r, g, b)
            self.Inundacion(x, y-1, r, g, b)    

    def point(self, x, y, color = None):
    # 0,0 was intentionally left in the bottom left corner to mimic opengl
        try:
            self.framebuffer[y][x] = color or self.current_color
        except:
        # To avoid index out of range exceptions
            pass
    
    def line(self, start, end, color = None):

        x1, y1 = start
        x2, y2 = end

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        offset = 0
        threshold = dx

        y = y1
        for x in range(x1, x2 + 1):
            if steep:
                self.point(y, x, color)
            else:
                self.point(x, y, color)
            
            offset += dy * 2
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += dx * 2
    
    def load(self, filename, translate, scale):
        model = Obj(filename)
    
        for face in model.faces:
            vcount = len(face)

            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j + 1) % vcount][0]

                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]
                
                x1 = round((v1[0] + translate[0]) * scale[0])
                y1 = round((v1[1] + translate[1]) * scale[1])
                x2 = round((v2[0] + translate[0]) * scale[0])
                y2 = round((v2[1] + translate[1]) * scale[1])

                self.line((x1, y1), (x2, y2))

r = Render()
r.glCreateWindow(500,1000)
print(r.glInit())
r.load('./Models/face.obj', (10,10),(10,10))
r.glFinish('output.bmp')
