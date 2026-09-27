# Domain checklists

These are technical prompts for the user's core fields. ★ marks points the user raised in past reviews. Tool names are examples of current practice. Before asking authors to cite something, check it is still current and appropriate; this file does not replace that check.

## Contents

1. GWAS, shared genetics and pleiotropy
2. Mendelian randomization
3. Statistical fine-mapping
4. Functional annotation, heritability partitioning, regulatory variant scoring
5. QTL mapping, colocalization and TWAS
6. Transcriptomics, multi-omics, single-cell
7. Drug repurposing and connectivity analysis
8. Machine learning in biomedicine
9. Mechanistic and agent-based models
10. Wet-lab mechanism
11. Clinical and translational claims
12. Statistics and reporting sanity checks (run on every manuscript)
13. Causal graphs, knowledge graphs and time-ordered data

---

## 1. GWAS, shared genetics and pleiotropy

- **Counting loci.** Count independent signals after LD clumping or conditional analysis (e.g. COJO), not all genome-wide significant SNPs ★. Correlated SNPs represent the same signal, so raw counts distort the overlap statistics ★.
- **Defining "shared".** Physical proximity (e.g. within ±500 kb) is a generous proxy for shared biology ★. Stronger evidence comes from:
  - colocalization: coloc-ABF, or coloc with SuSiE when a locus carries several signals ★;
  - multi-trait fine-mapping ★;
  - SNP-level pleiotropy tests (e.g. PLACO) ★;
  - local genetic correlation (e.g. LAVA, SUPERGNOVA, ρ-HESS) ★;
  - genome-wide genetic correlation (LDSC), with a citation for any rg value quoted ★.
- **Kinds of pleiotropy.** Horizontal (independent effects on both traits) and vertical (mediated: trait A → trait B) ★. A review that covers only one should acknowledge the other.
- **Allelic heterogeneity.** Multiple signals per locus complicate pairwise colocalization. Ask how the analysis handles it ★.
- **Nearest gene ≠ causal gene** ★. Ask for a caveat in figures and text, or for gene prioritization evidence: eQTL/pQTL colocalization, fine-mapped coding variants, or integrative scores such as PoPS or Open Targets locus-to-gene.
- **Multi-trait methods.** MTAG, GWIS, cross-trait meta-analysis ★; state what each assumes.
- **Clustering and partitioned polygenic scores.** Distinguish hard from soft clustering (e.g. bNMF) and say what each assumes ★. Ask what limits predictive accuracy: methods, data quality, or biology ★. Be careful when asserting what a specific clustering method "requires"; a past claim of this kind was successfully rebutted.
- **Population structure and diversity.** Look for PCs or mixed models, genomic inflation and the LDSC intercept, ancestry diversity, and whether findings transfer across ancestries ★ (cite multi-ancestry studies where they exist).
- **Effect reporting.** Show "OR (95% CI)" for binary traits, not "effect" ★. The CI must contain the point estimate ★. The effect allele must be defined and the genome build stated.
- **Polygenic scores.** Check that training and validation samples are separate, that calibration and portability across ancestries are reported, and that incremental value over clinical risk factors is shown.

## 2. Mendelian randomization

- **Instruments.** Check the selection threshold, clumping, F-statistics for weak instruments, sample overlap between exposure and outcome GWAS, and allele harmonization (palindromic SNPs).
- **Assumptions.** Relevance, independence and exclusion restriction. Ask for sensitivity analyses: MR-Egger (intercept), weighted median and mode, MR-PRESSO, heterogeneity (Cochran's Q), and leave-one-out.
- **Direction.** Ask for Steiger filtering or directionality tests. Consider bidirectional MR when reverse causation is plausible ★. If the authors believe in one direction, they should make that case explicitly ★.
- **Mediation and confounding pathways.** Multivariable MR (e.g. for obesity as a shared driver) ★. For a drug-target MR, ask which pathway mediates the effect (e.g. glucose lowering vs weight loss) ★.
- **Cis-MR and drug targets.** Pair with colocalization so the exposure and outcome signals are known to share a causal variant.
- **Which sensitivity analyses apply.** MR-Egger, the weighted median and MR-PRESSO need many independent instruments. With one or a few independent cis instruments they cannot be used or have little power. Correlated cis variants can be used with methods that model the LD between them (e.g. generalized least squares with an Egger correction). State the conditions rather than saying a method "cannot be used for molecular MR".
- **Drug-target vs polygenic instruments.** They can give different answers for the same exposure, e.g. a null estimate from variants in the drug-target gene and a significant one from genome-wide variants. Ask for both estimates to be reported separately; don't let a review cite only one.
- **Univariable vs multivariable MR.** They estimate different effects (total vs direct), so an estimate that weakens after adjustment is not a conflict between studies.
- **What colocalization and HEIDI show.** They test whether two traits share a causal variant, rather than having distinct variants in LD. They do not rule out horizontal pleiotropy, and a shared variant does not by itself show that the molecular trait mediates the effect on disease.
- **Interpretation.** For a binary exposure, interpret per unit of log-odds of liability. Consider collider and selection bias. For late-onset outcomes, survival bias and family-history proxy phenotypes can weaken MR estimates.

## 3. Statistical fine-mapping

- **Concepts.** Conditional analysis (detecting secondary signals) is not fine-mapping (identifying causal variants with quantified uncertainty) ★. Multi-trait fine-mapping and colocalization answer different questions ★.
- **Method coverage.**
  - Single-causal and LD-free: ABF, simple and widely used. It assumes one causal variant per locus ★.
  - Multi-causal: SuSiE / SuSiE-RSS, FINEMAP, CAVIAR / CAVIARBF. CAVIAR and PAINTOR are limited in practice by computational cost, not by a hard cap on k; hedge claims like this ★.
  - Annotation-informed: PAINTOR, PolyFun ★.
  - Multi-ancestry: SuSiEx, MESuSiE, and alternatives such as cross-ancestry meta-analysis or combining credible sets ★.
  - Multi-trait: e.g. mvSuSiE ★.
  - Robust to LD mismatch: CARMA, RSparsePro ★.
- **QC of summary statistics.** Allele-flip detection (e.g. `kriging_rss` in susieR) ★, GWAS–LD reference heterogeneity (DENTIST) ★, suspicious loci in meta-analyses (SLALOM) ★. Also: an in-sample LD reference vs an external panel, and SNPs missing from the reference, which cause false negatives ★.
- **Outputs.**
  - PIPs and credible sets: coverage, size and purity ★.
  - Post-hoc filters, e.g. a purity threshold or dropping credible sets without a significant variant ★.
  - Calibration and resolution metrics ★.
  - Within one single-effect credible set the probabilities sum to 1, and PIPs displayed for one credible set can't add up to more than 1 ★.
  - Whether a PIP is overall or signal-specific must be stated ★.
- **Hyperparameters.** The maximum number of causal variants (L/k) ★, with practical guidance (e.g. using conditional analysis to estimate the number of independent signals); prior effect variance; convergence.
- **Evaluation.** Simulations *and* real-data validation: functional or heritability enrichment of high-PIP variants, replication across ancestries, validated variant sets ★.
- **Downstream.** Annotation, colocalization, MR and variant prioritization bridge fine-mapping to experimental validation. Exhaustive testing is rarely feasible even for small credible sets ★.
- **Choosing data.** For multi-trait analysis, which traits to include and how many ★; including every genome-wide correlated trait can mislead a regional analysis ★. For multi-cohort or multi-ancestry analysis: consensus vs heterogeneous effects, missing data, and matched LD ★.

## 4. Functional annotation, heritability partitioning, regulatory variant scoring

- **Chromatin state models.** Enough marks, including repressive and silencing marks, to capture the major regulatory states (cf. the ChromHMM 15/18-state models) ★. Are the latent states biologically interpretable, and what fraction of the genome do they cover ★?
- **Imputed vs observed signals** (e.g. ChromImpute). Which is used when both exist, and how consistent they are ★.
- **Partitioned heritability (S-LDSC).**
  - How annotations are built (binary vs continuous, tissue-specific weighting) ★;
  - conditioning on the baseline(-LD) model;
  - reporting enrichment *and* τ* ★;
  - trait breadth, using public summary statistics rather than a handful of traits ★.
- **Validation.** Curated, experimentally validated regulatory variants; MPRA; allelic imbalance; QTLs — assessed systematically, not through two showcase examples ★. Compare with sequence-based scores (e.g. deltaSVM) and integrative, context-specific scores (e.g. cepip, CADD) ★. If a single raw feature (e.g. DNase) outperforms the model, explain why, e.g. correlated features ★.
- **Choosing annotations.** Which tissue or cell type, and how that choice is justified for non-coding variants ★. Resources such as ENCODE and CADD, and their limits ★.
- **Terminology.** "Resolution" of predicted regions, not "width" ★.

## 5. QTL mapping, colocalization and TWAS

- **Tools.** TensorQTL, QTLtools, MatrixEQTL. FastQTL is no longer maintained, so benchmark against current tools ★.
- **Covariates.** Genotype PCs; hidden factors (PEER or PCs of expression); cell-type composition (critical for methylation and bulk tissue).
- **Methods.** Phenotype normalization (e.g. inverse-normal), cis-window definition, permutation or beta-approximation for gene-level significance, FDR, conditionally independent QTLs.
- **mQTL specifics.** Array type (450K/EPIC), removing probes that contain SNPs or cross-hybridize, correcting cell composition.
- **Data types.** Imputed dosages, rare variants, missing data; how multiple testing scales ★.
- **Benchmarks.** Speed and memory *and* concordance of results with established tools; several data sizes; fair settings ★.
- **Release details.** State which release was used (e.g. GTEx version), single-tissue vs tissue-specific associations, and how lead variants are defined ★.
- **TWAS and PWAS.** Associations can arise from LD between the prediction-model SNPs and a causal variant acting through another gene, or from co-regulation of nearby genes (Wainberg et al., Nat Genet 2019). These methods prioritize genes; they don't establish causality by themselves.
- **Colocalization assumptions.** The original coloc method assumes at most one causal variant per trait in a region. With several independent signals it can miss or mis-assign colocalization; extensions exist (e.g. coloc with SuSiE; Wallace, PLoS Genet 2021). When QTL samples are small (e.g. brain), a low posterior probability of a shared variant is weak evidence against sharing; strong support for distinct variants is more informative.
- **pQTL instruments.** Ask which tissue the proteins were measured in (plasma, CSF or brain; large plasma studies include the UK Biobank Pharma Proteomics Project, Sun et al., Nature 2023), whether assay platform or epitope effects could explain a cis signal, and whether the pQTL replicates across platforms.

## 6. Transcriptomics, multi-omics, single-cell

- **Platforms.** Microarray vs RNA-seq; mixed array versions; probe-set bias ★.
- **Batch effects.** Normalization and batch correction (e.g. ComBat) with diagnostics ★. Watch for batch confounded with the biological contrast.
- **Design.** Sample sizes (e.g. 4 vs 7 is fragile) ★; paired designs; tissue heterogeneity.
- **DEGs.**
  - Justified thresholds (fold change and FDR) ★;
  - counts that match across sections ★;
  - up- and down-regulated numbers reported ★;
  - meta-analysis (rank-based, random-effects) rather than intersecting lists ★.
- **Composition.** Deconvolution, or at least a discussion, when the compared groups differ in cell or tissue type ★.
- **Single-cell.**
  - Pseudobulk DE with donor as the unit of replication; avoid pseudoreplication;
  - doublets and ambient RNA;
  - over-correction during integration;
  - annotation markers shown.
- **Enrichment.** Background set, multiple testing, redundancy, direction.
- **Validation.** qPCR, independent cohorts, protein level ★.
- **Multi-omics integration.**
  - How data are harmonized; early, intermediate or late fusion ★;
  - cross-omics validation ★;
  - worked integrative examples rather than lists of studies ★;
  - field-standard terminology ★ (e.g. "multi-omics network analysis" rather than invented terms).

## 7. Drug repurposing and connectivity analysis

- **Nature of the evidence.** L1000CDS² and CMap/CLUE connectivity is correlational ★. Check for cell-line context mismatch and dose and time effects.
- **Face-value hits** ★. Filter by potency data, clinical phase, target tractability and toxicity ★.
- **Mechanism.** Link each top compound's known targets to the signature genes or pathways ★.
- **Sanity checks.** Do known positive controls (compounds with documented effects in the system) rank highly ★?
- **Validation.** At least one experimental test, or a clearly stated limitation.

## 8. Machine learning in biomedicine

- **Taxonomy** ★. Supervised, unsupervised, semi-supervised and reinforcement learning are paradigms; deep learning is a model family used within them.
- **Definitions.**
  - PCA transforms features into orthogonal components that capture maximal variance ★.
  - Choose linear (PCA) or nonlinear (UMAP, t-SNE) dimensionality reduction for the purpose at hand ★.
  - Feature selection and dimensionality reduction are distinct, with their own trade-offs ★.
- **Leakage and imbalance.**
  - Feature selection, normalization and resampling (e.g. SMOTE) go inside the training folds;
  - splits are made at patient level;
  - batch must not be confounded with the label.
- **Evaluation.**
  - External validation; calibration;
  - metrics suited to prevalence (AUPRC for rare outcomes);
  - comparison with simple baselines (e.g. regularized logistic regression);
  - uncertainty estimates.
- **Interpretability and adoption.** SHAP for tree models, saliency or attribution maps for CNNs, and how they bear on clinical adoption and regulatory expectations ★.
- **Ethics.** Actionable points rather than generalities ★:
  - consent for data reuse;
  - bias audits and health disparities;
  - privacy-preserving training (e.g. federated learning).
- **Reporting.** Follow the relevant guideline (e.g. TRIPOD+AI for prediction models); make code and models available.

## 9. Mechanistic and agent-based models

- **Accuracy.** Quantify with MAE or RMSE, not only correlation ★. Justify the validation sample size (power analysis) ★.
- **Calibration vs validation.** Keep them separate. Report parameter sensitivity (e.g. global sensitivity analysis), identifiability, and stochastic replicates.
- **Mechanistic insight.** Which parameters or input features drive responder vs non-responder differences ★?
- **Limits.** Cell types, pathways and spatial structure left out, and how adding them might change predictions ★.
- **Translation.** From ex vivo to in vivo; validation steps needed before clinical use; a workflow usable at the point of care ★.
- **Terminology.** "In silico" and "in vitro/in vivo", not "virtual/wet" experiments ★.

## 10. Wet-lab mechanism

- **TF → target.** ChIP-qPCR or EMSA for binding; a luciferase assay with wild-type vs mutated sites ★.
- **Protein–protein interaction.** Co-IP, ideally reciprocal ★.
- **Causality.** Loss- and gain-of-function with rescue; ≥2 independent siRNAs or guides.
- **Pathway claims.** Direct functional readouts, not enrichment alone ★.
- **Phenotypes.** Organism-level endpoints tied to the manipulation ★.
- **Reporting.** n (biological vs technical), tests, exact P values ★; representative images plus quantification; scale bars.
- **Reagents.** Cell line sources and authentication, culture conditions, construct maps ★.

## 11. Clinical and translational claims

- **Plausible numbers.** Global or disease statistics must be internally plausible ★. For example, a disease-specific death count cannot exceed all-cause mortality; check prevalence vs mortality.
- **Models vs human disease.** What the model does not capture (e.g. vasculopathy, comorbidities) ★.
- **Treatment realism.** Delivery barriers (e.g. the blood–brain barrier), off-target effects, safety ★.
- **Case reports.** Follow CARE; define outcome claims against the literature ★.
- **Population context.** Ancestry diversity; social determinants where relevant.

## 12. Statistics and reporting sanity checks (run on every manuscript)

- [ ] The same quantity matches wherever it appears (abstract, results, figures, tables, supplement) ★
- [ ] CIs contain their point estimates; OR vs beta vs "effect" are labeled correctly ★
- [ ] Probabilities lie in [0, 1]; mutually exclusive probabilities sum to ≤ 1 ★; percentages add up
- [ ] n agrees across methods, figures and tables; the unit of analysis is clear
- [ ] Tests fit the data; multiple testing is handled; exact P values are given where the journal expects them
- [ ] Magnitudes are plausible (effect sizes, fold changes, death counts) ★
- [ ] Significance markers, scales and axes are defined ★
- [ ] Legends match the figures (no leftovers from other projects) ★; figures and supplements are cited in the right order ★
- [ ] Units and symbols are consistent (μM), and gene/protein nomenclature is correct ★
- [ ] Genome build, effect allele and data versions are stated for genomic results

## 13. Causal graphs, knowledge graphs and time-ordered data

- **Bayesian networks and causal discovery.** The authors should state the causal Markov and faithfulness assumptions and how latent confounding is handled. From observational conditional independences alone, a network is generally identified only up to its Markov equivalence class. Extra assumptions (functional form, non-Gaussian noise, time order, interventions, genetic anchors) can orient more edges. State the conditions; don't say edge direction can never be learned.
- **Two kinds of knowledge-graph reasoning.** Signed, directed reasoning over curated causal interactions (e.g. upstream-regulator analysis) makes a causal claim that rests on the curation. Embedding-based link prediction over literature-mined graphs is associational. A review should keep them apart and say what claim each supports.
- **Adjusting for a mediator.** It is wrong when the total effect is the target. Under additional assumptions it is how a direct effect is estimated. Check that tables and figures don't just say "never adjust for a mediator".
- **Time order is not causation.** Temporal precedence alone does not show that the earlier change causes the later one. Keep Granger-type time-series methods apart from disease-progression models. Their assumptions and outputs differ. For example, subtype-and-stage models (e.g. SuStaIn) do not assume one uniform trajectory and can be fitted to cross-sectional data.
- **Longitudinal cohorts.** Time-varying confounding needs g-methods or target trial emulation. Suggest this briefly; in a review it is rarely worth a Major item on its own.
