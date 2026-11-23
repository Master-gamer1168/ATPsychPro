# Our Study: Effort Heuristic Replication

Everything about **our** study in one place: the design as planned in the workbook, reconciled with the data that was actually collected.

| File | What it is |
|---|---|
| [`workbook-transcription.md`](workbook-transcription.md) | The handwritten workbook, transcribed page by page |
| [`original/Choosing_a_study_workbook.pdf`](original/Choosing_a_study_workbook.pdf) | The workbook scan (6 pages) |
| [`data/`](data/) | Raw data, analysis script and **all computed results** ([`data/RESULTS.md`](data/RESULTS.md)). Start with [`data/README.md`](data/README.md) |

> The guide says the report is written **in class from the workbook and data**. This page shows what the workbook already covers and **what's missing or inconsistent**, so you can fix the workbook before the writing sessions.

---

## Study profile (workbook + data, reconciled)

| Report element | Our study | Source |
|---|---|---|
| **Anchor study** | Kruger, J., Wirtz, D., Van Boven, L., & Altermatt, T. W. (2004). The effort heuristic. *Journal of Experimental Social Psychology, 40*(1), 91–98. **Experiment 1** | Workbook p. 1 |
| Anchor: aim | Does the time a poet supposedly spent on a poem influence how much people like it, how they judge its quality, and how much they think it's worth? | p. 1 |
| Anchor: method | 144 Williams College intro psych students (final N = 138: 89 women, 45 men, 4 undeclared [?]). Random allocation. All read the same poem; half were told it took **18 hours**, half **4 hours**. Participants wrote about it, then rated likeability, quality and monetary value. Independent measures. | p. 1 |
| Anchor: findings | Liking and quality ratings significantly higher in the 18-hour condition. Monetary value only marginally significant (*p* = .059). Gender made no difference. | p. 1 |
| Anchor: conclusion | People use perceived effort as a heuristic for quality. | p. 1 |
| **Theory / model** | **Heuristics** (mental shortcuts that usually work but produce predictable errors). Attribute substitution: a hard question ("how good is this?") is replaced by an easier one ("how much effort went in?"). Stronger when information is ambiguous. The effort heuristic is a specific case. | p. 2 |
| **IV** | Perceived effort to create a song, operationalized as the stated production time: **1 week** (high effort) vs **2 days** (low effort). Changed from 20 hrs vs 2 hrs after the pilot. | p. 2, p. 6 |
| **DV** | Mean of two ratings: **likeability** (1 = hate, 11 = love) and **quality** (1 = bad, 11 = great) | p. 2 |
| **H₁** (update the wording; see issue 1) | High school students will give a higher overall rating of likeability and quality (1–11 scale) to a song they are told took **1 week** to make than to a song they are told took **2 days** to make. | p. 3, amended |
| **H₀** | There will be no significant difference in combined likeability and quality ratings between the song described as taking 1 week and the song described as taking 2 days; any difference is due to chance. | p. 3, amended |
| **Design** | **Repeated measures + counterbalancing.** Controls participant variables, since each participant is compared with themselves. Which song gets the "1 week" label is swapped to control for one song being better. Play order is varied to control order effects (boredom, practice). | p. 3 |
| **Sampling** | Convenience (opportunity) sampling of SAS advisory groups. Target: 4 advisories. AT Psych students could take part, but their data was excluded. | p. 3, p. 5 |
| **Sample (actual)** | **N = 32** (4 data sheets × 8). Age, gender and other characteristics are **not recorded**; the "Actual" column on p. 4 is blank. | Data PDF |
| Controlled characteristic | Not taking AT Psych → reduces **demand characteristics**, because those students know about heuristics and could guess the IV | p. 4 |
| **Ethics** | Consent: what the study involves (without revealing effort/time), procedure, voluntary, confidential (no names). Debrief: deception (made-up production times), true aim, real song info, right to withdraw data, a request not to tell other advisories, whether they guessed the aim. Advisor permission obtained. | p. 4 |
| **Materials** | 2 songs (similar genre, style and duration); 2 answer-sheet versions (X/Y) with filler details so time isn't obviously the IV, handed out alternately and face down; consent form; standardized instructions; data table; debrief; advisory schedule | p. 5 |
| **Procedure** | Arrange a time → introduce the study, consent → sit apart, quietly → alternate answer-sheet versions, participant numbers → read instructions → flip the sheet (filler + effort info) → play song 1, rate → play song 2, rate → collect → debrief → thank | p. 5 |
| **Pilot changes** | Production times changed from 2 hrs / 20 hrs to **2 days / 1 week**. Participants made to write down the additional and effort info. "Changed genre?" crossed out. | p. 6 |
| **Inferential test** | **Wilcoxon signed-rank**, one-tailed (repeated measures, ordinal ratings, directional H₁) | — |
| **Result** | Combined DV: *M* = 7.06 (1 week) vs 6.08 (2 days); ***T* = 18**, critical value = 110, *N* = 29 non-tied, ***p* < .01** → **H₀ rejected** | [`data/RESULTS.md`](data/RESULTS.md) |

### Modifications vs the anchor study (for Introduction Part 3)

The categories are my suggestions against the guide's five; adjust them to your own reasoning.

| Original (Kruger et al., 2004, Exp. 1) | Ours | Suggested category | Why the core phenomenon is intact |
|---|---|---|---|
| A poem | Two songs (similar genre, style and duration) | Construct adaptation and access | Still a creative work whose quality is ambiguous to judge, which is the condition under which heuristics operate |
| 18 hours vs 4 hours | 1 week vs 2 days (after the pilot) | Construct validity and measurement | Production times have to be believable for songs; still a high- vs low-effort contrast |
| Independent measures, random allocation | Repeated measures, label and order counterbalanced | Methodological control | Removes participant variables (e.g. music taste); counterbalancing controls song quality and order effects |
| Liking, quality and monetary value | The mean of liking and quality (monetary value dropped) | Feasibility and standardization | Keeps the two DVs that were significant in the original |
| University intro psych students | High school advisory groups, AT Psych excluded | Feasibility (access) + methodological control (demand characteristics) | Same kind of non-expert judges |

---

## ⚠️ Inconsistencies and gaps to resolve before writing

1. **Hypothesis wording is out of date.** H₁/H₀ (p. 3) and the IV definition (p. 2) still say **20 hrs vs 2 hrs**, but the pilot changed this to **1 week vs 2 days**, and the data uses 1 week / 2 days. Update the workbook. The guide requires the hypothesis to be worded identically in the Abstract, Introduction and Discussion.
2. **Rating scale: 1–11 or 1–10?** Pages 2 and 3 say 1–11; the p. 6 summary says 1–10. Check the actual answer sheet. (No 10s or 11s were given, so the ceiling-effect conclusion is the same either way.)
3. **Experiment 1 vs Experiment 2.** The anchor is Experiment 1, which was **between-subjects**. The design rationale says "very similar to experiment 2". In the report, keep the anchor as Experiment 1 and present repeated measures as a **modification** (see the table above).
4. **What does each data sheet represent?** The workbook says answer-sheet versions X/Y were handed out **alternately within each advisory**, and that play order was varied. But each data sheet has one fixed label assignment (sheets 1/4: SoR = 1 week; sheets 2/3: CYFI = 1 week). Record which **advisory**, which **version (X/Y)** and which **song played first** each sheet corresponds to. This matters for the Procedure section and for testing order effects.
5. **Actual sample characteristics missing.** You need age range, gender split, N per advisory, and how many AT Psych students were excluded, for the Participants section. The target was about 40 participants; the data has 32.
6. **Original study's numbers.** The workbook has no means or test statistics from Kruger et al. Experiment 1. Intro Part 2 asks for "key numbers where available", and Discussion ¶2 compares effect size. Note the original condition means (18 h vs 4 h) from the article.
7. **Theory link to check.** The note "effort heuristic based on availability heuristic" should be checked against the article's introduction before it goes in the report. If you use "attribute substitution", note where that term comes from and cite it properly.
8. **Pilot data.** "Pilot study completed?" is blank, yet changes are listed. The p. 6 means (song 1: liking 4.75, quality 5.25; song 2: liking 7.5, quality 6.5) don't match the main data and look like pilot figures with no *n*. If you mention the pilot, record its *n*.
9. **Planned "rerun without guessers"** (p. 6): who guessed the aim isn't recorded in the data. If the debrief captured it, add it so the analysis can be re-run.
10. Minor: version Y's description on p. 5 says "2 hrs". It presumably means 2 days.
