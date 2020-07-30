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
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

NEGRO = color(0,0,0)
BLANCO = color(1,1,1)


class Render(object):

    def __init__(self, width, height):
        self.curr_color = BLANCO
        self.clear_color = NEGRO
        self.glCreateWindow(width, height)

    def glCreateWindow(self,width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0, 0, width, height)

    def glViewport(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

    def glClear(self):
        self.pixels = [ [ self.clear_color for x in range(self.width)] for y in range(self.height) ]

    def glVertex(self, x, y):
        pixelX = ( x + 1) * (self.vpWidth  / 2 ) + self.vpX
        pixelY = ( y + 1) * (self.vpHeight / 2 ) + self.vpY

        try:
            self.pixels[round(pixelY)][round(pixelX)] = self.curr_color
        except:
            pass

    def glVertex_coord(self, x, y):
        try:
            self.pixels[y][x] = self.curr_color
        except:
            pass

    def glColor(self, r, g, b):
        self.curr_color = color(r,g,b)

    def glClearColor(self, r, g, b):
        self.clear_color = color(r,g,b)

    def glFinish(self, filename):
        f = open(filename, 'wb')
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

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y])

        f.close()

    def glLine(self, x0, y0, x1, y1): # NDC
        x0 = round(( x0 + 1) * (self.vpWidth  / 2 ) + self.vpX)
        x1 = round(( x1 + 1) * (self.vpWidth  / 2 ) + self.vpX)
        y0 = round(( y0 + 1) * (self.vpHeight / 2 ) + self.vpY)
        y1 = round(( y1 + 1) * (self.vpHeight / 2 ) + self.vpY)

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

    def glLine_coord(self, x0, y0, x1, y1): # Window coordinates

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

    def loadModel(self, filename, translate, scale):
        model = Obj(filename)

        for face in model.faces:

            vertCount = len(face)

            for vert in range(vertCount):
                
                v0 = model.vertices[ face[vert][0] - 1 ]
                v1 = model.vertices[ face[(vert + 1) % vertCount][0] - 1]

                x0 = round(v0[0] * scale[0]  + translate[0])
                y0 = round(v0[1] * scale[1]  + translate[1])
                x1 = round(v1[0] * scale[0]  + translate[0])
                y1 = round(v1[1] * scale[1]  + translate[1])

                self.glLine_coord(x0, y0, x1, y1)

r = Render(700,900)
r.loadModel('./models/chicken.obj', (378,189), (378,378) )
r.glFinish('output.bmp')
