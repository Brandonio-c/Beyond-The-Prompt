# Beyond-The-Prompt

**Supplementary materials storage cache** for the systematic literature review:

> **Beyond the Prompt: Approaches to Knowledge Boundary Detection in Large Language Models — A Systematic Literature Review**  
> *Anonymous Authors*

---

## Summary

Large Language Models (LLMs) are increasingly used in critical domains (e.g. clinical decision-making) but often produce incorrect or fabricated outputs (hallucinations). Determining what knowledge a generative model holds *internally*, without adding external information, remains an open challenge. This review maps architectures and methods that **detect or determine the knowledge boundary** of a generative system without providing external sources of information.

- **Screening:** 5,919 articles → dual independent screening by **8 reviewers** → **199** relevant papers.
- **Eligibility:** Pilot data extraction and scoping → **43** eligible studies.
- **Synthesis:** Convergent, segregated synthesis → **5** prevalent areas of interest; notable gaps between what models know and how well they use that knowledge.

**Index terms:** Large Language Models, Knowledge Boundary Detection, Hallucination Mitigation, Mechanistic Interpretability, Uncertainty in AI, Benchmark Evaluation, Explainable AI, Systematic Literature Review.

---

## Repository structure

```
Beyond-The-Prompt/
├── README.md                 # This file
├── data/                     # Screening, extraction, and reference data
│   ├── Annotator Reconcilliation/   # Reconciliation & conflict resolution
│   ├── Beyond the Prompt (NLM) Full Text Review - Information Extraction (Responses).xlsx
│   ├── bib_files/            # Bibliographies and Covidence RIS exports
│   ├── covidence_full_text_review.ris
│   ├── Covidence-Inter-rater reliability - Title and abstract screening.csv
│   └── full_text_review_papers.xlsm
└── documentation/            # Protocol and search documentation
```

---

## `data/`

### Annotator reconciliation

- **Location:** `data/Annotator Reconcilliation/`
- **Contents:**
  - **annotator_reports_final/** — Final screening reports per reviewer (Brandon, Davis, Ishan, Kwesi, Mike, Mohammed Afaan, Srividya, Xinchen, Yuexi).
  - **conflict_report_summary.xlsx**, **conflicts_final.xlsx** — Conflict summaries and resolved conflicts from dual independent screening.
  - **covidence_conflicts/** — Covidence conflict workflow:
    - `extract.py` — Extracts conflict data from Covidence (JSON in saved HTML).
    - Annotator reports (original and final), conflict Excel outputs, `conflict_info.html` (input JSON), `intermediate_data.json`.
    - See **`data/Annotator Reconcilliation/covidence_conflicts/README.MD`** for usage (Covidence URL, save webpage, run script; note: script filename in that README is `extract_v2.py`, actual file is `extract.py`).

### Full-text review and extraction

- **Beyond the Prompt (NLM) Full Text Review - Information Extraction (Responses).xlsx** — Full-text review information extraction responses.
- **full_text_review_papers.xlsm** — Full-text review paper list (with macros).
- **covidence_full_text_review.ris** — Full-text review export from Covidence (RIS).

### Bibliographies and RIS exports

- **bib_files/**
  - **BTP_final_included_papers.bib** — BibTeX for the final included papers (45 entries in this cache; review reports 43 eligible studies).
  - **covidence_title-and-abstracr_included_papers.ris** — Title/abstract screening: included papers (RIS).
  - **covidence_title-and-abstracr_excluded_papers.ris** — Title/abstract screening: excluded papers (RIS).

### Inter-rater reliability

- **Covidence-Inter-rater reliability - Title and abstract screening.csv** — Pairwise title/abstract screening agreement (e.g. proportionate agreement, Yes/No probabilities, Cohen’s Kappa) for reviewer pairs (e.g. Davis, Kwesi, Mike, Srividya, Xinchen, Yuexi, Ishan, Mohammed Afaan, Brandon).

---

## `documentation/`

Protocol and search materials (dates in filenames indicate versions):

- **241002 - Beyond the Prompt Systematic Review Protocol - Brandon Colelough.docx** — Initial protocol.
- **241118** — Inclusion–exclusion criteria and examples.
- **241127** — Updated inclusion–exclusion examples.
- **Search Summary - Beyond the Prompt - TIAB.docx** — Search summary for title/abstract screening.

---

## Quick reference

| Item | Location |
|------|----------|
| Final included papers (BibTeX) | `data/bib_files/BTP_final_included_papers.bib` |
| Full-text extraction responses | `data/Beyond the Prompt (NLM) Full Text Review - Information Extraction (Responses).xlsx` |
| Conflict resolution & annotator reports | `data/Annotator Reconcilliation/` |
| Inter-rater reliability (title/abstract) | `data/Covidence-Inter-rater reliability - Title and abstract screening.csv` |
| Protocol & search docs | `documentation/` |
| Covidence conflict extractor | `data/Annotator Reconcilliation/covidence_conflicts/` (see README.MD there) |

---

*This repository is a supplementary materials cache for the systematic review and is not intended as a standalone replication package; use in conjunction with the review manuscript and protocol.*
