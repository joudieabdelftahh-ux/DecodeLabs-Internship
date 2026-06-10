import numpy as np
import matplotlib
matplotlib.use('TkAgg')          
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import warnings
warnings.filterwarnings('ignore')
from m_math import*

def extrude_profile(profile_2d, height=3.0):
    n      = len(profile_2d)
    bottom = [(x, y, 0.0)      for x, y in profile_2d]
    top    = [(x, y, height)   for x, y in profile_2d]
    verts  = np.array(bottom + top, dtype=float)
    faces  = []
    for i in range(n):
        next_i = (i + 1) % n

    faces.append([i, next_i, next_i + n, i + n])
    faces.append(list(range(n-1, -1, -1)))   # bottom cap (reversed winding)
    faces.append(list(range(n, 2*n)))        # top cap
 
    return {'verts': verts, 'faces': faces, 'label': 'Extruded Profile'}

#REVOLVE OPERATION
def revolve_profile(profile_rz, n_steps=36, label='Revolved Solid'):
    angles = np.linspace(0, 2*np.pi, n_steps, endpoint=False)
    verts  = []
    for r, z in profile_rz:
        for a in angles:
            verts.append([r * np.cos(a), r * np.sin(a), z])
    verts = np.array(verts, dtype=float)

    m = len(profile_rz)
    faces = []
    for pi in range(m - 1):
        for ai in range(n_steps):
            aj = (ai + 1) % n_steps
            v0 = pi*n_steps + ai
            v1 = pi*n_steps + aj
            v2 = (pi+1)*n_steps + aj
            v3 = (pi+1)*n_steps + ai
            faces.append([v0, v1, v2, v3])
 
    return {'verts': verts, 'faces': faces, 'label': label}

# BOOLEAN OPERATIONS 

def point_in_box(pts, mn, mx):
    """True for each point inside axis-aligned box [mn, mx]."""
    return np.all((pts >= mn) & (pts <= mx), axis=1)
 
 
def point_in_cylinder(pts, cx, cy, r, z_bot, z_top):
    """True for each point inside a cylinder."""
    lateral = ((pts[:,0]-cx)**2 + (pts[:,1]-cy)**2) <= r**2
    axial   = (pts[:,2] >= z_bot) & (pts[:,2] <= z_top)
    return lateral & axial
 
 
def boolean_union(mask_A, mask_B):
    """A ∪ B — points in A OR B."""
    return mask_A | mask_B
 
 
def boolean_subtract(mask_A, mask_B):
    """A − B — points in A but NOT in B."""
    return mask_A & ~mask_B
 
 
def boolean_intersect(mask_A, mask_B):
    """A ∩ B — points in BOTH A and B."""
    return mask_A & mask_B

def extrude_profile(profile_2d, height=3.0):

    n      = len(profile_2d)
    bottom = [(x, y, 0.0)      for x, y in profile_2d]
    top    = [(x, y, height)   for x, y in profile_2d]
    verts  = np.array(bottom + top, dtype=float)

    faces  = []
    for i in range(n):                       # side walls
        j = (i+1) % n
        faces.append([i, j, j+n, i+n])
    faces.append(list(range(n-1, -1, -1)))   # bottom cap (reversed winding)
    faces.append(list(range(n, 2*n)))        # top cap
 
    return {'verts': verts, 'faces': faces, 'label': 'Extruded Profile'}

def revolve_profile(profile_rz, n_steps=36, label='Revolved Solid'):

    angles = np.linspace(0, 2*np.pi, n_steps, endpoint=False)
    verts  = []
    for r, z in profile_rz:
        for a in angles:
            verts.append([r * np.cos(a), r * np.sin(a), z])
    verts = np.array(verts, dtype=float)
 
    m     = len(profile_rz)
    faces = []
    for pi in range(m - 1):
        for ai in range(n_steps):
            aj = (ai + 1) % n_steps
            v0 = pi*n_steps + ai
            v1 = pi*n_steps + aj
            v2 = (pi+1)*n_steps + aj
            v3 = (pi+1)*n_steps + ai
            faces.append([v0, v1, v2, v3])
 
    return {'verts': verts, 'faces': faces, 'label': label}
 
 

#  BOOLEAN OPERATIONS  (point-cloud / voxel approximation)

def point_in_box(pts, mn, mx):
    """True for each point inside axis-aligned box [mn, mx]."""
    return np.all((pts >= mn) & (pts <= mx), axis=1)
 
 
def point_in_cylinder(pts, cx, cy, r, z_bot, z_top):
    """True for each point inside a cylinder."""
    lateral = ((pts[:,0]-cx)**2 + (pts[:,1]-cy)**2) <= r**2
    axial   = (pts[:,2] >= z_bot) & (pts[:,2] <= z_top)
    return lateral & axial
 
 
def boolean_union(mask_A, mask_B):
    """A ∪ B — points in A OR B."""
    return mask_A | mask_B
 
 
def boolean_subtract(mask_A, mask_B):
    """A − B — points in A but NOT in B."""
    return mask_A & ~mask_B
 
 
def boolean_intersect(mask_A, mask_B):
    """A ∩ B — points in BOTH A and B."""
    return mask_A & mask_B

def orthographic_views(mesh):
    verts = mesh['verts']
    faces = mesh['faces']

    def project_edges(ax_pair):
        """Extract line segments projected onto given two axes."""
        segs = []
        for face in faces:
            n = len(face)
            for i in range(n):
                j = (i+1) % n
                p1 = verts[face[i]][list(ax_pair)]
                p2 = verts[face[j]][list(ax_pair)]
                segs.append((p1, p2))
        return segs
 
    return {
        'Front (XZ)': project_edges([0, 2]),
        'Side (YZ)':  project_edges([1, 2]),
        'Top (XY)':   project_edges([0, 1]),
    }
def isometric_transform(verts):
    theta_y = np.radians(45)
    theta_x = np.radians(35.264)
 
    Ry = np.array([[ np.cos(theta_y), 0, np.sin(theta_y)],
                   [               0, 1,               0],
                   [-np.sin(theta_y), 0, np.cos(theta_y)]])
 
    Rx = np.array([[1,0,0],
                   [0,  np.cos(theta_x), -np.sin(theta_x)],
                   [0,  np.sin(theta_x),  np.cos(theta_x)]])
 
    R   = Rx @ Ry
    pts = (R @ verts.T).T
    return pts[:, 0], pts[:, 1]   # project by dropping Z

PALETTE = {
    'bg':    '#0a0f1e', 'panel': '#111827', 'grid':  '#1e2d40',
    'acc':   '#00d4ff', 'gold':  '#ffd166', 'green': '#06d6a0',
    'red':   '#ef476f', 'text':  '#e0e6f0',
}
 
 
def style_3d_ax(ax, title):
    ax.set_facecolor(PALETTE['panel'])
    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.fill = False
        pane.set_edgecolor(PALETTE['grid'])
    ax.tick_params(colors=PALETTE['text'], labelsize=6)
    ax.set_title(title, color=PALETTE['acc'], fontsize=9,
                 fontfamily='monospace', pad=4)
 
 
def draw_mesh(ax, mesh, color, alpha=0.55, edge_color='#ffffff22'):
    verts, faces = mesh['verts'], mesh['faces']
    polys = [[verts[i] for i in f] for f in faces if len(f) >= 3]
    coll  = Poly3DCollection(polys, alpha=alpha, facecolor=color,
                              edgecolor=edge_color, linewidth=0.3)
    ax.add_collection3d(coll)
    v = verts
    pad = 0.3
    ax.set_xlim(v[:,0].min()-pad, v[:,0].max()+pad)
    ax.set_ylim(v[:,1].min()-pad, v[:,1].max()+pad)
    ax.set_zlim(v[:,2].min()-pad, v[:,2].max()+pad)
 
 
def draw_ortho_row(fig, gs, mesh, row, row_start_col=2):
    """
    Draw orthographic projections (Front, Top, Side) in a row.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
    gs : matplotlib.gridspec.GridSpec - the FULL gridspec
    mesh : dict - mesh data with 'verts' and 'faces'
    row : int - which row in the gridspec to use
    row_start_col : int - starting column index
    """
    verts = mesh['verts']
    faces = mesh['faces']
    
    # Define the 3 orthographic views: (title, azim, elev)
    views = [
        ('FRONT',  0,    0),    # Looking along -Y axis
        ('TOP',   -90,  90),    # Looking down along -Z axis  
        ('SIDE',  90,   0),     # Looking along +X axis
    ]
    
    for idx, (name, azim, elev) in enumerate(views):
        col = row_start_col + idx
        ax = fig.add_subplot(gs[row, col], projection='3d')
        style_3d_ax(ax, name)
        draw_mesh(ax, mesh, color=PALETTE['acc'], alpha=0.7)
        ax.view_init(elev=elev, azim=azim)
 
 
def annotation_box(ax, text, border_color):
    ax.set_facecolor(PALETTE['panel'])
    ax.axis('off')
    ax.text(0.05, 0.95, text, transform=ax.transAxes,
            va='top', ha='left', color=PALETTE['text'],
            fontfamily='monospace', fontsize=6.5,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#0d1b2a',
                      edgecolor=border_color, lw=0.8))

 
 
