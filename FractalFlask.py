import pandas as pd
import numpy as np
from flask import Flask, request,render_template
import string
import openai
import os
import shutil
import regex as re
import time
import datetime
from subprocess import PIPE, STDOUT,run
from functools import partial
from itertools import repeat
from multiprocessing import Pool, freeze_support
from iterative_fractals import *
app = Flask(__name__)
from subprocess import PIPE, STDOUT,run
def get_path():
    return os.path.join(os.path.expanduser('~'), 'Documents')
documents = get_path()
folder = f'{documents}/Fractals'
if not os.path.exists(folder):
    os.makedirs(folder)

function = 'z**2+c'
transform = 'z'
color_transform = '5*np.abs(np.angle(z))'
max_iterations = 100
center_x = 0
center_y = 0
scale = 1
dim = int(scale*256)
files = os.listdir(f'{folder}')
files = [f for f in files if (f != '.DS_Store')]
file_name = files[0]
display_size = 1024
zoom = 0
zoom_input = zoom
name = 'fractal'
number_colors = 4
colors = [[10,10,10,0],[0,0,0,100],[10,10,10,0],[0,0,0,100]]#np.random.randint(0,100,(number_colors,4))#[[100,0,0,0],[0,100,0,0],[0,0,100,0]]
color_lengths = [1,12,12,12]#np.random.randint(2,20,number_colors)#[10,10,10]
color_variation_scalars = [0,1]
coloring_method = False
palette_folder = 'test'
palette_scale = 1
@app.route('/', methods=['GET', 'POST'])
def writer():
    global function, transform, max_iterations, center_x, center_y, scale
    global files, file_name, display_size, zoom, name, zoom_input,colors,color_lengths,color_transform,coloring_method
    global palette_folder,palette_scale
    if request.method == 'POST':
        function = request.form['function']
        transform = request.form['transform']

        max_iterations = int(request.form['max_iterations_input'])

        center_x = float(request.form['center_x'])
        center_y = float(request.form['center_y'])
        scale = int(request.form['scale'])
        zoom_input = float(request.form['zoom_input'])

        zoom = 2**(-1*zoom_input)
        display_size = int(request.form['display_size'])
        button = request.form['action']
        name = request.form['name']
        #color_variation_scalars = [float(request.form['color_scalar_0']),float(request.form['color_scalar_1'])]
        color_transform = request.form['color_transform']
        coloring_method = request.form['coloring_method']
        palette_folder = request.form['palette_folder']
        palette_scale = float(request.form['palette_scale'])
        def Load():
            global files, file_name
            files = [file_name]
            new_files = os.listdir(f'{folder}')
            included_files = [f for f in new_files if (f != '.DS_Store' and f != file_name)]
            for f in included_files:
                files.append(f)
        def get_colors():
            color_1 = [eval(request.form['c1_0']),eval(request.form['c1_1']),eval(request.form['c1_2']),eval(request.form['c1_3'])]
            c1_length = int(request.form['c1_len'])
            color_2 = [eval(request.form['c2_0']),eval(request.form['c2_1']),eval(request.form['c2_2']),eval(request.form['c2_3'])]
            c2_length = int(request.form['c2_len'])
            color_3 = [eval(request.form['c3_0']),eval(request.form['c3_1']),eval(request.form['c3_2']),eval(request.form['c3_3'])]
            c3_length = int(request.form['c3_len'])
            color_4 = [eval(request.form['c4_0']),eval(request.form['c4_1']),eval(request.form['c4_2']),eval(request.form['c4_3'])]
            c4_length = int(request.form['c4_len'])

            return([color_1,color_2,color_3,color_4],[c1_length,c2_length,c3_length,c4_length])
        def render(render_type = 0,n=0):
            global zoom,zoom_input, colors, color_lengths,function,transform
            if render_type == 1:
                zoom_input+= .05
                zoom = 2 ** (-1 * zoom_input)
            if render_type == 2:
                transform = f'z**(1+{n}/100)'
            if render_type == 3:
                zoom_input += .05
                zoom = 2 ** (-1 * zoom_input)
                transform = f'z**(1+{n}/100)'
            colors, color_lengths = get_colors()
            t = time.localtime()
            current_time = datetime.datetime.today().strftime('%Y%m%d_%H_%M')
            function_history = pd.DataFrame([[current_time,transform,function,color_transform,center_x,center_y,zoom,scale,colors,color_lengths,folder,color_variation_scalars,coloring_method]],
                                            columns=['Time','Transform','Function','Color Transformation','x','y','zoom','scale','palette','palette lengths','path','color_var','method'])
            #function_history = pd.read_csv('history.csv')
            if os.path.exists('history.csv'):
                function_history.to_csv('history.csv',mode='a',index = False,header=False)
            else:
                function_history.to_csv('history.csv', mode='a', index=False, header=True)
            os.system('python3 iterative_fractals.py')
            # Parallel_Render(function, transform, center_x, center_y, zoom, scale, colors, color_lengths, folder)
            new_file_name = f'{current_time}.jpeg'
            return(new_file_name)
        if button == 'Load File':
            file_name = request.form['files']
            Load()
        elif button == 'Render':
            file_name = render()
        elif button == 'Delete File':
            file_name = request.form['files']
            os.remove(f'{folder}/{file_name}')
            files = []
            new_files = os.listdir(f'{folder}')
            included_files = [f for f in new_files if (f != '.DS_Store' and f != file_name)]
            for f in included_files:
                files.append(f)
            file_name = files[0]
        elif button == 'Rename':
            name = request.form['name']
            filed = request.form['files']
            os.rename(f'{folder}/{filed}', f'{folder}/{name}.jpeg')
            files = os.listdir(f'{folder}')
            files = [f for f in files if (f != '.DS_Store')]
            files.append(file_name)
            files = files[-1::]
            file_name = f'{name}.jpeg'
        elif button == 'Zoom Video':
            for n in range(500):
                file_name = render(render_type=1)
                file_path = f'{folder}/{file_name}'
                shutil.copyfile(file_path, f'video/{n}.jpeg')
        elif button == 'Function Video':
            for n in range(1000):
                file_name = render(render_type=2,n=n)
                file_path = f'{folder}/{file_name}'
                shutil.copyfile(file_path, f'video/{n}.jpeg')
        elif button == 'Zoom Transform Video':
            for n in range(500):
                file_name = render(render_type=3,n=n)
                file_path = f'{folder}/{file_name}'
                shutil.copyfile(file_path, f'video/{n}.jpeg')
    file_path = f'{folder}/{file_name}'
    shutil.copyfile(file_path, f'static/render.png')
    return render_template('home.html',function = function, transform = transform,
                           max_iterations = max_iterations, center_x = center_x,
                           center_y = center_y, scale=scale,files=files,file_name=file_name,display_size=display_size,
                           name=name,zoom=zoom_input,colors=colors,color_lengths=color_lengths,
                           color_transform=color_transform,coloring_method=coloring_method,
                           palette_folder=palette_folder,palette_scale=palette_scale)

if __name__ == '__main__':
    os.system('open -a Safari "http://127.0.0.1:5002"')
    app.run(port='5002')
