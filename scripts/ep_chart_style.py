"""
EP Chart Style — Módulo de estilo reutilizable para gráficos de Emerson Performance.

Aplica un sistema visual consistente (colores, tipografía real de marca,
jerarquía) a cualquier gráfico de matplotlib. Usa las fuentes oficiales EP
(Poppins para títulos, Lora para texto de cuerpo) en vez de la tipografía
default de matplotlib — la tipografía custom es la señal más fuerte de que
un gráfico es de una marca específica y no una plantilla genérica.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

_FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
_FONT_FILES = {
    "poppins_bold": "Poppins-Bold.ttf",
    "poppins_semibold": "Poppins-SemiBold.ttf",
    "poppins_medium": "Poppins-Medium.ttf",
    "poppins_regular": "Poppins-Regular.ttf",
    "lora_regular": "Lora-Regular.ttf",
    "lora_italic": "Lora-Italic.ttf",
}

EP_FONTS = {}
for _key, _fname in _FONT_FILES.items():
    _path = os.path.join(_FONT_DIR, _fname)
    if os.path.exists(_path):
        fm.fontManager.addfont(_path)
        EP_FONTS[_key] = fm.FontProperties(fname=_path)

FONT_TITLE = EP_FONTS.get("poppins_bold")
FONT_SUBTITLE_ITALIC = EP_FONTS.get("lora_italic")
FONT_LABEL = EP_FONTS.get("poppins_semibold")
FONT_TICK = EP_FONTS.get("lora_regular")

EP_COLORS = {
    "navy": "#0B1B33",
    "gold": "#D4A53A",
    "off_white": "#F5F3EC",
    "grid": "#D8D3C4",
    "subtitle_grey": "#555555",
    "red": "#B0413E",
    "green": "#4C7A5A",
}


def apply_ep_style(fig, ax):
    fig.patch.set_facecolor(EP_COLORS["off_white"])
    ax.set_facecolor(EP_COLORS["off_white"])
    ax.grid(True, axis="both", color=EP_COLORS["grid"], linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(EP_COLORS["navy"])
    ax.tick_params(colors=EP_COLORS["navy"])
    if FONT_TICK:
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(FONT_TICK)
            label.set_fontsize(10.5)


def add_reference_lines(ax, x=0, y=0):
    if x is not None:
        ax.axvline(x, color=EP_COLORS["navy"], linewidth=1, alpha=0.4, zorder=1)
    if y is not None:
        ax.axhline(y, color=EP_COLORS["navy"], linewidth=1, alpha=0.4, zorder=1)


def add_finding_title(fig, ax, finding: str, context: str = None):
    kwargs = {"fontsize": 17, "color": EP_COLORS["navy"], "y": 0.98}
    if FONT_TITLE:
        kwargs["fontproperties"] = FONT_TITLE
    else:
        kwargs["fontweight"] = "bold"
    fig.suptitle(finding, **kwargs)
    if context:
        kwargs2 = {"fontsize": 11, "color": EP_COLORS["subtitle_grey"], "pad": 14}
        if FONT_SUBTITLE_ITALIC:
            kwargs2["fontproperties"] = FONT_SUBTITLE_ITALIC
        else:
            kwargs2["style"] = "italic"
        ax.set_title(context, **kwargs2)


def add_stat_box(ax, text: str, loc=(0.03, 0.96)):
    kwargs = {"fontsize": 11, "color": EP_COLORS["navy"]}
    if FONT_LABEL:
        kwargs["fontproperties"] = FONT_LABEL
    else:
        kwargs["fontweight"] = "bold"
    ax.text(
        loc[0], loc[1], text, transform=ax.transAxes, va="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                  edgecolor=EP_COLORS["gold"], linewidth=1.5),
        **kwargs,
    )


def style_axis_label(ax, axis: str, text: str, fontsize=12):
    kwargs = {"fontsize": fontsize, "color": EP_COLORS["navy"]}
    if FONT_LABEL:
        kwargs["fontproperties"] = FONT_LABEL
    else:
        kwargs["fontweight"] = "bold"
    if axis == "x":
        ax.set_xlabel(text, **kwargs)
    else:
        ax.set_ylabel(text, **kwargs)


def directional_xlabel(ax, low_label: str, metric_label: str, high_label: str):
    # Sin flechas Unicode: Poppins no tiene esos glifos. Se usan palabras solas.
    style_axis_label(ax, "x", f"{low_label}          {metric_label}          {high_label}")


def directional_ylabel(ax, low_label: str, metric_label: str, high_label: str):
    style_axis_label(ax, "y", f"{low_label}          {metric_label}          {high_label}")


def label_point_direct(ax, x, y, text, offset=(3, -1.3), fontsize=11):
    kwargs = {"fontsize": fontsize, "color": EP_COLORS["navy"]}
    if FONT_LABEL:
        kwargs["fontproperties"] = FONT_LABEL
    else:
        kwargs["fontweight"] = "bold"
    ax.annotate(
        text, xy=(x, y), xytext=(x + offset[0], y + offset[1]),
        arrowprops=dict(arrowstyle="->", color=EP_COLORS["navy"], lw=1.5),
        **kwargs,
    )


def label_line_end(ax, x_end, y_end, text, color=None, offset=(0.5, 0)):
    kwargs = {"fontsize": 11, "color": color or EP_COLORS["navy"], "va": "center"}
    if FONT_LABEL:
        kwargs["fontproperties"] = FONT_LABEL
    else:
        kwargs["fontweight"] = "bold"
    ax.text(x_end + offset[0], y_end + offset[1], text, **kwargs)


def add_source(fig, text: str):
    kwargs = {"ha": "right", "fontsize": 8.5, "color": EP_COLORS["subtitle_grey"]}
    if FONT_SUBTITLE_ITALIC:
        kwargs["fontproperties"] = FONT_SUBTITLE_ITALIC
    else:
        kwargs["style"] = "italic"
    fig.text(0.99, 0.01, text, **kwargs)


if __name__ == "__main__":
    import numpy as np
    x = np.random.randn(100) * 5
    y = -0.05 * x + np.random.randn(100) * 2

    fig, ax = plt.subplots(figsize=(9, 6))
    apply_ep_style(fig, ax)
    add_reference_lines(ax)
    ax.scatter(x, y, color=EP_COLORS["navy"], alpha=0.5, s=60)
    add_finding_title(fig, ax, "Título de ejemplo: el hallazgo en una frase",
                       "Contexto de muestra: n=100, datos simulados")
    add_stat_box(ax, "r = -0.05\n(ejemplo)")
    directional_xlabel(ax, "menor", "VARIABLE X", "mayor")
    directional_ylabel(ax, "menor", "VARIABLE Y", "mayor")
    add_source(fig, "Source: demo data")
    fig.tight_layout()
    plt.savefig("epp_style_demo.png", dpi=150, facecolor=EP_COLORS["off_white"])
    print("Demo guardada")
