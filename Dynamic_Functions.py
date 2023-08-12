import os
import pandas as pd
import numpy as np
import tqdm
class Heated_Voroni():
    def __init__(self,Z=[],H=[]):
        self.Z = Z
        self.heated_points(H)
    # Z - an array of x,y coordinates
    # H - an array of Heat Values
    # Returns a lambda function which takes input p, a point(x,y), and returns an index for the closest element in Z.
    def heated_points(self,H=[]):
        M = []
        for i,z_i in enumerate(self.Z):
            M_row = []
            for z_j in self.Z:
                if abs(z_i[0]-z_j[0])+abs(z_i[1]-z_j[1])>0:
                    M_row.append(H[i]*((z_i[0]+z_j[0])/2+(z_i[1]+z_j[1])/2))
                else:
                    M_row.append(np.inf)
            M.append(M_row)
        self.hot_points = M
    def find_hottest_point(self,p):
        if p is not np.inf:
            x = np.real(p)
            y = np.imag(p)
            heated_voroni_distance_array = [
                ([abs(abs(x - self.Z[i][0]) + abs(y - self.Z[i][1]) - boundary_distance) for j, boundary_distance in enumerate(row)])
                for i, row in enumerate(self.hot_points)]
            flatten_heated_voroni_array = list(np.array(heated_voroni_distance_array).flatten())
            hottest_point = np.min(heated_voroni_distance_array)
            #print(hottest_point)
            hottest_point_location = int(flatten_heated_voroni_array.index(hottest_point)/len(self.Z))
            return hottest_point_location
        else:
            return 0

class dFunc():
    def __init__(self,function_id=''):
        functions_df = pd.read_csv(f'functions/{function_id}.csv')
        functions = functions_df['functions'].tolist()
        coordinates = [eval(coord) for coord in functions_df['coordinates'].tolist()]
        #print(coordinates)
        #heats = functions_df['Heat'].tolist()
        #self.boundary_diagram = Heated_Voroni(coordinates,heats)
        self.lambda_functions = [eval(f'lambda z,c:{function}') for function in functions]
        #self.dLambda = lambda z,c: self.lambda_functions[self.boundary_diagram.find_hottest_point(p=z)](z,c)
        self.dLambda = lambda z,c: self.lambda_functions[self.closest_node(node=[np.real(z),np.imag(z)],nodes=coordinates)](z,c)
    def closest_node(self, node, nodes):
        nodes = np.asarray(nodes)
        deltas = nodes - node
        dist_2 = np.einsum('ij,ij->i', deltas, deltas)
        return np.argmin(dist_2)


