# Prerequisites: what to have in place before Week 1

> Disclaimer: personal academic, research-only, non-commercial project. This file lists only **open learning sources whose license was verified on the lookup date** (table in §5). Sources under a non-commercial license (CC BY-NC-SA) are used **through the link only**; no content is copied into the repo. See [CLAUDE.md](../CLAUDE.md). Vietnamese version: [prerequisites_vi.md](prerequisites_vi.md).

## 1. How to use this file

- **Do not study all of this before starting.** The 18-week roadmap re-teaches most of it: math and learning theory in Weeks 1-3 (Phase 0, cited by page from the book shelf in [`../docs/books/README.md`](../docs/books/README.md)), PyTorch in Week 4, autograd in Week 5. This file is for (a) self-assessing gaps, (b) knowing which source to open when a specific gap shows up, and (c) collecting the background areas (DSA, OCR, big data, design patterns...) that do not fit neatly into any week.
- The table uses three levels. "Required" means that without it Weeks 1-6 stall, so check with the §4 checklist before starting. "Needed before Week X" can be caught up right before that week, not before Week 1. "Awareness" means understanding the concept and knowing the tool exists; the roadmap does not require deep practice.
- The Required / Needed / Awareness ratings are the author's judgment based on the content of the weeks in this repo, not an objective standard.

## 2. Map: background area, which weeks need it, level

| Area | Needed for | Level |
|---|---|---|
| Python (functions, classes, list/dict comprehensions, virtualenv/pip) | Every week | **Required** |
| Linear algebra and basic calculus (matrices, dot product, chain rule) | Taught systematically in Weeks 1-2; used from Week 4 | High-school math is enough; Weeks 1-2 re-teach it in full |
| Data structures and algorithms (big-O, hash map, heap, graph traversal, DP) | Throughout (attention O(n²), BPE merges, beam search, KV cache) | **Required** at the big-O and hash-map level; the rest Needed before Week 6 |
| Basic machine learning (train/val/test, overfitting, loss, metrics) | Taught systematically in Week 3; used in Weeks 8-11 (pretrain, fine-tune, eval) | Week 3 re-teaches it in full |
| Data science (NumPy, pandas: load, clean, transform data) | Weeks 9, 11, 13 (dataset preparation, RAG corpus) | Needed before Week 9 |
| DAG, directed acyclic graph | Week 5 (autograd is a DAG), Weeks 15-16 (LangGraph), Week 17 (KG) | Needed before Week 5 (concept) |
| Basic OCR and computer vision | Week 13 (ingesting scanned Vietnamese PDFs into RAG) | Needed before Week 13, at tool-use level |
| Big data and data pipelines (Spark, Airflow) | Week 8 (understanding how a FineWeb-scale pretraining corpus is processed) | Awareness |
| Design patterns | Weeks 15-16 (agent design: strategy, observer, pipeline...) | Awareness |
| System design | Weeks 15-18 (CornAgents.AI architecture, tool boundaries, HITL) | Needed before Week 15 |
| Developer tooling (git, shell, debugger) | Every week | **Required** at basic git and shell level |

## 3. Each area with open sources

### 3.1 General CS background and tooling

- **OSSU, Open Source Society University** ([github.com/ossu/computer-science](https://github.com/ossu/computer-science), MIT): a full CS curriculum assembled from free courses. Use it as a **lookup map** when you discover a gap, not sequentially.
- **The Missing Semester of Your CS Education** ([missing.csail.mit.edu](https://missing.csail.mit.edu/), CC BY-NC-SA 4.0, link only): shell, git, debugging, profiling, exactly the skills "nobody teaches" that this roadmap uses daily.

Enough when: you can clone, branch, commit and push with git; run a script, read an error, and activate a virtualenv in the shell.

### 3.2 Data structures, algorithms and algorithm theory

- **_Algorithms_, Jeff Erickson** ([jeffe.cs.illinois.edu/teaching/algorithms/](https://jeffe.cs.illinois.edu/teaching/algorithms/), CC BY 4.0, free full-text PDF): the best open algorithms textbook I could verify, covering recursion, DP, graph algorithms, NP-hardness.
- **cp-algorithms** ([cp-algorithms.com](https://cp-algorithms.com/), CC BY-SA 4.0): quick reference per algorithm with code.
- **MIT OCW 6.006 Introduction to Algorithms** ([ocw.mit.edu](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/), CC BY-NC-SA 4.0, link only): video lectures and problem sets if you prefer a course.

Why the roadmap needs it: attention is **O(n²·d)** in sequence length, which is why every KV-cache and FlashAttention technique exists (Week 6 and the advanced appendix); **BPE** is a greedy merge algorithm over a frequency table (Week 6); **beam search and sampling** are tree traversals (Week 7); hash maps underlie tokenizer vocabularies and vector stores. Enough when: you can estimate the big-O of a nested loop, use dict/set/heap fluently in Python, and know BFS/DFS.

### 3.3 Data science (NumPy, pandas)

- **NumPy user guide** ([numpy.org/doc/stable/](https://numpy.org/doc/stable/)): especially *broadcasting*; PyTorch tensor manipulation in Weeks 4-6 uses exactly these rules.
- **pandas user guide** ([pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)): load, filter, groupby, merge to prepare fine-tuning datasets (Weeks 9, 11) and clean the RAG corpus (Week 13).

Enough when: you can read CSV/JSON, filter and transform columns, and export JSONL (the fine-tuning dataset format).

### 3.4 Basic machine learning

- **Dive into Deep Learning (d2l)** ([d2l.ai](https://d2l.ai/), CC BY-SA 4.0): open code-first book; the early chapters (linear regression, MLP, optimization) overlap with and directly support Weeks 3-5.
- **scikit-learn MOOC (Inria)** ([inria.github.io/scikit-learn-mooc/](https://inria.github.io/scikit-learn-mooc/), CC BY 4.0): train/validation/test, over- and underfitting, cross-validation, metrics; the base for reading loss curves (Week 8) and designing evaluation (Weeks 11, 14, 18).
- **scikit-learn user guide** ([scikit-learn.org/stable/user_guide.html](https://scikit-learn.org/stable/user_guide.html)): metric reference (precision, recall, F1, reused as-is when measuring the KG in Week 17).

Enough when: you can explain why a held-out set is needed, read a loss curve and point at overfitting, and compute precision and recall by hand from a confusion matrix.

### 3.5 OCR and computer vision (for Vietnamese RAG, Week 13)

Real business documents are often **scanned PDFs** that must be OCR'd before chunking and embedding. This is the background area with the clearest Vietnamese-specific element:

- **Tesseract** ([github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract), Apache-2.0): classical OCR with Vietnamese traineddata (`vie`).
- **PaddleOCR** ([github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR), Apache-2.0): multilingual deep-learning OCR with Vietnamese support.
- **VietOCR** ([github.com/pbcquoc/vietocr](https://github.com/pbcquoc/vietocr), Apache-2.0): a Vietnamese-specific OCR model (TransformerOCR), aimed at exactly the tone and diacritic marks that multilingual OCR often gets wrong.
- **OpenCV** ([docs.opencv.org](https://docs.opencv.org/), Apache-2.0): image preprocessing before OCR (deskew, threshold, denoise).

For Vietnamese text, OCR errors in tone marks ("lãi suất" becoming "lai suat" or "lãi suắt") damage both BM25 and embeddings in Weeks 13-14: BM25 only matches exact spellings ("they work only if there is exact overlap of words between the query and document", SLP3 section 11.3, p. 264), and an embedding model's tokenizer splits a misspelled word into different pieces; so an OCR quality check plus Unicode NFC normalization (see `Week-13/01_theory_notes.md`) belongs before the chunking step. Enough when: you can run one of the tools above on one scanned PDF and judge the output by eye.

### 3.6 Big data and data pipelines (awareness)

- **Apache Spark docs** ([spark.apache.org/docs/latest/](https://spark.apache.org/docs/latest/), Apache-2.0): understand the distributed processing model; a FineWeb-scale pretraining corpus (Week 8) is filtered and deduplicated with pipelines of this kind. The roadmap does **not** require running Spark yourself.
- **Apache Airflow docs** ([airflow.apache.org/docs/](https://airflow.apache.org/docs/), Apache-2.0): DAG-based orchestration; reading the concept pages on DAG, task and operator is enough.

Enough when: you can explain why a pretraining dataset cannot be processed on one machine, and how a data pipeline is modeled as a DAG.

### 3.7 DAG: a concept running through the whole roadmap

One concept that appears at least four times in four guises:

| Week | Where the DAG appears |
|---|---|
| 5 | **Autograd's computation graph**: backward is a reverse traversal in topological order |
| 8 | The data pipeline that filters the corpus (Airflow/Spark style) |
| 15-16 | **Agent graph** (LangGraph): nodes are agents or tools, edges are control flow |
| 17 | Knowledge graph on **NetworkX** (BSD-3): note that a KG is a MultiDiGraph *that may contain cycles*, so it is no longer a DAG; the acyclic part applies to the pipeline that builds it |

Enough when: you can define a DAG and do a topological sort by hand on 5-6 nodes. Sources: **NetworkX docs** ([networkx.org/documentation/stable/](https://networkx.org/documentation/stable/), BSD-3) plus the graph chapter in Erickson's book (§3.2).

### 3.8 Design patterns and system design (for Phase 3, Weeks 15-18)

- **The System Design Primer** ([github.com/donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer), CC BY 4.0): caching, queues, load balancing, consistency versus availability trade-offs; the base for designing CornAgents.AI with tracing and HITL gates (Weeks 15-18).
- **The Architecture of Open Source Applications** ([aosabook.org](https://aosabook.org/), CC BY 3.0): real architectures of open-source systems, a case-study way to learn system design.
- A per-pattern overview of the GoF design patterns is on Wikipedia ([Software design pattern](https://en.wikipedia.org/wiki/Software_design_pattern), CC BY-SA 4.0, overview level). Patterns you will meet again in Phase 3: *Strategy* (choosing model or prompt per route), *Observer* (Langfuse tracing callbacks), *Chain of Responsibility* (prompt chaining), *Facade* (a tool interface wrapping an API).
- Transparency note: the popular `faif/python-patterns` repo **has no LICENSE file** (checked 2026-08-12) and is excluded under this repo's source policy. I could not verify any other in-depth design-pattern resource with a clear open license in that lookup.

Enough when: you can recognize and name a pattern when you meet it in agent framework code; system design at the level of a one-page diagram with data flow and failure points (exactly the Week 15 deliverable `03_cornagents_architecture.md`).

## 4. Self-check before Week 1 (Required level)

- [ ] Write a Python class with `__init__` and methods, and use list/dict comprehensions without looking anything up
- [ ] Multiply two matrices by hand (2×3 · 3×2) and state the result shape
- [ ] State the chain rule and use it to differentiate f(x) = (2x+1)²
- [ ] Estimate the big-O of a two-level nested loop
- [ ] Use Python dict/set where appropriate (O(1) lookup instead of scanning a list)
- [ ] git: clone, branch, commit, push; shell: run a script, activate a virtualenv

Any box unchecked: open that area's source in §3, fill only that gap, then start Week 1. "Needed before Week X" areas are caught up right before that week; "Awareness" areas are skimmed when the relevant week arrives.

## 5. Consolidated source table (licenses verified 2026-08-12)

| Source | Area | License | How verified |
|---|---|---|---|
| OSSU computer-science | General CS | MIT | GitHub API |
| Missing Semester (MIT) | Tooling | CC BY-NC-SA 4.0 *(link only)* | Repo README |
| _Algorithms_, Jeff Erickson | Algorithms | CC BY 4.0, free PDF | Book page (jeffe.cs.illinois.edu) |
| cp-algorithms | Algorithms | CC BY-SA 4.0 | GitHub API |
| MIT OCW 6.006 | Algorithms | CC BY-NC-SA 4.0 *(link only)* | OCW Terms of Use page |
| Dive into Deep Learning (d2l-en) | ML | CC BY-SA 4.0 | Repo LICENSE file |
| scikit-learn MOOC (Inria) | ML | CC BY 4.0 | GitHub API |
| NumPy / pandas / scikit-learn docs | Data science | Official docs, BSD projects | Docs pages |
| Tesseract | OCR | Apache-2.0 | GitHub API |
| PaddleOCR | OCR | Apache-2.0 | GitHub API |
| VietOCR (pbcquoc) | Vietnamese OCR | Apache-2.0 | GitHub API |
| OpenCV | Vision | Apache-2.0 | GitHub API |
| Apache Spark docs | Big data | Apache-2.0 | GitHub API |
| Apache Airflow docs | DAG/pipeline | Apache-2.0 | GitHub API |
| NetworkX docs | Graph | BSD-3 | Repo LICENSE file |
| System Design Primer | System design | CC BY 4.0 | Repo LICENSE file |
| AOSA (aosabook.org) | System design | CC BY 3.0 | Book home page |
| Wikipedia (Software design pattern) | Design patterns | CC BY-SA 4.0 | Wikipedia footer |
| underthesea | Vietnamese NLP (supports Week 13) | Apache-2.0 | GitHub API |

> Repo rule, repeated: a license is a **snapshot on the lookup date**; before reusing code or content from any source above, re-check the license at the time of use.
