import numpy as np

class Point:
    def __init__(self, x=0., y=0., z=0., vector=[]):
        if vector == []:
            self.x = x
            self.y = y
            self.z = z
        else:
            self.x = vector[0]
            self.y = vector[1]
            self.z = vector[2]

    def vector(self):
        return np.array([self.x, self.y, self.z])
    
    def __getitem__(self, i):
        return self.vector()[i]

def distance(a:Point, b:Point):      
    dx = a.x - b.x
    dy = a.y - b.y
    dz = a.z - b.z
    return np.sqrt(dx*dx + dy*dy + dz*dz)

def rotate(points, center, angle):

    for point in points:
        point.x -= center.x
        point.y -= center.y
        tempx = point.x * np.cos(angle) - point.y * np.sin(angle)
        tempy = point.x * np.sin(angle) + point.y * np.cos(angle)
        point.x = tempx + center.x
        point.y = tempy + center.y
