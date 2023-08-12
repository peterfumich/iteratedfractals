import numpy as np
import pandas as pd
from PIL import Image
Image.MAX_IMAGE_PIXELS =int(1073741824*2)
from tqdm import tqdm
escape_radius = 1.5
import Palette
from Dynamic_Functions import Heated_Voroni,dFunc
def build_frame(x_0, y_0, zoom,scaling):
    x_values = []
    y_values = []
    z_values = []
    for s in tqdm(range(scaling)):
        x_values.append(x_0 + 4 * np.longdouble(zoom) * int(s - scaling / 2) / scaling)
        y_values.append(y_0 + 4 * np.longdouble(zoom) * int(s - scaling / 2) / scaling)
    for y in tqdm(y_values):
        for x in x_values:
            z_values.append(np.clongdouble(x + y * 1j))
    return (z_values)
def Transform(initial_array,transform):
    array = []
    transform = eval(f'lambda z: {transform}')
    for z in tqdm(initial_array):
        array.append(transform(z))
    print("Transoformation of the complex plane Complete ")
    return(array)

def Render(function,transform, color_transform, center_x,center_y,scale,zoom,colors,color_lengths,folder,name,color_variation_scalars,frame_index,method):
    scale = int(256*scale)
    frame = build_frame(center_x,center_y,zoom,scale)
    transformed_frame = Transform(frame,transform)
    iterated_frame = Fractal_Recursion(function,color_transform, 200,transformed_frame,scale,color_variation_scalars)
    Build_Picture(iterated_frame,scaling=scale,colors=colors,color_lengths=color_lengths,folder=folder,name=f'{name}'.replace('/','over'),frame_index=frame_index,method=method)

def build_palette(palette_length,initial_color,final_color):
    delta=[]
    final_color = final_color
    initial_color = initial_color
    palette_length = palette_length
    for i in range(4):
        delta.append(int((final_color[i]-initial_color[i])/palette_length))
    new_palette = np.zeros((palette_length+1, 4), dtype=np.uint8)
    new_palette[0]=initial_color
    for p in range(palette_length):
        new_palette[p+1]=np.add(new_palette[p],delta)
    new_palette[-1] = final_color
    return(new_palette)

def random_color():
    rand_color =  []
    for i in range(4):
        rand_color.append(np.random.randint(0,100))
    return(rand_color)



def Fractal_Recursion(function,color_transform, iterations, complex_values, scaling,color_variation_scalars):
    converging_list = np.zeros((scaling * scaling, 1), dtype=np.uint8)
    if '.csv' in function:
        dynamic_function = dFunc(function.replace('.csv',''))
        color_func = eval(f'lambda z,c,i: {color_transform}')
        for n, c in enumerate(tqdm(complex_values)):
            z = 0
            for i in range(iterations):
                try:
                    z = dynamic_function.dLambda(z, c)
                except:
                    converging_list[n] = i + color_func(z, c, i)
                    break
                if abs(z) > escape_radius:
                    converging_list[n] = i + color_func(z, c, i)
                    break
        print("Recursion is complete on the set of complex values")
        return (converging_list)
    else:
        func = eval(f'lambda z,c: {function}')
        color_func = eval(f'lambda z,c,i: {color_transform}')
        for n, c in enumerate(tqdm(complex_values)):
            z = 0
            for i in range(iterations):
                try:
                    z = func(z,c)#eval(function)
                except:
                    converging_list[n] = i+color_func(z,c,i)#+color_variation_scalars[1]*np.log2(abs(np.abs(c)-np.abs(z)))+color_variation_scalars[0]*2*(np.angle(c)-np.angle(z))#int(color_variation_scalars[1]*np.log2(abs(np.abs(c)-np.abs(z)))+color_variation_scalars[0]*2*(np.angle(c)-np.angle(z)))
                    break
                if abs(z) > escape_radius:
                    converging_list[n] = i+color_func(z,c,i)#+color_variation_scalars[1]*np.log2(abs(np.abs(c)-np.abs(z)))+color_variation_scalars[0]*2*(np.angle(c)-np.angle(z))#int(color_variation_scalars[1]*np.log2(abs(np.abs(c)-np.abs(z)))+color_variation_scalars[0]*2*(np.angle(c)-np.angle(z)))
                    break
        print("Recursion is complete on the set of complex values")
        return (converging_list)

def Build_Picture(recursive_values,scaling,colors,color_lengths,folder,name,frame_index,method):
    picture = []
    #method = False
    color_lengths = eval(color_lengths)
    colors = eval(colors)
    if method:
        palette_length = len(colors)
        for length in color_lengths:
            palette_length+=int(length)
        palette = build_palette(color_lengths[0], [100, 100, 100, 250], colors[0])
        for i in range(len(colors)-1):
            palette = np.append(palette,build_palette(color_lengths[i+1],colors[i],colors[i+1]),axis=0)
        for value in recursive_values:
            picture.append(palette[value % palette_length])
        picture_output = np.reshape(picture, (scaling, scaling, 4))
        img = Image.fromarray(picture_output, mode = 'CMYK')
    else:
        palette = Palette.get_palette('bun')
        #flip each photo by frame_index 0 nothing, 1 horizontal, 2 vertical, 3 both
        img_lengths = []
        palette_length = len(palette)
        color_type=len(palette[0][0])
        if color_type==3:
            cmode = 'RGB'
        elif color_type==4:
            cmode='CMYK'
        #new_palette = []#[np.zeros((scaling * scaling,color_type))]
        for img in palette:
            img_lengths.append(len(img))
            #new_palette.append(img[0:int(scaling/2)][0:int(scaling/2)])
        #palette = new_palette

        for n,value in enumerate(recursive_values):
            picture.append(palette[value[0] % palette_length][n%img_lengths[value[0] % palette_length]])
        picture_output = np.reshape(picture, (scaling, scaling, color_type))
        img = Image.fromarray(picture_output, mode = cmode)
    #img = img.resize((scaling//2, scaling//2), Image.ANTIALIAS)
    file_name = f'{folder}/{name}.jpeg'
    print(f'writing {file_name}')
    img.save(file_name)
    return(recursive_values)

def Zip_Imgs(folder,name):

    from PIL import Image
    import cv2
    Image.MAX_IMAGE_PIXELS = 1000000000#603979776#178956970
    f1 = f"{folder}/pre_render_0.jpeg"
    f2 = f"{folder}/pre_render_1.jpeg"
    f3 = f"{folder}/pre_render_2.jpeg"
    f4 = f"{folder}/pre_render_3.jpeg"
    im = cv2.imread(f1)
    size = im.shape[0]
    image1 = Image.open(f1)
    image2 = Image.open(f2)
    image3 = Image.open(f3)
    image4 = Image.open(f4)
    out_image = f"{folder}/{name}.jpeg"
    img = Image.new("CMYK", (int(2*size), int(2*size)), (0, 0, 0,0))
    img.save("blank.jpeg", "JPEG")
    blank_image = Image.open("blank.jpeg")

    blank_image.paste(image1, (0, 0))
    blank_image.paste(image2, (size, 0))
    blank_image.paste(image3, (0, size))
    blank_image.paste(image4,(size, size))
    blank_image.save(out_image)

def Parallel_Render(function,transform,color_transform,center_x,center_y,zoom,scale,colors,color_lengths,folder,color_variation_scalars,method,current_time):
    from functools import partial
    from itertools import repeat
    from multiprocessing import Pool, freeze_support
    frame_args = []
    number_frames = 4
    for frame in range(number_frames):
        frame_args.append((function, transform, color_transform, center_x - 2 * zoom * (-1) ** frame,
                           center_y - 2 * zoom * (-1) ** (int(frame / 2)), scale, zoom, colors, color_lengths, folder,
                           f"pre_render_{frame}",color_variation_scalars,frame,method))
    with Pool() as pool:
        L = pool.starmap(Render, frame_args)
    Zip_Imgs(folder, str(current_time))
#Zip_Imgs('/Users/peterfumich/Documents/Fractals', 'zipped')

#function,transform,center_x,center_y,zoom,scale,colors,color_lengths,folder,color_variation_scalars
if __name__ == '__main__':
    history = pd.read_csv('history.csv')
    data = history.iloc[-1]
    function = data['Function']
    transform = data['Transform']
    color_transform = data['Color Transformation']
    center_x = data['x']
    center_y = data['y']
    zoom = data['zoom']
    scale = data['scale']
    palette = data['palette']
    palette_lengths = data['palette lengths']
    path = data['path']
    color_var = data['color_var']
    method = data['method']
    current_time = data['Time']
    #read functions here
    Parallel_Render(function,
                    transform,
                    color_transform,
                    center_x,
                    center_y,
                    zoom,
                    scale,
                    palette,
                    palette_lengths,
                    '/Users/peterfumich/Documents/Fractals',
                    color_var,method,current_time)