import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    #normalizing
    normal = normalize(normal)
    light[LOCATION] = normalize(light[LOCATION])
    view = normalize(view)
    
    length = len(normal)

    ambientC = calculate_ambient(ambient, areflect)
    diffuseC = calculate_diffuse(light, dreflect, normal)
    specularC = calculate_specular(light, sreflect, view, normal)
    
    return limit_color([ambientC[i]+diffuseC[i]+specularC[i] for i in range(length)])    

def calculate_ambient(alight, areflect):
    length = len(alight)
    retVal = []
    for i in range(length):
        retVal.append(int(alight[i]*areflect[i]))
    return retVal

def calculate_diffuse(light, dreflect, normal):
    length = len(light[COLOR])
    retVal = []
    for i in range(length):
        if dot_product(normal, light[LOCATION]):
            retVal.append(int(light[COLOR][i]*dreflect[i]*dot_product(normal,light[LOCATION])))
        else:
            retVal = [0,0,0]
            return retVal
    return retVal

def calculate_specular(light, sreflect, view, normal):
    length = len(normal)
    retVal = []
    r = []
    if dot_product(normal, light[LOCATION]) > 0:
        mult = dot_product(normal, light[LOCATION])
        mult *= 2
        for coord in range(length):
            r.append(mult*normal[coord]-light[LOCATION][coord])
        cosA = dot_product(r, view)**SPECULAR_EXP
        for coord in range(length):
            retVal.append(int(light[COLOR][coord]*sreflect[coord]*cosA))
        return retVal        
    else:
        return [0,0,0]

def limit_color(color):    
    length = len(color)
    for col in range(length):
        if color[col] > 255:
            color[col] = 255
        elif color[col] < 0:
            color[col] = 0
    return color

#vector functions
def normalize(vector):
    norm = (vector[0]**2 + vector[1]**2 + vector[2]**2) **0.5
    return [each/norm for each in vector]

def dot_product(a, b):
    length = len(a)
    return sum([a[i]*b[i] for i in range(length)])

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
