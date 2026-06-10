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
             'EXTRUDE OPERATION',
             ha='center', va='top', color=PALETTE['acc'],
             fontsize=18, fontfamily='monospace', fontweight='bold')

    gs = fig.add_gridspec(1, 5, hspace=0.45, wspace=0.35,
                          left=0.04, right=0.97, top=0.88, bottom=0.04)

    # L-shaped profile
    L = [(0,0),(2,0),(2,0.6),(0.6,0.6),(0.6,2),(0,2)]
    ext = extrude_profile(L, height=2.5)

    # 3D view
    ax0 = fig.add_subplot(gs[0, 0:2], projection='3d')
    style_3d_ax(ax0, '3D PERSPECTIVE')
    draw_mesh(ax0, ext, color=PALETTE['acc'])
    ax0.view_init(elev=28, azim=-50)

    # Orthographic views
    draw_ortho_row(fig, gs, ext, row=0, row_start_col=2)

    # Annotation
    annotation_box(fig.add_subplot(gs[0, 4]),
        "EXTRUDE\n"
        "─────────────────\n"
        "profile = L-shape\n"
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

    plt.savefig('extrude_output.png', dpi=150,
                bbox_inches='tight', facecolor=PALETTE['bg'])
    print("✓ Saved extrude_output.png")
    plt.show()

if __name__ == '__main__':
    main()