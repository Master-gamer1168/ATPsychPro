# CLAUDE.md

This repo is a resource bank for an **AT Psychology group-project research report** (an APA-style write-up of a replication experiment). The owner writes the report themselves. The repo holds the source documents, notes, templates and a stats helper. See `README.md` for the layout.

## Source precedence (highest first)

1. `sources/discussion-structure-revised.md` is the **authoritative Discussion structure**. It supersedes §6 of the guide. Keep it verbatim; don't paraphrase or soften it.
2. `sources/guide-how-to-write-research-report.md` covers everything else: structure, word counts, formatting, checklist.
3. `sources/sample-full-research-report.md` is a model of form only. Its Discussion ¶3–¶4 predate the revised structure, so don't treat them as compliant.

## Rules when working here

- Keep `sources/` transcriptions faithful to the originals. Editorial additions go in clearly marked notes.
- Any note, template or checklist that describes the Discussion must follow the revised structure:
  - ¶3: two specific design/materials/procedure limitations, at least one on internal validity or reliability, no bare "small sample" or "ecological validity", each tied to the results' means, spread or outliers, each with a concrete fix
  - ¶4: a conclusion supported by the data, plus one real-world situation the task mirrors and one where real-world factors would change the outcome
- The guide says the report is written **in class using only the workbook and collected data**. Material here is for preparation; don't present it as something to use during in-class writing.
- Verify numbers before stating them (`python3 tools/stats.py demo` reproduces the sample's Appendix E).
