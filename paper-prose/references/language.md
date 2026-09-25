# Language conventions

Correctness and convention at the sentence and word level: tense and voice by section, sentence clarity, word usage, grammar traps common in text written in or drafted from Chinese, and the mechanics of numbers, statistics, abbreviations, and nomenclature. AI-flavoured wording is covered in `ai-tells.md`, and claim strength in the verb ladder in SKILL.md.

Journal house style overrides these defaults. Copy editors will enforce house style anyway, but reviewers notice inconsistency first, and a manuscript that mixes spellings, tenses, and number formats reads as assembled rather than written.

## Contents

1. Tense, voice, and claim strength by section
2. Sentence clarity
3. Word usage
4. Grammar traps for Chinese-L1 writers
5. Numbers, units, and statistics
6. Abbreviations
7. Nomenclature and names
8. Spelling, hyphens, and punctuation
9. Concision

## 1. Tense, voice, and claim strength by section

The rule underneath every row: present tense for what is generally true, for what the paper or a figure shows, and for what a model or tool does; past tense for what was done and observed in a particular study, this one included. Tense tells the reader whether a statement is accepted knowledge or one study's result, so every shift should be deliberate.

| Section | Tense | Voice and person | Claim strength |
|---|---|---|---|
| Title | Present for a stated finding ("[Method] narrows..."); otherwise a noun phrase | none | Only what the main evidence directly supports |
| Abstract | Present for context and conclusion; past for what was done and found; "Here we present/show" | "we" | The strongest supported claim, with its boundary |
| Introduction | Present for established knowledge; present perfect for a body of work ("Several methods have been developed [cite]"); past for one study's specific result ("[A] fine-mapped [n] loci [cite]"); present for this paper ("Here we develop...") | "we" for this study; cited methods or authors as subjects for prior work | Every claim about the field cited |
| Methods | Past for procedures; present for definitions, equations, model assumptions, and what software does ("Let β denote...", "SuSiE assumes...") | Passive for routine steps; "we" for choices and their reasons | No interpretation |
| Results | Past for what was done and observed; present for what a figure or table shows and for general statements that follow from a result | Data and methods as subjects; "we" sparingly | Describe; at most one hedged sentence of interpretation per paragraph |
| Discussion | Present for interpretation, implications, and limitations; past to recall this study's specific results; present perfect for prior literature ("[A] and [B] have reported...") | "we", "our results" | The verb ladder matters most here; speculation is allowed only if labelled as such |
| Figure legends | Present for what is shown; past for how the data were generated | Passive or noun phrases | Nothing beyond the title sentence |
| Response to reviewers | Present perfect or past for revisions ("We have added..." or "We added..."), consistently | "we" | No stronger than the revised manuscript |

**Examples.**

- Introduction. Past tense turns accepted knowledge into one study's opinion.
  ✗ "Previous studies showed that most GWAS signals were located in non-coding regions."
  ✓ "Most GWAS signals lie in non-coding regions [cite]."
- Results. Observation in past tense, the comparison made explicit.
  ✗ "As shown in Figure 2, the credible sets of FastMap are smaller than SuSiE."
  ✓ "FastMap's credible sets were smaller than SuSiE's (median [a] versus [b] variants; Fig. 2a)."
- Methods. Procedures in one tense; no future tense for work already done.
  ✗ "We will first remove variants with MAF < [x], and then we fit a linear mixed model."
  ✓ "We removed variants with MAF < [x] and fitted a linear mixed model with [covariates] (REGENIE v[version])."
- Discussion. Interpretation in present tense, strength matched to evidence.
  ✗ "Our results proved that *GENE* regulated insulin secretion."
  ✓ "Colocalization with islet eQTLs suggests that the association acts through *GENE* expression in islets, which remains to be tested experimentally."

**Voice.**

- Active "we" is standard in these journals. It makes the agent clear and avoids the passive chains common in text translated from Chinese ("An analysis was performed, and it was found that...").
- A study does not perform actions: write "we performed", not "this study performed". "This study shows" is fine for the paper's argument.
- "I" only in single-author papers. Never "the authors" for yourselves in the main text.
- In Results, let the data and methods be subjects. A paragraph where every sentence starts with "We" reads like a lab notebook.

## 2. Sentence clarity

- **Subject and verb early and close together.**
  ✗ "The proportion of variants with posterior inclusion probability above 0.9 in loci containing more than one independent signal after conditional analysis was [x]%."
  ✓ "After conditional analysis, [x]% of variants in multi-signal loci had a posterior inclusion probability (PIP) above 0.9."
- **Old information before new.** Begin with what links to the previous sentence; end with the new point, where the stress falls.
- **One main idea per sentence.** A second idea joins only if it is logically subordinate (because, although, which).
- **Parallel structure** in lists and comparisons.
  ✗ "The method is fast, requires little memory, and with high accuracy."
  ✓ "The method is fast, needs little memory, and was accurate in all simulation settings."
- **Noun stacks.** Three nouns in a row is the practical limit.
  ✗ "multi-ancestry GWAS summary statistics fine-mapping method performance evaluation"
  ✓ "an evaluation of fine-mapping methods that use multi-ancestry GWAS summary statistics"
- **Dangling modifiers.** An opening phrase must describe the subject that follows it.
  ✗ "Using PLINK, variants with MAF < [x] were removed." ✓ "Using PLINK, we removed variants with MAF < [x]."
  ✗ "Compared with SuSiE, the credible sets were smaller." ✓ "Credible sets from FastMap were smaller than those from SuSiE."
- **Like with like in comparisons.**
  ✗ "The accuracy of FastMap was higher than SuSiE." ✓ "The accuracy of FastMap was higher than that of SuSiE." or "FastMap was more accurate than SuSiE."
- **"This" and "which" with a clear referent.** Follow "This" or "These" with a noun ("This enrichment suggests..."). When "which" could refer to either a noun or a whole clause, rewrite: ✗ "We removed related samples from the cohort, which reduced power." ✓ "Removing related samples reduced power."
- **"Respectively"** only when two short parallel lists line up exactly: "Heritability was [a] and [b] for height and BMI, respectively." With more than three items, write the pairs out.
- **Positive forms.** "few" over "not many", "lacked" over "did not have"; no double negatives ("not uncommon").

## 3. Word usage

| Prefer | Over | Note |
|---|---|---|
| compared with | compared to | "Compared to" likens one thing to another; use "compared with" for measured differences |
| whereas, although | while | Keep "while" for time |
| because | since, as, due to | "Since" can mean time; "due to" should modify a noun ("the loss was due to...") rather than open a sentence |
| different from | different than, different to | |
| fewer (countable), less (mass) | "less variants" | |
| affect (verb), effect (noun) | impact (verb) | "Impact" as a noun is fine in moderation |
| comprises, consists of, is composed of | is comprised of | |
| associated with | linked to, related to | "Correlated" only if a correlation was computed |
| higher, lower, larger, smaller (between groups) | increased, decreased | "Increased" implies change over time or after an intervention |
| replicated (same association, independent data); validated (a different kind of evidence) | "validated" for both | |
| support, confirm | prove | |
| such as X and Y | such as X, Y, etc. | "Such as" already says the list is incomplete |
| principal component | principle component | |
| the data are | the data is | Plural in most journals; "the dataset is" |
| sex (biological variable) | gender | Unless gender was what was recorded |
| genetic ancestry, genetic ancestry group | race or ethnicity as genetic labels; "Caucasian" | Follow current guidance on population descriptors, such as the 2023 NASEM report |
| participants, individuals | subjects (for people) | |
| can (ability), may (possibility) | "can" for possibility | "Variants can affect expression" states an ability; "these variants may affect expression" is a hypothesis |
| trend (a real change across ordered groups) | "a trend towards significance" | A P value above threshold is not a trend |
| sensitivity, specificity, precision, recall, accuracy, power | casual use | Each has a technical definition; use it only in that sense and define the one you report |

## 4. Grammar traps for Chinese-L1 writers

These are frequent in text written by Chinese-speaking authors and in machine translation from Chinese. They are not AI tells, but reviewers notice them, and fixing them is part of reading as carefully written. See also `ai-tells.md` section 8 for topic-comment structure and comma chains.

**Articles.**

- Singular countable nouns need an article: "we performed a GWAS", "a linear mixed model", "an eQTL analysis".
- Use "the" for something already identified or unique in context; use no article for general plurals and mass nouns. ✗ "The enhancers are enriched for GWAS signals" (meaning enhancers in general) ✓ "Enhancers are enriched for GWAS signals".
- Method and software names take no article ("SuSiE fits..."), but "the SuSiE model" does.
- Article choice follows sound, not spelling: "an MR analysis", "an eQTL", "a GWAS". "A SNP" or "an SNP" depends on whether readers say "snip" or the letters; choose one.

**Countability and agreement.**

- No plural for evidence, information, software, research, knowledge, feedback, or equipment. ✗ "evidences", "softwares", "researches" ✓ "lines of evidence", "software packages", "studies".
- "Data" is plural in most journals: "these data are".
- "A number of" takes a plural verb; "the number of" takes a singular verb.
- With long subjects, the verb agrees with the head noun: "The proportion of samples with missing phenotypes was..."

**Paired connectors.** English uses one connector where Chinese uses two.

- ✗ "Although the sample was small, but the signal replicated." ✓ "Although the sample was small, the signal replicated."
- ✗ "Because LD differs across ancestries, so joint analysis helps." ✓ "Because LD differs across ancestries, joint analysis helps."
- ✗ "despite of" ✓ "despite" or "in spite of". ✗ "The reason is because" ✓ "The reason is that", or just "because".

**Set phrases carried over from Chinese.**

| Chinese | Literal version | Better |
|---|---|---|
| 随着...的发展 | With the development of... | Open with the problem (see `ai-tells.md`) |
| 众所周知 | As we all know; It is well known that | Cut, and cite the fact |
| 其中 | Among them, ... | "Of these, [n] were..." or restructure |
| 尤其 | Especially, ... (as an opener) | "In particular," or put "especially" mid-sentence |
| 此外、另外 | Besides, / What's more, | Usually nothing; "In addition," at most |
| 同时 | Meanwhile, / At the same time, | Only for simultaneity; otherwise "also" mid-sentence |
| 另一方面 | On the other hand, | Only after "on the one hand", for two sides of one question |
| 总之 | In a word, / In short, | Cut, or "Overall," once |
| 最后 | At last, | "Finally," ("at last" means after a long wait) |
| 首先、其次 | Firstly, Secondly, | "First," or turn the list into prose |
| 等等 | etc.; and so on | "such as" before the list |
| 本文 | In this paper, | "Here" or "In this study" |
| 目前 | Nowadays, / At present, | "Currently", or cut |
| 进行了分析 | performed an analysis on | "analysed" |
| 对...有影响 | has an influence to | "affects", "has an effect on" |
| 证明 | prove | "show", "demonstrate" |
| 揭示 | reveal | "show", "identify" ("reveal" is overused) |
| 一系列 | a series of | "several", or the number |

**Fixed prepositions.** associated with; consistent with; compared with; in agreement with; differ from; depend on; contribute to; result in (cause) and result from (effect); focus on; effect on; influence on; sensitive to; research on or into; increase by (an amount) and increase to (a final value); enriched in or enriched for (choose one and keep it). Verbs that take no preposition: discuss X (not "discuss about"), emphasize X (not "emphasize on"), approach X, investigate X.

**Verbs.**

- "Can" for results turns a finding into a capability. ✗ "Our method can significantly improve accuracy." ✓ "Our method improved accuracy from [a] to [b]."
- Nominalization with "perform", "conduct", or "carry out". ✗ "We performed the normalization of the data." ✓ "We normalized the data."
- "There be" openings. ✗ "There are many studies that have shown..." ✓ "Many studies have shown... [cite]", or better, state what they showed.
- "Which" as a general-purpose linker between full clauses. Split the sentence or use a precise connector.

## 5. Numbers, units, and statistics

**Numbers.**

- Words for one to nine and numerals for 10 and above, but always numerals with units, in statistics, and in a series that includes larger numbers ("3, 8, and 15 loci").
- Do not start a sentence with a numeral. ✗ "12 loci replicated." ✓ "Twelve loci replicated." or "In total, 12 loci replicated."
- Ranges: "10–20 kb" (en dash, unit once) or "from 10 to 20 kb"; never "from 10–20" or "between 10–20".
- Leading zero on decimals ("0.05", not ".05"), unless the journal says otherwise for P values.
- Two or three significant figures for most estimates; more implies precision the data do not have ("OR = 1.2345").
- Give counts with percentages: "[a] of [b] loci ([x]%)". Use "percentage points" for differences between percentages (40% to 50% is 10 percentage points, a 25% increase).
- "Twofold" or "2-fold" means two times. Avoid "3-fold lower" and "50% fold"; write "one third of" or give both values.
- Thousands separators as the journal uses them (usually commas); consistent throughout, tables included.

**Units.** A space between number and unit (10 kb, 1 Mb, 3 GB, 24 h, 5 mg); no space before "%"; no plural on unit symbols ("kbs"). For runtime and memory, give the hardware and what was measured ("[x] CPU hours on [processor], [y] GB peak memory").

**Statistics.**

- P values: capital or lower-case P, italic or roman, as the journal specifies, and the same everywhere. Give exact values ("P = 0.03", "P = 3.2 × 10⁻⁸"); use "P < 0.001" only below the journal's display limit. Never "P = 0" or "P = 0.000", and never E-notation ("3.2E-08") in prose. In LaTeX: `$P = 3.2 \times 10^{-8}$`.
- Name the test, its sidedness, and the multiple-testing correction at first use.
- Effect sizes with uncertainty: "OR = 1.21 (95% CI 1.12–1.31)". With negative bounds use "to": "β = −0.12 (95% CI −0.20 to −0.04)". Use a true minus sign (−) in typeset text, not a hyphen.
- Say what n counts (individuals, cells, loci, replicates) and what error bars show (s.d., s.e.m., 95% CI).
- For GWAS, "genome-wide significant (P < 5 × 10⁻⁸)", not plain "significant".
- Keep symbols distinct and define each once: LD r² versus the coefficient of determination R²; h² versus SNP heritability h²_SNP; β for effect size, not also for a prior parameter.

## 6. Abbreviations

- Define at first use in the abstract and again at first use in the main text; some journals also want definitions in each figure legend. After defining, use the abbreviation every time instead of alternating with the full form.
- Do not abbreviate a term used fewer than about three times, and avoid abbreviations in the title except universal ones (DNA, RNA, GWAS).
- Do not coin abbreviations for your own concepts unless they recur heavily; each one is a load on the reader. AI drafts coin them freely ("multi-ancestry fine-mapping (MAFM)").
- Plurals take "s" with no apostrophe (SNPs, eQTLs, PCs); "SNP's" is possessive. For GWAS, "GWAS" and "GWASs" are both used as the plural; choose one.
- Avoid starting a sentence with a lower-case abbreviation or tool name when an easy rephrase exists.
- Which abbreviations count as standard differs by journal; when unsure, define.

## 7. Nomenclature and names

- **Genes and proteins.** Human gene symbols in italic capitals (*BRCA1*), using the current HGNC symbol; proteins in roman (BRCA1); mouse genes in italic with an initial capital (*Brca1*). If readers know a gene by an older name, give it in parentheses at first use.
- **Variants.** rsIDs in roman with no space (rs7903146). HGVS for sequence changes (c.1234A>G, p.Arg412Gly). State the genome build once (GRCh37 or GRCh38) and use it throughout. Say which allele is the effect allele.
- **Loci.** Naming a locus after a gene ("the *TCF7L2* locus") does not make that gene causal; say how the gene was chosen (nearest gene, eQTL, fine-mapped coding variant).
- **Species.** Italic binomials (*Homo sapiens*, *Mus musculus*); abbreviate the genus after first use (*M. musculus*).
- **Software and resources.** Exact capitalization (PLINK, REGENIE, SuSiE, LDSC, MAGMA, FUMA, GTEx, gnomAD, UK Biobank, FinnGen), version at first mention in Methods, and a citation.
- **Traits and cell types.** One name per trait, matching the phenotype definition, with its abbreviation defined (T2D, LDL-C). For cell types, follow the ontology or atlas used, consistently.

## 8. Spelling, hyphens, and punctuation

- **Spelling.** US or UK, consistently. The -ize/-ise choice is separate: Oxford spelling uses -ize with other British forms, so keep each choice consistent on its own. Pairs that drift in AI-assisted text: analyze/analyse, modeling/modelling, labeled/labelled, signaling/signalling, color/colour, behavior/behaviour, tumor/tumour, center/centre, hematopoietic/haematopoietic, fetal/foetal, aging/ageing, artifact/artefact. The script reports mixing.
- **Hyphens.** Hyphenate a compound modifier before a noun ("genome-wide significance", "cell-type-specific expression", "two-sided test"); usually not after the noun ("expression was cell type specific"), although "genome-wide" is commonly kept in both positions. No hyphen after an -ly adverb ("highly expressed genes"). For terms written several ways in the literature (fine-mapping or fine mapping, multi-ancestry or multiancestry), choose one.
- **Dashes.** En dash for ranges and relationships (10–20; Hardy–Weinberg; gene–environment); hyphen for compounds; no em dashes (see `ai-tells.md`).
- **Commas and Latin.** Use the serial comma or not, consistently. "e.g.," and "i.e.," with a following comma in US style. "et al." with a full stop, usually not italic.
- **Colons and semicolons.** A colon introduces what the clause before it promises; a semicolon joins two full clauses. AI-heavy text overuses "X: Y" constructions.
- **Cross-references.** Figure and table citations in the journal's form ("Fig. 2a" or "Figure 2A"; "Supplementary Table 3"), identical everywhere.
- **Headings** in sentence case unless the journal says otherwise.
- **Quotation marks.** Rarely needed. Do not use scare quotes around technical terms; define the term instead.

## 9. Concision

Rows here are general wordiness; AI-flavoured phrases such as "in order to" and "due to the fact that" are in `ai-tells.md`.

| Wordy | Shorter |
|---|---|
| a large number of; the majority of | many; most |
| in the case of | in, for |
| is able to; has the ability to | can |
| with respect to; with regard to; in terms of | for, in, about, or restructure |
| a total of [n] | [n] (keep "a total of" only at the start of a sentence) |
| it was found that; it was observed that | cut |
| it has been reported that X [cite] | X [cite] |
| was observed to be; was shown to be | was |
| performed an analysis of | analysed |
| the results showed that | cut, and state the result |
| both X as well as Y | both X and Y |
| whether or not | whether |
| completely eliminate; future prospects; exactly identical; final outcome | eliminate; prospects; identical; outcome |
