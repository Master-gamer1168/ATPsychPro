# ATPsychPro: AT Psychology Research Report Resource Bank

Reference material for writing the **AT Psychology group-project research report**, a formal APA-style write-up of a replication experiment. It banks the class's two source documents, plus notes, templates and a stats helper built from them.

> ⚠️ **In-class rule (from the guide):** *"All writing will be done IN CLASS, using only your workbook and the data you collect as resources unless directly instructed by your teacher."*
> This repo is for **preparation**: understanding the format, filling your workbook so it holds everything each section needs, and checking your statistics. Don't plan on using it during the in-class writing sessions unless your teacher allows it.

## Start here

| If you want to… | Open |
|---|---|
| See the whole format on one page | [`notes/01-quick-reference.md`](notes/01-quick-reference.md) |
| Know exactly what each section needs, with model examples | [`notes/02-section-by-section.md`](notes/02-section-by-section.md) |
| Understand what the sample does well, and its quirks | [`notes/03-sample-report-analysis.md`](notes/03-sample-report-analysis.md) |
| Choose, run and report the inferential test | [`notes/04-statistics.md`](notes/04-statistics.md) |
| Get APA citations, headings, terminology and tone right | [`notes/05-style-apa-formatting.md`](notes/05-style-apa-formatting.md) |
| Plan your own report section by section | [`templates/report-skeleton.md`](templates/report-skeleton.md) |
| Check the report before submitting | [`templates/submission-checklist.md`](templates/submission-checklist.md) |
| Read the original documents | [`sources/`](sources/) |

## Repository layout

```
README.md
sources/                                  ← the two original documents, banked
  guide-how-to-write-research-report.md     GUIDE, faithful Markdown transcription
  sample-full-research-report.md            SAMPLE report, faithful transcription with images
  discussion-structure-revised.md           REVISED Discussion structure (authoritative, supersedes guide §6)
  images/                                   figures and screenshots extracted from the sample
  original/                                 untouched .txt and .docx exports from Google Docs
notes/                                    ← study notes distilled from the sources
  01-quick-reference.md                     one-page cheat sheet: word budget, orders, rules, skeleton
  02-section-by-section.md                  requirements + how the sample meets them + pitfalls
  03-sample-report-analysis.md              verified numbers, moves to copy, quirks to avoid
  04-statistics.md                          test choice, hand methods, reporting, critical-value tables
  05-style-apa-formatting.md                language, terminology, APA 7, page formatting
templates/
  report-skeleton.md                        fill-in planner with sentence starters per section
  submission-checklist.md                   merged final checklist
tools/
  stats.py                                  descriptives + Mann-Whitney U + Wilcoxon, with full working
```

## Sources

| Document | Google Doc | What it is |
|---|---|---|
| **GUIDE: How to Write Your Research Report** | [link](https://docs.google.com/document/d/1HBH8O52bre5r7kpomWKvJay4BLvj62el635hsU6MlIQ/edit?tab=t.0) | The rules: structure, word counts, what each section must contain, formatting, checklist |
| **SAMPLE: Full Research Report** | [link](https://docs.google.com/document/d/1ND9DiAuGy_h8F0LgiiGBjAraSy2j2oOeNkKres_yVPM/edit?tab=t.0) | A complete model report: a partial replication of Craik & Tulving (1975) on Levels of Processing, N = 34, Mann-Whitney U |

| **Discussion structure (REVISED)** | [`sources/discussion-structure-revised.md`](sources/discussion-structure-revised.md) | Provided 23 Nov 2026. **Supersedes the guide's §6.** ¶1–2 are unchanged; ¶3 (limitations) and ¶4 (generalisation) are stricter |

The two Google Docs were retrieved on 22 Nov 2026. If your teacher updates either one, re-export it and replace the files in `sources/`.

> **Precedence:** where they differ, the **revised Discussion structure** overrides the guide and the sample. The sample's Discussion ¶3–¶4 were written to the older criteria, so don't model those two paragraphs on it.

## The format in 30 seconds

- **Main body (Intro → Discussion): 1,800–2,200 words.** Intro 600–750 · Method 400–500 · Results 200–300 · Discussion 600–700. Abstract 120–150 (not counted).
- **Write** Intro → Method → *(run study)* → Results → Discussion → Abstract. **Assemble** Title → Abstract → Intro → Method → Results → Discussion → References → Appendices A–E.
- **Third person, past tense, formal, concise, paragraphs.**
- The most-missed point: in the Introduction, explain **why** the anchor study's findings support the theory.
- **Discussion (revised):** limitations must be specific, at least one must be about internal validity or reliability, and each must be tied to *your* means, spread or outliers with a concrete fix. Generalise using one real-world situation the task mirrors and one where real-world factors would change the outcome.

## Stats helper

```bash
python3 tools/stats.py demo
```

```bash
python3 tools/stats.py mw "scores,for,A" "scores,for,B" --names CondA,CondB
```

```bash
python3 tools/stats.py wil "A,scores" "B,scores"
```

`demo` reproduces the sample report's Appendix E exactly. `mw` is for independent measures; `wil` is for repeated measures or matched pairs, with both lists in the same participant order. The script needs only the Python 3 standard library. See [`notes/04-statistics.md`](notes/04-statistics.md).
