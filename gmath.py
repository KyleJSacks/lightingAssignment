import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(view)
    a = calculate_ambient(ambient, areflect)
    d = calculate_diffuse(light, dreflect, normal)
    s = calculate_specular(light, sreflect, view, normal)
    r = a[0] + d[0] + s[0]
    g = a[1] + d[1] + s[1]
    b = a[2] + d[2] + s[2]
    c = [math.ceil(r), math.ceil(g), math.ceil(b)]
    limit_color(c)
    return c

def calculate_ambient(alight, areflect):
    if len(alight) == 1:
        alight = [alight[0], alight[0], alight[0]]
    r = alight[0] * areflect[0]
    g = alight[1] * areflect[1]
    b = alight[2] * areflect[2]
    return [r, g, b]

def calculate_diffuse(light, dreflect, normal):
    lv = light[0]
    normalize(lv)
    r = light[1][0] * dreflect[0] * dot_product(normal, lv)
    g = light[1][1] * dreflect[1] * dot_product(normal, lv)
    b = light[1][2] * dreflect[2] * dot_product(normal, lv)
    return [r, g, b]
    
def calculate_specular(light, sreflect, view, normal):
    lv = light[0]
    normalize(lv)
    R = vector_subt(scal_vect(dot_product(normal, lv), (scal_vect(2, normal))), lv)
    r = light[1][0] * sreflect[0] * (dot_product(R, view) ** 8)
    g = light[1][1] * sreflect[1] * (dot_product(R, view) ** 8)
    b = light[1][2] * sreflect[2] * (dot_product(R, view) ** 8)
    return [r, g, b]

def limit_color(color):
    for i in range(len(color)):
        if color[i] > 255:
            color[i] = 255
        elif color[i] < 0:
            color[i] = 0

def scal_vect(scalar, vector):
    ans = []
    for c in vector:
        ans.append(scalar * c)
    return ans

def vector_subt(v0, v1):
    ans = []
    for i in range(len(v0)):
        ans.append(v0[i] - v1[i])
    return ans
    
#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
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
