# Style guide

This file sets the voice, the shape of a comment, a phrase bank and four exemplar reports. The phrases come from the user's reviews and joint reports, lightly edited for grammar and for plainness. The exemplars are anonymized composites: topics, names, line numbers and numbers are invented, but the structure follows the user's current format.

## Contents

1. Voice principles
2. Anatomy of a comment
3. Weak vs strong comments
4. Item formats and anchors
5. Phrase bank
6. Wording pitfalls
7. Exemplars
   - A. Positive tool paper (minor revision)
   - B. Wet-lab mechanism paper (major revision)
   - C. Weak review article (reject)
   - D. Joint report organized by section (excerpt)

---

## 1. Voice principles

- **Plain words, short sentences.** The user rejected a draft because its long sentences and unusual words read as machine-written. Keep most sentences under about 25 words and give each one idea. Prefer the common academic word. Avoid words and habits that mark generated text, for example:
  - delve, crucial, pivotal, comprehensive, robust (outside its statistical sense), landscape, intricate, multifaceted, nuanced, holistic, leverage, underscore, showcase;
  - "shed light on", "pave the way", "play a crucial role", "a testament to", "it is worth noting that";
  - "Furthermore" or "Moreover" at the start of consecutive sentences; "not only … but also"; strings of three adjectives; em dashes.

  If the `paper-prose` skill is installed, its `references/ai-tells.md` has the full catalogue and `scripts/prose_check.py` flags these in a draft.
- **Person.**
  - Refer to "the authors".
  - A solo report uses "I" for judgments and hedges ("I suggest…", "as far as I know").
  - Joint reports use "we" or "the reviewers".
  - Don't mix persons within one report.
- **Content before judgment.** The opening paragraph first restates the study concretely: data (with accession IDs and sample sizes), design, methods, key numbers and main claim. Only then comes the overall quality, and then the tone sentence.
- **Credit what works, specifically.** "The Background explains well why associations alone cannot separate upstream drivers from reactive changes." Specific praise makes the criticism credible. Don't praise what a later comment criticizes.
- **Call errors errors.** Use "is incorrect", "is not supported by the cited study", "does not agree with the text", and follow each with the correct statement.
- **Hedge only what is uncertain.** "As far as I know…", "seems implausibly high and may confuse incidence with mortality". Don't hedge facts you have checked.
- **State conditions, not absolutes.** "When only one or a few independent instruments are available, MR-Egger cannot be used or has little power" is right; "MR-Egger cannot be used for molecular MR" is not.
- **Every criticism ends in an action:** a tool, analysis, experiment, reference, rewritten sentence, or at minimum a limitation to acknowledge.
- **Explain the stakes:** "Because this evidence supports the main conclusion of the abstract, the abstract should be checked as well."
- **Be firm when the evidence supports it.** Say plainly that a problem is fundamental; don't name the editorial decision in the text.
- **No sarcasm, no asides.** Rhetorical jabs ("without thinking too hard…", "but I digress") undermine a strong point and invite a defensive response.
- **Nothing about how the manuscript was written.** Never suggest AI use or carelessness; describe the error and the fix.

## 2. Anatomy of a comment

Location → observation → why it matters → request → (fallback).

> Lines 140 and 268. Line 140 reports 85 differentially expressed genes, whereas Line 268 gives a total of 1,150. [observation] Because the hub-gene and enrichment analyses depend on this list, it is unclear which set was analyzed. [why] Please reconcile the two numbers and justify the log2 fold-change cutoff. [request]

> Methods, section 2.4. The datasets come from different array platforms and laboratories, yet they are combined by intersecting per-dataset gene lists, with no cross-platform normalization or batch diagnostics. [observation] Technical variation, rather than biology, may therefore drive some of the overlap. [why] Please apply a formal meta-analysis (e.g. rank-based or random-effects) or batch correction, with diagnostics such as PCA colored by batch. [request] At minimum, please discuss how this limits the interpretation of the shared genes. [fallback]

A citation problem that supports a main conclusion follows the same shape, with the source's actual findings as the observation:

> Section "Risk factors", paragraph 2; Table 2, row 3. The text states that the effect of exposure X "largely disappears" in MR and cites ref 13. Ref 13 reports a null estimate from drug-target instruments (risk ratio 0.87, 95% CI 0.60–1.26), but a significant estimate from 200 genome-wide instruments (0.85, 95% CI 0.77–0.94), and its authors conclude that X may affect risk. [observation] This example is one of the two that support the main conclusion of the abstract. [why] Please report the two estimates separately and revise the statement, and check the abstract as well. [request]

## 3. Weak vs strong comments

| Weak | Strong |
|---|---|
| "The QC section is too short." | "Line 90. Quality control of summary statistics is essential for reliable fine-mapping, but the section names no methods. The authors could mention allele-flip detection (e.g. `kriging_rss` in susieR), checks for heterogeneity between the GWAS and the LD reference (e.g. DENTIST), and screens for suspicious loci in meta-analyses (e.g. SLALOM)." |
| "Compare with more tools." | "The benchmark compares the new tool only with PLINK 1.07, which was superseded years ago. A comparison with the current PLINK release (1.9 or 2.0) would be more informative. Please report runtime, peak memory and the agreement of the results on the same data, hardware and number of threads." |
| "Discuss the limitations of the model." | "The injection-based mouse model is appropriate but does not reproduce spontaneous human disease; for example, it lacks the underlying vasculopathy. Please discuss how this limits translation." |
| "Table 2 has errors." | "Table 2, trait pair A–B. The estimate is shown as 1.36 (1.05–1.30). A confidence interval must contain its point estimate, so please correct this entry and check the others." |
| "The ML section is confusing." | "Section 2 presents deep learning as a paradigm parallel to supervised and unsupervised learning. Deep learning is a family of models that can be trained in supervised, unsupervised or semi-supervised settings. Please reorganize Section 2 to reflect this." |
| "Soft clustering requires tissue-specific information." (overstated; the authors rebutted it) | "Soft clustering allows a variant to contribute to several processes. The tissues through which the clusters act are usually assessed afterwards, e.g. with tissue-specific annotations. Because the tissues that mediate the shared risk remain unclear, it would be worth acknowledging this." |
| "More experiments are needed." | "The pathway claim rests on enrichment analysis alone. A direct functional readout (e.g. platelet aggregation or P-selectin expression) in the cell model or in vivo would strengthen it. If this is not feasible, please present the pathway as a hypothesis." |
| "Several references are wrong: refs 2, 9, 15, 23, 35, 39, 40, 48 and 50." | "Citations and Table 2. Several citations do not support the statements they are attached to. For example, ref 2 analyzed only RNA-seq data, but it is cited for a study that aligned genotype, methylation, expression and protein data in the same samples. Please check all citations, and the data sources and methods in each row of Table 2, against the cited studies." |

## 4. Item formats and anchors

Anchors:
- With line numbers: `Line 18.` / `Lines 140 and 268.`
- Without line numbers: `Section "Colocalization and summary-data methods", paragraph 1.` / `Table 3, time-resolved row.` / `Figure 2, Panel E.` / `Abstract and the method sections.`
- Several places for one point: separate them with semicolons in one anchor.

Minor-item formats:
- Wrong statement: `Section "…", paragraph 2. "Structural pleiotropy" is not a standard term. Please define it or use a standard term.`
- Missing citation for one claim: `Section "…", paragraph 4. The statement that … needs a citation.`
- Table contradicts text: quote both, then give the accurate wording, and check that your wording is itself correct.
- Figure: `Figure 2, Panel E. The confounder is linked to the exposure and outcome by dashed lines, which the legend defines as non-causal associations. Arrows, as in Panel A, would be consistent.`
- Legend leftovers: `Figure 6 legend. "NASH, non-alcoholic steatohepatitis" is defined but is unrelated to this study, and is likely a copy-paste error.`
- Swapped references: `Lines 140 and 162. The in-text references to Tables S2 and S3 are swapped.`
- Typo: `Line 18. "principle component" should be "principal component".` Quote both the original and the correction.
- Citation mismatches: one item, 2–3 examples, then "Please check all citations … against the cited studies."
- Formatting: one short item for visible problems, e.g. `Tables 2 and 3. Capitalization is inconsistent (e.g. "Perturbation Screens" and "Knowledge graph reasoning").`

## 5. Phrase bank

### Opening: content
- "This manuscript presents / introduces / investigates / reviews …"
- "The authors first … They then … They conclude that …"
- "Using …, the authors show that …"
- "They call for …"

### Opening: overall quality
- "The topic is timely, and the manuscript is clearly written and well organized."
- "The Background explains well why …"
- "The manuscript brings the main methods together in one accessible overview."
- "The figures and tables are useful for readers new to the field."
- "The benchmark on … is useful for readers who choose between tools."
- "The question is relevant, and the design combines … and …"

### Opening: tone sentence (see report-templates §6)
- "Overall, this is a well-prepared manuscript, and my comments should be easy to address. My comments are below."
- "However, several parts of the manuscript need further improvement, mainly …, … and …. My comments are below."
- "However, the manuscript has several substantial problems, mainly … and …, that need to be addressed. My comments are below."
- "However, the manuscript has fundamental problems in … and …, which in my view a revision cannot resolve. My comments are below."

### Major-item starters
- "It is not clear whether …"
- "… requires clarification. … is usually used to …, rather than …"
- "The cited study does not support this statement. Ref N reports …"
- "These conclusions rest on few examples, mainly …"
- "The review does not discuss …, although …"
- "The study links … through enrichment analysis but does not include direct assays of …"
- "The distinction between … and … is not made clear."
- "The statement that … is incorrect. …"
- "… so technical variation, rather than biology, may drive …"
- "For both approaches, the assumptions and the type of causal claim should be stated more clearly."

### Requests and fallbacks
- "Please state …" / "Please report … separately."
- "I suggest ending each method section with a short summary of what the method has shown and what is still unclear."
- "A table or box of examples in which methods gave different results would also help."
- "It would be helpful to include a brief comparison of …"
- "Even qPCR confirmation in one additional dataset would strengthen the claim."
- "At minimum, please acknowledge this limitation in the text and in the Figure X legend."
- "If these experiments are not feasible, please present … as a hypothesis."

### Questions that open a line of thought
- "Were any criteria used to assess the quality or comparability of … beyond their availability?"
- "Is the limitation due to the methods, to insufficient or low-quality data, or to other factors?"
- "How many of these genes are proven beyond reasonable doubt to be causal? If many carry uncertainty, would it not be prudent to show that uncertainty in the figures or text?"

### Minor-item starters
- "… needs a citation." / "… is not a standard term. Please define it or use …" / "'…' should read '…'."
- "… does not agree with the text, which states that …"
- "Several citations do not support the statements they are attached to. For example, …"

### Revision rounds (R1/R2)
- "The authors have revised the manuscript carefully, and the new version is clearer, particularly …"
- "The authors have restructured several sections, expanded …, and corrected several of the technical errors noted in the first round. However, some of the main concerns remain, and a few new problems have appeared."
- "I agree that a detailed discussion is beyond the scope of this review, but a high-level one or two paragraphs on … would still help."
- "I defer to the editor on how much of this is relevant to the readership."
- "The additions to the '…' section are a welcome improvement."

## 6. Wording pitfalls

Taken from past drafts; check for these in every report.

| Avoid | Write |
|---|---|
| "three softwares" (and never "correct" an author's "three software" to it) | "three software tools / packages" |
| "undoubtably" | "undoubtedly" |
| "far to generous" | "far too generous" |
| "would strength the review" | "would strengthen the review" |
| "the author need completely rephase it" | "the authors need to rephrase it" |
| "Whether the authors used X?" | "Did the authors use X?" |
| "What is the functional components were used" | "Which functional components were used" |
| "historically context" / "the start of play" | "historical context" / "the state of play" |
| "the directionality of causal" | "the direction of causality" |
| "Correct the typo 'X with a low Y' (missing 'a')" | "'X with low Y' should read 'X with a low Y'" |
| "shouldn't", "doesn't" in the report | "should not", "does not" |
| Mixing "the author" and "the authors" | Use one, usually "the authors" |
| "Despite its comprehensive scope, the review could be strengthened by delving deeper into …" | "The review covers many methods, but it would be stronger if it discussed … in more detail." |

Also watch for these:
- **One point, two comments.** Merge them, e.g. two comments on overlapping lines that both criticize the same undefined term.
- **Garbled merges.** When combining a co-reviewer's fragment with your sentence, re-read the result aloud.
- **Ambiguous cross-references.** Both lists start at 1, so "comment 2" is ambiguous. Write "Major comment 2".
- **Praise that later comments contradict.** An opening that says "the assumptions are explained carefully", followed by three Major items asking for the assumptions, undermines both.
- **A tone sentence that contradicts the form's decision.** If the tone sentence says the problems are fundamental, don't pick minor revision in the form.
- **Absolute or unverified technical claims.** Add the conditions, or check first (guardrail 4 in SKILL.md).
- **"Not cited" claims.** Search the manuscript's reference list first; a relevant study may be cited under a different topic.
- **Suggested wording that keeps the error.** Replacing "estimates the unconfounded effect" with "estimates the causal effect" doesn't fix an overstatement; the fix needs the condition ("under the instrumental variable assumptions").
- **Formatting in the report.** No bold, italics, headings inside the lists, or bullets inside items.

---

## 7. Exemplars

The exemplars show the report exactly as it should look. The only headings are the plain lines "Major revisions" and "Minor revisions".

### A. Positive tool paper (minor revision)

> This manuscript introduces LDBlitz, a Rust tool for computing linkage disequilibrium (LD) matrices from biobank-scale genotype data for summary-statistics fine-mapping. The key idea is to store genotypes as packed bits and to compute LD block by block, so the full genotype matrix never has to be held in memory. It reads PLINK and BGEN files and runs on Linux and macOS. The authors compare LDBlitz with PLINK 1.07 and a reference R implementation on simulated data with 5,000 to 100,000 individuals, and on about 50,000 individuals from a population cohort. LDBlitz is 8 to 40 times faster and uses less than a tenth of the memory, and its LD estimates agree with those of the R implementation to within 10^-6. Fine-mapping with SuSiE-RSS gives the same credible sets with either LD matrix. The manuscript is clearly written, the software is well documented, and the code is openly available with test data. The benchmark uses both simulated and real data, and the figures are easy to read. The tool meets a practical need, because computing LD matrices is often the slowest step in large fine-mapping studies. The main gaps are the choice of comparator and the lack of a discussion of limitations. Overall, this is a well-prepared manuscript, and my comments should be easy to address. My comments are below.
>
> Major revisions
>
> 1. Benchmark section; Figure 3. The benchmark uses PLINK 1.07, which was superseded many years ago. A comparison with the current PLINK release (1.9 or 2.0) would be more informative. Please report runtime, peak memory and the agreement of the LD estimates on the same data, hardware and number of threads.
>
> 2. Conclusions. The Conclusions describe the strengths of LDBlitz but not its limits. Please add a short paragraph on scalability limits, the assumptions of the algorithm (e.g. hard-called genotypes), and support for other data types, such as imputed dosages, multi-allelic variants and related individuals.
>
> Minor revisions
>
> 1. Figure S2. The colors used for PLINK 1.07 and the R implementation are too similar to distinguish.
>
> 2. Line 18. "principle component" should be "principal component". Line 57: "effects the runtime" should be "affects the runtime".
>
> 3. Lines 140 and 162. The in-text references to Tables S2 and S3 are swapped.

### B. Wet-lab mechanism paper (major revision)

> This manuscript studies transcriptional changes after acute kidney injury (AKI). The authors re-analyze a public microarray dataset (GSE000000; 5 injured and 6 control kidneys) and identify the stress-inducible transcription factor TFX as a hub gene. Enrichment analysis links the differentially expressed genes to ferroptosis and oxidative stress. Bioinformatic prediction nominates GENEY as a target of TFX. In HK-2 cells and in a mouse ischemia–reperfusion model, TFX and GENEY both increase after hypoxia/reoxygenation or injury. A dual-luciferase assay suggests that TFX activates GENEY transcription. Knockdown of TFX lowers GENEY, reduces the expression of ferroptosis-related genes and improves cell viability. The authors conclude that a TFX–GENEY axis promotes ferroptosis and worsens kidney injury, and they propose the axis as a treatment target. The question is relevant, and the design combines public data, cell experiments and an animal model. The Introduction explains clearly why tubular cell death matters in AKI. The public data are identified by accession number, the cell experiments are clearly presented, and the figures are easy to follow. However, the main mechanistic claims need stronger evidence, mainly on ferroptosis itself, on the direct binding of TFX to the GENEY promoter, and on kidney function in vivo. My comments are below.
>
> Major revisions
>
> 1. Lines 140 and 268. Line 140 reports 85 differentially expressed genes, whereas Line 268 gives a total of 1,150. Because the hub-gene and enrichment analyses depend on this list, it is unclear which set was analyzed. Please reconcile the two numbers and justify the log2 fold-change cutoff.
>
> 2. Results, section 3.4; Figure 5. The ferroptosis claim rests on enrichment analysis. Direct assays in HK-2 cells or injured kidneys, such as lipid peroxidation with C11-BODIPY, GPX4 levels and rescue with ferrostatin-1, would show whether the axis acts through ferroptosis. If these are not feasible, please present ferroptosis as a hypothesis.
>
> 3. Results, section 3.3; Figure 4C. The binding of TFX to the GENEY promoter is inferred from motif prediction and a luciferase assay without mutation of the site. ChIP-qPCR or EMSA, together with a luciferase construct carrying the mutated site, would establish direct regulation.
>
> 4. Figure 6. Renal TFX and GENEY levels are shown, but no functional outcome, such as serum creatinine, blood urea nitrogen, histological injury score or survival, links TFX to kidney function.
>
> 5. Discussion, paragraphs 4 and 5. Ischemia–reperfusion in young, healthy mice lacks the comorbidities common in patients, such as diabetes and chronic kidney disease. Hypoxia/reoxygenation alone also does not reproduce the inflammatory signals that tubular cells face in vivo. Please discuss how these choices limit translation.
>
> 6. Discussion, last paragraph. The proposal to target the axis does not address delivery to tubular cells, off-target effects or safety. A few sentences on these points would make the proposal more realistic.
>
> Minor revisions
>
> 1. Introduction, Line 32. The number of deaths attributed to AKI each year seems implausibly high and may confuse incidence with mortality. Please check the source.
>
> 2. Figure 2. The significance markers are not explained in the legend.
>
> 3. Figure 6 legend. "NASH, non-alcoholic steatohepatitis" is defined but is unrelated to this study, and is likely a copy-paste error.
>
> 4. Lines 118 and 150. Methods states P < 0.05, whereas Results uses adjusted P < 0.05. Please state which threshold was used.

### C. Weak review article (reject)

> This manuscript reviews applications of deep learning to single-cell multi-omics data in colorectal cancer. It describes the main data types, such as single-cell RNA-seq, single-cell ATAC-seq and spatial transcriptomics, common preprocessing steps, and several model families, including autoencoders, graph neural networks and transformers. It then summarizes about 40 studies on diagnosis, prognosis and drug response, with a table of the data and models each study used, and ends with sections on interpretability and ethics. Each study is described in one or two paragraphs. The authors conclude that deep learning can integrate single-cell omics layers and improve clinical prediction in colorectal cancer. The topic is timely and clinically relevant, and the table of studies may be a useful starting point for readers new to the field. The figures give a clear overview of the model families. However, the text is disjointed and repeats itself, and several basic machine learning concepts are described incorrectly. Studies are summarized one by one without comparison, so the review does not show what deep learning has added to multi-omics integration or where it has failed. The sections on interpretability and ethics are too general to guide readers. Overall, the manuscript has fundamental problems in organization, technical accuracy and depth, which in my view a revision cannot resolve. My comments are below.
>
> Major revisions
>
> 1. Lines 70–125. Studies are presented one after another, with abrupt changes of topic and no comparison. Please group them by method (e.g. autoencoders, graph neural networks) or by clinical aim (e.g. diagnosis, prognosis, drug response). For each group, state what the studies show about multi-omics integration and what remains open.
>
> 2. Section 2. Deep learning is presented as a paradigm parallel to supervised and unsupervised learning. It is a family of models that can be trained in supervised, unsupervised or semi-supervised settings. Please reorganize Section 2 accordingly.
>
> 3. Line 460. t-SNE is described as preserving global distances between clusters. t-SNE mainly preserves local neighborhoods, and distances between clusters in a t-SNE plot are not reliably interpretable. Please correct this, and contrast linear (PCA) with nonlinear (t-SNE, UMAP) methods.
>
> 4. Sections 2 and 5. The same techniques, such as batch correction, are explained more than once. Please shorten the text, and use the space to compare how well specific model types suit specific data types and how they have been validated clinically.
>
> 5. Section 6.2. The section does not explain why interpretability matters in the clinic. Please discuss specific techniques, such as SHAP for tree-based models and attribution maps for neural networks, and their role in clinical use and regulation.
>
> 6. Section 6.3. The ethics section gives no concrete guidance. Please give examples, such as consent for reuse of single-cell data, checks for bias across patient groups, and privacy-preserving training such as federated learning.
>
> Minor revisions
>
> 1. Line 250. "Chance of relapse" should be "risk of recurrence", the standard clinical term.
>
> 2. Line 312. "Batch effects are removed by log-normalization" is incorrect. Normalization adjusts for sequencing depth; batch effects need dedicated methods such as Harmony or ComBat.

### D. Joint report organized by section (excerpt)

A joint report follows the co-reviewer's layout. This one, from a senior co-reviewer, has a general-assessment paragraph, comments grouped under plain section lines, and continuous numbering.

> This review describes Mendelian randomization (MR) methods for complex traits. It covers instrument selection, pleiotropy-robust estimators, multivariable and mediation designs, and recent extensions to molecular exposures. The authors address key challenges, including weak-instrument bias and horizontal pleiotropy. The review covers many methods, but it would be stronger if it discussed practical challenges (e.g. sample overlap, the choice of sensitivity analyses) in more detail, clarified some methodological distinctions, and said more about applications and future directions.
>
> Generally, the review is a good overview with helpful historical context. However, within each topic there is much nuance, and the key questions each approach addresses, together with its open gaps, would add much value. Some figures need heavy revision. Suggestions for each section are provided below.
>
> Introduction
>
> 1. Lines 30–60. The introduction goes into methodological detail early, which may overwhelm readers. To engage a broader audience, we suggest first outlining the broad challenges MR methods must address: instrument strength, pleiotropy, direction of effect, sample overlap and population structure. Specific methods can then follow in later sections.
>
> Pleiotropy-robust methods
>
> 2. The review covers the weighted median and MR-Egger but omits MR-PRESSO and contamination-mixture approaches. Each is widely used and has its own strengths and weaknesses. For example, MR-Egger is robust to directional pleiotropy under the InSIDE assumption but has low power. A short table of assumptions, one row per method, would help readers choose.
>
> 3. The reviewers could go either way on the section on colocalization. It answers a different question from MR, but many readers may not know how the two complement each other in drug-target MR. The authors might keep it with a sentence justifying its inclusion, or remove it if space is limited.
>
> Comments on Figures
>
> 4. Figure 3 relies heavily on buzzwords. We suggest redesigning it around the key objectives, e.g. "validated drug target". Working backwards, add a "you are here" marker for the current state of the art and show what further evidence is needed to reach the next level of inference.
>
> Minor comments
>
> 5. Line 118. For completeness, define the F-statistic threshold used.
>
> 6. Line 247. "MR-PRESO" should be "MR-PRESSO".
