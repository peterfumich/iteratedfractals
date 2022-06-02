import numpy as np
from PIL import Image
#from mpmath import *
from numba import jit, prange
import time

scale = 4
scaling = int(scale*256)
width = scaling
height = scaling

escape_radius = 2#2
#@jit
def build_frame(x_0, y_0, zoom,extra_precision):
    x_values = []
    y_values = []
    z_values = []
    for s in range(scaling):
        x_values.append(x_0 + 4 * np.float128(zoom) * int(s - scaling / 2) / scaling)
        y_values.append(y_0 + 4 * np.float128(zoom) * int(s - scaling / 2) / scaling)
    for y in y_values:
        for x in x_values:
            z_values.append(x + y * 1j)
    # return (x_values, y_values,z_values)
    print([x_values[0], x_values[-1]])
    print([y_values[0], y_values[-1]])
    return (z_values)

def build_palette(palette_length,initial_color,final_color):
    delta=[]
    for i in range(3):
        delta.append(int((final_color[i]-initial_color[i])/palette_length))
    new_palette = np.zeros((palette_length+1, 3), dtype=np.uint8)
    new_palette[0]=initial_color
    for p in range(palette_length-1):
        new_palette[p+1]=np.add(new_palette[p],delta)
    new_palette[-1] = final_color
    #print("palette =", new_palette)
    return(new_palette)

palette_length = int(15)
def random_color():
    rand_color =  []
    for i in range(3):
        rand_color.append(np.random.randint(0,255))
    return(rand_color)
color_1 = random_color()#[200,00,0]#random_color()
color_3 = random_color()#[55,55,55]#random_color()
color_2 = random_color()#[55,155,155]#random_color()
print(color_1,color_2,color_3)
palette = np.append(np.append(build_palette(3,[0,0,0],color_1),build_palette(5,color_1,color_2),axis = 0),build_palette(7,color_2,color_3),axis = 0)
#palette = np.append(build_palette(int(palette_length/3),[0,0,0],[55,160,50]),build_palette(int(2*palette_length/3),[0,0,0],[0,255,200]),axis=0)
print("Palette Built",palette)
def mobius_transformation_of_frame(initial_array,a,b,aa,bb):
    print("Beginning Mobius Transofrmation of the complex plane")
    #mobius_array = np.zeros((width,height),dtype=np.complex)
    mobius_array = []
    for z in initial_array:
        mobius_array.append(z*np.e**(1j*abs(z)*.4))
        #mobius_array.append((a * z + b) / (aa * z + bb))
    print("Mobius Transoformation of the complex plane Complete ")
    return(mobius_array)
# @jit
def function(z,c):
    #f = (abs(z.real) + 1j * abs(z.imag)) ** 2 + c
    #f = (z**(4)+c)/(np.conj(c)*z+1j)
    #u = (a*z+b)/(aa*z+bb)
    #f = u**2+(a*c+b)/(aa*c+bb)
    #f = (np.sin(z**(2+b/15))-np.cos(z**(2+b/15)))+c
    #f= np.sin(z**(a/15))+c
    #f = z**(2*a/15)+c
    #f = (z**2+c)
    #f = (1)/(2j*g+.25)
    #f = np.sin(z**4+c)**3
    f = np.sin(z**4+c)**c
    #f = z**3/(z+c)+c
    return(f)

def Fractal_Recursion(iterations, complex_values, method):
    converging_list = np.zeros((height * width, 1), dtype=np.uint8)
    # converging_list = matrix(height*width,1)
    # converging_list = []
    for n, z in enumerate(complex_values):
        Z = 0  # this initial setting can be changed
        for i in range(iterations):
            try:
                # print(Z)
                Z = function(Z, z)

            except:
                # converging_measurement = i
                converging_list[n] = i
                # converging_list.append(i)
                break
            if abs(Z) > escape_radius:
                converging_list[n] = i
                # converging_list.append(i)
                # converging_measurement = i
                break

        # converging_list.append(converging_measurement)
    print("Recursion is complete on the set of complex values")
    return (converging_list)

def Build_Picture(recursive_values,method,n, initial_k):#initial_k is used for multi-processing(e.g running the zoom and having a zoom for the even numbered frames and a zoom for the odd numbered frames and then interlace when creating the video)

    #identifier = np.random.randint(10000, 99999)
    #print("Building the picture:",identifier," is the identifier")
    picture = []
    for value in recursive_values:
        picture.append(palette[value % palette_length])
    picture_output = np.reshape(picture, (width, height, 3))
    # print(picture_output)
    img = Image.fromarray(picture_output, 'RGB')

    # img.save(str(n)+"funky mandelbrot sin"+str(identifier)+'.png')
    #img.save(str(n) + "_" + str(int(10*(.8-initial_k))) + ".png")#to zoom out
    img.save('gtest3'+str(n) + "_" + str(initial_k) + ".png")#to zoom in

def fractal_zoom(number_of_frames, initial_k):
    # #For mobius transformation of original array
    a = 1j
    b = -1
    aa = 1j
    bb = 1
    print('Starting initial k = '+str(initial_k))
    delta = .8
    initial_iterations = 100
    final_iterations = 2500
    iteration_change = int((final_iterations - initial_iterations)/number_of_frames)
    iterations = int(initial_iterations)# * initial_k*10*iteration_change)#10 because step size is .1
    initial_center = [0,0]
    k = initial_k-1.6#-3*delta
    zoom = 1/np.exp(k)
    extra_precision = 0
    #complex_array = build_frame(initial_center[0],initial_center[1],zoom,extra_precision)
    complex_array = mobius_transformation_of_frame(build_frame(initial_center[0],initial_center[1],zoom,extra_precision),a,b,aa,bb)
    for n in range(number_of_frames):
        print(n,"out of",number_of_frames)
        Build_Picture(Fractal_Recursion(iterations,complex_array,0),0,n,initial_k)
        k += delta
        zoom = 1/np.exp(k)
        iterations+=iteration_change
        #complex_array = build_frame(initial_center[0], initial_center[1], zoom, extra_precision)
        complex_array = mobius_transformation_of_frame(build_frame(initial_center[0],initial_center[1],zoom,extra_precision),a,b,aa,bb)