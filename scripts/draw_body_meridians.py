# -*- coding: utf-8 -*-
"""人体十二正经布线概念图 — 四肢为体积带状，经脉从头顶出发"""
from __future__ import division, print_function, unicode_literals
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

# ═══════════════ 配色 ═══════════════
BODY_FACE = '#FDF6ED'       # 身体底色
BODY_EDGE = '#B5A898'       # 轮廓线
LIMB_FILL = '#F7EFE4'       # 四肢填充

def darker(c, factor=0.75):
    """将颜色变深"""
    import re
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    return '#{:02x}{:02x}{:02x}'.format(int(r*factor), int(g*factor), int(b*factor))

# 前面 — 肺系统(金) + 脾系统(土)
C_LU = '#C48A50'
C_LI = '#E0C090'
C_ST = '#E8A040'
C_SP = '#B87030'

# 中间 — 心包系统(相火) + 肝系统(木)
C_PC = '#D45050'
C_TE = '#F08050'
C_GB = '#5DA060'
C_LR = '#3E8848'

# 后面 — 心系统(君火) + 肾系统(水)
C_HT = '#D03838'
C_SI = '#F07868'
C_BL = '#4880B8'
C_KI = '#285888'

MERIDIAN_LW = 3.0
HEAD_RADIUS_X = 1.05
HEAD_RADIUS_Y = 1.25


# ═══════════════════════════════════════════
#  身体轮廓绘制
# ═══════════════════════════════════════════

def draw_head(ax, cx, cy):
    """画头"""
    head = mpatches.Ellipse((cx, cy + 4.3), HEAD_RADIUS_X * 2, HEAD_RADIUS_Y * 2,
                            fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=2)
    ax.add_patch(head)
    # 头顶标记
    ax.plot(cx, cy + 5.55, marker='^', color=BODY_EDGE, markersize=8, zorder=3, clip_on=False)


def draw_torso_front_back(ax, cx, cy):
    """前/后视图躯干 (收腰 Bezier)"""
    verts = [
        (cx - 1.9, cy + 2.6),           # MOVETO 左肩
        (cx - 2.05, cy + 1.4),          # CURVE4
        (cx - 1.35, cy + 0.3),          # CURVE4
        (cx - 1.5, cy - 0.8),           # CURVE4 左腰
        (cx - 1.55, cy - 1.5),          # CURVE4
        (cx - 1.95, cy - 2.5),          # CURVE4
        (cx - 1.85, cy - 2.8),          # CURVE4 左髋底
        (cx + 1.85, cy - 2.8),          # LINETO 右髋底
        (cx + 1.95, cy - 2.5),          # CURVE4
        (cx + 1.55, cy - 1.5),          # CURVE4
        (cx + 1.5, cy - 0.8),           # CURVE4 右腰
        (cx + 1.35, cy + 0.3),          # CURVE4
        (cx + 2.05, cy + 1.4),          # CURVE4
        (cx + 1.9, cy + 2.6),           # CURVE4 右肩
        (cx - 1.9, cy + 2.6),           # CLOSEPOLY
    ]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.LINETO,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
    torso = PathPatch(Path(verts, codes), fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=1)
    ax.add_patch(torso)

    # 脖子
    neck = mpatches.FancyBboxPatch((cx - 0.33, cy + 2.55), 0.66, 0.4,
                                   boxstyle='round,pad=0.02', fc=BODY_FACE, ec=BODY_EDGE, lw=1.2, zorder=1)
    ax.add_patch(neck)


def draw_torso_side(ax, cx, cy):
    """侧视躯干"""
    verts = [
        (cx - 0.55, cy + 2.6),            # 肩前
        (cx + 0.5, cy + 2.6),             # 肩后
        (cx + 0.45, cy + 1.6),            # 背
        (cx + 0.15, cy + 0.1),            # 腰后
        (cx - 0.25, cy - 1.0),            # 腰前
        (cx + 0.15, cy - 2.0),            # 臀后
        (cx + 0.65, cy - 2.8),            # 髋底后
        (cx - 0.55, cy - 2.8),            # 髋底前
        (cx - 0.55, cy + 2.6),            # CLOSE
    ]
    codes = [Path.MOVETO, Path.LINETO, Path.CURVE4, Path.CURVE4,
             Path.CURVE4, Path.CURVE4, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    torso = PathPatch(Path(verts, codes), fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=1)
    ax.add_patch(torso)

    # 脖子 (稍前倾)
    neck = mpatches.FancyBboxPatch((cx - 0.25, cy + 2.55), 0.58, 0.4,
                                   boxstyle='round,pad=0.02', fc=BODY_FACE, ec=BODY_EDGE, lw=1.2, zorder=1)
    ax.add_patch(neck)


def draw_limb_band(ax, outer_pts, inner_pts, lw=1.5):
    """将四肢画成有体积的带状 (封闭多边形)"""
    all_pts = list(outer_pts) + list(reversed(inner_pts))
    band = mpatches.Polygon(all_pts, closed=True, fc=LIMB_FILL, ec=BODY_EDGE, lw=lw, zorder=0)
    ax.add_patch(band)


def draw_meridian(ax, pts, color, lw=MERIDIAN_LW, alpha=0.92,
                  label_pt=None, label_text='', zorder=10):
    """画经络线 + 箭头 + 标签"""
    xs, ys = zip(*pts)
    ax.plot(xs, ys, '-', color=color, lw=lw, alpha=alpha, zorder=zorder,
            solid_capstyle='round', solid_joinstyle='round')

    # 末端箭头
    n = len(pts)
    if n >= 2:
        dx = pts[-1][0] - pts[-2][0]
        dy = pts[-1][1] - pts[-2][1]
        d = np.sqrt(dx * dx + dy * dy)
        if d > 0.01:
            dx, dy = dx / d, dy / d
            ax.annotate('', xy=pts[-1],
                        xytext=(pts[-1][0] - dx * 0.5, pts[-1][1] - dy * 0.5),
                        arrowprops=dict(arrowstyle='->', color=color, lw=2.2,
                                        alpha=alpha, connectionstyle='arc3'),
                        zorder=zorder + 1)
    # 标签
    if label_pt and label_text:
        ax.text(label_pt[0], label_pt[1], label_text, fontsize=6.5,
                color=darker(color, 0.7), ha='center', va='center', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=color, alpha=0.85, lw=0.7),
                zorder=20)


# ═══════════════════════════════════════════
#  前面 — 肺系统 + 脾系统
# ═══════════════════════════════════════════

def draw_front_view(ax, cx=0, cy=5.0):
    draw_head(ax, cx, cy)
    draw_torso_front_back(ax, cx, cy)

    for s in [-1, 1]:
        # ── 手臂带状体积 ──
        arm_outer = [
            (cx + s * 1.7, cy + 2.4),    # 肩外侧 (连躯干肩)
            (cx + s * 2.1, cy + 1.3),    # 上臂外
            (cx + s * 2.45, cy + 0.2),   # 肘外
            (cx + s * 2.35, cy - 1.0),   # 前臂外
            (cx + s * 2.2, cy - 2.0),    # 腕外
        ]
        arm_inner = [
            (cx + s * 1.1, cy + 2.2),    # 肩内侧(腋,连躯干)
            (cx + s * 1.35, cy + 1.3),   # 上臂内
            (cx + s * 1.6, cy + 0.2),    # 肘内
            (cx + s * 1.55, cy - 1.0),   # 前臂内
            (cx + s * 1.45, cy - 2.0),   # 腕内
        ]
        draw_limb_band(ax, arm_outer, arm_inner)

        # 手 (椭圆)
        hand = mpatches.Ellipse((cx + s * 1.8, cy - 2.3), 0.75, 0.35,
                                fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=2)
        ax.add_patch(hand)

        # 手太阴肺经 (LU): 胸部 → 手臂内侧(阴面) → 拇指
        lu = [
            (cx + s * 0.45, cy + 2.1),   # 中府-胸部起点
            (cx + s * 0.8, cy + 1.6),
            (cx + s * 1.25, cy + 0.8),   # 上臂内侧
            (cx + s * 1.55, cy + 0.0),   # 肘内侧
            (cx + s * 1.55, cy - 0.9),   # 前臂内侧
            (cx + s * 1.5, cy - 1.9),    # 腕 → 拇指
        ]
        draw_meridian(ax, lu, C_LU, label_pt=(cx + s * 1.95, cy - 0.5),
                      label_text='肺经\n(太阴)')

        # 手阳明大肠经 (LI): 食指 → 手臂外侧(阳面) → 肩 → 头面(鼻旁)
        li = [
            (cx + s * 1.7, cy - 2.2),    # 食指
            (cx + s * 2.05, cy - 1.1),   # 前臂外侧
            (cx + s * 2.2, cy + 0.0),    # 肘外侧
            (cx + s * 1.9, cy + 1.1),    # 上臂外侧
            (cx + s * 1.55, cy + 1.75),  # 肩
            (cx + s * 1.0, cy + 2.35),   # 颈侧
            (cx + s * 0.5, cy + 3.2),    # 鼻旁(迎香)
            (cx + s * 0.25, cy + 4.3),   # 上行入头部
        ]
        draw_meridian(ax, li, C_LI, label_pt=(cx + s * 2.55, cy + 0.2),
                      label_text='大肠经\n(阳明)')

    for s in [-1, 1]:
        # ── 腿部带状体积 ──
        leg_outer = [
            (cx + s * 1.5, cy - 2.8),    # 髋外侧
            (cx + s * 1.1, cy - 5.5),    # 踝外侧
        ]
        leg_inner = [
            (cx + s * 0.4, cy - 2.8),    # 髋内侧
            (cx + s * 0.25, cy - 5.5),   # 踝内侧
        ]
        draw_limb_band(ax, leg_outer, leg_inner)

        # 足
        foot = mpatches.Ellipse((cx + s * 0.65, cy - 5.85), 1.1, 0.35,
                                fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=2)
        ax.add_patch(foot)

        # 足阳明胃经 (ST): 头顶 → 面部 → 颈前 → 胸腹 → 腿前外 → 足背 → 次趾
        st = [
            (cx + s * 0.2, cy + 5.0),    # 头顶区
            (cx + s * 0.35, cy + 3.4),   # 面部(眼下)
            (cx + s * 0.2, cy + 2.3),    # 颈前
            (cx + s * 0.55, cy + 1.2),   # 锁骨下
            (cx + s * 0.75, cy + 0.2),   # 胸部
            (cx + s * 0.85, cy - 1.0),   # 腹部
            (cx + s * 0.9, cy - 2.0),    # 大腿前
            (cx + s * 0.85, cy - 3.2),   # 膝前
            (cx + s * 0.7, cy - 4.2),    # 胫前
            (cx + s * 0.55, cy - 5.3),   # 足背 → 次趾
        ]
        draw_meridian(ax, st, C_ST, label_pt=(cx + s * 1.25, cy - 2.5),
                      label_text='胃经\n(阳明)')

        # 足太阴脾经 (SP): 大趾 → 内踝 → 小腿内侧 → 大腿内侧 → 腹 → 胸胁
        sp = [
            (cx + s * 0.4, cy - 5.4),    # 大趾
            (cx + s * 0.5, cy - 4.2),    # 内踝
            (cx + s * 0.35, cy - 2.9),   # 小腿内侧
            (cx + s * 0.25, cy - 1.6),   # 大腿内侧
            (cx + s * 0.15, cy - 0.2),   # 腹股沟
            (cx + s * 0.05, cy + 1.1),   # 腹部 → 大包(胁)
            (cx + s * 0.1, cy + 2.0),    # 上行至胸
        ]
        draw_meridian(ax, sp, C_SP, label_pt=(cx + s * 0.85, cy - 2.5),
                      label_text='脾经\n(太阴)')


# ═══════════════════════════════════════════
#  中间(侧视) — 心包系统 + 肝系统
# ═══════════════════════════════════════════

C_LR_LIGHT = '#8ED888'  # 肝经浅绿

def draw_middle_view(ax, cx=0, cy=5.0):
    """侧面图：头颈躯干腿一条直线，胆经垂直贯穿，肝经平行右侧"""
    mx = cx  # 中线 X 坐标

    # ── 头 (椭圆) ──
    head = mpatches.Ellipse((mx, cy + 4.3), HEAD_RADIUS_X * 2, HEAD_RADIUS_Y * 2,
                            fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=2)
    ax.add_patch(head)
    ax.plot(mx, cy + 5.55, marker='^', color=BODY_EDGE, markersize=8, zorder=3)

    # ── 颈 (窄矩形) ──
    neck_rect = mpatches.FancyBboxPatch((mx - 0.25, cy + 2.6), 0.5, 0.45,
                                         boxstyle='round,pad=0.02',
                                         fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=1)
    ax.add_patch(neck_rect)

    # ── 躯干 (矩形) ──
    torso_rect = mpatches.FancyBboxPatch((mx - 0.7, cy - 2.5), 1.4, 5.1,
                                          boxstyle='round,pad=0.08',
                                          fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=1)
    ax.add_patch(torso_rect)

    # 躯干上标注 "胸" 和 "腹" 分界
    ax.plot([mx - 0.7, mx + 0.7], [cy + 0.6, cy + 0.6], '--',
            color='#D0C8BC', lw=0.8, zorder=2)
    ax.text(mx - 0.85, cy + 1.6, u'胸', fontsize=7, ha='right', va='center', color='#B0A090')
    ax.text(mx - 0.85, cy - 1.0, u'腹', fontsize=7, ha='right', va='center', color='#B0A090')

    # ── 腿 (带状, 延续直线) ──
    leg_outer = [
        (mx - 0.3, cy - 2.5),
        (mx - 0.2, cy - 5.5),
    ]
    leg_inner = [
        (mx + 0.3, cy - 2.5),
        (mx + 0.2, cy - 5.5),
    ]
    draw_limb_band(ax, leg_outer, leg_inner)

    foot = mpatches.Ellipse((mx, cy - 5.85), 1.0, 0.32,
                            fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=2)
    ax.add_patch(foot)

    # ═══ 胆经 (GB): 垂直贯穿头→颈→躯干→腿中线 ═══
    gb_x = mx + 0.05  # 略偏右的中线
    gb = [
        (gb_x, cy + 5.5),      # 头顶
        (gb_x, cy + 4.0),      # 头
        (gb_x, cy + 2.8),      # 颈
        (gb_x, cy + 0.5),      # 胸
        (gb_x, cy - 1.0),      # 腹
        (gb_x, cy - 3.5),      # 腿
        (gb_x, cy - 5.4),      # 足 → 四趾
    ]
    draw_meridian(ax, gb, C_GB, label_pt=(mx + 0.6, cy - 2.0),
                  label_text='胆经\n(少阳)', zorder=10, lw=3.5)

    # ═══ 肝经 (LR): 胆经右侧平行，浅绿，上到胸为止 ═══
    lr_x = mx + 0.185  # 胆经右侧 50px (0.135u)
    lr = [
        (lr_x, cy - 5.4),      # 大趾
        (lr_x, cy - 4.0),      # 小腿
        (lr_x, cy - 2.5),      # 大腿
        (lr_x, cy - 0.8),      # 腹
        (lr_x, cy + 0.5),      # 入胸 (止于胸)
    ]
    draw_meridian(ax, lr, C_LR_LIGHT, label_pt=(mx + 1.1, cy - 2.0),
                  label_text='肝经\n(厥阴)', zorder=10, lw=3.5)

    # ═══ 手臂 (从躯干右侧伸出) ═══
    arm_outer = [
        (mx + 0.7, cy + 2.2),      # 肩
        (mx + 1.3, cy + 1.2),      # 上臂外
        (mx + 1.8, cy + 0.1),      # 肘外
        (mx + 1.7, cy - 1.0),      # 前臂外
        (mx + 1.5, cy - 2.0),      # 腕外
    ]
    arm_inner = [
        (mx + 0.3, cy + 2.0),      # 肩内侧
        (mx + 0.7, cy + 1.2),      # 上臂内
        (mx + 1.2, cy + 0.1),      # 肘内
        (mx + 1.1, cy - 1.0),      # 前臂内
        (mx + 0.9, cy - 2.0),      # 腕内
    ]
    draw_limb_band(ax, arm_outer, arm_inner)

    hand = mpatches.Ellipse((mx + 1.2, cy - 2.3), 0.7, 0.3,
                            fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=2)
    ax.add_patch(hand)

    # 手厥阴心包经 (PC): 胸 → 手臂阴面 → 中指
    pc = [
        (mx - 0.1, cy + 2.1),      # 胸部
        (mx + 0.4, cy + 1.4),      # 腋
        (mx + 0.8, cy + 0.5),      # 上臂内侧
        (mx + 1.15, cy - 0.1),     # 肘内侧
        (mx + 1.1, cy - 1.0),      # 前臂内侧
        (mx + 0.95, cy - 1.9),     # 腕 → 中指
    ]
    draw_meridian(ax, pc, C_PC, label_pt=(mx + 2.0, cy - 0.5),
                  label_text='心包经\n(厥阴)')

    # 手少阳三焦经 (TE): 无名指 → 手臂外侧 → 肩 → 入头(耳后) (距PC 50px)
    te = [
        (mx + 0.65, cy - 2.2),     # 无名指 (距PC 50px)
        (mx + 1.1, cy - 1.0),      # 前臂外侧 (距PC 50px)
        (mx + 1.285, cy + 0.0),    # 肘外侧 (PC肘1.15+0.135=50px)
        (mx + 1.0, cy + 1.1),      # 上臂外侧 (距PC 50px)
        (mx + 0.6, cy + 1.9),      # 肩
        (mx + 0.3, cy + 2.6),      # 颈
        (mx + 0.1, cy + 3.4),      # 耳后
        (mx, cy + 4.2),            # 入头部
    ]
    draw_meridian(ax, te, C_TE, label_pt=(mx + 2.0, cy + 0.5),
                  label_text='三焦经\n(少阳)')


# ═══════════════════════════════════════════
#  后面 — 心系统 + 肾系统
# ═══════════════════════════════════════════

def draw_back_view(ax, cx=0, cy=5.0):
    draw_head(ax, cx, cy)
    draw_torso_front_back(ax, cx, cy)

    for s in [-1, 1]:
        # ── 手臂带状体积 ──
        arm_outer = [
            (cx + s * 1.7, cy + 2.4),    # 肩外侧 (连躯干肩)
            (cx + s * 2.1, cy + 1.3),    # 上臂外
            (cx + s * 2.45, cy + 0.2),   # 肘外
            (cx + s * 2.35, cy - 1.0),   # 前臂外
            (cx + s * 2.2, cy - 2.0),    # 腕外
        ]
        arm_inner = [
            (cx + s * 1.1, cy + 2.2),    # 肩内侧(腋,连躯干)
            (cx + s * 1.35, cy + 1.3),   # 上臂内
            (cx + s * 1.6, cy + 0.2),    # 肘内
            (cx + s * 1.55, cy - 1.0),   # 前臂内
            (cx + s * 1.45, cy - 2.0),   # 腕内
        ]
        draw_limb_band(ax, arm_outer, arm_inner)

        hand = mpatches.Ellipse((cx + s * 1.8, cy - 2.3), 0.75, 0.35,
                                fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=2)
        ax.add_patch(hand)

        # 手少阴心经 (HT): 胸 → 腋 → 手臂内侧(阴面) → 小指
        ht = [
            (cx + s * 0.4, cy + 2.1),    # 极泉(胸→腋)
            (cx + s * 0.85, cy + 1.5),   # 腋
            (cx + s * 1.25, cy + 0.6),   # 上臂内侧
            (cx + s * 1.55, cy - 0.2),   # 肘内侧
            (cx + s * 1.5, cy - 1.0),    # 前臂内侧
            (cx + s * 1.45, cy - 1.9),   # 腕 → 小指
        ]
        draw_meridian(ax, ht, C_HT, label_pt=(cx + s * 1.95, cy - 0.5),
                      label_text='心经\n(少阴)')

        # 手太阳小肠经 (SI): 小指 → 手臂外侧 → 肩后 → 颈 → 头顶(面)
        si = [
            (cx + s * 1.7, cy - 2.2),    # 小指
            (cx + s * 2.05, cy - 1.0),   # 前臂外侧
            (cx + s * 2.2, cy + 0.0),    # 肘外侧
            (cx + s * 1.9, cy + 1.2),    # 上臂外侧
            (cx + s * 1.55, cy + 1.85),  # 肩后
            (cx + s * 0.9, cy + 2.5),    # 肩胛 → 颈
            (cx + s * 0.35, cy + 3.2),   # 上达面(听宫)
            (cx + s * 0.1, cy + 4.3),    # → 头顶区
        ]
        draw_meridian(ax, si, C_SI, label_pt=(cx + s * 2.5, cy + 0.4),
                      label_text='小肠经\n(太阳)')

    for s in [-1, 1]:
        # ── 腿部带状体积 ──
        leg_outer = [
            (cx + s * 1.5, cy - 2.8),    # 髋外侧
            (cx + s * 1.1, cy - 5.5),    # 踝外侧
        ]
        leg_inner = [
            (cx + s * 0.4, cy - 2.8),    # 髋内侧
            (cx + s * 0.25, cy - 5.5),   # 踝内侧
        ]
        draw_limb_band(ax, leg_outer, leg_inner)

        foot = mpatches.Ellipse((cx + s * 0.65, cy - 5.85), 1.1, 0.35,
                                fc=BODY_FACE, ec=BODY_EDGE, lw=1.5, zorder=2)
        ax.add_patch(foot)

        # 足太阳膀胱经 (BL): 头顶 → 目内眦 → 头顶 → 项 → 背(双线) → 腿后 → 小趾
        bl = [
            (cx + s * 0.15, cy + 5.5),   # 头顶(百会区)
            (cx + s * 0.3, cy + 4.0),    # 头部
            (cx + s * 0.3, cy + 2.8),    # 目内眦(睛明)
            (cx + s * 0.25, cy + 2.0),   # 项后(天柱)
            (cx + s * 0.5, cy + 1.0),    # 背(脊柱旁1.5寸)
            (cx + s * 0.6, cy - 0.3),    # 腰背
            (cx + s * 0.65, cy - 1.6),   # 臀
            (cx + s * 0.8, cy - 2.8),    # 大腿后
            (cx + s * 0.85, cy - 3.8),   # 腘窝(委中)
            (cx + s * 0.7, cy - 4.9),    # 小腿后 → 外踝 → 小趾
        ]
        draw_meridian(ax, bl, C_BL, label_pt=(cx + s * 1.2, cy - 2.5),
                      label_text='膀胱经\n(太阳)')

        # 足少阴肾经 (KI): 足底 → 内踝后 → 小腿内 → 大腿内 → 腹 → 胸
        ki = [
            (cx + s * 0.55, cy - 5.4),   # 足底(涌泉)
            (cx + s * 0.5, cy - 4.3),    # 内踝后(太溪)
            (cx + s * 0.4, cy - 2.9),    # 小腿内侧
            (cx + s * 0.3, cy - 1.3),    # 大腿内侧
            (cx + s * 0.2, cy + 0.1),    # 腹部
            (cx + s * 0.15, cy + 1.5),   # 胸部(俞府)
        ]
        draw_meridian(ax, ki, C_KI, label_pt=(cx + s * 0.95, cy - 2.5),
                      label_text='肾经\n(少阴)')


# ═══════════════════════════════════════════
#  图例 & 标注
# ═══════════════════════════════════════════

def add_legend(ax, items, x=0.03, y=0.12):
    handles = [mpatches.Patch(color=c, label=l) for c, l in items]
    leg = ax.legend(handles=handles, loc='lower left', fontsize=7,
                    framealpha=0.88, edgecolor='#CCCCCC', bbox_to_anchor=(x, y))
    leg.get_title().set_fontsize(8)
    return leg


def add_system_label(ax, text, cx, cy):
    ax.text(cx, cy - 6.4, text, fontsize=8.5, ha='center', va='top',
            color='#888888', style='italic')


# ═══════════════════════════════════════════
#  主程序
# ═══════════════════════════════════════════

def main():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(25, 11.5))
    fig.patch.set_facecolor('#FAFAF8')
    cy = 5.0

    # ━━━ 前面 ━━━
    ax1.set_facecolor('#FEFEFC')
    draw_front_view(ax1, cx=0, cy=cy)
    ax1.set_title(u'前面\n肺系统 + 脾系统', fontsize=16, fontweight='bold',
                  color='#5A4A3A', pad=14, linespacing=1.4)
    ax1.set_xlim(-4.2, 4.2)
    ax1.set_ylim(cy - 6.8, cy + 6.0)
    ax1.set_aspect('equal')
    ax1.axis('off')
    add_legend(ax1, [(C_LU, u'手太阴肺经'), (C_LI, u'手阳明大肠经'),
                      (C_ST, u'足阳明胃经'), (C_SP, u'足太阴脾经')])
    add_system_label(ax1, u'前面布线：肺系统(金) + 脾系统(土)', 0, cy)

    # ━━━ 中间(侧视) ━━━
    ax2.set_facecolor('#FEFEFC')
    draw_middle_view(ax2, cx=0, cy=cy)
    ax2.set_title(u'中间（侧面）\n心包系统 + 肝系统', fontsize=16, fontweight='bold',
                  color='#5A4A3A', pad=14, linespacing=1.4)
    ax2.set_xlim(-1.5, 3.0)
    ax2.set_ylim(cy - 6.8, cy + 6.0)
    ax2.set_aspect('equal')
    ax2.axis('off')
    add_legend(ax2, [(C_PC, u'手厥阴心包经'), (C_TE, u'手少阳三焦经'),
                      (C_GB, u'足少阳胆经'), (C_LR_LIGHT, u'足厥阴肝经')],
               x=0.03, y=0.12)
    add_system_label(ax2, u'中间布线：心包系统(相火) + 肝系统(木)', 0, cy)

    # ━━━ 后面 ━━━
    ax3.set_facecolor('#FEFEFC')
    draw_back_view(ax3, cx=0, cy=cy)
    ax3.set_title(u'后面\n心系统 + 肾系统', fontsize=16, fontweight='bold',
                  color='#5A4A3A', pad=14, linespacing=1.4)
    ax3.set_xlim(-4.2, 4.2)
    ax3.set_ylim(cy - 6.8, cy + 6.0)
    ax3.set_aspect('equal')
    ax3.axis('off')
    add_legend(ax3, [(C_HT, u'手少阴心经'), (C_SI, u'手太阳小肠经'),
                      (C_BL, u'足太阳膀胱经'), (C_KI, u'足少阴肾经')])
    add_system_label(ax3, u'后面布线：心系统(君火) + 肾系统(水)', 0, cy)

    # ━━━ 总标题 & 底栏 ━━━
    fig.suptitle(u'人体十二正经布线概念图', fontsize=22, fontweight='bold', y=0.995, color='#3A3A3A')

    fig.text(0.5, 0.003,
             (u'■ 每层 4 条经 (手阴·手阳 + 足阳·足阴) = 前中后共 12 条  '
              u'■ 阴经行于内侧  阳经行于外侧  '
              u'■ 箭头 = 经气方向  '
              u'■ 阳经起/止于头, 阴经起/止于胸'),
             fontsize=8.5, ha='center', va='bottom', color='#AAAAAA',
             bbox=dict(boxstyle='round,pad=0.35', fc='#F5F5F0', ec='#E0E0D8', alpha=0.85))

    plt.tight_layout(rect=[0, 0.04, 1, 0.94])

    for ext in ['png', 'svg']:
        path = 'docs/public/body_meridians_concept.' + ext
        fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
        print('Saved to', path)
    plt.close(fig)


if __name__ == '__main__':
    main()
