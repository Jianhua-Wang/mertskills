# Section guides

How each part of a paper should work, what reviewers look for, and where AI drafts typically go wrong. Read the part for the section you are drafting or revising.

Two paper types recur, and the guides separate them where they differ:

- **Methods paper:** a new statistical method, tool, pipeline, database, or web server (fine-mapping, PRS, colocalization, a QC pipeline).
- **Analysis paper:** new biological findings from applying methods to data (a GWAS, a multi-omics integration, a single-cell atlas).

Tense, voice, and claim strength for each section, and the conventions for numbers, statistics, and nomenclature, are in `language.md`.

Examples are invented for illustration. Bracketed values, and the specific claims inside the examples, must come from the user's own results. Journal formats change, so confirm word limits, section order, and required statements in the target journal's current author guidelines.

## Contents

1. Title and abstract
2. Introduction
3. Methods
4. Results
5. Discussion
6. Figure legends, availability statements, Key Points
7. Journal notes

## 1. Title and abstract

**Title.** State the finding (analysis paper) or what the method does and for whom (methods paper).

- "[Method] narrows fine-mapping credible sets by modelling LD differences across ancestries" says more than "A novel framework for multi-ancestry fine-mapping".
- A tool name, a colon, and a plain description is standard in Bioinformatics and NAR ("[Tool]: fine-mapping from summary statistics in linear time"). The problem is hype after the colon, not the colon.
- Avoid gerund openers (Unveiling, Deciphering, Unlocking, Harnessing), questions, and "novel".

**Abstract.** For an unstructured abstract, a sentence budget helps:

| Move | Sentences | Content |
|---|---|---|
| Context | 1 | The problem, specific to the field; not "In recent years" |
| Gap | 1 | What is unknown or what current methods cannot do, and why |
| Approach | 1–2 | "Here we..." what was done, on what data, and the key idea |
| Results | 2–4 | The main findings with numbers |
| Implication | 1 | What this enables, with its boundary |

- The results sentences carry the abstract. AI drafts spend most of the words on context and implication and reduce the results to adjectives ("substantially improved accuracy").
- Give the two to four most important numbers, not all of them.
- No citations, no abbreviations used only once, no "In this paper".
- In a structured abstract (Bioinformatics), keep each part to what its heading asks; Motivation holds context and gap, Results holds the numbers.

## 2. Introduction

**Job:** bring a reader from outside the subfield to the exact question this paper answers, and make them agree it is worth answering. After reading it, a reviewer should be able to state the gap in one sentence.

**Typical shape, four to six paragraphs:**

1. **Problem.** What the field is trying to do and why it matters, in concrete terms: a quantity, a decision, a biological question. One paragraph, not a history of genomics.
2. **What is known.** Prior work, grouped by idea or assumption, with citations. Say what each group achieves.
3. **The gap.** What remains unknown, or what current approaches cannot do, and why: the assumption that fails, the data they cannot use, the cost that limits them. Reviewers read this paragraph most closely.
4. **This study.** "Here we..." followed by the approach, its key idea (the design choice that addresses the gap), the data, and two to four main findings. Close with what the findings make possible. Most genomics journals, Nature Communications included, expect the main results summarized here.

**Methods paper versus analysis paper.**

- Methods paper: the gap is a technical limitation with a scientific consequence (the method cannot use some information, so some quantity stays poorly resolved). Explain the key idea in plain words before the method's name appears.
- Analysis paper: the gap is a biological unknown. Data are the means, not the gap: "no one has analysed dataset X" is not a gap unless analysing it answers a question.

**Writing about prior work.**

- Group by approach and name the shared assumption or limitation: "Summary-statistic methods such as [A] and [B] assume a single causal variant per locus [cite], which..." Avoid one sentence per paper ("[A] proposed... [B] developed... [C] introduced...").
- Be fair and specific. The reviewers are often the authors of the cited methods. Say what the methods do well before what they cannot do.
- Every factual claim about the field needs a citation. "Many studies have shown" without one reads as generated.

**Gap statements.**

- ✗ "However, accurate fine-mapping remains a significant challenge." (No reason, no consequence.)
- ✗ "However, no method currently integrates X and Y." (The absence of a method is not a scientific gap.)
- ✓ "Existing methods analyse each ancestry separately [cite], so they cannot use the shorter LD blocks of African-ancestry samples to separate correlated variants; at [x]% of loci, credible sets still contain more than [n] variants [cite]."

**AI failure modes in Introductions.**

- A grand opening sentence about the importance of genomics, big data, or AI.
- Prior methods listed one per sentence, with no synthesis.
- The gap stated as "remains a challenge", "remains elusive", or "is still in its infancy".
- "To address these challenges, we propose X, a novel..." followed by a numbered list of contributions. Contribution lists are a computer-science convention; genomics journals expect prose.
- A final paragraph that repeats the abstract.

**Example (gap paragraph).**

✗ "Despite these advances, several challenges remain. Existing methods often fail to fully leverage the rich information contained in multi-ancestry data, limiting their ability to accurately pinpoint causal variants. Moreover, their computational cost can be prohibitive for large-scale analyses. Therefore, there is a pressing need for novel approaches that can address these limitations."

✓ "Most fine-mapping methods analyse one ancestry at a time [cite]. Because causal variants are largely shared across populations while LD differs [cite], a joint analysis should separate variants that no single population can distinguish. Current joint methods [cite] assume one causal variant per locus, which fails at an estimated [x]% of loci [cite], and their cost grows [rate?] with the number of variants, restricting them to windows of about [n] variants."

The second version names who does what, gives the reason the gap exists, quantifies it (with placeholders), and implies the design of the solution. It has no connector-led sentences and no "pressing need".

## 3. Methods

**Job:** let a competent reader reproduce every number in the paper, and let a reviewer judge whether each choice was sound. Detail beats elegance. This is the one section where plainer and longer is often better.

**Order.** Follow the order of the Results, or the data flow: data, processing, model, analyses, evaluation, software. Use informative subheadings ("Genotype quality control", "Fine-mapping model", "Simulation design") with the same terms the Results use.

**What to report** (a checklist to draw from, not a template to fill):

- **Cohorts and data:** source and accession (dbGaP, EGA, GEO, UK Biobank application number), sample sizes after QC, ancestry definition, phenotype definition (codes, units, transformations), ethics approval and consent.
- **Genotyping, imputation, QC:** array, imputation panel and server, each filter with its threshold (INFO, MAF, call rate, HWE P), reference genome build, and how many samples and variants each step removed.
- **Association models:** software and version, model (for example a linear mixed model), covariates, significance threshold, and how loci were defined (window, LD r², LD reference panel).
- **The new method (methods papers):** define notation once, in a table if there is a lot of it; state the model, priors, and assumptions; derive or cite each key step; give the algorithm, its complexity, and convergence criteria; say what is new relative to the method it extends.
- **Downstream analyses:** fine-mapping (method, number of effects, coverage), colocalization (priors), Mendelian randomization (instrument selection, clumping parameters, instrument strength, sensitivity analyses), enrichment (background set, test, correction).
- **Simulations:** genotype source, heritability, polygenicity, number of causal variants, effect-size distribution, replicates, seeds; which parameters vary and which are fixed; how truth is defined for evaluation.
- **Benchmarking:** competing methods with versions, their parameters (defaults or tuned, and how), identical inputs, metrics defined, hardware and how runtime was measured.
- **Statistics:** each test with its sidedness, multiple-testing correction, what n refers to, what error bars and intervals show.
- **Software:** language, key packages with versions, where the analysis code lives.

**Style.**

- Passive voice is normal for procedures ("Variants with INFO < [x] were removed"). Use "we" for decisions that need a reason ("We used a [x]-kb window because...").
- Past tense for what was done; present tense for properties of a model or tool ("The model assumes...", "REGENIE fits...").
- Justify non-default choices in a clause. The reviewer will ask why this threshold.
- Cite standard methods instead of re-describing them, and state any deviation from their standard use.
- Keep results and interpretation out, except the numbers that describe the data (samples remaining after QC).

**AI failure modes in Methods.**

- Adjectives instead of details: "rigorous quality control", "carefully curated", "state-of-the-art pipeline", "standard parameters".
- Describing what a tool can do instead of what was done: "PLINK allows researchers to perform comprehensive QC..."
- Missing versions, thresholds, or n; "statistical analyses were performed in R" with no test named.
- Invented specifics. A draft model will readily write plausible thresholds such as "MAF < 0.01 and HWE P < 1 × 10^-6". They must come from the user's scripts, notes, or earlier papers; otherwise use placeholders and list them as author items.
- Notation that drifts between sections (β in one place, b in another; N and n for the same quantity).

**Example.**

✗ "Rigorous quality control was meticulously performed using PLINK to ensure the reliability of the data. Low-quality variants and samples were removed according to standard criteria, and population stratification was carefully accounted for."

✓ "We removed variants with call rate < [x], MAF < [x], or HWE P < [x], and samples with call rate < [x], sex mismatch, or excess heterozygosity (PLINK v[version]), leaving [N] samples and [M] variants. Ancestry was assigned by [method], and the first [k] principal components were included as covariates."

## 4. Results

**Job:** present the evidence for the paper's claims in the order that builds the argument, with enough interpretation for the reader to follow and no more.

**Order.**

- Methods paper: overview of the method with a schematic (Fig. 1); calibration in simulations (type I error or FDR first, then power, resolution, or accuracy); robustness when assumptions are violated (misspecified LD, sample overlap, model misspecification); comparison with existing methods on real data; a biological application showing what the method finds that others miss; runtime and scalability.
- Analysis paper: data and study overview; primary discovery; replication or validation; fine-mapping, functional annotation, or mechanism; secondary analyses and heterogeneity.

**Subheadings.** In Nature Communications and similar journals, Results subheadings state the finding ("[Method] reduces credible set size across ancestries" rather than "Fine-mapping results"). Keep them short and make sure the paragraph below delivers what the heading claims.

**Paragraph pattern** (a default, not a template; vary it):

1. The finding, or the question if the finding needs setup, in one sentence.
2. How it was assessed, briefly, pointing to Methods.
3. The evidence: numbers with effect sizes, intervals, tests, and figure references "(Fig. 2b; Supplementary Table 3)".
4. Where useful, one sentence of interpretation, marked as such ("suggesting", "consistent with").

**Reporting numbers.**

- Give absolute values with the comparison: "from [a] to [b] ([x]% fewer)", not only "[x]% fewer".
- Give effect sizes with uncertainty (95% CI or s.e.) and P values; name the test on first use.
- Report where the method did not win or the effect did not replicate. A Results section that shows its limits is more convincing.
- Do not restate every value in a figure. Give the values the argument needs and let the figure carry the rest.
- Round sensibly: two significant figures for most estimates, P values as [x] × 10^-[y].

**AI failure modes in Results.**

- Every paragraph opens "To investigate/evaluate/assess X, we...".
- Every paragraph ends with an inflated verdict ("These results demonstrate the superiority and robustness of our method").
- Adjectives instead of numbers ("substantially improved", "markedly higher").
- "Outperformed in all scenarios" when the figure shows exceptions.
- Long repeats of Methods detail, or interpretation that belongs in the Discussion.

**Example.**

✗ "To evaluate the performance of FastMap, we conducted extensive simulations. The results showed that FastMap significantly outperformed existing methods across all scenarios, demonstrating its superior accuracy and robustness. These findings highlight the potential of FastMap for fine-mapping studies."

✓ "In simulations with [2–5] causal variants per locus (Methods), FastMap's 95% credible sets contained the causal variant at close to the nominal rate ([x]%) and were smaller than those of SuSiE (median [a] versus [b] variants; Fig. 2a). The gain was largest when LD differed most between ancestries (Fig. 2b) and disappeared when all samples came from one ancestry (Supplementary Fig. [n])."

The second version checks calibration before claiming a gain, names the comparator, gives numbers, and says where the gain disappears.

## 5. Discussion

**Job:** say what the results mean, how far they can be trusted, and what they change. It is argument, not a second Results section.

**Typical shape, four to seven paragraphs:**

1. **Main finding and its meaning** in two or three sentences. Do not re-list results with numbers; the reader has just read them.
2. **Interpretation.** Mechanism or explanation, with verbs matched to the evidence. For a methods paper, why the method works (which modelling choice matters) and when it helps most.
3. **Relation to prior work.** Where the findings agree or disagree with earlier studies, and the likely reason for any disagreement (sample, ancestry, method, phenotype definition).
4. **Alternative explanations.** Confounding, LD, pleiotropy, ascertainment, batch effects: name the plausible ones and say what the data show about each.
5. **Limitations.** Each tied to the claim it weakens and, where possible, to what would resolve it.
6. **Implications and next steps.** Specific: which analysis, dataset, or experiment would test or extend the main claim.
7. **Closing.** One or two sentences with a concrete take-home, not "In conclusion, our study provides novel insights into...".

A methods-paper Discussion should also give practical guidance: when to use this method rather than the alternatives, what inputs it needs, where its assumptions break, and what it costs to run.

**Limitations done well.**

✗ "This study has several limitations. First, the sample size was relatively small. Second, our analysis was limited to European populations. Future studies with larger and more diverse cohorts are needed to validate our findings."

✓ "With [N] cases, we had [x]% power to detect variants with odds ratios below [y] at genome-wide significance, so the [n] loci reported are probably the larger-effect subset. Because all cohorts were of European ancestry, we could not test whether the [locus] association is shared across populations; [cohort or resource] would allow this."

Each limitation now says what it does to the conclusions and what would fix it.

**AI failure modes in Discussions.**

- Opening with "In this study, we developed..." and then re-summarizing every result.
- Generic limitations (small sample size, cross-sectional design) with no consequence stated.
- "Future studies are needed" or "future work will explore" as the only next step.
- Hedging everything, or the reverse: causal language for association results.
- A grand closing sentence ("paving the way for precision medicine").
- New results that appear only in the Discussion.

## 6. Figure legends, availability statements, Key Points

- **Figure legends:** a title sentence that states what the figure shows, then each panel, then the statistics (n and what it counts, the test, what error bars or boxes represent). Present tense. Define abbreviations used in the figure. No interpretation beyond the title sentence and no hype.
- **Data availability:** where each dataset is, with accession numbers or the access route for controlled data, and which summary statistics are released and where.
- **Code availability:** repository URL plus an archived, versioned copy with a DOI (for example on Zenodo) that matches the analyses in the paper, and the license.
- **Key Points (Briefings in Bioinformatics):** three to five bullets, each a complete and specific statement of a finding or contribution, not advertising.
- **Supplementary notes:** the same rules as the main text. Derivations still need defined notation and cross-references to the main text.

## 7. Journal notes

Stable conventions only; check limits and required statements in the current guidelines.

- **Nucleic Acids Research:** Materials and Methods usually comes before Results. Database and Web Server issue papers are judged partly on whether the resource is available, documented, and maintained.
- **Bioinformatics:** structured abstract (Motivation; Results; Availability and implementation; Contact; Supplementary information) and numbered sections in Original Papers. Application Notes are very short and centre on what the software does, how to get it, and one demonstration.
- **Briefings in Bioinformatics:** a Key Points box is required. Reviews and problem-solving protocols are common article types; reviews need synthesis and comparison, not a catalogue of tools.
- **Nature Communications:** a short, unreferenced abstract; Introduction, Results, and Discussion, with Methods at the end; Results subheadings usually state findings; data and code availability statements and a reporting summary are required.
