# 04 — Statistics Reference (Results section + Appendix E)

The guide treats statistics as part of the Results (summary only) and Appendix E (all the working). This note covers both. Your class's *Research Methods, Experimental Design and Statistics* guide is the authority. This file collects what the report guide and the sample actually use.

## Where things go

| Item | Results section | Appendix E |
|---|---|---|
| How the DV was scored | ✓ (1–3 sentences) | |
| Table of *M* and *SD* (or median/range) per condition | ✓ | |
| One graph | ✓ | |
| Test name + why + calculated value + critical value + *N* + H₀ decision | ✓ (1–2 sentences) | |
| Every participant's raw score | ✗ never | ✓ Table E1 |
| Step-by-step descriptive working | | ✓ Table E2 (+ calculator screenshots) |
| Rank table + U/T working + checks | | ✓ Table E3 (+ calculator screenshots) |

## Choosing the inferential test

| Design | Level of data | Test | Statistic | Significant when |
|---|---|---|---|---|
| **Independent measures** | Ordinal or higher (scores) | **Mann-Whitney U** | *U* = smaller of U_A, U_B | *U* ≤ critical value |
| **Repeated measures** or **matched pairs** | Ordinal or higher | **Wilcoxon signed-rank** | *T* = smaller rank sum | *T* ≤ critical value |
| Independent measures | Nominal (categories/frequencies) | Chi-square | χ² | χ² ≥ critical value |
| Repeated measures | Nominal (+/− change) | Sign test | *S* | *S* ≤ critical value |

The sample's justification sentence covers all three choices in one line:
> "A one-tailed Mann-Whitney U test was used because **the hypothesis was directional**, **the design was independent measures** and **the data were treated as ordinal**."

Why "treated as ordinal": a recall count is arguably interval/ratio data, but you can't assume it is normally distributed with a small classroom sample, so a non-parametric test is the safe choice.

## One-tailed vs two-tailed; significance level

- Directional H₁ (required by the guide) → **one-tailed** test.
- Default level: *p* < .05. If your result also passes a stricter level, you can report that one (the sample reported *p* < .01).
- A one-tailed result only supports H₁ if the difference is **in the predicted direction**. If your means go the other way, H₁ is not supported, whatever the U value says.
- Wording: "the null hypothesis was **rejected**" (significant) or "the null hypothesis was **retained/accepted**" (not significant). The guide uses "accepted or rejected".

## Descriptive statistics

| Measure | Formula / note |
|---|---|
| Mean *M* | Σx ÷ n |
| Sample standard deviation *SD* | √[(Σx² − (Σx)² ÷ n) ÷ (n − 1)] (the sample uses this form. Note **n − 1**) |
| Median | middle score, the mean of the middle two if n is even |
| Range | max − min. The sample reports it in prose ("0 to 8") |

Results sentence pattern (sample):
> "As shown in Table 1, participants in the semantic processing condition recalled more words on average than participants in the structural processing condition, a difference of 1.64 words. The standard deviation was larger in the structural processing condition, which indicates that scores in that condition were more widely spread around the mean."

## The graph

- One graph, usually a **bar chart of the condition means**. It is not a histogram and not a bar per participant.
- **Figure 1** (bold) → *Descriptive Title in Italic Title Case* → graph → *Note.* (explain the error bars and n)
- Both axes labelled. Y-axis **starts at 0** and ideally spans the possible range (the sample uses 0–10), so it is **not distorted**.
- Optional: ±1 *SD* error bars (the sample uses them and explains them in the Note).
- Add one summary sentence underneath.
- Reference image: [`../sources/images/fig1-bar-chart-mean-recall.png`](../sources/images/fig1-bar-chart-mean-recall.png)

## Mann-Whitney U by hand (Appendix E method, as in the sample)

1. Pool all scores from both conditions and rank them lowest = 1. **Tied scores get the mean of the ranks they occupy** (e.g. seven 4s occupying ranks 7–13 each get 10).
2. Sum the ranks for each condition: R_A, R_B. **Check:** R_A + R_B = N(N + 1) ÷ 2.
3. U_A = n1·n2 + n1(n1 + 1) ÷ 2 − R_A, and likewise U_B with n2 and R_B. **Check:** U_A + U_B = n1·n2.
4. Observed *U* = the smaller value.
5. Compare with the critical value for n1, n2 and the chosen tail and level. **Significant if U ≤ critical.**
6. Cross-check with an online calculator and screenshot it. The sample used VassarStats (Lowry, 1998).

A rank table layout that works (sample Table E3): `Score | Number in A | Number in B | Ranks occupied | Mean rank | Rank sum for A | Rank sum for B`

## Wilcoxon signed-rank by hand (if your design is repeated measures or matched pairs)

1. For each participant/pair, d = score A − score B. **Drop zero differences**; n = the number of non-zero d.
2. Rank |d| lowest = 1, with ties getting the mean rank.
3. Sum the ranks of the positive d and of the negative d. **Check:** the two sums add to n(n + 1) ÷ 2.
4. *T* = the smaller sum. **Significant if T ≤ critical value.**

## Reporting templates

Results (guide's example):
> A Mann-Whitney U test was used because the design was independent measures and the data were ordinal (*U* = 12, critical value = 23, *N* = 20, *p* < .05). The null hypothesis was therefore rejected.

Results (sample):
> …*U* = 75.5, the critical value was 77 (*N* = 34, *n*1 = *n*2 = 17, *p* < .01), and the null hypothesis was therefore rejected. The calculations are presented in Appendix E.

Not significant:
> …(*U* = 40, critical value = 27, *N* = 20, *p* > .05). The null hypothesis was therefore accepted.

Wilcoxon:
> A one-tailed Wilcoxon signed-rank test was used because the hypothesis was directional, the design was repeated measures and the data were treated as ordinal (*T* = 8, critical value = 10, *N* = 10, *p* < .05). The null hypothesis was therefore rejected.

## Using the helper script

[`../tools/stats.py`](../tools/stats.py) uses only the Python standard library. It prints the full working in the same layout as the sample's Appendix E, including the checks, so you can verify your hand calculations.

```bash
python3 tools/stats.py demo
```

```bash
python3 tools/stats.py mw "7,4,5,5,4,4,6,5,2" "4,6,8,8,5,6,6,5,7" --names Control,Experimental
```

```bash
python3 tools/stats.py wil "5,6,7,3,8,9,4,6" "3,6,5,2,6,5,4,3" --names Before,After
```

```bash
python3 tools/stats.py mw "..." "..." --alpha 0.01
```

```bash
python3 tools/stats.py mw "..." "..." --two-tailed
```

For Wilcoxon, both lists must be in the **same participant order**. The script works out critical values **exactly** from the null distribution. It reproduces published tables and the sample's 77.

## Critical-value tables (generated exactly by `tools/stats.py`)

### Mann-Whitney U, equal group sizes (significant if U ≤ value)

For unequal groups, run the script. "–" means no result can be significant at that level.

| n per group | .05 one-tailed | .025 one-tailed / .05 two-tailed | .01 one-tailed / .02 two-tailed | .005 one-tailed / .01 two-tailed |
|---|---|---|---|---|
| 5 | 4 | 2 | 1 | 0 |
| 6 | 7 | 5 | 3 | 2 |
| 7 | 11 | 8 | 6 | 4 |
| 8 | 15 | 13 | 9 | 7 |
| 9 | 21 | 17 | 14 | 11 |
| 10 | 27 | 23 | 19 | 16 |
| 11 | 34 | 30 | 25 | 21 |
| 12 | 42 | 37 | 31 | 27 |
| 13 | 51 | 45 | 39 | 34 |
| 14 | 61 | 55 | 47 | 42 |
| 15 | 72 | 64 | 56 | 51 |
| 16 | 83 | 75 | 66 | 60 |
| 17 | 96 | 87 | 77 | 70 |
| 18 | 109 | 99 | 88 | 81 |
| 19 | 123 | 113 | 101 | 93 |
| 20 | 138 | 127 | 114 | 105 |

### Wilcoxon signed-rank T (significant if T ≤ value)

| n (non-zero differences) | .05 one-tailed | .025 one-tailed / .05 two-tailed | .01 one-tailed / .02 two-tailed | .005 one-tailed / .01 two-tailed |
|---|---|---|---|---|
| 5 | 0 | – | – | – |
| 6 | 2 | 0 | – | – |
| 7 | 3 | 2 | 0 | – |
| 8 | 5 | 3 | 1 | 0 |
| 9 | 8 | 5 | 3 | 1 |
| 10 | 10 | 8 | 5 | 3 |
| 11 | 13 | 10 | 7 | 5 |
| 12 | 17 | 13 | 9 | 7 |
| 13 | 21 | 17 | 12 | 9 |
| 14 | 25 | 21 | 15 | 12 |
| 15 | 30 | 25 | 19 | 15 |
| 16 | 35 | 29 | 23 | 19 |
| 17 | 41 | 34 | 27 | 23 |
| 18 | 47 | 40 | 32 | 27 |
| 19 | 53 | 46 | 37 | 32 |
| 20 | 60 | 52 | 43 | 37 |
| 21 | 67 | 58 | 49 | 42 |
| 22 | 75 | 65 | 55 | 48 |
| 23 | 83 | 73 | 62 | 54 |
| 24 | 91 | 81 | 69 | 61 |
| 25 | 100 | 89 | 76 | 68 |
| 26 | 110 | 98 | 84 | 75 |
| 27 | 119 | 107 | 92 | 83 |
| 28 | 130 | 116 | 101 | 91 |
| 29 | 140 | 126 | 110 | 100 |
| 30 | 151 | 137 | 120 | 109 |

If your class's printed table differs by one at the boundary (rare), use your class table and cite it.
