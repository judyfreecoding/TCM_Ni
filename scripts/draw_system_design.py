# -*- coding: utf-8 -*-
"""
Render the system design diagram from TuiTiSheJi.docx.
Faithfully reproduces all 21 text boxes with exact positions,
text content, fill colors (Five Elements scheme), and borders
as extracted from the docx XML and theme.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.font_manager import FontProperties, fontManager
import numpy as np
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(BASE, 'docs', 'public', 'system_design_overview.png')

# --- Font ---
available_fonts = [f.name for f in fontManager.ttflist]
CHINESE_CANDIDATES = [
    'KaiTi', 'STKaiti', 'STSong', 'FangSong', 'STFangsong',
    'SimHei', 'STXihei', 'STZhongsong', 'Microsoft YaHei',
    'FZCuHeiSongS-B-GB', 'SimSun-ExtB', 'SimSun-ExtG'
]
chosen = 'sans-serif'
for fn in CHINESE_CANDIDATES:
    if fn in available_fonts:
        chosen = fn
        break
print('Font:', chosen)
fp = FontProperties(family=chosen)

DPI = 150

# --- Theme colors extracted from theme1.xml ---
# Five Elements color scheme:
#   Wood (green):  accent4 = #75BD42
#   Fire (red):    accent6 = #E54C5E
#   Earth (yellow): accent3 = #F2BA02
#   Metal (white): lt1 = white
#   Water (black): tx1 = dark (#000000, system windowText)
CLR_WHITE = '#FFFFFF'
CLR_GREEN = '#75BD42'    # accent4 - Wood: 肝, 胆
CLR_RED = '#E54C5E'      # accent6 - Fire: 心, 小肠
CLR_GOLD = '#F2BA02'     # accent3 - Earth: 脾, 胃
CLR_DARK = '#333333'     # tx1 (dark) - Water: 肾 (white text)
CLR_GRAY = '#D9D9D9'     # bg2 (light gray) - Water: 膀胱
CLR_BLACK = '#000000'
CLR_LTGRAY = '#E7E6E6'   # lt2
CLR_BLUE = '#4874CB'     # accent1
CLR_ORANGE = '#EE822F'    # accent2
CLR_TEAL = '#30C0B4'      # accent5
CLR_DKBLUE = '#44546A'    # dk2

# ============================================================
# SHAPE DATA
# ============================================================
# Left labels: (x, y, w, h, text) — NO border, white fill
LEFT_LABELS = [
    (-40.1, 32.4, 90.7, 42.8, u'应用层'),
    (-37.9, 112.6, 90.7, 42.8, u'协作层'),
    (-37.9, 166.6, 90.7, 42.8, u'网络层'),
    (-37.9, 218.3, 90.7, 162.0, u'服务层'),
    (-37.1, 459.1, 90.7, 42.8, u'基础层'),
    (-36.4, 512.4, 90.7, 42.8, u'基础理论层'),
]

# Right top: (x, y, w, h, text, fontsize) — white fill, black border
RIGHT_TOP = [
    (66.2, 33.1, 339.8, 42.8,
     u'消化吸收、运动、表情、思维、情绪、说话', 9),
    (65.5, 83.3, 339.8, 71.2,
     u'诸风掉眩皆属于肝；诸痛痒疮皆属于心；诸痉项强皆属于湿；\n诸湿肿满皆属于脾；诸气偾郁皆属于肺；诸寒收引皆属于肾。\n肝主怒；心主喜；脾主思；肺主忧；肾主恐。', 7),
]

# Meridians: (x, y, w, h, text, fill_color, text_color)
MERIDIANS = [
    (65.5, 165.8, 34.6, 42.8, u'肝经',   CLR_GREEN, CLR_BLACK),   # Wood
    (100.8, 165.8, 34.6, 42.8, u'胆经',   CLR_GREEN, CLR_BLACK),   # Wood
    (136.0, 165.8, 34.6, 42.8, u'心经',   CLR_RED, CLR_BLACK),     # Fire
    (171.2, 165.8, 34.6, 42.8, u'小肠经', CLR_RED, CLR_BLACK),     # Fire
    (206.5, 165.8, 34.6, 42.8, u'脾经',   CLR_GOLD, CLR_BLACK),    # Earth
    (241.8, 165.8, 34.6, 42.8, u'胃经',   CLR_GOLD, CLR_BLACK),    # Earth
    (277.0, 165.8, 34.6, 42.8, u'肺经',   CLR_WHITE, CLR_BLACK),   # Metal
    (312.2, 165.8, 34.6, 42.8, u'大肠经', CLR_WHITE, CLR_BLACK),   # Metal
    (347.5, 165.8, 34.6, 42.8, u'肾经',   CLR_DARK, CLR_WHITE),    # Water (dark bg + white text!)
    (382.8, 165.8, 34.6, 42.8, u'膀胱经', CLR_GRAY, CLR_BLACK),    # Water
]

# Bottom: (x, y, w, h, text) — white fill, black border
BOTTOM = [
    (66.2, 458.4, 339.8, 42.8, u'气血'),
    (67.0, 511.6, 339.8, 42.8, u'阴阳'),
]

# Service layer
SVC_BOX_X, SVC_BOX_Y = 65.5, 216.2
SVC_BOX_W, SVC_BOX_H = 339.8, 237.7
SVC_IMG_W, SVC_IMG_H = 324.4, 212.9
SVC_IMG_X = SVC_BOX_X + (SVC_BOX_W - SVC_IMG_W) / 2.0
SVC_IMG_Y = SVC_BOX_Y + (SVC_BOX_H - SVC_IMG_H) / 2.0

DOCX_IMG = os.path.join(BASE, 'docs', 'huangdi', 'appendix',
                        '_docx_extracted', 'image1_orig.png')

# ============================================================
# Compute bounds
# ============================================================
all_shapes = LEFT_LABELS + [s[:5] for s in RIGHT_TOP] + \
             [s[:5] for s in MERIDIANS] + BOTTOM
min_x = min(s[0] for s in all_shapes)
max_x = max(s[0] + s[2] for s in all_shapes)
min_y = min(s[1] for s in all_shapes) - 10
max_y = max(s[1] + s[3] for s in all_shapes) + 10

fig_w = (max_x - min_x) / 72.0 + 0.3
fig_h = (max_y - min_y) / 72.0 + 0.3

# ============================================================
# Create figure
# ============================================================
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=DPI)
ax.set_xlim(min_x - 15, max_x + 15)
ax.set_ylim(max_y + 10, min_y - 10)
ax.set_aspect('equal')
ax.axis('off')

# ============================================================
# Helpers
# ============================================================
def draw_label(ax, x, y, w, h, text, fontsize=10):
    """Left label: text only, NO box at all (white bg = page bg)."""
    ax.text(x + w/2.0, y + h/2.0, text,
            ha='center', va='center',
            fontproperties=fp, fontsize=fontsize,
            color=CLR_BLACK, zorder=6)

def draw_box(ax, x, y, w, h, text, fontsize=9,
             facecolor=CLR_WHITE, edgecolor=CLR_BLACK,
             textcolor=CLR_BLACK, zorder=5):
    """Right content box: with border and fill."""
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=patches.BoxStyle('square', pad=0),
        facecolor=facecolor, edgecolor=edgecolor,
        linewidth=0.5, zorder=zorder,
    )
    ax.add_patch(rect)

    lines = text.split('\n')
    cx, cy = x + w/2.0, y + h/2.0

    if len(lines) == 1:
        ax.text(cx, cy, text, ha='center', va='center',
                fontproperties=fp, fontsize=fontsize,
                color=textcolor, zorder=zorder+1)
    else:
        lh = fontsize * 1.4
        total_h = lh * len(lines)
        start_y = cy + total_h/2.0 - lh/2.0
        for i, line in enumerate(lines):
            ax.text(cx, start_y - i*lh, line,
                    ha='center', va='center',
                    fontproperties=fp, fontsize=fontsize,
                    color=textcolor, zorder=zorder+1)

# ============================================================
# 1. Embed enhanced docx image in service layer box
# ============================================================
if os.path.exists(DOCX_IMG):
    raw = plt.imread(DOCX_IMG)
    p2, p98 = np.percentile(raw, [2, 98])
    if p98 > p2:
        enhanced = np.clip((raw - p2) / (p98 - p2), 0, 1)
    else:
        enhanced = raw

    ax.imshow(enhanced,
              extent=[SVC_IMG_X, SVC_IMG_X + SVC_IMG_W,
                      SVC_IMG_Y + SVC_IMG_H, SVC_IMG_Y],
              aspect='auto', zorder=2, interpolation='bilinear')

# 2. Service box border on top of image
rect = patches.FancyBboxPatch(
    (SVC_BOX_X, SVC_BOX_Y), SVC_BOX_W, SVC_BOX_H,
    boxstyle=patches.BoxStyle('square', pad=0),
    facecolor='none', edgecolor=CLR_BLACK,
    linewidth=0.5, zorder=5,
)
ax.add_patch(rect)

# 3. Left labels (no border)
for s in LEFT_LABELS:
    x, y, w, h, text = s
    fs = 10 if len(text) <= 4 else 8
    draw_label(ax, x, y, w, h, text, fontsize=fs)

# 4. Right top boxes
for s in RIGHT_TOP:
    x, y, w, h, text, fs = s
    draw_box(ax, x, y, w, h, text, fontsize=fs, zorder=5)

# 5. Meridian row with Five Elements colors
for s in MERIDIANS:
    x, y, w, h, text, fc, tc = s
    draw_box(ax, x, y, w, h, text, fontsize=7.5,
             facecolor=fc, textcolor=tc, zorder=5)

# 6. Bottom boxes
for s in BOTTOM:
    x, y, w, h, text = s
    draw_box(ax, x, y, w, h, text, fontsize=10, zorder=5)

# ============================================================
# Save
# ============================================================
fig.savefig(output_path, dpi=DPI, bbox_inches='tight',
            facecolor='white', edgecolor='none', pad_inches=0.1)
plt.close(fig)
print('Saved:', output_path)
