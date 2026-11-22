# 02 — Section-by-Section Notes

For each section you get:
- **Guide says:** the requirements, condensed
- **Sample does:** how the [sample report](../sources/sample-full-research-report.md) meets them, as a model
- **Watch:** pitfalls and judgement calls
- **Workbook:** which workbook pages feed the section (from the guide)

Templates with sentence starters are in [`../templates/report-skeleton.md`](../templates/report-skeleton.md).

---

## 1. Title page

**Guide says:** The title names the **operationalized IV and DV**. It is bold, centered and in the upper half of the page. Below it: names, block, "AT Psychology, Singapore American School", submission month + year, and the main-body word count. Page number 1 goes in the top-right header.

**Sample does:**
- Title pattern: **"The Effect of [IV] on [DV] in [Population]"**, i.e. *The Effect of Structural versus Semantic Processing on Free Recall of Words in High School Students*
- A bold subtitle: *A Partial Replication of Craik and Tulving (1975)*. Not required by the guide, but a neat way to signal the anchor study.
- Word count written as: `Word count (Introduction to Discussion): 2,108`

**Watch:** Name both conditions of the IV ("X versus Y") and the measured DV ("free recall of words"), not just the topic ("memory").

---

## 2. Abstract (write last)

**Guide says:** One paragraph of 120–150 words on its own page, with a bold centered label **Abstract**. No first-line indent, double-spaced. Five components of one or two sentences each:

| Component | What the sample wrote |
|---|---|
| Context and aim | "This experiment partially replicated Craik and Tulving (1975) to investigate the effect of structural versus semantic processing on free recall of words, based on the Levels of Processing model." |
| Participants | "A sample of 34 high school students was recruited using opportunity sampling…" |
| Method | "…in an independent measures design. Participants answered yes-or-no questions about 10 words that directed attention to either appearance (structural processing) or meaning (semantic processing), then freely recalled the words for two minutes." |
| Findings | "Participants in the semantic condition (*M* = 5.76, *SD* = 1.48) recalled more words than those in the structural condition (*M* = 4.12, *SD* = 2.09). A Mann-Whitney U test indicated that this difference was significant (*U* = 75.5, critical value = 77, *p* < .01)." |
| Conclusion and application | "These findings supported the hypothesis that… suggesting that studying should emphasize meaning." |

**Watch:**
- Its hypothesis and conclusion must **match** the body.
- The guide's starter shows `p [< / >] .05`. Report whatever significance level you actually used. The sample used .01.
- Briefly define each condition in brackets so a cold reader understands it ("appearance (structural processing)").

---

## 3. Introduction (600–750 words)

One theory/model and one anchor study. Paragraphs flow Part 1 → 2 → 3 → 4, and every theory or study is cited in APA.

### Part 1: Theory or model (150–200 words)

**Guide says:** Name the phenomenon in plain terms, then name and cite the theory/model and summarise it, then define the key terms.

**Sample does:**
1. Opens with the phenomenon in plain English: "People tend to remember information better when they think about its meaning than when they attend only to its appearance."
2. Names and cites the model: Levels of Processing, (Craik & Lockhart, 1972, as cited in Popov et al., 2017). This is a **secondary citation**, which is the correct form when you only read about the original in a textbook.
3. Defines every term used later: shallow vs deep, structural, phonetic, semantic.
4. Adds context: how LOP extends the Multi-Store Model.

### Part 2: Anchor study (200–250 words)

**Guide says:** Cover four things: **Aim, Method (design, participants, IV, DV, task), Findings (with numbers), Link to theory.**

**Sample does:**
- Aim: "to investigate how shallow processing… and deep processing… affect the recall and recognition of words"
- Method: lab experiment, repeated measures, yes/no question → word shown 200 ms → button press. IV and DV are named explicitly ("The independent variable (IV) was… the dependent variable (DV) was…").
- Findings with numbers: 8% / 9% / 22% recall
- **Link to theory** (the commonly missed part): "These results supported the LOP model **because** every word was displayed for the same brief time, so the difference in memory could be attributed to the processing each question required. Semantic questions forced participants to link a word to existing knowledge, which produced deeper encoding…"

**Watch:** The link must explain *why* the result supports or challenges the theory (the mechanism and the control). Saying "this supported the theory" on its own is not enough.

### Part 3: Justifying the replication and modifications (150–200 words)

**Guide says:** Why replicate, what you changed, and why. Name the **modification category** for each change and show the core phenomenon is intact.

| Category | Typical reason |
|---|---|
| Ethical protection | Protects from distress, embarrassment or deception |
| Methodological control | Removes confounds, order effects or carryover effects |
| Construct adaptation and access | Feasible analogue for an inaccessible population or apparatus |
| Construct validity and measurement | Turns qualitative observations into a measurable DV |
| Feasibility and standardization | Fits the timetable and keeps conditions identical |

**Sample does:**
- Why replicate: does the effect hold for high school students in a simplified classroom setting? Relevance: "Memory is central to learning…"
- States up front: "Three modifications were made, and each preserved the core manipulation…"
- Uses "First… Second… Third…", with the **category in brackets** after each change:
  1. Repeated → independent measures *(methodological control)*: removes order effects, reduces demand characteristics
  2. Two conditions only, a 10-word list and free recall only *(feasibility and standardization)*: fits a class period
  3. Slides + paper instead of a 200 ms display + buttons *(construct adaptation and access)*: a feasible analogue

### Part 4: Aim, variables, hypotheses (subheadings allowed)

**Guide says:**
- **Aim:** "To investigate the effect of [IV] on [DV] in [population]."
- **IV:** name + operational definition of **both conditions**
- **DV:** name + operational definition (**exactly** how it was measured)
- **H₁:** directional; names population, operationalized IV and DV, and expected outcome
- **H₀:** "no significant difference in [DV] between [A] and [B]; any difference is due to chance"
- The hypothesis must follow logically from Parts 1–3.

**Sample does:** Bold level-2 subheadings (Aim / Independent Variable / Dependent Variable / Research Hypothesis (H1) / Null Hypothesis (H0)), each followed by a full sentence or two. The IV definition gives an example question for each condition. The DV gives the scoring rule: "the number of the 10 words correctly written down during a two-minute free-recall task."

**Watch:** Copy the exact H₁ sentence into the Discussion. The checklist requires the same wording in the Introduction, Discussion and Abstract.

---

## 4. Method (400–500 words)

Four subheadings in this order: **Design → Participants → Materials → Procedure**. Write in paragraphs.

### Design

**Guide says:** method + design → why (name the extraneous variable it controls) → how you controlled the design's weakness (random allocation / counterbalancing / matching).

**Sample does:** "laboratory experiment with an independent measures design" → controls **order effects and expectancy effects**, and allows the same word list in both conditions → weakness = **participant variables**, handled by **random allocation** (random group generator, then conditions randomly assigned to groups).

| Design | Controls | Weakness | Fix |
|---|---|---|---|
| Independent measures | Order effects, demand characteristics | Participant variables | Random allocation |
| Repeated measures | Participant variables | Order effects (practice, fatigue), demand characteristics | Counterbalancing |
| Matched pairs | Participant variables (on the matched variable) and order effects | Matching is imperfect and time-consuming | Match on a pre-test score |

### Participants

**Guide says:** N, age, gender and any other relevant trait of the **actual** sample → target population → sampling method + recruitment + why → justify at least one sample characteristic as a control → ethics: consent, withdrawal, confidentiality, debrief, and any deception.

**Sample does:**
- 34 students (20 F, 14 M), aged 16–17, one international school, with the gender split per condition
- Target population: high school students at international schools
- Opportunity sampling: teachers released a class, which was "convenient and quick" (a practical reason is acceptable)
- Controlled characteristics: normal colour vision (the structural questions use colour) and English fluency, "so color perception and language comprehension did not confound recall"
- Ethics paragraph: written consent (App. C), duration, confidentiality/anonymity, right to withdraw with data destroyed. **Deception named:** told only "memory", with the hypothesis withheld to reduce demand characteristics. Full debrief (App. D) and a contact sheet.

### Materials

**Guide says:** list the materials with appendix references (leave out pens, chairs) → explain at least one self-made material and the extraneous variable it controlled.

**Sample does:** the word list, the question sets, the slides and the answer sheet "(see Appendix A)". Word list from a random generator → prevents **researcher bias**. All words are 5 letters → **word length** can't affect recall. Slides with a ring and fixed timings → identical **pace** for everyone.

### Procedure

**Guide says:** chronological, greeting to debrief. Past tense, third person, paragraphs. Include timings, the instructions given, how the DV was recorded, and pilot-study changes (briefly).

**Sample does:** Instructions read (App. B) → consent collected and checked → answer sheets → 10 trials (ring, question 8 s, word 2 s, prompt, 8 s to answer) → sheets collected → 2 min free recall (+ up to 1 min extra) → recall sheets collected → debrief + contact sheet → repeated with the other group.

**Watch:** The sample doesn't mention a pilot. If yours led to changes, add one sentence here.

---

## 5. Results (200–300 words + table + graph)

**Guide says:** Report only, no interpretation. Four parts in this order:
1. How the DV was scored (1–3 sentences)
2. **Table** of central tendency + dispersion per condition, followed by a sentence on which condition scored higher
3. **One graph**, usually a bar chart of the means: descriptive title, both axes labelled, undistorted axes. One summary sentence beneath it.
4. **Inferential test**: name it + why (one sentence), calculated value, critical value, N, and whether H₀ was accepted or rejected

Raw data and step-by-step calculations go in **Appendix E**, not here.

**Sample does:**
- Scoring: "the number of the 10 words correctly written down… giving each participant a score from 0 to 10. Raw scores are presented in Appendix E."
- Points to the table and gives the difference (1.64 words), compares SDs (spread) and gives ranges (0–8 vs 3–8)
- APA table: **Table 1** (bold) / *italic title* / columns Condition, *n*, *M*, *SD* / *Note.* Scores could range from 0 to 10.
- APA figure: **Figure 1** / *italic title* / bar chart, y-axis 0–10 (the full possible range, so undistorted), axis titles, ±1 SD error bars / *Note.* explaining the error bars and n ([image](../sources/images/fig1-bar-chart-mean-recall.png))
- One sentence under the figure: higher in semantic, "although the error bars of the two conditions overlapped"
- Test sentence: "A one-tailed Mann-Whitney U test was used because the hypothesis was directional, the design was independent measures and the data were treated as ordinal… *U* = 75.5, the critical value was 77 (*N* = 34, *n*1 = *n*2 = 17, *p* < .01), and the null hypothesis was therefore rejected."

**Watch:**
- The justification for the test needs **three** things: design + level of data + (one- or two-tailed, from the directional hypothesis).
- Don't explain *why* a condition did better. That belongs in the Discussion.
- See [`04-statistics.md`](04-statistics.md) for test choice and the reporting format.

---

## 6. Discussion (600–700 words)

Four paragraphs, as the guide lays out.

### ¶1 Findings and the hypothesis
**Guide says:** restate H₁ → supported or not → key numbers (means + test) → **why** → unexpected results or outliers and their likely effect.
**Sample does:** Restates H₁ word for word, then gives *M*, *SD*, *U*, the critical value, *N* and *p*. The "why" is deeper encoding from linking to prior knowledge. Outlier: one structural participant recalled 0 words (possible inattention), which widened the spread. The overlapping error bars mean the effect is "a tendency across the groups rather than an advantage for every individual."

### ¶2 Comparison with anchor study and theory
**Guide says:** same direction? similar size? If different, explain why (modifications, sample, procedure) → support, challenge or partly support the theory, with citations.
**Sample does:** Same direction. Converts both studies to percentages to compare size: **41% vs 58%** here, **8% vs 22%** in the original. Higher recall is explained by the shorter list and longer display, which may have raised structural recall and shrunk the relative advantage. **"Partly supports"** the model, because only 2 of the 3 levels were tested.

### ¶3 Limitations and improvements
**Guide says:** **two** limitations (reliability/validity: sample, design, procedure). For each one: its effect on the results + a **specific** modification.
**Sample does:**
1. Independent measures → participant variables → lower internal validity → **matched pairs** on a baseline recall task, randomly allocated within pairs
2. One school, a humanities class that may know psychology → demand characteristics + unrepresentative sample → **pre-screen** for familiarity + **random sampling across several schools**

### ¶4 Conclusion and implications
**Guide says:** a specific conclusion for the sample → generalisable? → justified real-world application → one direction for further research.
**Sample does:** "For this sample of 34 students aged 16 to 17…" → not confidently generalisable (small, one school, opportunity sample, artificial task) → application: semantic participants recalled ~40% more, so **study by relating new material to prior knowledge rather than colour-coding**, and teachers should set linking tasks → further research: a phonetic condition, realistic material, delayed recall.

**Watch:** Give each limitation's *consequence* ("this would reduce internal validity because…"), not only the fix.

---

## 7. References and citations

See [`05-style-apa-formatting.md`](05-style-apa-formatting.md). Minimum: the anchor study + the source for the theory/model. The sample also cites every website or tool it used (random word generator, calculators).

## 8. Appendices

| Appendix | Sample's content |
|---|---|
| A: Materials | Word list + generator settings screenshot, both question sets, answer sheet |
| B: Standardized instructions | Full verbatim script, with italic bracketed stage directions *[not read aloud]* |
| C: Informed consent | Purpose (vague: "memory"), duration, task, confidentiality, withdrawal at any time with data destroyed, signature line, screening checkboxes (colour-blind, English) |
| D: Debriefing | **A separate debrief per condition** stating the true aim, the theory and which condition they were in. Support offer, withdraw-data checkbox, results-copy option. Plus a contact sheet |
| E: Raw data + calculations | Table E1 raw scores, Table E2 mean/SD working, calculator screenshots, Table E3 rank table, U working with checks, VassarStats screenshots |

Every appendix gets its own page, a bold centered label + bold centered title, and is referenced in the body ("see Appendix C").
