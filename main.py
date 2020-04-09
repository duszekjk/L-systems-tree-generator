
from vpython import *
from vectors import Point, Vector


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
        self.position_calc= Position(0.0, 0.0, 0.0)
        self.axis_abs     = Position(0.0, 0.0, 0.0)
        
    def __str__(self):
        return self.symbol
    def set_from_root(self, d = 0):
        self.from_root = d
        for child in self.children:
            child.set_from_root(d+1)
    def calculate_position(self):
        sum_pos = (self.parent.position_calc.x+self.parent.position_calc.y+self.parent.position_calc.z)
#        if sum_pos > 0:
#            self.axis_abs.x = self.parent.position_calc.x/sum_pos
#            self.axis_abs.y = self.parent.position_calc.y/sum_pos
#            self.axis_abs.z = self.parent.position_calc.z/sum_pos
#            self.position_calc.x = self.position.x * self.axis_abs.x
#            self.position_calc.y = self.position.y * self.axis_abs.y
#            self.position_calc.z = self.position.z * self.axis_abs.z
#        else:
        self.position_calc.x = self.position.x
        self.position_calc.y = self.position.y
        self.position_calc.z = self.position.z
        print(self.position_calc.y)
        
            
    

system = System()
elements_templates = {}
elements_templates["ar"] = Element(symbol = "ar", position = Position(0.15, 0.7, 0.2), rotation = Position(0,0,0))
elements_templates["al"] = Element(symbol = "al", position = Position(0.05, 0.8, -0.45), rotation = Position(0,0,0))
elements_templates["br"] = Element(symbol = "br", position = Position(0.0, 0.9, 0.0), rotation = Position(0,0,0))
elements_templates["bl"] = Element(symbol = "bl", position = Position(-0.35, 0.5, 0.35), rotation = Position(0,0,0))

elements = []
element = Element(symbol = system.w)
elements.append(element)

for i in range(0, 20):
    new_row = system.next(elements[i].symbol)
    
    for new_element in new_row:
        element = Element(template = elements_templates[new_element], parent = elements[i])
        elements[i].children.append(element)
        elements.append(element)
elements[0].set_from_root()

for i in range(0, 20):
    print("")
    for element in elements:
        if element.from_root == i:
            print(element, "("+str(element.parent)+")", end="\t")

#sphere()
#scene = canvas(x=0, y=0, width=3200, height=2400, autocenter=True, background=vector(0, 0, 1))
#scene.select()
#

cylinder(pos = vector(0.0,0.0,0.0), axis = vector(elements[0].position.x, elements[0].position.y, elements[0].position.z), radius = 0.02, color=color.red)
elements[0].position_abs.x = 0.0 + elements[0].position.x
elements[0].position_abs.y = 0.0 + elements[0].position.y
elements[0].position_abs.z = 0.0 + elements[0].position.z
for element in elements[1:]:
    element.calculate_position()
    if element.symbol == "al":
        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = 0.02, color=color.green)
    elif element.symbol == "ar":
        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = 0.02, color=color.blue)
    else:
        cylinder(pos = vector(element.parent.position_abs.x, element.parent.position_abs.y, element.parent.position_abs.z), axis = vector(element.position_calc.x, element.position_calc.y, element.position_calc.z), radius = 0.02)
    element.position_abs.x = element.parent.position_abs.x + element.position_calc.x
    element.position_abs.y = element.parent.position_abs.y + element.position_calc.y
    element.position_abs.z = element.parent.position_abs.z + element.position_calc.z
