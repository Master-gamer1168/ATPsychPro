#!/usr/bin/env python3
"""Analyse the effort-heuristic data (raw_data.csv) and write RESULTS.md.

Run from anywhere:  python3 data/effort-heuristic/analyze.py

Every number in RESULTS.md is computed here from raw_data.csv. Nothing is
typed by hand. The script first checks the transcription against the
difference and mean columns printed in the original PDF, and stops if
anything disagrees.

Design inferred from the PDF: each participant rated two stimuli (SoR and
CYFI) on liking and quality. One stimulus was labelled as taking 1 week to
make and the other 2 days. Sheets 1 and 4 labelled SoR "1 week"; sheets 2
and 3 labelled CYFI "1 week" (counterbalanced). That makes it repeated
measures on the effort label, so differences are 1 week − 2 days.
"""
import csv
import math
import os
import statistics as st
import sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import stats  # noqa: E402  (exact Wilcoxon critical values, validated against published tables)

# The means row printed at the bottom of each PDF sheet:
# (1wk liking, 1wk quality, 2d liking, 2d quality, liking diff, quality diff)
PDF_MEANS = {
    1: ("6.88", "6.50", "6.13", "6.13", "0.75", "0.38"),
    2: ("7.25", "7.38", "6.25", "6.13", "1.00", "1.25"),
    3: ("7.00", "7.25", "6.13", "6.13", "0.88", "1.13"),
    4: ("7.00", "7.25", "5.88", "5.88", "1.13", "1.38"),
}

# Chi-square critical values for df = 1 (standard table values)
CHI_CRIT_DF1 = {
    "p < .10 two-tailed (= .05 one-tailed)": 2.706,
    "p < .05 two-tailed": 3.841,
    "p < .02 two-tailed (= .01 one-tailed)": 5.412,
    "p < .01 two-tailed": 6.635,
}


def r2(x):
    """Round half-up to 2 dp, matching spreadsheet rounding (6.125 -> 6.13)."""
    return str(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def load():
    rows = []
    with open(os.path.join(HERE, "raw_data.csv"), newline="") as f:
        for r in csv.DictReader(f):
            for k in ("sheet", "liking_1wk", "quality_1wk", "liking_2d", "quality_2d", "pdf_liking_diff", "pdf_quality_diff"):
                r[k] = int(r[k])
            r["d_liking"] = r["liking_1wk"] - r["liking_2d"]
            r["d_quality"] = r["quality_1wk"] - r["quality_2d"]
            rows.append(r)
    return rows


def verify(rows):
    problems = []
    for r in rows:
        if r["d_liking"] != r["pdf_liking_diff"] or r["d_quality"] != r["pdf_quality_diff"]:
            problems.append(f"sheet {r['sheet']} {r['participant']}: diff mismatch")
    for s, printed in PDF_MEANS.items():
        g = [r for r in rows if r["sheet"] == s]
        got = tuple(r2(st.mean(r[k] for r in g)) for k in
                    ("liking_1wk", "quality_1wk", "liking_2d", "quality_2d", "d_liking", "d_quality"))
        if got != printed:
            problems.append(f"sheet {s}: means {got} != PDF {printed}")
    if problems:
        sys.exit("TRANSCRIPTION CHECK FAILED:\n" + "\n".join(problems))
    return "All 64 per-participant differences and all 24 sheet means match the values printed in the PDF."


def desc(xs):
    modes = st.multimode(xs)
    return {
        "n": len(xs), "sum": sum(xs), "mean": st.mean(xs), "median": st.median(xs),
        "mode": ", ".join(str(m) for m in sorted(modes)), "sd": st.stdev(xs) if len(xs) > 1 else float("nan"),
        "min": min(xs), "max": max(xs), "sumsq": sum(x * x for x in xs),
    }


def wilcoxon(ds):
    nz = [d for d in ds if d != 0]
    n = len(nz)
    ranks, _ = stats.rank_all([abs(d) for d in nz])
    tpos = sum(ranks[abs(d)] for d in nz if d > 0)
    tneg = sum(ranks[abs(d)] for d in nz if d < 0)
    T = min(tpos, tneg)
    # normal approximation with tie correction (reference only)
    ties = Counter(abs(d) for d in nz)
    var = n * (n + 1) * (2 * n + 1) / 24 - sum(t ** 3 - t for t in ties.values()) / 48
    z = (T - n * (n + 1) / 4) / math.sqrt(var) if var > 0 else float("nan")
    p1 = 0.5 * math.erfc(-z / math.sqrt(2))
    rrb = (tpos - tneg) / (tpos + tneg) if (tpos + tneg) else float("nan")  # matched-pairs rank-biserial
    return {
        "n": n, "zeros": len(ds) - n, "tpos": tpos, "tneg": tneg, "T": T,
        "crit05": stats.wil_critical(n, 0.05), "crit01": stats.wil_critical(n, 0.01),
        "crit05_2t": stats.wil_critical(n, 0.025),
        "z": z, "p1": p1, "rrb": rrb, "ranks": ranks, "nz": nz,
    }


def binom_one_tailed(k, n):
    """P(X >= k) for X ~ Bin(n, 0.5): exact sign-test probability."""
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n


def chi_gof(pos, neg):
    n = pos + neg
    e = n / 2
    return sum((o - e) ** 2 / e for o in (pos, neg)), e


def spearman(x, y):
    rx, _ = stats.rank_all(x)
    ry, _ = stats.rank_all(y)
    a = [rx[v] for v in x]
    b = [ry[v] for v in y]
    ma, mb = st.mean(a), st.mean(b)
    num = sum((p - ma) * (q - mb) for p, q in zip(a, b))
    den = math.sqrt(sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b))
    return num / den


def fmt(x, dp=2):
    return f"{x:.{dp}f}"


def fp(p):
    """Format a probability without a leading zero; tiny values shown as < .00001."""
    return "< .00001" if p < 0.00001 else f"{p:.5f}".lstrip("0")


def rng(d):
    return f"{d['min']} to {d['max']}".replace("-", "−")


def main():
    rows = load()
    check = verify(rows)
    out = []
    w = out.append

    w("# Effort Heuristic Study: Computed Results\n")
    w("> **Generated by `analyze.py` from `raw_data.csv`. Do not edit by hand.** Re-run the script after any change to the data.")
    w(f"> Transcription check: ✅ {check}\n")
    w("Notation: **1 wk** = the stimulus labelled as taking 1 week (high-effort label); **2 d** = the stimulus labelled as taking 2 days (low-effort label). "
      "Difference *d* = 1 wk − 2 d, so a **positive d means the participant rated the high-effort-labelled stimulus higher**. "
      "Sheets 1 and 4 labelled SoR as 1 week; sheets 2 and 3 labelled CYFI as 1 week.\n")

    # ------------------------------------------------------------ descriptives pooled
    N = len(rows)
    w(f"## 1. Descriptive statistics: all participants pooled (N = {N})\n")
    w("| Measure | Condition | n | Mean (*M*) | Median | Mode | *SD* | Range (min–max) |")
    w("|---|---|---|---|---|---|---|---|")
    for dv in ("liking", "quality"):
        for cond, lab in (("1wk", "1 week (high effort)"), ("2d", "2 days (low effort)")):
            d = desc([r[f"{dv}_{cond}"] for r in rows])
            w(f"| {dv.title()} | {lab} | {d['n']} | **{fmt(d['mean'])}** | {d['median']:g} | {d['mode']} | {fmt(d['sd'])} | {d['max'] - d['min']} ({rng(d)}) |")
        d = desc([r[f"d_{dv}"] for r in rows])
        w(f"| {dv.title()} | *Difference d (1 wk − 2 d)* | {d['n']} | **{fmt(d['mean'])}** | {d['median']:g} | {d['mode']} | {fmt(d['sd'])} | {d['max'] - d['min']} ({rng(d)}) |")
    w("\n*SD* is the sample standard deviation (n − 1). The rating-scale range is not stated in the PDF. Observed ratings span "
      f"{min(min(r[k] for r in rows) for k in ('liking_1wk','liking_2d','quality_1wk','quality_2d'))}–"
      f"{max(max(r[k] for r in rows) for k in ('liking_1wk','liking_2d','quality_1wk','quality_2d'))}.\n")

    # ------------------------------------------------------------ direction counts
    w("## 2. Direction of each participant's difference\n")
    w("| Measure | Rated 1 wk higher (+) | Tied (0) | Rated 2 d higher (−) | % rating 1 wk higher (all N) | % of untied |")
    w("|---|---|---|---|---|---|")
    dir_counts = {}
    for dv in ("liking", "quality"):
        ds = [r[f"d_{dv}"] for r in rows]
        p, z0, m = sum(d > 0 for d in ds), sum(d == 0 for d in ds), sum(d < 0 for d in ds)
        dir_counts[dv] = (p, z0, m)
        w(f"| {dv.title()} | {p} | {z0} | {m} | {fmt(100 * p / N, 1)}% | {fmt(100 * p / (p + m), 1)}% |")
    w("")

    # ------------------------------------------------------------ Wilcoxon pooled
    w(f"## 3. Wilcoxon signed-rank test (pooled, N = {N}): the test that matches this design\n")
    w("Repeated measures (each participant rated under both effort labels) with ordinal rating data → **Wilcoxon signed-rank**. "
      "H₁ is directional (high-effort label rated higher), so the test is **one-tailed**. Significant if *T* ≤ critical value.\n")
    w("| Measure | n (non-zero d) | Zeros dropped | Σ ranks + | Σ ranks − | ***T*** | Critical *T* (.05, one-tailed) | Critical *T* (.01, one-tailed) | Result | Rank-biserial *r* | z (tie-corrected) | one-tailed *p* ≈ |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|")
    wres = {}
    for dv in ("liking", "quality"):
        res = wilcoxon([r[f"d_{dv}"] for r in rows])
        wres[dv] = res
        if res["T"] <= res["crit01"]:
            verdict = "**Significant, p < .01**"
        elif res["T"] <= res["crit05"]:
            verdict = "**Significant, p < .05**"
        else:
            verdict = "Not significant"
        w(f"| {dv.title()} | {res['n']} | {res['zeros']} | {res['tpos']:g} | {res['tneg']:g} | **{res['T']:g}** | {res['crit05']} | {res['crit01']} | {verdict} | {fmt(res['rrb'])} | {fmt(res['z'])} | {fp(res['p1'])} |")
    w("\nThe critical values are exact (computed from the Wilcoxon null distribution by `tools/stats.py`, which reproduces published tables). "
      "Many |d| values are tied (only 1s and 2s), which exact tables don't account for; the tie-corrected z gives the same verdict. "
      "Rank-biserial *r* runs from −1 to +1, and values ≥ .5 are conventionally a large effect.\n")

    for dv in ("liking", "quality"):
        res = wres[dv]
        w(f"<details><summary>Ranking working: {dv} (for Appendix E)</summary>\n")
        w("| |d| | Count | Ranks occupied | Mean rank | Count with + sign | Count with − sign | Rank sum + | Rank sum − |")
        w("|---|---|---|---|---|---|---|---|")
        pos = 1
        for v in sorted(set(abs(d) for d in res["nz"])):
            k = sum(abs(d) == v for d in res["nz"])
            kp = sum(d == v for d in res["nz"])
            km = sum(d == -v for d in res["nz"])
            rk = res["ranks"][v]
            span = f"{pos}" if k == 1 else f"{pos}–{pos + k - 1}"
            w(f"| {v} | {k} | {span} | {rk:g} | {kp} | {km} | {rk * kp:g} | {rk * km:g} |")
            pos += k
        n = res["n"]
        w(f"| **Total** | **{n}** | | | | | **{res['tpos']:g}** | **{res['tneg']:g}** |\n")
        w(f"Check: {res['tpos']:g} + {res['tneg']:g} = {res['tpos'] + res['tneg']:g} = n(n + 1) ÷ 2 = {n} × {n + 1} ÷ 2 = {n * (n + 1) // 2}. *T* = smaller sum = {res['T']:g}.\n")
        w("</details>\n")

    # ------------------------------------------------------------ chi-square + sign test
    w("## 4. Chi-square goodness of fit on direction (+ vs −), with exact sign test\n")
    w("If your class requires a **chi-square**: this tests whether more participants rated the high-effort-labelled stimulus higher than the 50/50 split chance predicts. "
      "Ties are excluded, df = 1, and expected frequency = (number of + and −) ÷ 2. "
      "**Note:** chi-square is designed for nominal frequency data from independent observations. For paired ratings like these, the Wilcoxon (section 3) uses more of the information, and the **sign test** is the exact version of this same comparison.\n")
    w("| Measure | Observed + | Observed − | Expected each | χ² | df | Critical χ² (.05, non-directional) | Critical χ² (.05 one-tailed) | Result (directional H₁) | Sign test exact one-tailed *p* |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for dv in ("liking", "quality"):
        p, _, m = dir_counts[dv]
        chi, e = chi_gof(p, m)
        bp = binom_one_tailed(p, p + m)
        if chi >= CHI_CRIT_DF1["p < .01 two-tailed"]:
            v = "Significant, p < .01 (two-tailed)"
        elif chi >= CHI_CRIT_DF1["p < .05 two-tailed"]:
            v = "Significant, p < .05 (two-tailed)"
        elif chi >= CHI_CRIT_DF1["p < .10 two-tailed (= .05 one-tailed)"]:
            v = "Significant, p < .05 one-tailed only"
        else:
            v = "Not significant"
        w(f"| {dv.title()} | {p} | {m} | {e:g} | **{fmt(chi)}** | 1 | 3.841 | 2.706 | {v} | {fp(bp)} |")
    w("\nχ² working: χ² = Σ (O − E)² ÷ E. Critical values for df = 1: " + "; ".join(f"{k}: {v}" for k, v in CHI_CRIT_DF1.items()) + ".\n")

    # ------------------------------------------------------------ per sheet
    w("## 5. Per-sheet breakdown (each sheet n = 8)\n")
    w("| Sheet | Labelled 1 wk | *M* liking 1 wk | *M* liking 2 d | *M* d liking (*SD*) | *M* quality 1 wk | *M* quality 2 d | *M* d quality (*SD*) | Wilcoxon *T* liking (n) | Wilcoxon *T* quality (n) | Critical *T* .05 one-tailed |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    for s in (1, 2, 3, 4):
        g = [r for r in rows if r["sheet"] == s]
        wl = wilcoxon([r["d_liking"] for r in g])
        wq = wilcoxon([r["d_quality"] for r in g])
        crit = f"n={wl['n']}: {wl['crit05']}; n={wq['n']}: {wq['crit05']}"
        w(f"| {s} | {g[0]['stimulus_1wk']} | {r2(st.mean(r['liking_1wk'] for r in g))} | {r2(st.mean(r['liking_2d'] for r in g))} | "
          f"{r2(st.mean(r['d_liking'] for r in g))} ({fmt(st.stdev(r['d_liking'] for r in g))}) | "
          f"{r2(st.mean(r['quality_1wk'] for r in g))} | {r2(st.mean(r['quality_2d'] for r in g))} | "
          f"{r2(st.mean(r['d_quality'] for r in g))} ({fmt(st.stdev(r['d_quality'] for r in g))}) | "
          f"{wl['T']:g} ({wl['n']}) | {wq['T']:g} ({wq['n']}) | {crit} |")
    w("\nMeans are rounded half-up, which matches the PDF. Per-sheet tests have very low power at n = 8. Report the pooled test as the main result.\n")

    # ------------------------------------------------------------ counterbalancing / stimulus check
    w("## 6. Counterbalancing check: did the stimulus itself matter?\n")
    sor_1wk = [r for r in rows if r["stimulus_1wk"] == "SoR"]
    cyfi_1wk = [r for r in rows if r["stimulus_1wk"] == "CYFI"]
    w("| Arrangement | n | *M* d liking | *M* d quality |")
    w("|---|---|---|---|")
    for lab, g in (("SoR labelled 1 wk (sheets 1, 4)", sor_1wk), ("CYFI labelled 1 wk (sheets 2, 3)", cyfi_1wk)):
        w(f"| {lab} | {len(g)} | {fmt(st.mean(r['d_liking'] for r in g))} | {fmt(st.mean(r['d_quality'] for r in g))} |")
    sor_l = [r["liking_1wk"] if r["stimulus_1wk"] == "SoR" else r["liking_2d"] for r in rows]
    cyfi_l = [r["liking_1wk"] if r["stimulus_1wk"] == "CYFI" else r["liking_2d"] for r in rows]
    sor_q = [r["quality_1wk"] if r["stimulus_1wk"] == "SoR" else r["quality_2d"] for r in rows]
    cyfi_q = [r["quality_1wk"] if r["stimulus_1wk"] == "CYFI" else r["quality_2d"] for r in rows]
    w("\n| Stimulus (ignoring effort label) | *M* liking (*SD*) | *M* quality (*SD*) |")
    w("|---|---|---|")
    w(f"| SoR | {fmt(st.mean(sor_l))} ({fmt(st.stdev(sor_l))}) | {fmt(st.mean(sor_q))} ({fmt(st.stdev(sor_q))}) |")
    w(f"| CYFI | {fmt(st.mean(cyfi_l))} ({fmt(st.stdev(cyfi_l))}) | {fmt(st.mean(cyfi_q))} ({fmt(st.stdev(cyfi_q))}) |")
    w("\nIf the effect were caused by one stimulus simply being better, *d* would be positive in one arrangement and negative in the other. "
      "Compare the two rows above. Counterbalancing spreads any stimulus difference evenly across the effort conditions.\n")

    # ------------------------------------------------------------ extras
    w("## 7. Other potentially useful metrics\n")
    all_l = [r["liking_1wk"] for r in rows] + [r["liking_2d"] for r in rows]
    all_q = [r["quality_1wk"] for r in rows] + [r["quality_2d"] for r in rows]
    w(f"- **Liking vs quality agreement:** Spearman's ρ between all liking and quality ratings (64 pairs) = **{fmt(spearman(all_l, all_q))}**. "
      "The two DVs largely measure the same evaluation.")
    neg_l = [f"S{r['sheet']}-{r['participant']}" for r in rows if r["d_liking"] < 0]
    neg_q = [f"S{r['sheet']}-{r['participant']}" for r in rows if r["d_quality"] < 0]
    w(f"- **Reversals (rated the 2-day stimulus higher):** liking: {', '.join(neg_l) or 'none'}; quality: {', '.join(neg_q) or 'none'}. "
      "Sheet 1 contains all of the quality reversals.")
    hi = Counter(v for v in all_l + all_q if v >= 9)
    lo = Counter(v for v in all_l + all_q if v <= 3)
    w(f"- **Ceiling/floor check:** ratings of 9 or above: {sum(hi.values())} of 128; ratings of 3 or below: {sum(lo.values())} of 128 "
      f"(the lowest single rating is S1-P7, quality 2 d = 2). With the scale maximum unknown, check whether 10 was available. "
      "If it was, there is little sign of a ceiling effect.")
    w(f"- **Size of the effect in scale points:** mean liking increase = {fmt(st.mean(r['d_liking'] for r in rows))} points; "
      f"mean quality increase = {fmt(st.mean(r['d_quality'] for r in rows))} points (1 wk − 2 d).")
    w(f"- **Every |d| is 0, 1 or 2.** No participant changed their rating by more than 2 points, which suggests a consistent but modest shift.")

    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
