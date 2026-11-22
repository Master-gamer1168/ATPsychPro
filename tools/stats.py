#!/usr/bin/env python3
"""Statistics helper for the AT Psychology research report.

Produces the numbers (and step-by-step working) that the report guide asks
for in the Results section and Appendix E:

  * descriptive statistics per condition (n, sum, mean, median, mode, range,
    sample SD) with the SD working shown the same way as the sample report
  * Mann-Whitney U test   (independent measures / two separate groups)
  * Wilcoxon signed-rank  (repeated measures or matched pairs)

Critical values are computed EXACTLY from the distribution of the statistic
(no ties), which is how published tables are produced, so you do not need a
printed table. Always state in the report which critical value you used.

Usage
-----
  python3 tools/stats.py mw   "7,4,5,5,4"   "4,6,8,8,5"       # Mann-Whitney
  python3 tools/stats.py wil  "7,4,5,5,4"   "4,6,8,8,5"       # Wilcoxon (paired, same order!)
  python3 tools/stats.py desc "7,4,5,5,4"                     # descriptives only
  python3 tools/stats.py demo                                 # re-runs the sample report

Options: --alpha 0.05 (default) or 0.01 ; --two-tailed (default is one-tailed,
because the guide asks for a directional hypothesis).

Only the Python standard library is used. No installation needed.
"""
import argparse
import math
import statistics as st
from collections import Counter
from functools import lru_cache


# ---------------------------------------------------------------- helpers
def parse(s):
    return [float(x) if "." in x else int(x) for x in s.replace(" ", "").split(",") if x != ""]


def fmt(x, dp=2):
    return f"{x:.{dp}f}"


def descriptives(name, xs):
    n = len(xs)
    sx = sum(xs)
    sx2 = sum(v * v for v in xs)
    mean = sx / n
    modes = st.multimode(xs)
    print(f"\n== Descriptive statistics: {name} ==")
    print(f"n = {n}")
    print(f"Sum (Σx) = {sx}")
    print(f"Mean M = Σx ÷ n = {sx} ÷ {n} = {fmt(mean)}")
    print(f"Median = {st.median(xs)}")
    print(f"Mode = {', '.join(str(m) for m in modes)}" + ("  (no single mode)" if len(modes) > 1 else ""))
    print(f"Range = {max(xs)} − {min(xs)} = {max(xs) - min(xs)}  (min {min(xs)}, max {max(xs)})")
    if n > 1:
        corr = sx * sx / n
        var = (sx2 - corr) / (n - 1)
        print("Sample SD = √[(Σx² − (Σx)² ÷ n) ÷ (n − 1)]")
        print(f"  Σx² = {sx2}")
        print(f"  (Σx)² ÷ n = {sx}² ÷ {n} = {fmt(corr)}")
        print(f"  Variance = ({sx2} − {fmt(corr)}) ÷ {n - 1} = {fmt(var)}")
        print(f"  SD = √{fmt(var)} = {fmt(math.sqrt(var))}")
    return mean


def rank_all(values):
    """Return {value: mean rank} for the pooled values (ties get mean rank)."""
    ordered = sorted(values)
    ranks = {}
    i = 0
    while i < len(ordered):
        j = i
        while j < len(ordered) and ordered[j] == ordered[i]:
            j += 1
        ranks[ordered[i]] = (i + 1 + j) / 2  # mean of ranks i+1 .. j
        i = j
    return ranks, ordered


# ------------------------------------------------- exact null distributions
@lru_cache(maxsize=None)
def _mw_count(n1, n2, u):
    """Number of arrangements of n1 A's and n2 B's giving U = u."""
    if u < 0:
        return 0
    if n1 == 0 or n2 == 0:
        return 1 if u == 0 else 0
    return _mw_count(n1 - 1, n2, u - n2) + _mw_count(n1, n2 - 1, u)


def mw_critical(n1, n2, alpha):
    """Largest U with P(U <= u) <= alpha (one-tailed). None if impossible."""
    total = math.comb(n1 + n2, n1)
    cum, crit = 0, None
    for u in range(n1 * n2 + 1):
        cum += _mw_count(n1, n2, u)
        if cum / total <= alpha + 1e-12:
            crit = u
        else:
            break
    return crit


@lru_cache(maxsize=None)
def _wil_count(n, t):
    """Number of sign assignments to ranks 1..n giving T+ = t."""
    if t < 0:
        return 0
    if n == 0:
        return 1 if t == 0 else 0
    return _wil_count(n - 1, t) + _wil_count(n - 1, t - n)


def wil_critical(n, alpha):
    total = 2 ** n
    cum, crit = 0, None
    for t in range(n * (n + 1) // 2 + 1):
        cum += _wil_count(n, t)
        if cum / total <= alpha + 1e-12:
            crit = t
        else:
            break
    return crit


# ------------------------------------------------------------------ tests
def mann_whitney(a, b, alpha, two_tailed, names=("A", "B")):
    n1, n2 = len(a), len(b)
    ranks, ordered = rank_all(a + b)
    ca, cb = Counter(a), Counter(b)
    print("\n== Mann-Whitney U test ==")
    print("Pooled ranking (ties receive the mean of the ranks they occupy):")
    print(f"{'Score':>6} {'#'+names[0]:>6} {'#'+names[1]:>6} {'Ranks':>9} {'Mean':>6} {'R_'+names[0]:>8} {'R_'+names[1]:>8}")
    pos = 1
    for v in sorted(set(ordered)):
        k = ca[v] + cb[v]
        span = f"{pos}" if k == 1 else f"{pos}–{pos + k - 1}"
        r = ranks[v]
        print(f"{v:>6} {ca[v]:>6} {cb[v]:>6} {span:>9} {r:>6.1f} {r * ca[v]:>8.1f} {r * cb[v]:>8.1f}")
        pos += k
    ra = sum(ranks[v] for v in a)
    rb = sum(ranks[v] for v in b)
    N = n1 + n2
    print(f"R_{names[0]} = {ra:g}, R_{names[1]} = {rb:g}; check: {ra + rb:g} = N(N+1)/2 = {N * (N + 1) // 2}")
    ua = n1 * n2 + n1 * (n1 + 1) / 2 - ra
    ub = n1 * n2 + n2 * (n2 + 1) / 2 - rb
    print(f"U_{names[0]} = n1·n2 + n1(n1+1)/2 − R_{names[0]} = {n1 * n2} + {n1 * (n1 + 1) / 2:g} − {ra:g} = {ua:g}")
    print(f"U_{names[1]} = n1·n2 + n2(n2+1)/2 − R_{names[1]} = {n1 * n2} + {n2 * (n2 + 1) / 2:g} − {rb:g} = {ub:g}")
    print(f"Check: U_{names[0]} + U_{names[1]} = {ua + ub:g} = n1·n2 = {n1 * n2}")
    u = min(ua, ub)
    one_tail_alpha = alpha / 2 if two_tailed else alpha
    crit = mw_critical(n1, n2, one_tail_alpha)
    tails = "two-tailed" if two_tailed else "one-tailed"
    print(f"Observed U = smaller value = {u:g}")
    # normal approximation (with tie correction) for reference only
    mu = n1 * n2 / 2
    tie = sum(t ** 3 - t for t in Counter(a + b).values())
    sigma = math.sqrt(n1 * n2 / 12 * ((N + 1) - tie / (N * (N - 1))))
    z = (u - mu) / sigma if sigma else float("nan")
    p1 = 0.5 * math.erfc(-z / math.sqrt(2))
    if crit is None:
        print(f"Critical value: none exists for n1={n1}, n2={n2} at {tails} α={alpha} — samples too small.")
    else:
        sig = u <= crit
        print(f"Critical value ({tails}, α = {alpha}, n1 = {n1}, n2 = {n2}): U ≤ {crit}")
        print(f"Result: U = {u:g} {'≤' if sig else '>'} {crit} → {'SIGNIFICANT, reject H0' if sig else 'NOT significant, retain H0'}")
    print(f"(Normal approximation, tie-corrected, for reference only: z = {z:.2f}, one-tailed p ≈ {p1:.4f}."
          " Online calculators without tie correction, e.g. VassarStats, give a slightly smaller |z|.)")
    print("Remember: a one-tailed test only supports H1 if the difference is in the PREDICTED direction.")


def wilcoxon(a, b, alpha, two_tailed, names=("A", "B")):
    if len(a) != len(b):
        raise SystemExit("Wilcoxon needs paired data: both lists must be the same length and in participant order.")
    diffs = [x - y for x, y in zip(a, b)]
    print("\n== Wilcoxon signed-rank test ==")
    print(f"Differences d = {names[0]} − {names[1]} (zero differences are dropped):")
    nz = [d for d in diffs if d != 0]
    print(f"  d = {diffs}")
    print(f"  dropped {len(diffs) - len(nz)} zero difference(s); n = {len(nz)}")
    ranks, _ = rank_all([abs(d) for d in nz])
    print(f"{'|d|':>5} {'count':>6} {'mean rank':>10}")
    for v in sorted(set(abs(d) for d in nz)):
        print(f"{v:>5} {sum(1 for d in nz if abs(d) == v):>6} {ranks[v]:>10.1f}")
    tpos = sum(ranks[abs(d)] for d in nz if d > 0)
    tneg = sum(ranks[abs(d)] for d in nz if d < 0)
    n = len(nz)
    print(f"Sum of ranks for positive d = {tpos:g}; negative d = {tneg:g}; check: {tpos + tneg:g} = n(n+1)/2 = {n * (n + 1) // 2}")
    T = min(tpos, tneg)
    one_tail_alpha = alpha / 2 if two_tailed else alpha
    crit = wil_critical(n, one_tail_alpha)
    tails = "two-tailed" if two_tailed else "one-tailed"
    print(f"Observed T = smaller sum = {T:g}")
    if crit is None:
        print(f"Critical value: none exists for n={n} at {tails} α={alpha} — sample too small.")
    else:
        sig = T <= crit
        print(f"Critical value ({tails}, α = {alpha}, n = {n}): T ≤ {crit}")
        print(f"Result: T = {T:g} {'≤' if sig else '>'} {crit} → {'SIGNIFICANT, reject H0' if sig else 'NOT significant, retain H0'}")
    print("Remember: a one-tailed test only supports H1 if the difference is in the PREDICTED direction.")


# ------------------------------------------------------------------- main
SAMPLE_STRUCTURAL = [7, 4, 5, 5, 4, 4, 6, 5, 2, 6, 4, 8, 0, 2, 1, 3, 4]
SAMPLE_SEMANTIC = [4, 6, 8, 8, 5, 6, 6, 5, 7, 3, 8, 4, 5, 6, 5, 7, 5]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("test", choices=["mw", "wil", "desc", "demo"])
    p.add_argument("a", nargs="?", help="comma-separated scores, condition A")
    p.add_argument("b", nargs="?", help="comma-separated scores, condition B")
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--two-tailed", action="store_true")
    p.add_argument("--names", default="A,B", help="labels for the two conditions, e.g. Structural,Semantic")
    args = p.parse_args()
    names = tuple(args.names.split(","))

    if args.test == "demo":
        print("Re-running the SAMPLE report (Craik & Tulving replication). Expected: M 4.12/5.76, SD 2.09/1.48, U = 75.5, crit 77 at .01")
        names = ("Structural", "Semantic")
        descriptives(names[0], SAMPLE_STRUCTURAL)
        descriptives(names[1], SAMPLE_SEMANTIC)
        mann_whitney(SAMPLE_STRUCTURAL, SAMPLE_SEMANTIC, 0.01, False, names)
        return

    a = parse(args.a)
    descriptives(names[0], a)
    if args.test == "desc":
        return
    b = parse(args.b)
    descriptives(names[1], b)
    if args.test == "mw":
        mann_whitney(a, b, args.alpha, args.two_tailed, names)
    else:
        wilcoxon(a, b, args.alpha, args.two_tailed, names)


if __name__ == "__main__":
    main()
