import numpy as np
import matplotlib
matplotlib.use('TkAgg')          
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import warnings
warnings.filterwarnings('ignore')


def make_box(cx=0, cy=0, cz=0, w=2, h=2, d=2):
    x0,y0,z0 = cx-w/2, cy-h/2, cz-d/2
    x1,y1,z1 = cx+w/2, cy+h/2, cz+d/2
    verts = np.array([
        [x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],   # bottom ring
        [x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1],   # top ring
    ], dtype=float)
    faces = [
        [0,1,2,3],[4,5,6,7],   # bottom, top caps
        [0,1,5,4],[2,3,7,6],   # front, back walls
        [1,2,6,5],[0,3,7,4],   # right, left walls
    ]
    return {'verts': verts, 'faces': faces, 'label': 'Box'}


def make_cylinder(cx=0, cy=0, cz=0, r=1.0, h=2.0, n=32):
    angles  = np.linspace(0, 2*np.pi, n, endpoint=False)
    bot_z, top_z = cz - h/2, cz + h/2
 
    bot_ring = np.column_stack([cx + r*np.cos(angles),
                                cy + r*np.sin(angles),
                                np.full(n, bot_z)])
    top_ring = np.column_stack([cx + r*np.cos(angles),
                                cy + r*np.sin(angles),
                                np.full(n, top_z)])
    bot_ctr  = np.array([[cx, cy, bot_z]])
    top_ctr  = np.array([[cx, cy, top_z]])
 
    verts = np.vstack([bot_ring, top_ring, bot_ctr, top_ctr])
    bc, tc = 2*n, 2*n+1   # center vertex indices
 
    faces = []
    for i in range(n):
        j = (i+1) % n
        faces.append([i, j, j+n, i+n])    # lateral quad
        faces.append([bc, j, i])           # bottom triangle
        faces.append([tc, i+n, j+n])       # top triangle
 
    return {'verts': verts, 'faces': faces, 'label': 'Cylinder'}