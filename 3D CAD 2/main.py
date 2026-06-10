import numpy as np
import matplotlib
matplotlib.use('TkAgg')          
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import warnings
warnings.filterwarnings('ignore')
from m_math import *
from operations import*


from operations import PALETTE, annotation_box, draw_mesh, draw_ortho_row, style_3d_ax


def main():
    fig = plt.figure(figsize=(20, 14), facecolor=PALETTE['bg'])
    fig.text(0.5, 0.97,
             '3D SOLID MODELER  ·  Python CAD Engine',
             ha='center', va='top', color=PALETTE['acc'],
             fontsize=18, fontfamily='monospace', fontweight='bold')
    fig.text(0.5, 0.945,
             'Extrude · Revolve · Boolean (Union / Subtract / Intersect) · Orthographic Projections',
             ha='center', va='top', color=PALETTE['gold'],
             fontsize=10, fontfamily='monospace')
 
    gs = fig.add_gridspec(3, 6, hspace=0.45, wspace=0.35,
                          left=0.04, right=0.97, top=0.91, bottom=0.04)
 
    # ── ROW 0 : EXTRUDE ─────────────────────────────────────────────
    L = [(0,0),(2,0),(2,0.6),(0.6,0.6),(0.6,2),(0,2)]
    ext = extrude_profile(L, height=2.5)
 
    ax0 = fig.add_subplot(gs[0, 0:2], projection='3d')
    style_3d_ax(ax0, '① EXTRUDE  —  L-Profile → Solid')
    draw_mesh(ax0, ext, color=PALETTE['acc'])
    ax0.view_init(elev=28, azim=-50)
 
    draw_ortho_row(fig, gs, ext, row=0, row_start_col=2)
 
    annotation_box(fig.add_subplot(gs[0, 5]),
        "EXTRUDE OPERATION\n"
        "─────────────────\n"
        "profile = L-shape polygon\n"
        "\n"
        "solid = extrude_profile(\n"
        "  profile_2d,\n"
        "  height = 2.5\n"
        ")\n\n"
        "→ Sweeps cross-section\n"
        "  along Z-axis\n\n"
        "ML link: conv. kernel\n"
        "sliding along 1-D axis",
        PALETTE['acc'])
 
    # ── ROW 1 : REVOLVE ─────────────────────────────────────────────
    vase = [(0.0,0.0),(0.5,0.0),(0.7,0.5),(0.9,1.0),(1.0,1.5),
            (0.8,2.0),(0.6,2.5),(0.5,3.0),(0.55,3.3),(0.45,3.3)]
    rev = revolve_profile(vase, n_steps=40, label='Revolved Vase')
 
    ax1 = fig.add_subplot(gs[1, 0:2], projection='3d')
    style_3d_ax(ax1, '② REVOLVE  —  Profile → Vase Solid')
    draw_mesh(ax1, rev, color=PALETTE['gold'])
    ax1.view_init(elev=20, azim=40)
 
    draw_ortho_row(fig, gs, rev, row=1, row_start_col=2)
 
    annotation_box(fig.add_subplot(gs[1, 5]),
        "REVOLVE OPERATION\n"
        "─────────────────\n"
        "profile_rz = vase curve\n"
        "\n"
        "solid = revolve_profile(\n"
        "  profile_rz,\n"
        "  n_steps = 40\n"
        ")\n\n"
        "→ Spins profile 360°\n"
        "  around Z-axis\n\n"
        "ML link: rotational\n"
        "data augmentation",
        PALETTE['gold'])
 
    # ── ROW 2 : BOOLEAN ─────────────────────────────────────────────
    box_mesh = make_box(0,0,0,2,2,2)
    cyl_mesh = make_cylinder(0,0,0,r=0.8,h=2.5,n=36)
 
    # Sample a dense point cloud, then apply Boolean masks
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
        ax = fig.add_subplot(gs[2, col_i*2:col_i*2+2], projection='3d')
        style_3d_ax(ax, f'③ BOOLEAN  —  {title}')
 
        sel = pts[mask]
        if len(sel) > 0:
            ds = sel[::max(1, len(sel)//1500)]
            ax.scatter(ds[:,0], ds[:,1], ds[:,2],
                       c=bcol, alpha=0.22, s=1.5, edgecolors='none')
 
        # reference wireframes
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
 
    plt.savefig('solid_modeler_output.png', dpi=150,
                bbox_inches='tight', facecolor=PALETTE['bg'])
    print("✓ Saved solid_modeler_output.png")
    plt.show()
 
 
if __name__ == '__main__':
    main()



    
