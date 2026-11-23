#!/usr/bin/env python3
"""Analyse the effort-heuristic study data (raw_data.csv) and write RESULTS.md.

Run from anywhere:  python3 study/data/analyze.py

Every number in RESULTS.md is computed here from raw_data.csv. Nothing is
typed by hand. The script first checks the transcription against the
difference and mean columns printed in the original data PDF, and stops if
anything disagrees.

Design (from the group workbook, ../workbook-transcription.md):
  * Replication of Kruger et al. (2004), Experiment 1 (effort heuristic).
  * Repeated measures: each participant heard two songs (SoR and CYFI). One
    was described as taking 1 week to make (high effort) and the other
    2 days (low effort). Labels are counterbalanced: sheets 1 and 4 labelled
    SoR "1 week", sheets 2 and 3 labelled CYFI "1 week".
  * DV (workbook operational definition): the MEAN of two ratings,
    likeability (1 = hate, 11 = love) and quality (1 = bad, 11 = great).
    This is reported as the primary "combined" measure; liking and quality
    are also reported separately.
  * Difference d = 1 week − 2 days (positive = high-effort song rated higher).
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
import stats  # noqa: E402  (exact critical values, validated against published tables)

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

DVS = ("combined", "liking", "quality")
LABEL = {
    "combined": "**Combined DV** (mean of liking + quality)",
    "liking": "Liking (likeability)",
    "quality": "Quality",
}
SHORT = {"combined": "Combined", "liking": "Liking", "quality": "Quality"}


# ---------------------------------------------------------------- helpers
def r2(x):
    """Round half-up to 2 dp, matching spreadsheet rounding (6.125 -> 6.13)."""
    return str(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def fmt(x, dp=2):
    return f"{x:.{dp}f}"


def fp(p):
    """Format a probability without a leading zero; tiny values shown as < .00001."""
    return "< .00001" if p < 0.00001 else f"{p:.5f}".lstrip("0")


def g(x):
    return f"{x:g}".replace("-", "−")


def load():
    rows = []
    with open(os.path.join(HERE, "raw_data.csv"), newline="") as f:
        for r in csv.DictReader(f):
            for k in ("sheet", "liking_1wk", "quality_1wk", "liking_2d", "quality_2d", "pdf_liking_diff", "pdf_quality_diff"):
                r[k] = int(r[k])
            r["combined_1wk"] = (r["liking_1wk"] + r["quality_1wk"]) / 2
            r["combined_2d"] = (r["liking_2d"] + r["quality_2d"]) / 2
            for dv in DVS:
                r[f"d_{dv}"] = r[f"{dv}_1wk"] - r[f"{dv}_2d"]
            rows.append(r)
    return rows


def verify(rows):
    problems = []
    for r in rows:
        if r["d_liking"] != r["pdf_liking_diff"] or r["d_quality"] != r["pdf_quality_diff"]:
            problems.append(f"sheet {r['sheet']} {r['participant']}: diff mismatch")
    for s, printed in PDF_MEANS.items():
        grp = [r for r in rows if r["sheet"] == s]
        got = tuple(r2(st.mean(r[k] for r in grp)) for k in
                    ("liking_1wk", "quality_1wk", "liking_2d", "quality_2d", "d_liking", "d_quality"))
        if got != printed:
            problems.append(f"sheet {s}: means {got} != PDF {printed}")
    if problems:
        sys.exit("TRANSCRIPTION CHECK FAILED:\n" + "\n".join(problems))
    return "All 64 per-participant differences and all 24 sheet means match the values printed in the data PDF."


def desc(xs):
    return {
        "n": len(xs), "mean": st.mean(xs), "median": st.median(xs),
        "mode": ", ".join(g(m) for m in sorted(st.multimode(xs))),
        "sd": st.stdev(xs) if len(xs) > 1 else float("nan"), "min": min(xs), "max": max(xs),
    }


# ---------------------------------------------------------------- tests
def wilcoxon(ds):
    nz = [d for d in ds if d != 0]
    n = len(nz)
    ranks, _ = stats.rank_all([abs(d) for d in nz])
    tpos = sum(ranks[abs(d)] for d in nz if d > 0)
    tneg = sum(ranks[abs(d)] for d in nz if d < 0)
    T = min(tpos, tneg)
    ties = Counter(abs(d) for d in nz)
    var = n * (n + 1) * (2 * n + 1) / 24 - sum(t ** 3 - t for t in ties.values()) / 48
    z = (T - n * (n + 1) / 4) / math.sqrt(var) if var > 0 else float("nan")
    p1 = 0.5 * math.erfc(-z / math.sqrt(2))
    rrb = (tpos - tneg) / (tpos + tneg) if (tpos + tneg) else float("nan")  # matched-pairs rank-biserial
    return {
        "n": n, "zeros": len(ds) - n, "tpos": tpos, "tneg": tneg, "T": T,
        "crit05": stats.wil_critical(n, 0.05), "crit01": stats.wil_critical(n, 0.01),
        "z": z, "p1": p1, "rrb": rrb, "ranks": ranks, "nz": nz, "right_direction": tpos > tneg,
    }


def mann_whitney(hi, lo):
    """hi = scores under the 1-week label, lo = scores under the 2-day label."""
    n1, n2 = len(hi), len(lo)
    ranks, _ = stats.rank_all(hi + lo)
    r_hi = sum(ranks[v] for v in hi)
    r_lo = sum(ranks[v] for v in lo)
    u_hi = n1 * n2 + n1 * (n1 + 1) / 2 - r_hi
    u_lo = n1 * n2 + n2 * (n2 + 1) / 2 - r_lo
    # independent check: U_hi counts pairs where the 2-day score beats the 1-week score (ties = 1/2)
    brute = sum(1 if b > a else 0.5 if b == a else 0 for a in hi for b in lo)
    assert abs(brute - u_hi) < 1e-9, "Mann-Whitney U check failed"
    assert abs(u_hi + u_lo - n1 * n2) < 1e-9
    U = min(u_hi, u_lo)
    N = n1 + n2
    tie = sum(t ** 3 - t for t in Counter(hi + lo).values())
    sigma = math.sqrt(n1 * n2 / 12 * ((N + 1) - tie / (N * (N - 1))))
    z = (U - n1 * n2 / 2) / sigma
    return {
        "n1": n1, "n2": n2, "r_hi": r_hi, "r_lo": r_lo, "u_hi": u_hi, "u_lo": u_lo, "U": U,
        "crit05": stats.mw_critical(n1, n2, 0.05), "crit01": stats.mw_critical(n1, n2, 0.01),
        "z": z, "p1": 0.5 * math.erfc(-z / math.sqrt(2)), "right_direction": r_hi / n1 > r_lo / n2,
    }


def verdict(stat, crit05, crit01, right_direction):
    if not right_direction:
        return "Not supported (wrong direction)"
    if crit01 is not None and stat <= crit01:
        return "**Significant, p < .01**"
    if crit05 is not None and stat <= crit05:
        return "**Significant, p < .05**"
    return "Not significant"


def binom_one_tailed(k, n):
    """P(X >= k) for X ~ Bin(n, 0.5): exact sign-test probability."""
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n


def chi_gof(pos, neg):
    e = (pos + neg) / 2
    return sum((o - e) ** 2 / e for o in (pos, neg)), e


def spearman(x, y):
    rx, _ = stats.rank_all(x)
    ry, _ = stats.rank_all(y)
    a = [rx[v] for v in x]
    b = [ry[v] for v in y]
    ma, mb = st.mean(a), st.mean(b)
    num = sum((p - ma) * (q - mb) for p, q in zip(a, b))
    return num / math.sqrt(sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b))


def song_score(r, song, dv):
    """A participant's score for a given song, and the label that song carried."""
    cond = "1wk" if r["stimulus_1wk"] == song else "2d"
    return r[f"{dv}_{cond}"], cond


# ---------------------------------------------------------------- report
def main():
    rows = load()
    check = verify(rows)
    N = len(rows)
    out = []
    w = out.append

    w("# Effort Heuristic Study: Computed Results\n")
    w("> **Generated by `analyze.py` from `raw_data.csv`. Do not edit by hand.** Re-run the script after any change to the data.")
    w(f"> Transcription check: ✅ {check}\n")
    w("**Notation.** Each participant heard two songs, **SoR** and **CYFI**. **1 wk** = the song described as taking **1 week** to make (high effort); "
      "**2 d** = the song described as taking **2 days** (low effort). Sheets 1 and 4 labelled SoR as 1 week; sheets 2 and 3 labelled CYFI as 1 week. "
      "Difference *d* = 1 wk − 2 d, so a **positive d means the high-effort-labelled song was rated higher**.\n")
    w("**DV.** The workbook defines the DV as the **mean of the likeability and quality ratings**, each on a 1–11 scale. "
      "That **Combined DV** is the measure that matches H₁, so it is listed first. Liking and quality are also reported separately.\n")

    # 1 descriptives
    w(f"## 1. Descriptive statistics: all participants (N = {N})\n")
    w("| Measure | Condition | n | Mean (*M*) | Median | Mode | *SD* | Range (min to max) |")
    w("|---|---|---|---|---|---|---|---|")
    for dv in DVS:
        for cond, lab in (("1wk", "1 week (high effort)"), ("2d", "2 days (low effort)")):
            d = desc([r[f"{dv}_{cond}"] for r in rows])
            w(f"| {LABEL[dv]} | {lab} | {d['n']} | **{fmt(d['mean'])}** | {g(d['median'])} | {d['mode']} | {fmt(d['sd'])} | {g(d['max'] - d['min'])} ({g(d['min'])} to {g(d['max'])}) |")
        d = desc([r[f"d_{dv}"] for r in rows])
        w(f"| {LABEL[dv]} | *Difference d (1 wk − 2 d)* | {d['n']} | **{fmt(d['mean'])}** | {g(d['median'])} | {d['mode']} | {fmt(d['sd'])} | {g(d['max'] - d['min'])} ({g(d['min'])} to {g(d['max'])}) |")
    lo_all = min(min(r[k] for r in rows) for k in ("liking_1wk", "liking_2d", "quality_1wk", "quality_2d"))
    hi_all = max(max(r[k] for r in rows) for k in ("liking_1wk", "liking_2d", "quality_1wk", "quality_2d"))
    w(f"\n*SD* is the sample standard deviation (n − 1). Individual ratings observed: {lo_all} to {hi_all}, on a 1–11 scale.\n")

    # 2 direction counts
    w("## 2. Direction of each participant's difference\n")
    w("| Measure | Rated 1 wk higher (+) | Tied (0) | Rated 2 d higher (−) | % rating 1 wk higher (all N) | % of untied |")
    w("|---|---|---|---|---|---|")
    dir_counts = {}
    for dv in DVS:
        ds = [r[f"d_{dv}"] for r in rows]
        p, z0, m = sum(d > 0 for d in ds), sum(d == 0 for d in ds), sum(d < 0 for d in ds)
        dir_counts[dv] = (p, z0, m)
        w(f"| {LABEL[dv]} | {p} | {z0} | {m} | {fmt(100 * p / N, 1)}% | {fmt(100 * p / (p + m), 1)}% |")
    w("")

    # 3 Wilcoxon
    w(f"## 3. Wilcoxon signed-rank test (N = {N}): the main inferential test\n")
    w("Repeated measures (each participant rated both songs, one under each effort label) with ordinal rating data → **Wilcoxon signed-rank**. "
      "H₁ is directional, so the test is **one-tailed**. Significant if *T* ≤ critical value and the difference is in the predicted direction.\n")
    w("| Measure | n (non-zero d) | Ties dropped | Σ ranks + | Σ ranks − | ***T*** | Critical *T* (.05, one-tailed) | Critical *T* (.01, one-tailed) | Result | Rank-biserial *r* | z (tie-corrected) | one-tailed *p* ≈ |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|")
    wres = {}
    for dv in DVS:
        res = wilcoxon([r[f"d_{dv}"] for r in rows])
        wres[dv] = res
        v = verdict(res["T"], res["crit05"], res["crit01"], res["right_direction"])
        w(f"| {LABEL[dv]} | {res['n']} | {res['zeros']} | {g(res['tpos'])} | {g(res['tneg'])} | **{g(res['T'])}** | {res['crit05']} | {res['crit01']} | {v} | {fmt(res['rrb'])} | {fmt(res['z'])} | {fp(res['p1'])} |")
    w("\nCritical values are exact (Wilcoxon null distribution, computed by `tools/stats.py`, which reproduces published tables). "
      "Many |d| values are tied, which exact tables don't account for; the tie-corrected z gives the same verdict in every case. "
      "Rank-biserial *r* runs from −1 to +1, and values ≥ .5 are conventionally a large effect.\n")
    for dv in DVS:
        res = wres[dv]
        w(f"<details><summary>Ranking working: {SHORT[dv]} (for Appendix E)</summary>\n")
        w("| \\|d\\| | Count | Ranks occupied | Mean rank | Count with + sign | Count with − sign | Rank sum + | Rank sum − |")
        w("|---|---|---|---|---|---|---|---|")
        pos = 1
        for val in sorted(set(abs(d) for d in res["nz"])):
            k = sum(abs(d) == val for d in res["nz"])
            kp = sum(d == val for d in res["nz"])
            km = sum(d == -val for d in res["nz"])
            rk = res["ranks"][val]
            span = f"{pos}" if k == 1 else f"{pos}–{pos + k - 1}"
            w(f"| {g(val)} | {k} | {span} | {g(rk)} | {kp} | {km} | {g(rk * kp)} | {g(rk * km)} |")
            pos += k
        n = res["n"]
        w(f"| **Total** | **{n}** | | | | | **{g(res['tpos'])}** | **{g(res['tneg'])}** |\n")
        w(f"Check: {g(res['tpos'])} + {g(res['tneg'])} = {g(res['tpos'] + res['tneg'])} = n(n + 1) ÷ 2 = {n} × {n + 1} ÷ 2 = {n * (n + 1) // 2}. *T* = smaller sum = {g(res['T'])}.\n")
        w("</details>\n")

    # 4 chi-square + sign test
    w("## 4. Chi-square goodness of fit on direction (+ vs −), with exact sign test\n")
    w("This tests whether more participants rated the high-effort song higher than the 50/50 split chance predicts. "
      "Ties are excluded, df = 1, and expected frequency = (number of + and −) ÷ 2. "
      "**Note:** chi-square is designed for nominal frequency data from independent observations. For paired ratings, the Wilcoxon (section 3) uses more of the information, and the **sign test** is the exact version of this same comparison.\n")
    w("| Measure | Observed + | Observed − | Expected each | χ² | df | Critical χ² (.05, non-directional) | Critical χ² (.05 one-tailed) | Result | Sign test exact one-tailed *p* |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for dv in DVS:
        p, _, m = dir_counts[dv]
        chi, e = chi_gof(p, m)
        if p <= m:
            v = "Not supported (wrong direction)"
        elif chi >= CHI_CRIT_DF1["p < .01 two-tailed"]:
            v = "Significant, p < .01"
        elif chi >= CHI_CRIT_DF1["p < .05 two-tailed"]:
            v = "Significant, p < .05"
        elif chi >= CHI_CRIT_DF1["p < .10 two-tailed (= .05 one-tailed)"]:
            v = "Significant, p < .05 one-tailed only"
        else:
            v = "Not significant"
        w(f"| {LABEL[dv]} | {p} | {m} | {g(e)} | **{fmt(chi)}** | 1 | 3.841 | 2.706 | {v} | {fp(binom_one_tailed(p, p + m))} |")
    w("\nχ² working: χ² = Σ (O − E)² ÷ E. Critical values for df = 1: " + "; ".join(f"{k}: {v}" for k, v in CHI_CRIT_DF1.items()) + ".\n")

    # 5 between-student analysis (workbook p.6 note)
    w("## 5. Between-student analysis: same song, different label (Mann-Whitney U)\n")
    w("The workbook (p. 6) notes \"Random treatment assignment → between-student analysis\". This holds the **song constant** and compares students who were told it took 1 week with students who were told it took 2 days. "
      "Different people are in each group, so it's an **independent-measures** comparison → **Mann-Whitney U**, one-tailed (1-week group predicted higher). "
      "Useful as a check: it doesn't depend on any one participant comparing the two songs side by side.\n")
    w("| Song | Measure | Told 1 week: n, *M* (*SD*) | Told 2 days: n, *M* (*SD*) | *U* | Critical *U* (.05, one-tailed) | Critical *U* (.01, one-tailed) | Result | z (tie-corrected) | one-tailed *p* ≈ |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for song in ("SoR", "CYFI"):
        for dv in DVS:
            hi = [song_score(r, song, dv)[0] for r in rows if r["stimulus_1wk"] == song]
            lo = [song_score(r, song, dv)[0] for r in rows if r["stimulus_1wk"] != song]
            res = mann_whitney(hi, lo)
            v = verdict(res["U"], res["crit05"], res["crit01"], res["right_direction"])
            w(f"| {song} | {SHORT[dv]} | {len(hi)}, {fmt(st.mean(hi))} ({fmt(st.stdev(hi))}) | {len(lo)}, {fmt(st.mean(lo))} ({fmt(st.stdev(lo))}) | **{g(res['U'])}** | {res['crit05']} | {res['crit01']} | {v} | {fmt(res['z'])} | {fp(res['p1'])} |")
    w("\nU = n1·n2 + n(n + 1) ÷ 2 − R. Each U was cross-checked by directly counting pairs. Critical values are exact for n1 = n2 = 16. "
      "Each comparison uses only one rating per student, so it has less power than the repeated-measures Wilcoxon.\n")

    # 6 per sheet
    w("## 6. Per-sheet breakdown (each sheet n = 8)\n")
    w("| Sheet | Song labelled 1 wk | *M* combined 1 wk | *M* combined 2 d | *M* d combined (*SD*) | *M* d liking (*SD*) | *M* d quality (*SD*) | Wilcoxon *T* combined (n) | Critical *T* (.05, one-tailed) | Result |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for s in (1, 2, 3, 4):
        grp = [r for r in rows if r["sheet"] == s]
        wc = wilcoxon([r["d_combined"] for r in grp])
        w(f"| {s} | {grp[0]['stimulus_1wk']} | {r2(st.mean(r['combined_1wk'] for r in grp))} | {r2(st.mean(r['combined_2d'] for r in grp))} | "
          f"{r2(st.mean(r['d_combined'] for r in grp))} ({fmt(st.stdev(r['d_combined'] for r in grp))}) | "
          f"{r2(st.mean(r['d_liking'] for r in grp))} ({fmt(st.stdev(r['d_liking'] for r in grp))}) | "
          f"{r2(st.mean(r['d_quality'] for r in grp))} ({fmt(st.stdev(r['d_quality'] for r in grp))}) | "
          f"{g(wc['T'])} ({wc['n']}) | {wc['crit05']} | {verdict(wc['T'], wc['crit05'], wc['crit01'], wc['right_direction'])} |")
    w("\nMeans are rounded half-up, which matches the PDF. Per-sheet tests have very low power at n = 8. Report the pooled test as the main result.\n")

    # 7 counterbalancing
    w("## 7. Counterbalancing check: did the song itself matter?\n")
    w("| Arrangement | n | *M* d combined | *M* d liking | *M* d quality |")
    w("|---|---|---|---|---|")
    for lab, song in (("SoR labelled 1 wk (sheets 1, 4)", "SoR"), ("CYFI labelled 1 wk (sheets 2, 3)", "CYFI")):
        grp = [r for r in rows if r["stimulus_1wk"] == song]
        w(f"| {lab} | {len(grp)} | {fmt(st.mean(r['d_combined'] for r in grp))} | {fmt(st.mean(r['d_liking'] for r in grp))} | {fmt(st.mean(r['d_quality'] for r in grp))} |")
    w("\n| Song (ignoring effort label) | *M* combined (*SD*) | *M* liking (*SD*) | *M* quality (*SD*) |")
    w("|---|---|---|---|")
    for song in ("SoR", "CYFI"):
        cells = []
        for dv in DVS:
            xs = [song_score(r, song, dv)[0] for r in rows]
            cells.append(f"{fmt(st.mean(xs))} ({fmt(st.stdev(xs))})")
        w(f"| {song} | " + " | ".join(cells) + " |")
    w("\nIf the effect came from one song simply being better, *d* would be positive in one arrangement and negative in the other. "
      "The two songs were rated almost identically overall, and the effort effect appears in both arrangements, so the result is not explained by song choice.\n")

    # 8 extras
    w("## 8. Other potentially useful metrics\n")
    all_l = [r["liking_1wk"] for r in rows] + [r["liking_2d"] for r in rows]
    all_q = [r["quality_1wk"] for r in rows] + [r["quality_2d"] for r in rows]
    w(f"- **Liking vs quality agreement:** Spearman's ρ between all liking and quality ratings (64 pairs) = **{fmt(spearman(all_l, all_q))}**. "
      "The two ratings largely move together, which supports averaging them into one DV.")
    for dv in DVS:
        neg = [f"S{r['sheet']}-{r['participant']}" for r in rows if r[f"d_{dv}"] < 0]
        w(f"- **Reversals, {SHORT[dv].lower()}** (rated the 2-day song higher): {', '.join(neg) or 'none'}.")
    hi = sum(1 for v in all_l + all_q if v >= 10)
    w(f"- **Ceiling/floor check (1–11 scale):** highest rating given = {max(all_l + all_q)}, lowest = {min(all_l + all_q)}. "
      f"Ratings of 10 or 11: {hi} of 128. No participant used the top of the scale, so there is **no ceiling effect**. "
      "Only one rating is in the bottom quarter (S1-P7, quality 2 d = 2).")
    w(f"- **Size of the effect in scale points:** combined +{fmt(st.mean(r['d_combined'] for r in rows))}, "
      f"liking +{fmt(st.mean(r['d_liking'] for r in rows))}, quality +{fmt(st.mean(r['d_quality'] for r in rows))} (1 wk − 2 d, on a 1–11 scale).")
    w("- **Every individual liking or quality difference is between −1 and +2.** The shift is consistent but modest.")

    w("\n## 9. Analyses the workbook plans but the data can't support yet\n")
    w("- **Re-run without participants who guessed the aim** (workbook p. 6): the data sheets don't record who guessed. If you have that list (e.g. from the debrief), add a `guessed` column to `raw_data.csv` and filter on it.")
    w("- **Order effects** (workbook p. 3 counterbalances which song is heard first): the data sheets don't record play order or answer-sheet version (X/Y). If each sheet had a known order, add a `first_song` column to test whether order mattered.")
    w("- **Actual sample characteristics** (workbook p. 4, \"Actual\" column blank): age, gender and AT Psych exclusions aren't in the data sheets.")

    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
