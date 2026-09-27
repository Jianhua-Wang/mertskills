# Checklists by article type

Use these as prompts for thought, not a form to fill in: raise only the items that matter for this manuscript. ★ marks points the user has raised in past reviews; these are the user's habitual concerns and deserve extra attention.

## Contents

0. Every manuscript
1. Computational research article (analysis of existing or new data)
2. Wet-lab / translational research article
3. Public-data mining, meta-analysis, bioinformatic screening
4. Methods / software / tool paper
5. Database / web resource
6. Review / perspective
7. Case report
8. Thesis (学位论文)

---

## 0. Every manuscript

- [ ] The central claim can be stated in two sentences, and the conclusions don't go beyond the evidence ★
- [ ] Numbers match across the abstract, text, figures and tables ★ (e.g. one section reports 92 DEGs and another 1,208)
- [ ] Thresholds and parameters are justified ★ (e.g. the log2FC cutoff)
- [ ] Factual claims are cited ★ (e.g. a genetic-correlation value stated without a reference)
- [ ] The key citations behind the main claims say what the text says they say ★. Read the sources (SKILL.md, workflow step 5) before calling a citation wrong.
- [ ] Summary tables agree with the text they summarize ★ (e.g. a table row claims a method shows what the text says it cannot show)
- [ ] The abstract has no citations if the journal forbids them ★
- [ ] Low priority, noted but left out of the report by default: citation and reference-list style, abbreviation lists, the order in which tables are first cited
- [ ] Figures, viewed as images (separate TIFF files included, compared with the embedded versions):
  - legible fonts; distinguishable colors ★
  - significance markers explained ★
  - legends that match the content (no copy-paste leftovers) ★
  - panels cited in the right order (no swapped figure references) ★
- [ ] There is a limitations section and it is honest ★
- [ ] Data and code availability, ethics approval, consent and conflicts of interest are stated
- [ ] The language is clear. If errors are pervasive, suggest professional editing ★ and give 2–3 quoted examples

## 1. Computational research article

- [ ] Data provenance is clear: source, release or version, sample sizes, inclusion criteria, QC ★ (e.g. which eQTL release; single-tissue or tissue-specific pairs; how "lead" variants are defined)
- [ ] Each method choice is justified, and field-standard analyses are present (see the domain checklists)
- [ ] Results are replicated or independently validated ★
- [ ] Results are compared with existing methods or resources ★
- [ ] Sensitivity analyses cover the key choices; multiple testing is handled
- [ ] Interpretation goes beyond gene or variant lists to mechanism ★ (e.g. which model features drive differential responses)
- [ ] The evaluation is broad enough. If public resources exist, ask for more traits or datasets ★ (e.g. 21 traits, when summary-statistic repositories offer hundreds)
- [ ] When a simple baseline beats the proposed approach, the paper explains why ★

## 2. Wet-lab / translational research article

- [ ] There is direct functional evidence for the mechanism claimed, not only enrichment or correlation ★
  - a pathway claim needs a direct assay (e.g. platelet aggregation or P-selectin for platelet activation);
  - a TF→target claim needs binding evidence (ChIP-qPCR or EMSA) and a luciferase assay with the binding site mutated ★;
  - a protein–protein interaction needs Co-IP ★.
- [ ] Phenotypic outcomes are linked to the manipulation ★ (behavior scores, lesion volume, edema, survival)
- [ ] The model's relevance and limits are discussed ★ (e.g. an injected-blood model lacks the underlying vasculopathy; healthy donors vs patients; an in vitro assay vs the in vivo microenvironment)
- [ ] The stimulus is realistic ★ (a single toxic component vs a complex mixture; suggest a more complete stimulus, e.g. whole-blood lysate)
- [ ] Controls, n per group, biological vs technical replicates, statistical tests, and randomization and blinding are all reported
- [ ] Reagents and cells are described: sources, culture conditions, construct design ★
- [ ] Knockdown or overexpression specificity is shown: multiple siRNAs or guides, rescue, off-target considerations
- [ ] Translational barriers are discussed ★ (delivery across the blood–brain barrier, off-target effects, safety)
- [ ] Gene symbols are italicized and proteins are not ★; units are consistent (μM, not uM) ★

## 3. Public-data mining, meta-analysis, bioinformatic screening

- [ ] Dataset selection criteria are stated, and quality and comparability are assessed beyond availability ★
- [ ] Platform heterogeneity is addressed: microarray only vs RNA-seq; different array versions and labs ★
- [ ] Data are normalized across platforms or batch-corrected (e.g. ComBat), with diagnostics such as PCA colored by batch ★
- [ ] Datasets are integrated statistically (rank-based or random-effects meta-analysis), not just by intersecting per-dataset DEG lists ★
- [ ] Composition confounding is considered ★ (e.g. cell types or tissues unbalanced between the two arms)
- [ ] Sample sizes are adequate (e.g. 4 vs 7), and robustness is shown ★
- [ ] Findings are replicated independently: in silico in another resource, or at minimum qPCR in one extra dataset ★
- [ ] Markers are distinguished from drivers ★. A gene that changes during a transition may be a lineage marker rather than a barrier, so suggest a perturbation test such as RNAi.
- [ ] Enrichment analyses have an appropriate background set, multiple-testing control, and redundancy handled
- [ ] Hub-gene and network claims are validated, not only asserted
- [ ] Computational drug hits are filtered and put in context (see the domain checklist) ★

## 4. Methods / software / tool paper

- [ ] It is benchmarked against the current, maintained state of the art, not only unmaintained tools ★ (e.g. for QTL mapping, TensorQTL rather than only FastQTL)
- [ ] It is compared with alternative paradigms, not only its own family ★ (e.g. sequence-based and integrative regulatory scores, not only segmentation methods)
- [ ] The benchmark is fair:
  - same data, thresholds, hardware, threads and versions;
  - several data sizes;
  - accuracy and concordance as well as speed and memory.
- [ ] It is validated on ground-truth simulations *and* real data, with calibration reported (type I error, FDR)
- [ ] The evaluation is systematic, on curated validated sets rather than cherry-picked examples ★ (e.g. two illustrative variants, when curated validated-variant collections exist)
- [ ] Surprising baselines are explained ★ (e.g. why a raw input signal outperforms the model; correlated features)
- [ ] Limitations and scope are discussed ★:
  - scalability limits and algorithmic assumptions;
  - supported data types (imputed dosages, rare variants, covariates, missing data).
- [ ] The software is usable: repository, license, versioned release, documentation, example data, installation, input/output formats
- [ ] The paper is written in journal style, not as a thesis chapter ★. Technical detail and long formulas go to the supplement ★.
- [ ] Terminology is precise ★ (e.g. "resolution" rather than "width"); latent states are biologically interpretable ★ (e.g. what fraction of the genome is assigned to interpretable classes)

## 5. Database / web resource

- [ ] Scope, data sources and versions, and the curation and QC pipeline are described; the update plan is stated
- [ ] The unique value over existing resources is shown by an explicit comparison
- [ ] It is usable: search, browse, download, API, documentation, example queries
- [ ] Sustainability is addressed: hosting, maintenance plan, license, versioned releases
- [ ] Case studies demonstrate real utility
- [ ] The URL works at review time, with reasonable responsiveness

## 6. Review / perspective

- [ ] The framing lays out the challenges before the methods ★
- [ ] The key questions and objectives are stated ★; solved and open questions are distinguished
- [ ] Concepts are distinguished correctly ★ (see report-templates.md §2)
- [ ] The taxonomy is correct ★ (e.g. deep learning is a model family usable in supervised, unsupervised or semi-supervised settings, not a parallel paradigm)
- [ ] Widely used methods are covered, with their weaknesses ★
- [ ] There is practical guidance: QC, hyperparameters, choice of data sources and trade-offs ★
- [ ] The review synthesizes rather than describes ★:
  - studies grouped by method or clinical objective;
  - comparisons and conflicting results, with the reason for each difference (a difference is not always a conflict; e.g. univariable and multivariable MR estimate different effects);
  - a short summary at the end of each method section: what the method has shown and what is still unclear.
- [ ] Specific studies are integrated into general conclusions rather than read as anecdotes ★
- [ ] Headline conclusions rest on more than one or two examples, and those examples are reported correctly ★. Read the sources behind them.
- [ ] Methods reviews state, for each method, its assumptions and the type of claim it supports (causal effect, shared variant, prioritization, association) ★
- [ ] Summary tables give estimates with 95% CIs, units, data sources and the number of instruments or samples, and each row matches the cited study ★
- [ ] A self-described narrative review is not asked for a systematic search strategy
- [ ] Length is appropriate ★ (e.g. ~14k words, with repeated explanations of the same techniques); sections are ordered logically ★ (data types before methods)
- [ ] Worked examples or case studies are given where the text stays abstract ★
- [ ] The ethics discussion has substructure and practical examples ★ (data privacy, bias mitigation, regulatory guidance)
- [ ] Figures are accurate and informative, not buzzword collages ★; tables have useful comparison columns ★
- [ ] References are recent and diverse (e.g. multi-ancestry studies) ★
- [ ] The depth suits the journal's readership ★

## 7. Case report

- [ ] The rationale for each treatment decision and its sequencing is given ★
- [ ] Molecular findings are discussed for *this* disease or tumor type specifically ★
- [ ] Claims are quantified against the literature ★ (e.g. "relatively long survival" compared with reported median survival)
- [ ] The key lessons for future management are stated explicitly ★
- [ ] A timeline, CARE-checklist items and patient consent are present
- [ ] The literature review is focused and up to date
- [ ] The abstract has no citations (per journal) ★; the citation format is correct ★

## 8. Thesis (学位论文)

The categories and recurring items are in [report-templates.md §7](report-templates.md). Beyond those:
- [ ] The research questions are clearly derived from the background; each chapter answers one
- [ ] The level matches the degree: PhD work needs mechanistic depth or a methodological contribution ★
- [ ] Statistics support every claim of significance ★
- [ ] Figures support the text; mismatches are explained ★
- [ ] Grouping or model choices introduce no selection bias ★
- [ ] The innovation claims are realistic
