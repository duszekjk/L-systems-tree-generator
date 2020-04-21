
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
    def __init__(self, V = ["ar", "al", "br", "bl"], w = "ar", P = {"ar": ["al", "br"], "al": ["bl", "ar"], "br": ["ar"], "bl": ["al"]}):
        self.V = V
        self.w = w
        self.P = P
    def next(self, symbol: "a"):
        return self.P[symbol]

class Element:
    position     = Position()
    position_abs = Position()
    axis_abs     = Position()
    position_calc= Position()
    rotation     = Position()
    rotation_abs = Position()
    symbol       = "a"
    parent       = None
    children     = []
    from_root    = 0
    def __init__(self, symbol = "a", parent = None, position = Position(), rotation = Position(), template = None):
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
        self.from_root    = 0
        self.position_abs = Position(0.0, 0.0, 0.0)
        self.rotation_abs = Position(0.0, 0.0, 0.0)
        self.position_calc= Position(0.0, 0.0, 0.0)
        self.axis_abs     = Position(0.0, 0.0, 0.0)
        if(self.parent != None):
            self.rotation_abs.x = (self.parent.rotation_abs.x + self.rotation.x)%360.0
            self.rotation_abs.y = (self.parent.rotation_abs.y + self.rotation.y)%360.0
            self.rotation_abs.z = (self.parent.rotation_abs.z + self.rotation.z)%360.0
        
    def __str__(self):
        return self.symbol
    def set_from_root(self, d = 0):
        self.from_root = d
        for child in self.children:
            child.set_from_root(d+1)
    def alignWithVector(self):
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
        print("x0 : \t", angle,  self.symbol, self.rotation, self.rotation_abs, self.position_abs, self.parent.symbol, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
        angle = radians(angle)
        if angle == 0:
            print("x0 : \t", self.symbol, self.rotation, self.rotation_abs, self.position_abs, self.parent.symbol, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
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
        print("y0 : \t", angle, self.symbol, self.rotation, self.rotation_abs, self.position_abs, self.parent.symbol, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
        angle = radians(angle)
        if angle == 0:
            print("y0 : \t", self.symbol, self.rotation, self.rotation_abs, self.position_abs, self.parent.symbol, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
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
        print("z0 : \t", angle, self.symbol, self.rotation, self.rotation_abs, self.position_abs, self.parent.symbol, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
        angle = radians(angle)
        if angle == 0:
            print("z0 : \t", self.symbol, self.rotation, self.rotation_abs, self.position_abs, self.parent.symbol, self.parent.rotation, self.parent.rotation_abs, self.parent.position_abs)
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

        newveca = ((np.array(rotationz).dot(np.array(rotationy))).dot(np.array(rotationx))).dot(np.array([c.x, c.y, c.z]))
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


#system = System(V = ["ar", "al", "br", "bl", "p"], w = "p", P = {"p":["p", "ar", "al"],"ar": ["al", "br"], "al": ["p", "bl", "ar"], "br": ["ar"], "bl": ["al"]})
system = System(V = ["ar", "al", "p"], w = "p", P = {"p":["p", "ar", "al"],"ar": ["p", "al"], "al": ["p", "ar"]})
#elements_templates["ar"] = Element(symbol = "ar", position = Position(0.1, 0.7, 0.4), rotation = Position(0,0,0))
#elements_templates["al"] = Element(symbol = "al", position = Position(0.05, 0.8, -0.75), rotation = Position(0,40,0))
#elements_templates["br"] = Element(symbol = "br", position = Position(0.3, 1.4, 0.5), rotation = Position(0,0,0))
#elements_templates["bl"] = Element(symbol = "bl", position = Position(0.35, 0.5, -0.35), rotation = Position(0,0,0))
#elements_templates["p"] = Element(symbol = "p", position = Position(0.0, 2.0, 0.0), rotation = Position(0.0,30.0,0.0))

elements_templates["p"] = Element(symbol = "p", position = Position(0.0, 2.0, 0.0), rotation = Position(0.0,31.0,0.0))
elements_templates["ar"] = Element(symbol = "ar", position = Position(0.0, 1.1, 0.0), rotation = Position(47.0,5.0,5.0))
elements_templates["al"] = Element(symbol = "al", position = Position(0.0, 0.9, 0.0), rotation = Position(65.0,180.0,0.0))


nrOfNodes = 92

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
        element = Element(template = elements_templates[new_element], parent = elements[i])
        elements[i].children.append(element)
        elements.append(element)
elements[0].set_from_root()

for i in range(0, len(elements)):
    print("")
    for element in elements:
        if element.from_root == i:
            print(element, "("+str(element.parent)+")", end="\t")

#sphere()
scene = canvas(x=0, y=0, width=3200, height=2400, background=vector(0, 0, 1))
scene.center = vector(0.0, 5.0, 0.0)
scene.select()


cylinder(pos = vector(0.0,0.01,0.0), axis = vector(elements[0].position.x, elements[0].position.y, elements[0].position.z), radius = 0.02, color=color.red)
elements[0].position_abs.x = 0.0 + elements[0].position.x
elements[0].position_abs.y = 0.0 + elements[0].position.y
elements[0].position_abs.z = 0.0 + elements[0].position.z
ii = 0
for element in elements[1:]:
    ii+=1
    print(ii," nodes")
    element.calculate_position()
    if element.symbol == "al":
        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = 0.02, color=color.green)
    elif element.symbol == "ar":
        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = 0.02, color=color.blue)
    elif element.symbol == "p":
        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = 0.02, color=color.red)
    else:
        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = 0.02)
    element.position_abs.x = element.parent.position_abs.x + element.position_calc.x
    element.position_abs.y = element.parent.position_abs.y + element.position_calc.y
    element.position_abs.z = element.parent.position_abs.z + element.position_calc.z


##########################################################################################################################################
##############################################      ---         RENDERING         ---      ###############################################
##########################################################################################################################################
