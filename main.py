
from vpython import *
from vectors import Point, Vector
import numpy as np
import math
import random
import open3d as o3d
import time
import os
import sys
import gc

#from pympler.tracker import SummaryTracker
#tracker = SummaryTracker()

##########################################################################################################################################
#####################################      ---         definitions and classes         ---      ##########################################
##########################################################################################################################################

NR_OF_BATCHES      = 5
NR_OF_BATCHES_NOW  = 4
SAVE_PATH          = "/Users/jacekkaluzny/Pictures/untitled folder/"    #for json models, images are saved in downloads
COLOR_TREE         = color.black        # default tree color
COLOR_BACKGROUND   = color.white
NODES_SIMPLIFIER   = 1.0                #devide nr of nodes by this number to have smaller trees (with fewer elements)

#       coloring based on node type, length or angle (rgb colors)

COLORS_TREE = {"p":vec(21, 67, 96), "pp":vec(169, 204, 227), "ppp":vec(52, 73, 94), "pppp":vec(133, 193, 233), "ppppp":vec(46, 134, 193), "ar":vec(125, 102, 8), "al":vec(243, 156, 18), "br":vec(123, 36, 28), "b":vec(253, 237, 236), "bl":vec(231, 76, 60), "cr":vec(135, 54, 0), "cl":vec(220, 118, 51), "dr":vec(25, 111, 61), "dl":vec(88, 214, 141), "pa":vec(74, 35, 90), "pb":vec(187, 143, 206), }
#COLORS_TREE = {"p":vec(21, 67, 96), "pp":vec(169, 204, 227), "ppp":vec(52, 73, 94), "pppp":vec(133, 193, 233), "ppppp":vec(46, 134, 193), "ar":vec(125, 102, 8), "al":vec(243, 156, 18), "br":vec(123, 36, 28), "b":vec(253, 237, 236), "bl":vec(231, 76, 60), "cr":vec(135, 54, 0), "cl":vec(220, 118, 51), "dr":vec(25, 111, 61), "dl":vec(88, 214, 141), "pa":vec(74, 35, 90), "pb":vec(187, 143, 206), }
#COLORS_TREE = {"p":vec(21, 67, 96), "pp":vec(169, 204, 227), "ppp":vec(52, 73, 94), "pppp":vec(133, 193, 233), "ppppp":vec(46, 134, 193), "ar":vec(125, 102, 8), "al":vec(243, 156, 18), "br":vec(123, 36, 28), "b":vec(253, 237, 236), "bl":vec(231, 76, 60), "cr":vec(135, 54, 0), "cl":vec(220, 118, 51), "dr":vec(25, 111, 61), "dl":vec(88, 214, 141), "pa":vec(74, 35, 90), "pb":vec(187, 143, 206), }

for tree in COLORS_TREE:
    COLORS_TREE[tree] /= 255.0

species = ["pine", "thuja", "akazia", "maple", "poplar", "birch", "oak", "lemon"]

settings = sys.argv
last_batch_id = 0
timeStart = time.time()
continue_task = False

for s in settings:
    if s == "c":
        continue_task = True
        continue
    if continue_task == True and last_batch_id == 0:
        last_batch_id = float(s)
        continue
    if continue_task == True:
        timeStart = float(s)

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
    id = 0
    element_templates = {}
    nrOfNodes = 20
    width_scale = 0.07
    width_rate = 0.9
    width_rate = 0.9
    def __init__(self, id = 0, V = ["ar", "al", "br", "bl"], w = "ar", P = {"ar": ["al", "br"], "al": ["bl", "ar"], "br": ["ar"], "bl": ["al"]}, width_rate = 0.9):
        self.id = id
        self.V = V
        self.w = w
        self.P = P
        self.width_rate = width_rate
        self.element_templates = {}
    def render(self, scene):
        ##########################################################################################################################################
        ##############################################      ---         RENDERING         ---      ###############################################
        ##########################################################################################################################################


        elements = []
        element = Element(template = self.element_templates[self.w], parent = None)
        elements.append(element)

        for i in range(0, round(self.nrOfNodes/NODES_SIMPLIFIER)):
            new_row = self.next(elements[i].symbol)
            
            for new_element in new_row:
                element = Element(template = self.element_templates[new_element], parent = elements[i], width = self.width_rate**i)
                elements[i].children.append(element)
                elements.append(element)
        elements[0].set_from_root()

        for i in range(0, len(elements)):
            for element in elements:
                if element.from_root == i:
                    print(element, "("+str(element.parent)+")", end="\t")


        cylinder(pos = vector(0.0,0.01,0.0), axis = vector(elements[0].position.x, elements[0].position.y, elements[0].position.z), radius = elements[0].width*self.width_scale+min_width, color=color.white)
        elements[0].position_abs.x = 0.0 + elements[0].position.x
        elements[0].position_abs.y = 0.0 + elements[0].position.y
        elements[0].position_abs.z = 0.0 + elements[0].position.z
        ii = 0
        for element in elements[1:]:
            ii+=1
            print(ii," nodes")
            element.calculate_position()
            if element.width > min_width:
                cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = element.width*self.width_scale+min_width, color=color.white)
            else:
                cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = element.width*self.width_scale+min_width, color=color.white)
                
            element.position_abs.x = element.parent.position_abs.x + element.position_calc.x
            element.position_abs.y = element.parent.position_abs.y + element.position_calc.y
            element.position_abs.z = element.parent.position_abs.z + element.position_calc.z


        ##########################################################################################################################################
        ##############################################      ---         RENDERING         ---      ###############################################
        ##########################################################################################################################################
        
    def next(self, symbol: "a"):
        return self.P[symbol]
        
        
        
def add_system(system):
    global systems_array_simple
    global all_dictionary
    
    systems_array_simple.append(system)
    for key in system.P:
#        print(key)
        j = 0
        while key+"."+str(j) in all_dictionary and str(system.P[key]) != str(all_dictionary[key+"."+str(j)][1]):
            j+=1
        if key+"."+str(j) in all_dictionary:
            all_dictionary[key+"."+str(j)][2].append(system.id)
        else:
            all_dictionary[key+"."+str(j)] = (5, system.P[key], [system.id,])
#        print(key+"."+str(j), all_dictionary[key+"."+str(j)])



class SystemAll():
    V = []
    w = ""
    P = {}
    p1 = 0.0
    p2 = 0.0
    p3 = 0.0
    a = {}
    r = {}
    id = 0
    nrOfNodes = 20
    width_scale = 0.07
    width_rate = 0.9
    min_width = 0.3
    element_templates = {}
    ply_shape = None
    json = ""
    #    P = {"ar.0": (95,["al", "br"]), "al.0": (95, ["bl", "ar"]), "br.0": (95, ["ar"]), "bl.0": (95, ["al"])}
    def __init__(self, V = None, w = None, P = None, width_rate = None, system = None):
        self.a = {}
        self.r = {}
        self.P = {}
        self.element_templates = {}
        self.V = []
        if system != None:
            self.V = system.V
            self.w = system.w
            self.P = system.P
            self.id = system.id
            self.width_rate = system.width_rate
            self.nrOfNodes = system.nrOfNodes
            self.width_scale = system.width_scale
            self.width_rate = system.width_rate
            self.min_width = system.min_width
        if V != None:
            self.V = V
        if P != None:
            self.P = P
        if width_rate != None:
            self.width_rate = width_rate
    def __str__(self):
        description = ""
        description += str(self.nrOfNodes)
        description += ", "
        description += str(self.width_rate)
        description += ", "
        description += str(self.min_width)
        description += ", "
        description += str(self.width_scale)
        description += ", "
        description += str(self.p1)
        description += ", "
        description += str(self.p2)
        description += ", "
        description += str(self.p3)
        description += ", "
        for p in sorted (self.P):
            description += str(self.P[p][0])
            description += ", "
        for aa in sorted (self.a):
            description += str(self.a[aa])
            description += ", "
        for rr in sorted (self.r):
            description += str(self.r[rr])
            description += ", "
        description = description[:-1]
        description += "\n"
        return description
    def header(self):
        description = "File Name, "
        description += "species"
        description += ", "
        description += "nrOfNodes"
        description += ", "
        description += "width_rate"
        description += ", "
        description += "min_width"
        description += ", "
        description += "width_scale"
        description += ", "
        description += "p_rotation_x"
        description += ", "
        description += "p_rotation_y"
        description += ", "
        description += "p_rotation_z"
        description += ", "
        for p in sorted (self.P):
            description += str(p)+"->"+str(self.P[p][1]).replace(",", "|")
            description += ", "
        for aa in sorted (self.a):
            description += aa + " rotation"
            description += ", "
        for rr in sorted (self.r):
            description += rr + " length"
            description += ", "
        description = description[:-1]
        description += "\n"
        return description
        
    def refresh(self):
        for s in self.P:
            symbol = s.split(".")[0]
            if symbol+"x" not in self.a:
                self.a[symbol+"x"] = 0.0
                self.a[symbol+"y"] = 0.0
                self.a[symbol+"z"] = 0.0
            if symbol not in self.r:
                self.r[symbol] = 0.0
        self.element_templates = {}
        self.element_templates[self.w] = Element(symbol = self.w, position = Position(0.0, float(self.r[self.w]), 0.0), rotation = Position(float(self.p1),float(self.p2),float(self.p3)))
        for s in self.P:
            symbol = s.split(".")[0]
            if symbol not in self.element_templates:
                self.element_templates[symbol] = Element(symbol = symbol, position = Position(0.0, float(self.r[symbol]), 0.0), rotation = Position(float(self.a[symbol+"x"]),float(self.a[symbol+"y"]),float(self.a[symbol+"z"])))
                
                
    def random(self):
        for aa in self.a:
            self.a[aa] = str(float(self.a[aa]) + random.uniform(-2.0, 2.0))
        for rr in self.r:
            self.r[rr] = str(float(self.r[rr]) + random.uniform(-0.05, 0.05))
        for p in self.P:
            self.P[p] = (max(0,min(100,self.P[p][0]+random.randint(-5, 5))), self.P[p][1], self.P[p][2])
        self.nrOfNodes += random.randint(-200, 200)
        self.width_scale += random.uniform(-0.01, 0.01)
        self.width_rate += random.uniform(-0.01, 0.01)
        self.min_width += random.uniform(-0.01, 0.01)
        
        self.nrOfNodes = max(20, self.nrOfNodes)
        self.width_scale = max(0.01, self.width_scale)
        self.width_rate = max(0.01, self.width_rate)
        self.min_width = max(0.02, self.min_width)
    def next(self, symbol= "a"):
        next_s = []
        okok = False
        next_i = 0
        while not okok and next_i < 5:
            next_i+=1
            for i in range(0, 100):
                try:
                    next_all = self.P[symbol+"."+str(i)]
#                    if (random.randint(0, 101) < int(next_all[0]) and symbol != "p") or (symbol == "p" and int(next_all[0]) > 80):
                    if (random.randint(0, 101) < int(next_all[0])):
                        next_s = next_all[1]
                        okok = True
                        break
                except:
                    break
        return next_s
        
    def render(self, scene):
        global element_id
        ##########################################################################################################################################
        ##############################################      ---         RENDERING         ---      ###############################################
        ##########################################################################################################################################


        elements = []
        element_id = 2
        element = Element(template = self.element_templates[self.w], parent = None)
        elements.append(element)
        
        for i in range(0, round(self.nrOfNodes/NODES_SIMPLIFIER)):
            try:
                new_row = self.next(elements[i].symbol)
            except:
                break
            
            for new_element in new_row:
                element = Element(template = self.element_templates[new_element], parent = elements[i], width = self.width_rate**i)
                elements[i].children.append(element)
                elements.append(element)
        elements[0].set_from_root()
#        print("")
        if elements[0].symbol in COLORS_TREE:
            cylinder(pos = vector(0.0,0.01,0.0), axis = vector(elements[0].position.x, elements[0].position.y, elements[0].position.z), radius = elements[0].width*self.width_scale+min_width, color=COLORS_TREE[elements[0].symbol])
        else:
            cylinder(pos = vector(0.0,0.01,0.0), axis = vector(elements[0].position.x, elements[0].position.y, elements[0].position.z), radius = elements[0].width*self.width_scale+min_width, color=COLOR_TREE)
        elements[0].position_abs.x = 0.0 + elements[0].position.x
        elements[0].position_abs.y = 0.0 + elements[0].position.y
        elements[0].position_abs.z = 0.0 + elements[0].position.z
        ii = 0

        json_string = """{
    "tree": [
        {
            "children": [
                {
                    "id": 2
                }
            ],
            "id": 1,
            "parent": 0",
            "position": [
                {
                    "x": 0.0
                },
                {
                    "y": 0.0
                },
                {
                    "z": 0.0
                }
            ],
            "thickness": """+str(self.width_scale+self.min_width)+"""
        },"""

        json_string += elements[0].json().replace("THIREPLACE", str(elements[0].width*self.width_scale+self.min_width)) + ","
        for element in elements[1:]:
            ii+=1

            element.calculate_position()
            
            if element.symbol in COLORS_TREE:
                cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = element.width*self.width_scale+self.min_width, color=COLORS_TREE[element.symbol])
            else:
                cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = element.width*self.width_scale+self.min_width, color=COLOR_TREE)
                
            element.position_abs.x = element.parent.position_abs.x + element.position_calc.x
            element.position_abs.y = element.parent.position_abs.y + element.position_calc.y
            element.position_abs.z = element.parent.position_abs.z + element.position_calc.z
            
            json_string += element.json().replace("THIREPLACE", str(element.width*self.width_scale+self.min_width)) + ","

        json_string = json_string[:-1]
        json_string += """
            ]
        }"""
        self.json = json_string

        ##########################################################################################################################################
        ##############################################      ---         RENDERING         ---      ###############################################
        ##########################################################################################################################################
element_id = 1
class Element:
    position     = Position()
    position_abs = Position()
    position_old = [0.0,0.0,0.0]
    axis_abs     = Position()
    position_calc= Position()
    rotation     = Position()
    rotation_abs = Position()
    width        = 1.0
    symbol       = "a"
    parent       = None
    children     = []
    from_root    = 0
    rotation_matrix = []
    id = 0
    def __init__(self, symbol = "a", parent = None, position = Position(), rotation = Position(), template = None, width = 1.0, from_root = 0):
        global element_id
        self.id = element_id
        element_id += 1
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
        self.position_old = [0.0, 0.0, 0.0]
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
    def ply(self):
         return pymesh.generate_cylinder(np.ndarray([self.parent.position_abs.x, self.parent.position_abs.y, self.parent.position_abs.z]), np.ndarray([self.position_abs.x, self.position_abs.y, self.position_abs.z]), self.parent.width*self.parent.width_scale+self.min_width, self.width*self.width_scale+self.min_width, num_segments=32)
    def json(self):
        json_string = """
        {
            "children": [
                {"""
        for child in self.children:
            json_string += """
                    "id": """+str(child.id)+""","""
        if self.parent == None:
            json_string += """
                }
            ],
            "id": """+str(self.id)+""",
            "parent": 0",
            "position": [
                {
                    "x": """+str(self.position_abs.x)+"""
                },
                {
                    "y": """+str(self.position_abs.y)+"""
                },
                {
                    "z": """+str(self.position_abs.z)+"""
                }
            ],
            "thickness": THIREPLACE
        }"""
        else:
            json_string += """
                }
            ],
            "id": """+str(self.id)+""",
            "parent": """+str(self.parent.id)+""",
            "position": [
                {
                    "x": """+str(self.position_abs.x)+"""
                },
                {
                    "y": """+str(self.position_abs.y)+"""
                },
                {
                    "z": """+str(self.position_abs.z)+"""
                }
            ],
            "thickness": THIREPLACE
        }"""
        return json_string
    def a(self):
        a = {self.symbol+"x": str(self.rotation.x), self.symbol+"y": str(self.rotation.y), self.symbol+"z": str(self.rotation.z)}
        return a

    def r(self):
        if self.position.x == 0 and self.position.z == 0:
            r = {self.symbol: str(self.position.y), }
        else:
            r = {self.symbol+"x": str(self.postition.x), self.symbol+"y": str(self.position.y), self.symbol+"z": str(self.position.z)}
        return r
        
    def set_from_root(self, d = 0):
        self.from_root = d
        for child in self.children:
            child.set_from_root(d+1)
    def alignWithVector(self):
        if(self.parent != None):
            self.rotation_abs.x = (self.parent.rotation_abs.x + self.rotation.x)%360.0
            self.rotation_abs.y = (self.parent.rotation_abs.y + self.rotation.y)%360.0
            self.rotation_abs.z = (self.parent.rotation_abs.z + self.rotation.z)%360.0
        
        
        
        if self.parent.parent == None:
            b = self.parent.position_calc
        else:
            b = self.parent.parent.position_calc - self.parent.position_calc
        c = self.position

        mesh_cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=0.3, height=0.9)
        self.rotation_matrix = np.array(mesh_cylinder.get_rotation_matrix_from_yzx((radians(self.rotation_abs.y), radians(self.rotation_abs.z), radians(self.rotation_abs.x))))
        newveca = self.rotation_matrix.dot(np.array([c.x **(1.0*self.from_root), c.y**(1.0*self.from_root), c.z**(1.0*self.from_root)]))
        
        newvec = vector(newveca[2], newveca[1], newveca[0])
        return newvec

    def calculate_position(self):
        sum_pos = (self.parent.position_calc.x+self.parent.position_calc.y+self.parent.position_calc.z)
        if self.parent != None:#sum_pos > 0:
            self.position_calc = self.alignWithVector()
        else:
            self.position_calc.x = self.position.x
            self.position_calc.y = self.position.y
            self.position_calc.z = self.position.z


systems_array_simple = []
all_dictionary = {}

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
#system.element_templates["ar"] = Element(symbol = "ar", position = Position(0.1, 0.7, 0.4), rotation = Position(0,0,0))
#system.element_templates["al"] = Element(symbol = "al", position = Position(0.05, 0.8, -0.75), rotation = Position(0,40,0))
#system.element_templates["br"] = Element(symbol = "br", position = Position(0.3, 1.4, 0.5), rotation = Position(0,0,0))
#system.element_templates["bl"] = Element(symbol = "bl", position = Position(0.35, 0.5, -0.35), rotation = Position(0,0,0))
#system.element_templates["p"] = Element(symbol = "p", position = Position(0.0, 2.0, 0.0), rotation = Position(0.0,30.0,0.0))
#system.element_templates["cr"] = Element(symbol = "cr", position = Position(0.0, r1, 0.0), rotation = Position(0.0,1.0,0.0))
#system.element_templates["cl"] = Element(symbol = "cl", position = Position(0.0, r2, 0.0), rotation = Position(0.0,1.0,0.0))


##00

element_id = 1
i_all = 0
r1 = 0.9
r2 = 0.85
r3 = 0.6
a1 = 90
a2 = 90
p1 = 0.0
p2 = 137.5
p3 = 0.0
wr = 0.8
min_width = 0.004
system = System(id = 0, V = ["ar", "al", "p"], w = "p", P = {"p":["p", "al", "ar"],"ar": ["bl"], "al": ["br"], "br":["cr"], "bl": ["cl"], "cr":["dr", "dl"], "cl":["dr", "dl"], "dr":["dr", "dl"], "dl":["dr"]}, width_rate = wr)
system.min_width = min_width
system.element_templates
system.element_templates["p"] = Element(symbol = "p", position = Position(0.0, 0.94, 0.0), rotation = Position(p1,p2,p3))
system.element_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, a1))
system.element_templates["al"] = Element(symbol = "al", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, 360-a1))
system.element_templates["br"] = Element(symbol = "br", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,50.0))
system.element_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,360-50.0))
system.element_templates["cr"] = Element(symbol = "cr", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,360.0-25.0))
system.element_templates["cl"] = Element(symbol = "cl", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,25.0))
system.element_templates["dr"] = Element(symbol = "dr", position = Position(0.0, r3, 0.0), rotation = Position(15.0,0.0,0.0))
system.element_templates["dl"] = Element(symbol = "dl", position = Position(0.0, r3, 0.0), rotation = Position(360.0-15.0,0.0,0.0))

system.nrOfNodes = 3505
system.width_scale = 0.07
add_system(system)

    

#
#01
#
element_id = 1
r1 = 0.93
r2 = 0.92
r3 = 0.75
a1 = 150
a2 = 150
wr = 0.96
min_width = 0.003
system = System(id = 1, V = ["ar", "al", "p"], w = "p", P = {"p":["p", "al", "ar"],"ar": ["pb"], "al": ["pb"], "pb":["pb", "br", "bl"], "br":[], "bl":[]}, width_rate = wr)
system.min_width = min_width
system.element_templates["p"] = Element(symbol = "p", position = Position(0.0, 0.995, 0.0), rotation = Position(0.0,137.5,0.0))
system.element_templates["pb"] = Element(symbol = "pb", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,0.0))
system.element_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, a1))
system.element_templates["al"] = Element(symbol = "al", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, 360-a1))
system.element_templates["br"] = Element(symbol = "br", position = Position(0.0, r2, 0.0), rotation = Position(180.0,0.0, a1))
system.element_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r2, 0.0), rotation = Position(180.0,0.0, 360-a1))


system.nrOfNodes = 3400
system.width_scale = 0.09

add_system(system)

##02b
#
element_id = 1
r1 = 0.95
r2 = 0.9
a1 = 31.0
a2 = 3.0
p1 = 5.0
p2 = 110.0
p3 = 4.0
wr = 0.987
min_width = 0.003
system = System(id = 2, V = ["ar", "al", "p"], w = "p", P = {"p":["pp"], "pp":["p","ppp"], "ppp":["ppp", "al", "ar"],"ar": ["b"], "al": ["b"], "b":["ar", "al"]}, width_rate = wr)
system.min_width = min_width

system.element_templates["p"] = Element(symbol = "p", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
system.element_templates["pp"] = Element(symbol = "pp", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
system.element_templates["ppp"] = Element(symbol = "ppp", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
system.element_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r2, 0.0), rotation = Position(a2,0.0,a1 ))
system.element_templates["al"] = Element(symbol = "al", position = Position(0.0, r2, 0.0), rotation = Position(-a2,0.0,-a1))
system.element_templates["b"] = Element(symbol = "b", position = Position(0.0, r2, 0.0), rotation = Position(-p1,0.0,p3))


system.nrOfNodes = 1202
system.width_scale = 0.07

add_system(system)


#03
#
element_id = 1
r1 = 0.77
r2 = 0.92
a1 = 41.0
a2 = 17.0
wr = 0.987
min_width = 0.003
system = System(id = 3, V = ["ar", "al", "p"], w = "p", P = {"p":["p", "al", "ar"],"ar": ["b", "al"], "al": ["b", "ar"], "b":["b", "ar", "al"]}, width_rate = wr)
system.min_width = min_width

system.element_templates["p"] = Element(symbol = "p", position = Position(0.0, r1, 0.0), rotation = Position(0.0,40.0,0.0))
system.element_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r2, 0.0), rotation = Position(0.0,2.0,a1 ))
system.element_templates["al"] = Element(symbol = "al", position = Position(0.0, r2, 0.0), rotation = Position(0.0,-2.0,-a1))
system.element_templates["b"] = Element(symbol = "b", position = Position(0.0, r1, 0.0), rotation = Position(1.0,8.0,1.0))


system.nrOfNodes = 1502
system.width_scale = 0.07

add_system(system)

##04

element_id = 1
r1 = 0.94
r2 = 0.92
r3 = 0.9
a1 = 150
a2 = 150
wr = 0.984
min_width = 0.0045
system = System(id = 4, V = ["ar", "al", "p"], w = "p", P = {"p":["p", "al", "ar"],"ar": ["pb"], "al": ["pa"], "pa":["pa", "br", "bl"], "pb":["pb", "br", "bl"], "br":[], "bl":[]}, width_rate = wr)
system.min_width = min_width
system.element_templates["p"] = Element(symbol = "p", position = Position(0.0, 0.999, 0.0), rotation = Position(0.0,137.5,0.0))
system.element_templates["pa"] = Element(symbol = "pa", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,-2.0))
system.element_templates["pb"] = Element(symbol = "pb", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,2.0))
system.element_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, a1))
system.element_templates["al"] = Element(symbol = "al", position = Position(0.0, r1, 0.0), rotation = Position(180.0,0.0, 360-a1))
system.element_templates["br"] = Element(symbol = "br", position = Position(0.0, r3, 0.0), rotation = Position(180.0,0.0, a1))
system.element_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r3, 0.0), rotation = Position(180.0,0.0, 360-a1))


system.nrOfNodes = 3700
system.width_scale = 0.09

add_system(system)


#05

element_id = 1
r1 = 0.984
r2 = 0.999
r3 = 0.91
r4 = 0.99
a1 = 150
a2 = 88
a3 = 4
wr = 0.98
min_width = 0.003
system = System(id = 5, V = ["ar", "al", "p"], w = "p", P = {"p":["ppp"], "ppp":["pppp"], "pppp":["ppppp"], "ppppp":["pp"], "pp":["pp", "ar", "al"],"ar":["br"], "al":["bl"], "br":["cr"], "bl":["cl"], "cr":["cr", "dr"], "cl":["cl", "dl"], "dr":["b"], "dl": ["b"], "b":[]}, width_rate = wr)
system.min_width = min_width
system.element_templates["p"] = Element(symbol = "p", position = Position(0.0, r4, 0.0), rotation = Position(0.0,0.0,0.0))
system.element_templates["ppp"] = Element(symbol = "ppp", position = Position(0.0, r4, 0.0), rotation = Position(0.0,0.0,0.0))
system.element_templates["pppp"] = Element(symbol = "pppp", position = Position(0.0, r4, 0.0), rotation = Position(0.0,0.0,0.0))
system.element_templates["ppppp"] = Element(symbol = "ppppp", position = Position(0.0, r4, 0.0), rotation = Position(0.0,0.0,0.0))
system.element_templates["pp"] = Element(symbol = "pp", position = Position(0.0, r1, 0.0), rotation = Position(0.0,137.5,0.0))
system.element_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r2, 0.0), rotation = Position(180.0,0.0, a1))
system.element_templates["al"] = Element(symbol = "al", position = Position(0.0, r2, 0.0), rotation = Position(180.0,0.0, -a1))
system.element_templates["br"] = Element(symbol = "br", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, -a2))
system.element_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, a2))
system.element_templates["cr"] = Element(symbol = "cr", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, -a3))
system.element_templates["cl"] = Element(symbol = "cl", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, a3))
system.element_templates["dr"] = Element(symbol = "dr", position = Position(0.0, r1, 0.0), rotation = Position(0.0,0.0, -a3*3))
system.element_templates["dl"] = Element(symbol = "dl", position = Position(0.0, r1, 0.0), rotation = Position(0.0,0.0, a3*3))
system.element_templates["b"] = Element(symbol = "b", position = Position(0.0, r3, 0.0), rotation = Position(0.0,0.0, 1.0))




system.nrOfNodes = 850
system.width_scale = 0.05

add_system(system)


##06

element_id = 1
r1 = 0.92
r2 = 0.99
a1 = 31.0
a2 = 20.0
p1 = 40.0
p2 = 110.0
p3 = 15.0
wr = 0.93
min_width = 0.0005
system = System(id = 6, V = ["ar", "al", "p"], w = "p", P = {"p":["p", "al", "ar"],"ar": ["b", "al"], "al": ["b", "ar"], "b":["p", "ar", "al"]}, width_rate = wr)
system.min_width = min_width

system.element_templates["p"] = Element(symbol = "p", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
system.element_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r2, 0.0), rotation = Position(a2,0.0,a1 ))
system.element_templates["al"] = Element(symbol = "al", position = Position(0.0, r2, 0.0), rotation = Position(-a2,0.0,-a1))
system.element_templates["b"] = Element(symbol = "b", position = Position(0.0, r1, 0.0), rotation = Position(-p1,p2,p3))


system.nrOfNodes = 802
system.width_scale = 0.10

add_system(system)



##07

element_id = 1
r1 = 0.99
r2 = 0.89
a1 = 71.0
a2 = 3.0
b1 = 9.0
b2 = 15.0
p1 = 4.0
p2 = 100.0
p3 = 3.0
wr = 0.95
min_width = 0.003
system = System(id = 7, V = ["ar", "al", "p"], w = "p", P = {"p":["pp"], "pp":["ppp"], "ppp":["p", "al", "ar"],"ar": ["b"], "al": ["b"], "b":["br", "bl"], "br":["bb"], "bl":["br"], "bb":["b"]}, width_rate = wr)
system.min_width = min_width

system.element_templates["p"] = Element(symbol = "p", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
system.element_templates["pp"] = Element(symbol = "pp", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
system.element_templates["ppp"] = Element(symbol = "ppp", position = Position(0.0, r1, 0.0), rotation = Position(p1,p2,p3))
system.element_templates["ar"] = Element(symbol = "ar", position = Position(0.0, r2, 0.0), rotation = Position(a2,0.0,a1))
system.element_templates["al"] = Element(symbol = "al", position = Position(0.0, r2, 0.0), rotation = Position(-a2,0.0-a1))
system.element_templates["br"] = Element(symbol = "br", position = Position(0.0, r2, 0.0), rotation = Position(b2,0.0,b1))
system.element_templates["bl"] = Element(symbol = "bl", position = Position(0.0, r2, 0.0), rotation = Position(-b2,0.0,-b1))
system.element_templates["b"] = Element(symbol = "b", position = Position(0.0, r2, 0.0), rotation = Position(-p1,0.0,p3))
system.element_templates["bb"] = Element(symbol = "bb", position = Position(0.0, r2, 0.0), rotation = Position(0.0,0.0,0.0))


system.nrOfNodes = 700
system.width_scale = 0.18

add_system(system)


##########################################################################################################################################
###############################################      ---         SETTINGS         ---      ###############################################
##########################################################################################################################################


##########################################################################################################################################
###############################################      ---  PREPARE FOR EXPORTING   ---      ###############################################
##########################################################################################################################################

#scene = canvas(x=0, y=0, width=2048, height=2048, background=vector(0, 0, 0))
#scene.center = vector(1.0, 0.0, 1.0)
#scene.select()

def scene_clear(sc):
    for obj in sc.objects:
        obj.visible = False
    for obj in sc.objects:
        del obj

try:
    os.system("killall Finder")
    time.sleep(3)
except:
    print("")
jj = 0
timeStart = time.time()
if not continue_task:
    try:
        CSVfile = open(SAVE_PATH+"desc.csv", "r")
        ll = ""
        for l in CSVfile:
            ll = l

        jj = int(float(ll.split("_")[0]))
        last_batch_id = int(jj/8)
        NR_OF_BATCHES_NOW += last_batch_id
        jj = 8*last_batch_id
        print("starting from: ", last_batch_id)
        CSVfile.close()
    except:
        CSVfile = open(SAVE_PATH+"desc.csv", "w+")
        system = SystemAll(system = systems_array_simple[0])
        scene = canvas(x=0, y=0, width=2048, height=2048, background=COLOR_BACKGROUND)
        system.P = all_dictionary.copy()

        for key in systems_array_simple[0].P:
#            print(key+": "+str(system_load.P[key]), end=", ")
            for ii in range(0,100):
                if key+"."+str(ii) in system.P:
                    if systems_array_simple[0].id in system.P[key+"."+str(ii)][2]:
                        system.P[key+"."+str(ii)] = (95, system.P[key+"."+str(ii)][1], system.P[key+"."+str(ii)][2])
                else:
                    break
            if key == 'p':
                system.p1 = systems_array_simple[0].element_templates[key].rotation.x
                system.p2 = systems_array_simple[0].element_templates[key].rotation.y
                system.p3 = systems_array_simple[0].element_templates[key].rotation.z
            else:
                system.a.update(systems_array_simple[0].element_templates[key].a())
            system.r.update(systems_array_simple[0].element_templates[key].r())
        system.refresh()
        system.render(scene)
        CSVheader = system.header()
        CSVfile.write(CSVheader)
        CSVfile.close()
        scene.delete()
        del scene
CSVfile = open(SAVE_PATH+"desc.csv", "a+")
NR_OF_BATCHES_NOW = min(NR_OF_BATCHES_NOW, NR_OF_BATCHES)
for batch_id in range(last_batch_id, NR_OF_BATCHES_NOW):
    if last_batch_id > batch_id:
        continue
    for system_load in systems_array_simple:
#        scene_clear(scene)
#        scene_clear(scene)
        scene = canvas(x=0, y=0, width=2048, height=2048, background=COLOR_BACKGROUND)
        timeChange = time.time()-timeStart
        timeAvg = timeChange/(1.0+(batch_id-last_batch_id))
        scene.caption = "<br> <p>"+str("%6.2f" % (batch_id*100.0/NR_OF_BATCHES_NOW))+"%\t\ttime: "+ str("%8.2f" % (timeChange/60.0))+"m\t\tfor batch:"+ str("%6.2f" % (timeAvg))+ "s\t\ttime 1000: "+ str("%6.2f" % (timeAvg*1000.0/3600.0))+ "h\t\t"+ "time left: "+ str("%8.2f m\t\t" % (timeAvg*(NR_OF_BATCHES_NOW-batch_id)/60.0))+str("""<br>
        <style>
        #batch[value]::-webkit-progress-bar
        {
            background-color: #eee;
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25) inset;
        }
        #batch[value]::-webkit-progress-value {
            background-color: #4e4;
            border-radius: 4px;
        }
        #all[value]::-webkit-progress-bar
        {
            background-color: #eee;
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25) inset;
        }
        #all[value]::-webkit-progress-value {
            background-color: #e44;
            border-radius: 4px;
        }
        </style><br><progress id="batch" value="0"""+str(((batch_id-last_batch_id)*100.0/(NR_OF_BATCHES_NOW-last_batch_id)))+"""0" max="100.0" style="width:90%;-webkit-appearance: none;appearance: none;" title="batch"> """+str(((batch_id-last_batch_id)*100.0/(NR_OF_BATCHES_NOW-last_batch_id)))+"""% </progress> Batch\t\t""")+str("""<br><progress id="all" value="0"""+str(((batch_id)*100.0/(NR_OF_BATCHES)))+"""0" max="100.0" style="width:90%;-webkit-appearance: none;appearance: none;" title="all"> """+str((batch_id*100.0/NR_OF_BATCHES))+"""% </progress> All\t\t""")
        scene.exit = 0
        autoscale = False
        scene.center = vector(0.0, 5.0, 0.0)
        scene.camera.pos = vector(-12.0079, 2.1538, -0.307841)
        scene.camera.axis = vector(20.8079, 5.98597, 0.607841)
        if system_load.id == 5:
            scene.camera.pos = vector(-24.0079, 4.1538, -0.607841)
        if system_load.id == 1:
            scene.camera.pos = vector(-26.0079, 4.5538, -0.607841)
        if system_load.id == 4:
            scene.camera.pos = vector(-26.0079, 4.5538, -0.607841)
            
        scene.select()
        
        system = None
        system = SystemAll(system = system_load)
        system.P = all_dictionary.copy()

        for key in system_load.P:
#            print(key+": "+str(system_load.P[key]), end=", ")
            for ii in range(0,100):
                if key+"."+str(ii) in system.P:
                    if system_load.id in system.P[key+"."+str(ii)][2]:
                        system.P[key+"."+str(ii)] = (95, system.P[key+"."+str(ii)][1], system.P[key+"."+str(ii)][2])
                else:
                    break
            if key == 'p':
                system.p1 = system_load.element_templates[key].rotation.x
                system.p2 = system_load.element_templates[key].rotation.y
                system.p3 = system_load.element_templates[key].rotation.z
            else:
                system.a.update(system_load.element_templates[key].a())
            system.r.update(system_load.element_templates[key].r())
#        print("")
#        for key in system.P:
#            if int(system.P[key][0]) > 80:
#                print(key+': '+str(system.P[key][1])+" "+str(system.P[key][0])+', ', end=" ")
        system.random()
        system.refresh()

        name = str("%04d_" % (jj)) + species[system.id]
        system.render(scene)
        CSVfile.write(name+", "+species[system.id]+", "+str(system))
        file_json = open(SAVE_PATH+name+".json", "w+")
        file_json.write(system.json)
        file_json.close()
        time.sleep(0.3)
        scene.capture("LSystemphoto"+name)
        scene.caption = ""
        scene.caption = None
#        input("Press Enter to continue...")
        del system
        jj += 1
        if jj % 500 == 499:
            try:
                os.system("killall Finder")
                time.sleep(1)
                gc.collect()
            except:
                print("")

        if jj % 10 == 9:
            scene.caption = "<script>sessionStorage.clear()</script>";
#            time.sleep(1)
#        scene.wrapper.delete()
        scene.delete()
        del scene
#        if jj % 10 == 9:
#            time.sleep(15)
            
    timeChange = time.time()-timeStart
    timeAvg = timeChange/(1.0+(batch_id-last_batch_id))
    print(str("%6.2f" % (batch_id*100.0/NR_OF_BATCHES_NOW))+"%\t\ttime: ", str("%8.2f" % (timeChange/60.0)), "m\t\tfor batch:", str("%6.2f" % (timeAvg)), "s\t\ttime 1000:", str("%6.2f" % (timeAvg*1000.0/3600.0)), "h\t\t", "time left: ", str("%8.2f m\t\t" % (timeAvg*(NR_OF_BATCHES_NOW-batch_id)/60.0)), "["+'{:<50}'.format(('{:|<'+str(int(batch_id*50.0/NR_OF_BATCHES)+0)+'}').format(''))+"]\t\t")
#    tracker.print_diff()

CSVfile.close()
try:
    os.system("killall Finder")
    time.sleep(3)
except:
    print("")
##########################################################################################################################################
###############################################      ---  PREPARE FOR EXPORTING   ---      ###############################################
##########################################################################################################################################

exit()

