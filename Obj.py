# ===============================================================
# Maria Isabel Ortiz Naranjo
# Carne: 18176
# ===============================================================

class Obj(object):
    def __init__(self,filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.faces = []
        self.read()

    def read(self):
        for line in self.lines:
                if line:
                    prefix, value = line.split(' ', 1)
                    if prefix == 'v': # vertices
                        self.vertices.append(list(map(float,value.split(' '))))
                    elif prefix == 'f': # Faces
                        self.faces.append([list(map(int,vert.split('/'))) for vert in value.split(' ')])

