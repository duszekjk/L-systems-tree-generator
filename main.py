
from vpython import *
from vectors import Point, Vector
import numpy as np
import math




##########################################################################################################################################
#####################################      ---         definitions and classes         ---      ##########################################
##########################################################################################################################################



class Position:
    x = 0.0
    y = 0.0
    z = 0.0
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        self.x = x
        self.y = y
        self.z = z
    def __vector__(self):
        return vector(self.x, self.y, self.z)
    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+", "+str(self.z)+"),\t"
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Position(x, y, z)
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Position(x, y, z)
    def __mul__(self, other):
        x = self.x * other.x
        y = self.y * other.y
        z = self.z * other.z
        return Position(x, y, z)
    def __dev__(self, other):
        x = self.x / other.x
        y = self.y / other.y
        z = self.z / other.z
        return Position(x, y, z)
        
class System():
    V = []
    w = "ar"
    P = {}
    width_rate = 0.9
    def __init__(self, V = ["ar", "al", "br", "bl"], w = "ar", P = {"ar": ["al", "br"], "al": ["bl", "ar"], "br": ["ar"], "bl": ["al"]}, width_rate = 0.9):
        self.V = V
        self.w = w
        self.P = P
        self.width_rate = width_rate
    def next(self, symbol: "a"):
        return self.P[symbol]

class Element:
    position     = Position()
    position_abs = Position()
    axis_abs     = Position()
    position_calc= Position()
    rotation     = Position()
    rotation_abs = Position()
    width        = 1.0
    symbol       = "a"
    parent       = None
    children     = []
    from_root    = 0
    def __init__(self, symbol = "a", parent = None, position = Position(), rotation = Position(), template = None, width = 1.0, from_root = 0):
        if template == None:
            self.symbol   = symbol
            self.position = position
            self.rotation = rotation
        else:
            self.symbol   = template.symbol
            self.position = template.position
            self.rotation = template.rotation
        self.parent       = parent
        self.children     = []
        self.from_root    = from_root
        self.position_abs = Position(0.0, 0.0, 0.0)
        self.rotation_abs = Position(0.0, 0.0, 0.0)
        self.position_calc= Position(0.0, 0.0, 0.0)
        self.axis_abs     = Position(0.0, 0.0, 0.0)
        self.width        = width
        if(self.parent != None):
            self.rotation_abs.x = (self.parent.rotation_abs.x + (self.rotation.x*(0.9**from_root)))%360.0
            self.rotation_abs.y = (self.parent.rotation_abs.y + self.rotation.y*(0.9**from_root))%360.0
            self.rotation_abs.z = (self.parent.rotation_abs.z + self.rotation.z*(0.9**from_root))%360.0
        
    def __str__(self):
        return self.symbol
    def set_from_root(self, d = 0):
        self.from_root = d
        for child in self.children:
            child.set_from_root(d+1)
    def alignWithVector(self):
        if(self.parent != None):
            self.rotation_abs.x = (self.parent.rotation_abs.x + self.rotation.x)%360.0
            self.rotation_abs.y = (self.parent.rotation_abs.y + self.rotation.y)%360.0
            self.rotation_abs.z = (self.parent.rotation_abs.z + self.rotation.z)%360.0
#        if self.parent.parent == None:
#            b = self.parent.position_calc
#        else:
#            b = self.parent.parent.position_calc - self.parent.position_calc
#        c = Position(self.rotation.x/360.0, self.rotation.y/360.0, self.rotation.z/360.0)
#        try:
#            sinbx = b.z / ((b.y*b.y)+(b.z*b.z))**(1.0/2.0)
#        except:
#            sinbx = 0.0
#        if self.parent.rotation_abs.x == 0:
#            angle = degrees((np.arcsin(sinbx)))%360.0
#        else:
#            angle = self.parent.rotation_abs.x%360.0
##        print("----\n\n", self.symbol)
#        angle = radians(angle)
##        print("x0 : \t", self.symbol, self.rotation, self.rotation_abs, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
#        sinbx = np.sin(angle)
#        cosbx = np.cos(angle)
#        rotationx = [
#                    [1, 0, 0],
#                    [0,cosbx,-sinbx],
#                    [0, sinbx, cosbx]
#                    ]
#        newvec = [rotationx[0][0]*c.x+rotationx[0][1]*c.y+rotationx[0][2]*c.z, rotationx[1][0]*c.x+rotationx[1][1]*c.y+rotationx[1][2]*c.z, rotationx[2][0]*c.x+rotationx[2][1]*c.y+rotationx[2][2]*c.z]
#        try:
#            sinby = b.z / ((b.x*b.x)+(b.z*b.z))**(1.0/2.0)
#        except:
#            sinby = 0.0
#        if self.rotation_abs.y == 0:
#            angle = degrees((np.arcsin(sinby)))%360.0
#        else:
#            angle = self.parent.rotation_abs.y%360.0
#        angle = radians(angle)
#        sinby = np.sin(angle)
#        cosby = np.cos(angle)
#        rotationy = [
#                    [cosby, 0, sinby],
#                    [0,1,0],
#                    [-sinby, 0, cosby]
#                    ]
#
#        try:
#            sinbz = b.x / ((b.y*b.y)+(b.x*b.x))**(1.0/2.0)
#        except:
#            sinbz = 0.0
#        if self.rotation_abs.z == 0.0:
#            angle = degrees((np.arcsin(sinbz)))%360.0
#        else:
#            angle = self.parent.rotation_abs.z%360.0
#        angle = radians(angle)
#        sinbz = np.sin(angle)
#        cosbz = np.cos(angle)
#        rotationz = [
#                    [cosbz, -sinbz, 0],
#                    [sinbz,cosbz,0],
#                    [0, 0, 1]
#                    ]
##        print(c.y, (1.0*self.from_root),  c.y**(1.0*self.from_root))
#        suma = abs(self.rotation.x)+abs(self.rotation.y)+abs(self.rotation.z)
#        newvecrota = ((np.array(rotationz).dot(np.array(rotationy))).dot(np.array(rotationx))).dot(np.array([c.x **(1.0*self.from_root), c.y**(1.0*self.from_root), c.z**(1.0*self.from_root)]))
#        sumb = abs(newvecrota[0])+abs(newvecrota[1])+abs(newvecrota[2])
#        scale_rot = 360.0#suma/sumb
#        if scale_rot:
#            newvecrot = vector((newvecrota[0]*scale_rot)%360.0, (newvecrota[1]*scale_rot)%360.0, (newvecrota[2]*scale_rot)%360.0)
#        else:
#            newvecrot = vector(0.0,0.0,0.0)
#        print(self.parent.rotation_abs, self.rotation, newvecrot, scale_rot, suma, sumb)
#        self.rotation_abs = (self.parent.rotation_abs + newvecrot)
        
        
        
        if self.parent.parent == None:
            b = self.parent.position_calc
        else:
            b = self.parent.parent.position_calc - self.parent.position_calc
        c = self.position
        try:
            sinbx = b.z / ((b.y*b.y)+(b.z*b.z))**(1.0/2.0)
        except:
            sinbx = 0.0
        if self.rotation_abs.x == 0:
            angle = degrees((np.arcsin(sinbx)))%360.0
        else:
            angle = self.rotation_abs.x%360.0
        print("----\n\n", self.symbol)
        angle = radians(angle)
#        if angle == 0:
        print("x0 : \t", self.symbol, self.rotation, self.rotation_abs, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
        sinbx = np.sin(angle)
        cosbx = np.cos(angle)
#        try:
#            cosbx = b.y / ((b.y*b.y)+(b.z*b.z))**(1.0/2.0)
#        except:
#            cosbx = 1.0
        rotationx = [
                    [1, 0, 0],
                    [0,cosbx,-sinbx],
                    [0, sinbx, cosbx]
                    ]
#        print(rotationx)

        newvec = [rotationx[0][0]*c.x+rotationx[0][1]*c.y+rotationx[0][2]*c.z, rotationx[1][0]*c.x+rotationx[1][1]*c.y+rotationx[1][2]*c.z, rotationx[2][0]*c.x+rotationx[2][1]*c.y+rotationx[2][2]*c.z]
#        print(newvec)
        try:
            sinby = b.z / ((b.x*b.x)+(b.z*b.z))**(1.0/2.0)
        except:
            sinby = 0.0
        if self.rotation_abs.y == 0:
            angle = degrees((np.arcsin(sinby)))%360.0
        else:
            angle = self.rotation_abs.y%360.0
#        print("y0 : \t", angle, self.symbol, self.rotation, self.rotation_abs, self.position_abs, self.parent.symbol, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
        angle = radians(angle)
#        if angle == 0:
#            print("y0 : \t", self.symbol, self.rotation, self.rotation_abs, self.position_abs, self.parent.symbol, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
        sinby = np.sin(angle)
        cosby = np.cos(angle)
#        try:
#            cosby = b.x / ((b.x*b.x)+(b.z*b.z))**(1.0/2.0)
#        except:
#            cosby = 1.0
        rotationy = [
                    [cosby, 0, sinby],
                    [0,1,0],
                    [-sinby, 0, cosby]
                    ]

#        newvec = [rotationy[0][0]*c.x+rotationy[0][1]*c.y+rotationy[0][2]*c.z, rotationy[1][0]*c.x+rotationy[1][1]*c.y+rotationy[1][2]*c.z, rotationy[2][0]*c.x+rotationy[2][1]*c.y+rotationy[2][2]*c.z]

        #b = vector(newvec[0], newvec[1], newvec[2])
        try:
            sinbz = b.x / ((b.y*b.y)+(b.x*b.x))**(1.0/2.0)
        except:
            sinbz = 0.0
        if self.rotation_abs.z == 0.0:
            angle = degrees((np.arcsin(sinbz)))%360.0
        else:
            angle = self.rotation_abs.z%360.0
#        print("z0 : \t", angle, self.symbol, self.rotation, self.rotation_abs, self.position_abs, self.parent.symbol, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
        angle = radians(angle)
#        if angle == 0:
#            print("z0 : \t", self.symbol, self.rotation, self.rotation_abs, self.position_abs, self.parent.symbol, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
        sinbz = np.sin(angle)
        cosbz = np.cos(angle)
#        try:
#            cosbz = b.y / ((b.y*b.y)+(b.x*b.x))**(1.0/2.0)
#        except:
#            cosbz = 1.0
        rotationz = [
                    [cosbz, -sinbz, 0],
                    [sinbz,cosbz,0],
                    [0, 0, 1]
                    ]

#        newvec = [rotationz[0][0]*c.x+rotationz[0][1]*c.y+rotationz[0][2]*c.z, rotationz[1][0]*c.x+rotationz[1][1]*c.y+rotationz[1][2]*c.z, rotationz[2][0]*c.x+rotationz[2][1]*c.y+rotationz[2][2]*c.z]
        print(c.y, (1.0*self.from_root),  c.y**(1.0*self.from_root))
        newveca = ((np.array(rotationz).dot(np.array(rotationy))).dot(np.array(rotationx))).dot(np.array([c.x **(1.0*self.from_root), c.y**(1.0*self.from_root), c.z**(1.0*self.from_root)]))
        newvec = vector(newveca[2], newveca[1], newveca[0])
#        print("last", newvec)
        return newvec

    def calculate_position(self):
        sum_pos = (self.parent.position_calc.x+self.parent.position_calc.y+self.parent.position_calc.z)
        if self.parent != None:#sum_pos > 0:
            self.position_calc = self.alignWithVector()
#            self.axis_abs.x = self.parent.position_calc.x/sum_pos
#            self.axis_abs.y = self.parent.position_calc.y/sum_pos
#            self.axis_abs.z = self.parent.position_calc.z/sum_pos
#            self.position_calc.x = self.position.x * self.axis_abs.x
#            self.position_calc.y = self.position.y * self.axis_abs.y
#            self.position_calc.z = self.position.z * self.axis_abs.z
        else:
            self.position_calc.x = self.position.x
            self.position_calc.y = self.position.y
            self.position_calc.z = self.position.z
        print(self.position_calc.y)

elements_templates = {}


##########################################################################################################################################
#####################################      ---         definitions and classes         ---      ##########################################
##########################################################################################################################################




##########################################################################################################################################
###############################################      ---         SETTINGS         ---      ###############################################
##########################################################################################################################################


##demo

#r1 = 0.9
#r2 = 0.7
#a1 = 10.0
#a2 = 20.0
#wr = 0.977
#min_width = 0.003
#system = System(V = ["ar", "al", "br", "bl", "p"], w = "p", P = {"p":["p", "ar", "al"],"ar": ["al", "br"], "al": ["p", "bl", "ar"], "br": ["ar"], "bl": ["al"]})
#elements_templates["ar"] = Element(symbol = "ar", position = Position(0.1, 0.7, 0.4), rotation = Position(0,0,0))
#elements_templates["al"] = Element(symbol = "al", position = Position(0.05, 0.8, -0.75), rotation = Position(0,40,0))
#elements_templates["br"] = Element(symbol = "br", position = Position(0.3, 1.4, 0.5), rotation = Position(0,0,0))
#elements_templates["bl"] = Element(symbol = "bl", position = Position(0.35, 0.5, -0.35), rotation = Position(0,0,0))
#elements_templates["p"] = Element(symbol = "p", position = Position(0.0, 2.0, 0.0), rotation = Position(0.0,30.0,0.0))
#elements_templates["cr"] = Element(symbol = "cr", position = Position(0.0, r1, 0.0), rotation = Position(0.0,1.0,0.0))
#elements_templates["cl"] = Element(symbol = "cl", position = Position(0.0, r2, 0.0), rotation = Position(0.0,1.0,0.0))

##00
#
#r1 = 0.9
#r2 = 0.85
#r3 = 0.6
#a1 = 90
#a2 = 90
#p1 = 0.0
#p2 = 137.5
#p3 = 0.0
#wr = 0.9
#min_width = 0.003
#system = System(V = ["ar", "al", "p"], w = "p", P = {"p":["p", "al", "ar"],"ar": ["bl"], "al": ["br"], "br":["cr"], "bl": ["cl"], "cr":["dr", "dl"], "cl":["dr", "dl"], "dr":["dr", "dl"], "dl":["dr"]}, width_rate = wr)
#
#elements_templates["p"] = Element(symbol = "p", position = Position(0.0, 0.9, 0.0), rotation = Position(p1,p2,p3))
#elements_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, a1))
#elements_templates["al"] = Element(symbol = "al", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, 360-a1))
#elements_templates["br"] = Element(symbol = "br", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,50.0))
#elements_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,360-50.0))
#elements_templates["cr"] = Element(symbol = "cr", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,360.0-25.0))
#elements_templates["cl"] = Element(symbol = "cl", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,25.0))
#elements_templates["dr"] = Element(symbol = "dr", position = Position(0.0, r3, 0.0), rotation = Position(15.0,0.0,0.0))
#elements_templates["dl"] = Element(symbol = "dl", position = Position(0.0, r3, 0.0), rotation = Position(360.0-15.0,0.0,0.0))
#
#
#nrOfNodes = 2005
#width_scale = 0.07

#
#01
#
#r1 = 0.9
#r2 = 0.82
#r3 = 0.6
#a1 = 160
#a2 = 160
#wr = 0.9
#min_width = 0.003
#system = System(V = ["ar", "al", "p"], w = "p", P = {"p":["p", "al", "ar"],"ar": ["pb"], "al": ["pb"], "pb":["pb", "br", "bl"], "br":[], "bl":[]}, width_rate = wr)
#elements_templates["p"] = Element(symbol = "p", position = Position(0.0, 0.9, 0.0), rotation = Position(0.0,137.5,0.0))
#elements_templates["pb"] = Element(symbol = "pb", position = Position(0.0, r2, 0.0), rotation = Position(0.0,137.5,0.0))
#elements_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, a1))
#elements_templates["al"] = Element(symbol = "al", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, 360-a1))
#elements_templates["br"] = Element(symbol = "br", position = Position(0.0, r2, 0.0), rotation = Position(180.0,0.0, a1))
#elements_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r2, 0.0), rotation = Position(180.0,0.0, 360-a1))
#
#
#nrOfNodes = 200
#width_scale = 0.07


##02
#
#r1 = 0.9
#r2 = 0.7
#a1 = 10.0
#a2 = 20.0
#wr = 0.977
#min_width = 0.003
#system = System(V = ["ar", "al", "p"], w = "p", P = {"p":["al", "ar"],"ar": ["br", "bl"], "al": ["ar", "al"], "br":["al", "ar"], "bl": ["al", "br"], "cr":["br", "bl"], "cl":["ar", "al"]}, width_rate = wr)
#
#elements_templates["p"] = Element(symbol = "p", position = Position(0.0, 0.9, 0.0), rotation = Position(0.0,0.0,0.0))
#elements_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r1, 0.0), rotation = Position(0.0,137.5, 360.0-a2))
#elements_templates["al"] = Element(symbol = "al", position = Position(0.0, r2, 0.0), rotation = Position(0.0,137.5,a1))
#elements_templates["br"] = Element(symbol = "br", position = Position(0.0, r1, 0.0), rotation = Position(0.0,137.5,a2))
#elements_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r2, 0.0), rotation = Position(0.0,137.5,360.0-a1))
#
#
#nrOfNodes = 152
#width_scale = 0.07


#03
#
#r1 = 0.7
#r2 = 0.9
#a1 = 51.0
#a2 = 20.0
#wr = 0.987
#min_width = 0.003
#system = System(V = ["ar", "al", "p"], w = "p", P = {"p":["p", "al", "ar"],"ar": ["b", "al"], "al": ["b", "ar"], "b":["b", "ar", "al"]}, width_rate = wr)
#
#elements_templates["p"] = Element(symbol = "p", position = Position(0.0, r1, 0.0), rotation = Position(0.0,40.0,0.0))
#elements_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,a1 ))
#elements_templates["al"] = Element(symbol = "al", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,-a1))
#elements_templates["b"] = Element(symbol = "b", position = Position(0.0, r1, 0.0), rotation = Position(0.0,0.0,0.0))
#
#
#nrOfNodes = 1502
#width_scale = 0.07
#
##04
#
#r1 = 0.9
#r2 = 0.85
#r3 = 0.7
#a1 = 160
#a2 = 160
#wr = 0.9
#min_width = 0.003
#system = System(V = ["ar", "al", "p"], w = "p", P = {"p":["p", "al", "ar"],"ar": ["pb"], "al": ["pa"], "pa":["pa", "br", "bl"], "pb":["pb", "br", "bl"], "br":[], "bl":[]}, width_rate = wr)
#elements_templates["p"] = Element(symbol = "p", position = Position(0.0, 0.9, 0.0), rotation = Position(0.0,137.5,0.0))
#elements_templates["pa"] = Element(symbol = "pa", position = Position(0.0, r2, 0.0), rotation = Position(0.0,137.5,-2.0))
#elements_templates["pb"] = Element(symbol = "pb", position = Position(0.0, r2, 0.0), rotation = Position(0.0,137.5,2.0))
#elements_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, a1))
#elements_templates["al"] = Element(symbol = "al", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, 360-a1))
#elements_templates["br"] = Element(symbol = "br", position = Position(0.0, r3, 0.0), rotation = Position(180.0,0.0, a1))
#elements_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r3, 0.0), rotation = Position(180.0,0.0, 360-a1))
#
#
#nrOfNodes = 200
#width_scale = 0.07


##05 TO_DO
#
#r1 = 0.999
#r2 = 1.1
#r3 = 1.0
#r4 = 7.0
#a1 = 160
#a2 = 220
#a3 = 10
#wr = 0.9999
#min_width = 0.003
#system = System(V = ["ar", "al", "p"], w = "p", P = {"p":["pp"], "pp":["ppp"],"ppp":["pppp"],"pppp":["pp", "cl", "cr", "ct"],"cl":["al"],"cr":["ar"],"ct":["ar"], "ar": ["pb"], "al": ["pa"], "pa":[ "br", "bl"], "pb":["br", "bl"], "br":["d"], "bl":["d"], "d":["dr", "dl"], "dr":["e"], "dl":["e"], "e":["el", "er"], "el":[], "er":[]}, width_rate = wr)
#elements_templates["p"] = Element(symbol = "p", position = Position(0.0, r4, 0.0), rotation = Position(0.0,137.5,0.0))
#elements_templates["pp"] = Element(symbol = "pp", position = Position(0.0, r1, 0.0), rotation = Position(0.0,137.5,0.0))
#elements_templates["ppp"] = Element(symbol = "ppp", position = Position(0.0, r1, 0.0), rotation = Position(0.0,137.5,0.0))
#elements_templates["pppp"] = Element(symbol = "pppp", position = Position(0.0, r1, 0.0), rotation = Position(0.0,137.5,0.0))
#elements_templates["cr"] = Element(symbol = "cr", position = Position(0.0, r2, 0.0), rotation = Position(a1,0.0, a1))
#elements_templates["cl"] = Element(symbol = "cl", position = Position(0.0, r2, 0.0), rotation = Position(-a1,0.0, 360-a1))
#elements_templates["ct"] = Element(symbol = "ct", position = Position(0.0, r2, 0.0), rotation = Position(+a1,0.0, 360-a1))
#elements_templates["pa"] = Element(symbol = "pa", position = Position(0.0, r3, 0.0), rotation = Position(0.0,10.0,-2.0))
#elements_templates["pb"] = Element(symbol = "pb", position = Position(0.0, r3, 0.0), rotation = Position(0.0,10.0,2.0))
#elements_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, a2))
#elements_templates["al"] = Element(symbol = "al", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, 360-a2))
#elements_templates["br"] = Element(symbol = "br", position = Position(0.0, r3, 0.0), rotation = Position(180.0,0.0, a1))
#elements_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r3, 0.0), rotation = Position(180.0,0.0, 360-a1))
#elements_templates["d"] = Element(symbol = "d", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, 0.0))
#elements_templates["dr"] = Element(symbol = "dr", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, 360-a3))
#elements_templates["dl"] = Element(symbol = "dl", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, a3))
#elements_templates["e"] = Element(symbol = "e", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, 0.0))
#elements_templates["er"] = Element(symbol = "er", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, 360-a3))
#elements_templates["el"] = Element(symbol = "el", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, a3))
#
#
#nrOfNodes = 550
#width_scale = 0.07



##06
#
#r1 = 0.7
#r2 = 0.9
#a1 = 31.0
#a2 = 20.0
#p1 = 40.0
#p2 = 110.0
#p3 = 15.0
#wr = 0.987
#min_width = 0.003
#system = System(V = ["ar", "al", "p"], w = "p", P = {"p":["p", "al", "ar"],"ar": ["b", "al"], "al": ["b", "ar"], "b":["p", "ar", "al"]}, width_rate = wr)
#
#elements_templates["p"] = Element(symbol = "p", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
#elements_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r2, 0.0), rotation = Position(a2,0.0,a1 ))
#elements_templates["al"] = Element(symbol = "al", position = Position(0.0, r2, 0.0), rotation = Position(-a2,0.0,-a1))
#elements_templates["b"] = Element(symbol = "b", position = Position(0.0, r1, 0.0), rotation = Position(-p1,p2,p3))
##elements_templates["br"] = Element(symbol = "br", position = Position(0.0, r1, 0.0), rotation = Position(0.0,137.5,a2))
##elements_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r2, 0.0), rotation = Position(0.0,137.5,360.0-a1))
#
#
#nrOfNodes = 702
#width_scale = 0.07

##02b
#
#r1 = 0.95
#r2 = 0.9
#a1 = 31.0
#a2 = 3.0
#p1 = 5.0
#p2 = 110.0
#p3 = 4.0
#wr = 0.987
#min_width = 0.003
#system = System(V = ["ar", "al", "p"], w = "p", P = {"p":["pp"], "pp":["p","ppp"], "ppp":["ppp", "al", "ar"],"ar": ["b"], "al": ["b"], "b":["ar", "al"]}, width_rate = wr)
#
#elements_templates["p"] = Element(symbol = "p", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
#elements_templates["pp"] = Element(symbol = "pp", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
#elements_templates["ppp"] = Element(symbol = "ppp", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
#elements_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r2, 0.0), rotation = Position(a2,0.0,a1 ))
#elements_templates["al"] = Element(symbol = "al", position = Position(0.0, r2, 0.0), rotation = Position(-a2,0.0,-a1))
#elements_templates["b"] = Element(symbol = "b", position = Position(0.0, r2, 0.0), rotation = Position(-p1,p2,p3))
#
#
#nrOfNodes = 1002
#width_scale = 0.07


##07
#
#r1 = 0.99
#r2 = 0.89
#a1 = 71.0
#a2 = 3.0
#b1 = 9.0
#b2 = 15.0
#p1 = 4.0
#p2 = 100.0
#p3 = 3.0
#wr = 0.95
#min_width = 0.003
#system = System(V = ["ar", "al", "p"], w = "p", P = {"p":["pp"], "pp":["ppp"], "ppp":["p", "al", "ar"],"ar": ["b"], "al": ["b"], "b":["br", "bl"], "br":["bb"], "bl":["br"], "bb":["b"]}, width_rate = wr)
#
#elements_templates["p"] = Element(symbol = "p", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
#elements_templates["pp"] = Element(symbol = "pp", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
#elements_templates["ppp"] = Element(symbol = "ppp", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
#elements_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r2, 0.0), rotation = Position(a2,0.0,a1 ))
#elements_templates["al"] = Element(symbol = "al", position = Position(0.0, r2, 0.0), rotation = Position(-a2,0.0,-a1))
#elements_templates["br"] = Element(symbol = "br", position = Position(0.0, r2, 0.0), rotation = Position(b2,0.0,b1 ))
#elements_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r2, 0.0), rotation = Position(-b2,0.0,-b1))
#elements_templates["b"] = Element(symbol = "b", position = Position(0.0, r2, 0.0), rotation = Position(-p1,p2,p3))
#elements_templates["bb"] = Element(symbol = "bb", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,0.0))
##elements_templates["br"] = Element(symbol = "br", position = Position(0.0, r1, 0.0), rotation = Position(0.0,137.5,a2))
##elements_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r2, 0.0), rotation = Position(0.0,137.5,360.0-a1))
#
#
#nrOfNodes = 300
#width_scale = 0.18


##########################################################################################################################################
###############################################      ---         SETTINGS         ---      ###############################################
##########################################################################################################################################







##########################################################################################################################################
##############################################      ---         RENDERING         ---      ###############################################
##########################################################################################################################################


elements = []
element = Element(template = elements_templates[system.w], parent = None)
elements.append(element)

for i in range(0, nrOfNodes):
    new_row = system.next(elements[i].symbol)
    
    for new_element in new_row:
        element = Element(template = elements_templates[new_element], parent = elements[i], width = system.width_rate**i)
        elements[i].children.append(element)
        elements.append(element)
elements[0].set_from_root()

for i in range(0, len(elements)):
    for element in elements:
        if element.from_root == i:
            print(element, "("+str(element.parent)+")", end="\t")

#sphere()
scene = canvas(x=0, y=0, width=3200, height=2400, background=vector(0, 0, 0))
scene.center = vector(0.0, 5.0, 0.0)
scene.select()


cylinder(pos = vector(0.0,0.01,0.0), axis = vector(elements[0].position.x, elements[0].position.y, elements[0].position.z), radius = elements[0].width*width_scale+min_width, color=color.white)
elements[0].position_abs.x = 0.0 + elements[0].position.x
elements[0].position_abs.y = 0.0 + elements[0].position.y
elements[0].position_abs.z = 0.0 + elements[0].position.z
ii = 0
for element in elements[1:]:
    ii+=1
    print(ii," nodes")
    element.calculate_position()
    if element.width > min_width:
        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = element.width*width_scale+min_width, color=color.white)
    else:
        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = element.width*width_scale+min_width, color=color.white)
        
#    if element.symbol == "al":
#        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = element.width*width_scale+min_width, color=color.green)
#    elif element.symbol == "ar":
#        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = element.width*width_scale+min_width, color=color.blue)
#    elif element.symbol == "p":
#        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = element.width*width_scale+min_width, color=color.red)
#    else:
#        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = element.width*width_scale+min_width)
    element.position_abs.x = element.parent.position_abs.x + element.position_calc.x
    element.position_abs.y = element.parent.position_abs.y + element.position_calc.y
    element.position_abs.z = element.parent.position_abs.z + element.position_calc.z


##########################################################################################################################################
##############################################      ---         RENDERING         ---      ###############################################
##########################################################################################################################################
