from Mandelbrot import fractal_zoom
import os
import multiprocessing
from functools import partial
import numpy as np
# processes = ("-c 'import Mandelbrot; Mandebrot.fractal_zoom(100,0)'", "-c 'import Mandelbrot; Mandebrot.fractal_zoom(100,.1)'",
#              "-c 'import Mandelbrot; Mandebrot.fractal_zoom(100,.2)'","-c 'import Mandelbrot; Mandebrot.fractal_zoom(100,0.4)'")

# processes = ("Mandebrot.fractal_zoom(100,0)", "Mandebrot.fractal_zoom(100,.1)",
#              "Mandebrot.fractal_zoom(100,.2)","Mandebrot.fractal_zoom(100,0.4)")
# def run_process(process):
#     os.system('python '.format(process))
#
#
# pool = Pool(processes=4)
# pool.map(run_process, processes)
def main():
    iterable = np.array([0.0])#np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])#np.array([0.0, 0.1, 0.2, 0.3])# 0.4, 0.5, 0.6, 0.7]#
    pool = multiprocessing.Pool()
    number_of_frames = 1
    func = partial(fractal_zoom, number_of_frames)
    pool.map(func, iterable)
    pool.close()
    pool.join()
if __name__ == "__main__":
    main()