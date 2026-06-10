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
    fig = plt.figure(figsize=(16, 8), facecolor=PALETTE['bg'])
    fig.text(0.5, 0.95,
             'REVOLVE OPERATION',
             ha='center', va='top', color=PALETTE['gold'],
             fontsize=18, fontfamily='monospace', fontweight='bold')

    gs = fig.add_gridspec(1, 5, hspace=0.45, wspace=0.35,
                          left=0.04, right=0.97, top=0.88, bottom=0.04)

    # Vase profile
    vase = [(0.0,0.0),(0.5,0.0),(0.7,0.5),(0.9,1.0),(1.0,1.5),
            (0.8,2.0),(0.6,2.5),(0.5,3.0),(0.55,3.3),(0.45,3.3)]
    rev = revolve_profile(vase, n_steps=40, label='Revolved Vase')

    # 3D view
    ax1 = fig.add_subplot(gs[0, 0:2], projection='3d')
    style_3d_ax(ax1, '3D PERSPECTIVE')
    draw_mesh(ax1, rev, color=PALETTE['gold'])
    ax1.view_init(elev=20, azim=40)

    # Orthographic views
    draw_ortho_row(fig, gs, rev, row=0, row_start_col=2)

    # Annotation
    annotation_box(fig.add_subplot(gs[0, 4]),
        "REVOLVE\n"
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

    plt.savefig('revolve_output.png', dpi=150,
                bbox_inches='tight', facecolor=PALETTE['bg'])
    print("✓ Saved revolve_output.png")
    plt.show()

if __name__ == '__main__':
    main()