# 03 — Sample Report: Analysis & Verification

The sample is a partial replication of **Craik & Tulving (1975)** that tests the **Levels of Processing** model: structural vs semantic processing → free recall of 10 words, with N = 34 high school students.

The sample is a model of **form**. Its topic, numbers and wording belong to that study. Use the structure and the moves; don't reuse its content unless your study is the same.

---

## Study at a glance

| Element | Sample |
|---|---|
| Theory/model | Levels of Processing (Craik & Lockhart, 1972, as cited in Popov et al., 2017) |
| Anchor study | Craik & Tulving (1975), lab experiment, repeated measures, 3 levels |
| Method / design | Lab experiment, **independent measures**, random allocation |
| IV (operationalized) | Type of yes/no question: structural ("Is this word written in red?") vs semantic ("Is this word a body part?") |
| DV (operationalized) | Number of the 10 words correctly written in 2-minute free recall (0–10) |
| H₁ | Directional: semantic > structural |
| Sample | 34 students aged 16–17 (20 F, 14 M), opportunity sample from one international school, 17 per condition |
| Controls | Same 5-letter random word list in both conditions, timed slides, standardized script, colour-vision and English screening |
| Ethics | Written consent, right to withdraw, confidentiality, mild deception (aim given only as "memory"), condition-specific debrief |
| Descriptives | Structural *M* = 4.12, *SD* = 2.09 (range 0–8). Semantic *M* = 5.76, *SD* = 1.48 (range 3–8) |
| Inferential | One-tailed Mann-Whitney U: *U* = 75.5, critical *U* = 77, *p* < .01 → H₀ rejected |

## Independent verification

These numbers were recomputed from the raw data in Table E1 using [`../tools/stats.py`](../tools/stats.py) (`python3 tools/stats.py demo`).

| Claim in sample | Recomputed | ✓ |
|---|---|---|
| Σx = 70 / 98 | 70 / 98 | ✓ |
| *M* = 4.12 / 5.76 | 4.118 / 5.765 | ✓ |
| Σx² = 358 / 600 | 358 / 600 | ✓ |
| *SD* = 2.09 / 1.48 (sample SD, n − 1) | 2.088 / 1.480 | ✓ |
| Rank sums R_A = 228.5, R_B = 366.5 | 228.5 / 366.5 | ✓ |
| U_A = 213.5, U_B = 75.5 | 213.5 / 75.5 | ✓ |
| Critical U (n1 = n2 = 17, one-tailed .01) = 77 | 77 (exact distribution; VassarStats screenshot also shows 96 / 87 / 77 for .05 / .025 / .01) | ✓ |
| Difference = 1.64 words | 1.647 → 1.65 if computed from unrounded means; 1.64 comes from subtracting the rounded means. Trivial. | ≈ |
| 41% vs 58% of words recalled | 41.2% / 57.6% | ✓ |
| "about 40% more words" | 5.765 ÷ 4.118 = 1.40 | ✓ |
| Abstract = 120–150 words | 142 | ✓ |
| Main body 2,108 words | ≈ 2,100 by my count (exact figure depends on whether headings are counted) | ✓ |

**One number I could not verify here:** the anchor-study figures (8% / 9% / 22% recall). They come from the sample, not from the original paper. If your report cites Craik & Tulving, check the numbers against your workbook or textbook.

## Section lengths (prose, approx.)

| Section | Guide | Sample |
|---|---|---|
| Introduction | 600–750 | ~710 |
| Method | 400–500 | **~530**, slightly over, absorbed by a short Results |
| Results | 200–300 | ~200 |
| Discussion | 600–700 | ~655 |

The per-section lengths are guidance; the 1,800–2,200 total is the rule. Even the model report runs over in one section.

## What the sample does well (moves to copy)

1. **The phenomenon in plain English is the first sentence** of the Introduction, before any jargon.
2. **The theory-to-study link spelled out with "because"**: equal display time means the difference is due to processing.
3. **"Three modifications were made, and each preserved the core manipulation"**, then First/Second/Third, each with the *(category)* in brackets.
4. **Each control names the extraneous variable it controls**: word length, researcher bias, pace, colour perception, language comprehension, order effects, demand characteristics.
5. **The test is justified on three grounds**: directional hypothesis (one-tailed), independent measures, and data treated as ordinal.
6. **The Results stay descriptive**: SD is described as spread, and overlapping error bars are noted without explaining them.
7. **H₁ is restated word for word** at the start of the Discussion.
8. **Effect size is compared across studies** by converting both to percentages. Differences are explained by the modifications.
9. **"Partly supports"** is used where only part of the theory was tested. That is nuanced evaluation.
10. **Each limitation is a chain: problem → consequence (validity/generalisability) → specific fix.** Under the revised structure, extend the chain with *→ the distortion visible in your own numbers*. See below.
11. **The application is tied to a number**: ~40% more recall leads to study advice.
12. **Appendix E shows the working *and* a cross-check**: hand calculation, an online calculator, and the sum checks (R_A + R_B = N(N+1)/2, U_A + U_B = n1n2).
13. **Separate debriefs per condition**, each telling participants which condition they were in.

## ⚠️ The sample's Discussion ¶3–¶4 predate the REVISED structure

The sample was written to the original guide. Against the [revised Discussion structure](../sources/discussion-structure-revised.md):
- **¶3:** its limitations are not tied to its own results (the 0 score, the larger structural *SD*, the overlapping error bars). Limitation 1 is a generic design trade-off rather than a specific flaw in its materials or procedure.
- **¶4:** its generalisation is the "small, one school, artificial task" move the revision asks you to go beyond. It names no mirrored real-world situation and no situation where extra factors would change the outcome.

So copy its ¶1 and ¶2, and use [`02-section-by-section.md` §6](02-section-by-section.md#6-discussion-600700-words) for ¶3 and ¶4. That section includes worked illustrations.

## Small things to notice (so you don't copy them blindly)

- **The Abstract's hypothesis is a paraphrase**: "students recall significantly more words after semantic than structural processing questions." It is not the exact H₁ sentence. The guide's checklist says "worded the same way". To be safe, use the same key wording in the Abstract, or at least the same IV/DV/direction terms.
- **Ties in Mann-Whitney.** The data have many tied scores. Exact critical-value tables assume no ties, which is standard practice at this level, but it is worth one clause if you have heavy ties. VassarStats' z (−2.36) is uncorrected for ties; a tie-corrected z is −2.41. Either way it is significant.
- **The Introduction has no "Introduction" heading.** The title is repeated (bold, centered) at the top of page 3. That is APA 7 convention, so do the same.
- **Statistical symbols are italic** (*M*, *SD*, *U*, *p*, *N*, *n*, *z*, *H*). The plain-text export loses this, but the .docx has it.
- **No pilot study is mentioned.** If you ran one that changed anything, the guide wants a brief mention in the Procedure.
- **Secondary citation** "(Craik & Lockhart, 1972, as cited in Popov et al., 2017)": only Popov et al. goes in the reference list. Craik & Tulving is cited directly, so it is listed in full with a DOI.

## Formatting observed in the .docx

- Times New Roman 12 pt, double-spaced (line = 480), 1" margins (1440 twips)
- Level-1 headings (**Method**, **Results**, **Discussion**, **References**, **Appendix X**, repeated title, **Abstract**): bold, centered
- Level-2 headings (**Design**, **Participants**, **Aim**, **Word List**…): bold, flush left
- Body paragraphs: 0.5" first-line indent. The Abstract has none.
- References: 0.5" hanging indent. Journal name + volume and book titles in italics.
- Tables and figures: **Table 1** bold → title in *italic title case* on the next line → table → *Note.* in italics
- Appendix pages: bold centered "Appendix A", then a bold centered title ("Materials") on the next line
