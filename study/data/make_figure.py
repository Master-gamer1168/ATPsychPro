#!/usr/bin/env python3
"""Draw Figure 1 for the report from raw_data.csv (needs matplotlib).

Run:  python3 study/data/make_figure.py
Writes figure1_mean_rating_by_effort.png (300 dpi, grayscale for printing).

APA caption, which goes in the report text, not in the image:
  Figure 1
  Mean Combined Likeability and Quality Rating for Songs Described as Taking
  1 Week or 2 Days to Make
  Note. Ratings are the mean of likeability and quality ratings (1–11).
  Error bars show ±1 standard deviation; N = 32.
"""
import csv
import os
import statistics as st

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

rows = list(csv.DictReader(open(os.path.join(HERE, "raw_data.csv"), newline="")))
hi = [(int(r["liking_1wk"]) + int(r["quality_1wk"])) / 2 for r in rows]
lo = [(int(r["liking_2d"]) + int(r["quality_2d"])) / 2 for r in rows]
means = [st.mean(hi), st.mean(lo)]
sds = [st.stdev(hi), st.stdev(lo)]

plt.rcParams.update({"font.family": "serif", "font.serif": ["Liberation Serif", "DejaVu Serif"], "font.size": 12})
fig, ax = plt.subplots(figsize=(6.0, 4.2))
x = [0, 1]
ax.bar(x, means, width=0.5, color=["#5a5a5a", "#c4c4c4"], edgecolor="black", linewidth=0.8, zorder=2)
ax.errorbar(x, means, yerr=sds, fmt="none", ecolor="black", elinewidth=1, capsize=6, zorder=3)
for xi, m, s in zip(x, means, sds):
    ax.text(xi, m + s + 0.25, f"{m:.2f}", ha="center", va="bottom", fontsize=11)
ax.set_xticks(x, ["1 week\n(high effort)", "2 days\n(low effort)"])
ax.set_xlabel("Stated time taken to make the song")
ax.set_ylabel("Mean rating (1–11)")
ax.set_ylim(0, 11)  # full scale range, so the axis is not distorted
ax.set_yticks(range(0, 12, 1))
ax.set_xlim(-0.6, 1.6)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
fig.tight_layout()
out = os.path.join(HERE, "figure1_mean_rating_by_effort.png")
fig.savefig(out, dpi=300)
print(f"Wrote {out}: means {means[0]:.2f}/{means[1]:.2f}, SDs {sds[0]:.2f}/{sds[1]:.2f}")
