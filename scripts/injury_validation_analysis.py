"""
EP-TSP — Elbow Injury Risk: Empirical Validation
Emerson Performance (EP)

wheeler-workload-fatigue-study built a literature-based elbow torque
proxy from arm angle alone. This project tests that proxy against real
Tommy John surgery history across 165 MLB starters (2020-2026) — moving
from a theoretical estimate to an empirical validation.

Uso:
    python scripts/injury_validation_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from ep_chart_style import *

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"


def load_data():
    df = pd.read_csv(DATA_DIR / "pitching_full_2020_2026.csv")
    df.columns = [c.strip() for c in df.columns]
    injured = pd.read_csv(DATA_DIR / "injury_list_full.csv")
    injured_names = set(injured["name"])

    per_pitcher = df.sort_values("year").groupby("last_name, first_name").first().reset_index()
    per_pitcher["has_tj_history"] = per_pitcher["last_name, first_name"].isin(injured_names)
    return per_pitcher


def summarize(df: pd.DataFrame) -> dict:
    tj = df[df["has_tj_history"]]
    no_tj = df[~df["has_tj_history"]]
    return {
        "n_tj": len(tj),
        "n_no_tj": len(no_tj),
        "arm_angle_tj": tj["arm_angle"].mean(),
        "arm_angle_no_tj": no_tj["arm_angle"].mean(),
        "velocity_tj": tj["ff_avg_speed"].mean(),
        "velocity_no_tj": no_tj["ff_avg_speed"].mean(),
    }


def plot_comparison(df: pd.DataFrame, lang: str) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6.5))
    fig.patch.set_facecolor(EP_COLORS["off_white"])

    tj = df[df["has_tj_history"]]
    no_tj = df[~df["has_tj_history"]]

    for ax, col, title_en, title_es in [
        (ax1, "arm_angle", "Arm Angle", "Arm Angle"),
        (ax2, "ff_avg_speed", "Fastball Velocity", "Velocidad de Fastball"),
    ]:
        apply_ep_style(fig, ax)
        labels = ["No TJ", "TJ history"] if lang == "en" else ["Sin TJ", "Con TJ"]
        bp = ax.boxplot([no_tj[col].dropna(), tj[col].dropna()],
                         labels=labels, patch_artist=True, widths=0.5, zorder=3)
        bp["boxes"][0].set_facecolor(EP_COLORS["navy"])
        bp["boxes"][1].set_facecolor(EP_COLORS["red"])
        for box in bp["boxes"]:
            box.set_alpha(0.75)
        # Colores de marca en vez de los defaults de matplotlib (bigotes/mediana/outliers
        # negros y naranja no existen en la paleta EP - se ven fuera de lugar)
        for whisker in bp["whiskers"]:
            whisker.set_color(EP_COLORS["navy"])
            whisker.set_linewidth(1.3)
        for cap in bp["caps"]:
            cap.set_color(EP_COLORS["navy"])
            cap.set_linewidth(1.3)
        for i, median in enumerate(bp["medians"]):
            # Color de mediana distinto por caja: blanco sobre navy (oscuro, alto contraste),
            # navy sobre rojo/salmón (más claro - blanco ahí se perdía, poco contraste)
            median.set_color(EP_COLORS["off_white"] if i == 0 else EP_COLORS["navy"])
            median.set_linewidth(2.8)
        for flier in bp["fliers"]:
            flier.set(marker="o", markerfacecolor=EP_COLORS["off_white"],
                      markeredgecolor=EP_COLORS["navy"], markersize=6)
        ax.set_title(title_en if lang == "en" else title_es, fontsize=12,
                     color=EP_COLORS["subtitle_grey"], pad=8)
        if FONT_TICK:
            for label in ax.get_xticklabels():
                label.set_fontproperties(FONT_TICK)
                label.set_fontsize(11)

    if lang == "en":
        fig.suptitle("Arm Angle Doesn't Separate Injured Pitchers From Healthy Ones",
                     fontsize=15.5, color=EP_COLORS["navy"], y=0.99,
                     fontproperties=FONT_TITLE if FONT_TITLE else None)
        fig.text(0.5, 0.925, "165 starters, 2020-2026 — 66 with confirmed Tommy John history, 99 without",
                  ha="center", fontsize=10.5, color=EP_COLORS["subtitle_grey"],
                  fontproperties=FONT_SUBTITLE_ITALIC if FONT_SUBTITLE_ITALIC else None)
        add_source(fig, "Source: Baseball Savant + Roegele Tommy John Surgery Database")
        fname = OUTPUT_DIR / "injury_comparison_EN.png"
    else:
        fig.suptitle("El Arm Angle No Separa a Pitchers Lesionados de los Sanos",
                     fontsize=14.5, color=EP_COLORS["navy"], y=0.99,
                     fontproperties=FONT_TITLE if FONT_TITLE else None)
        fig.text(0.5, 0.925, "165 abridores, 2020-2026 — 66 con historial confirmado de Tommy John, 99 sin él",
                  ha="center", fontsize=10.5, color=EP_COLORS["subtitle_grey"],
                  fontproperties=FONT_SUBTITLE_ITALIC if FONT_SUBTITLE_ITALIC else None)
        add_source(fig, "Fuente: Baseball Savant + base de datos de cirugías Tommy John de Roegele")
        fname = OUTPUT_DIR / "injury_comparison_ES.png"

    fig.tight_layout(rect=[0, 0.01, 1, 0.82])
    plt.savefig(fname, dpi=200, facecolor=EP_COLORS["off_white"])
    plt.close(fig)
    print(f"Guardado: {fname}")


if __name__ == "__main__":
    df = load_data()
    summary = summarize(df)
    print("=== Resumen ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    for lang in ["en", "es"]:
        plot_comparison(df, lang)

    df.to_csv(OUTPUT_DIR / "per_pitcher_injury_comparison.csv", index=False)
