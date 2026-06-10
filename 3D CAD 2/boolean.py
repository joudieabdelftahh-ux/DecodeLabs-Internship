import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import warnings
warnings.filterwarnings('ignore')
from m_math import *
from operations import *

def main():
    fig = plt.figure(figsize=(18, 7), facecolor=PALETTE['bg'])
    fig.text(0.5, 0.95,
             'BOOLEAN OPERATIONS',
             ha='center', va='top', color=PALETTE['acc'],
             fontsize=18, fontfamily='monospace', fontweight='bold')

    gs = fig.add_gridspec(1, 3, hspace=0.45, wspace=0.25,
                          left=0.04, right=0.97, top=0.88, bottom=0.04)

    # Create reference meshes
    box_mesh = make_box(0,0,0,2,2,2)
    cyl_mesh = make_cylinder(0,0,0,r=0.8,h=2.5,n=36)

    # Point cloud
    N   = 14000
    pts = np.random.uniform(-1.5, 1.5, (N, 3))

    mask_box = point_in_box(pts, np.full(3,-1.0), np.full(3,1.0))
    mask_cyl = point_in_cylinder(pts, 0, 0, r=0.8, z_bot=-1.0, z_top=1.0)

    ops = [
        (boolean_union(mask_box, mask_cyl),     'UNION  (A ∪ B)',     PALETTE['green']),
        (boolean_subtract(mask_box, mask_cyl),  'SUBTRACT  (A − B)',  PALETTE['red']),
        (boolean_intersect(mask_box, mask_cyl), 'INTERSECT  (A ∩ B)', PALETTE['gold']),
    ]

    for col_i, (mask, title, bcol) in enumerate(ops):
        ax = fig.add_subplot(gs[0, col_i], projection='3d')
        style_3d_ax(ax, title)

        sel = pts[mask]
        if len(sel) > 0:
            ds = sel[::max(1, len(sel)//1500)]
            ax.scatter(ds[:,0], ds[:,1], ds[:,2],
                       c=bcol, alpha=0.22, s=1.5, edgecolors='none')

        # Reference wireframes
        for msh, mc in [(box_mesh,'#ffffff20'),(cyl_mesh,'#ffffff15')]:
            v, f = msh['verts'], msh['faces']
            for face in f:
                n = len(face)
                for i in range(n):
                    j = (i+1)%n
                    ax.plot([v[face[i],0],v[face[j],0]],
                            [v[face[i],1],v[face[j],1]],
                            [v[face[i],2],v[face[j],2]],
                            color=mc, lw=0.5)

        ax.set_xlim(-1.5,1.5)
        ax.set_ylim(-1.5,1.5)
        ax.set_zlim(-1.5,1.5)
        ax.view_init(elev=22, azim=35)

    plt.savefig('boolean_output.png', dpi=150,
                bbox_inches='tight', facecolor=PALETTE['bg'])
    print("✓ Saved boolean_output.png")
    plt.show()

if __name__ == '__main__':
    main()