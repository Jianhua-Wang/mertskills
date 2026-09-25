# AI tells in scientific prose: catalogue and fixes

Examples are invented for illustration. Bracketed values in the fixes must come from the author's material; never fill them with plausible numbers.

## Contents

1. Word swaps
2. Inflation and promotion
3. Sentence patterns
4. Paragraph patterns
5. Hedging
6. Rhythm: a worked example
7. Formatting and residue
8. Chinese-to-English transfer
9. False alarms: keep these

## 1. Word swaps

These are defaults, not bans. One "crucial" in a paper is fine; the problem is density. Prefer rebuilding the sentence over swapping a single word.

| AI-flavoured | Plainer choice |
|---|---|
| utilize, employ | use |
| leverage, harness (verbs) | use, build on, exploit (technical sense) |
| facilitate | enable, allow, help |
| elucidate, shed light on | show, explain, identify |
| delve into | examine, study |
| underscore, highlight | show, or cut the sentence |
| showcase | show |
| pave the way for | enable, make possible |
| bolster, foster | strengthen, support, encourage |
| unlock, unveil | reveal, identify, allow |
| crucial, pivotal, vital, paramount | important, key, required, or say why it matters |
| intricate | complex, detailed |
| multifaceted, nuanced | cut, or name the facets |
| landscape, realm | field, area, set, range |
| interplay | interaction |
| tapestry, a testament to | cut |
| seamless(ly), meticulous(ly) | cut; show care through detail |
| robust (non-statistical) | reliable, stable, or give the evidence |
| novel | new, or cut and let the result show it |
| comprehensive | systematic, genome-wide, or the actual scope |
| numerous, various, a wide range of | the count, or "several", "many" |
| a number of | several, some, or the number |
| in order to | to |
| due to the fact that | because |
| prior to, subsequent to | before, after |
| exhibit, possess | show, have |
| enhance | improve, increase |
| commence, endeavour | start, attempt |
| it is worth noting that | cut |
| plays a crucial role in | say which role: "is required for", "regulates", "encodes" |
| serves as, stands as | is |
| linked to (statistical) | associated with |
| Beyond X, (sentence opener) | In addition to X, or restructure |

## 2. Inflation and promotion

- **Significance inflation.** ✗ "This work represents a significant step forward in our understanding of the genetic architecture of type 2 diabetes." ✓ "The [N] new loci roughly double the number of known loci for [trait] in East Asian populations." (State what was found; let the reader judge the step.)
- **Promotional adjectives.** ✗ "a powerful tool", "an innovative approach", "cutting-edge methods". ✓ Name what the method does and how well: "a Bayesian method that fits [K] annotations jointly in [time] per trait".
- **Novelty claims.** ✗ "For the first time, we..." ✓ "To our knowledge, this is the first..." only after checking; otherwise leave `[verify novelty]`.
- **Generic implications.** ✗ "These findings have important implications for precision medicine." ✓ Name the implication and its limit: "Scores built this way could be used for [use] in cohorts with [condition], although we did not test [boundary]."

## 3. Sentence patterns

- **-ing tail** (a participle clause adding commentary after the fact).
  ✗ "We identified 23 loci associated with height, highlighting the polygenic nature of the trait."
  ✓ "We identified 23 loci associated with height." Then either cut the commentary or make it a real claim with evidence.
- **Not only... but also / not X but Y.**
  ✗ "FastMap not only reduces credible set size but also improves computational efficiency."
  ✓ "FastMap reduced the median credible set from [a] to [b] variants and ran [k] times faster than SuSiE."
- **Reflexive triplet.**
  ✗ "Our method is fast, accurate, and scalable."
  ✓ Keep only the properties you measured, each with its number.
- **Copula avoidance.**
  ✗ "PRS-CS serves as a powerful tool for polygenic prediction."
  ✓ "PRS-CS is a Bayesian method that places a continuous shrinkage prior on SNP effects."
- **Vague attribution.**
  ✗ "Studies have shown that enhancers play a crucial role in disease."
  ✓ "Most GWAS signals lie in non-coding regions enriched for enhancer marks [cite]."
- **Stock opener.**
  ✗ "With the rapid development of single-cell RNA sequencing (scRNA-seq), researchers can now..."
  ✓ "Single-cell RNA sequencing (scRNA-seq) measures expression in individual cells, which allows..." or open with the problem.
- **Paraphrastic repeat.**
  ✗ "Variants near the TSS had larger effects. In other words, proximity to the TSS was associated with effect size."
  ✓ Keep one of the two sentences, usually the more specific one.
- **False range.**
  ✗ "applications ranging from drug discovery to personalized medicine" (not a range; just two items).
  ✓ "applications such as drug-target prioritization" or list the real ones.
- **Nominalization plus filler.**
  ✗ "An evaluation of the performance of the model was performed in order to assess its generalizability."
  ✓ "We tested whether the model generalized to [cohort]."

## 4. Paragraph patterns

- **Closing moral.** A last sentence that restates the paragraph's point in grander terms ("Taken together, these findings underscore the importance of..."). Cut it, or replace it with the next concrete implication.
- **Content-free verdict.** "These results are very promising." Say what the results allow or rule out.
- **Connector or "This/These" openings** on most paragraphs ("Furthermore, ...", "This suggests...", "These results..."). Open with the new subject instead.
- **Formula openings** in Results: every paragraph starting "To investigate/assess/evaluate X, we...". Lead with the finding in some paragraphs: "Credible sets were smaller for [class] loci ([numbers]; Fig. 2b)."
- **Symmetric shapes.** Every paragraph with the same length and the same arc (setup, three points, moral). Let paragraph length follow the content.

## 5. Hedging

- **Stacked hedges.** ✗ "These data may potentially suggest a possible role for *TCF7L2*." ✓ "These data suggest a role for *TCF7L2*." or "*TCF7L2* may be involved in..." (one hedge).
- **Hedge asymmetry.** Strong verbs for weak evidence and weak verbs for strong evidence in the same paragraph. Match each verb to its evidence (see the verb ladder in SKILL.md).
- **"Significant" without a test.** ✗ "Expression was significantly higher in cases." ✓ "Expression was higher in cases (Wilcoxon P = [P?])." or "substantially higher" if no test was run.

## 6. Rhythm: a worked example

✗ Four sentences of 12–13 words, all opening with "The":

> The proposed method integrates GWAS summary statistics with eQTL data to prioritize candidate genes. The method was applied to twelve complex traits from the UK Biobank cohort. The results showed that the method identified more genes than existing approaches. The identified genes were enriched in relevant biological pathways for each trait.

✓ Three sentences of different length and shape, carrying the same content plus the specifics the reader needs:

> We combined GWAS summary statistics with eQTL data to prioritize genes for twelve UK Biobank traits. The method nominated [N] genes, [x]% more than S-PrediXcan. Most of the additional genes were in trait-relevant pathways, such as lipid metabolism for LDL cholesterol (FDR = [q?]).

What made the difference: merging two thin sentences, naming the comparator, giving the number, and ending on a concrete example rather than a general claim. No synonym was swapped.

## 7. Formatting and residue

- **Em dashes.** Replace with a comma, colon, parentheses, or a new sentence. In LaTeX, `---` is an em dash. En dashes are correct for number ranges (10–20) and paired names (Hardy–Weinberg, Mann–Whitney).
- **Markdown in prose.** Bold key phrases, bullet lists inside a Results paragraph, `###` headings pasted into a .docx. Journals use plain paragraphs.
- **Title Case headings** where the journal uses sentence case ("Results And Key Findings" should be "Results and key findings" for most journals).
- **Curly quotes in .tex files.** Use ``` ``like this'' ``` in LaTeX.
- **Chat residue.** "Certainly! Here is the revised paragraph:", "I hope this helps", "Let me know if you want...". Also emoji, "Key Takeaways" boxes, and summary tables of "Advantages" that no journal asked for.

## 8. Chinese-to-English transfer

These are common in text drafted from Chinese notes and are separate from AI tells, but they also make text read as machine-produced. Grammar, set phrases, and prepositions are covered more fully in `language.md` section 4.

- **Topic-comment structure.** ✗ "For this dataset, its quality control was performed using PLINK." ✓ "We performed quality control on this dataset with PLINK [version]."
- **Comma chains.** ✗ "The model was trained on UKB, it was tested on FinnGen, the AUC was 0.71." ✓ "We trained the model on UKB and tested it on FinnGen (AUC = 0.71)."
- **Set phrases.** "more and more" (use "increasingly"), "has attracted increasing attention" (cut, or cite who uses it), "and so on" or "etc." at the end of a list (use "such as" before the list).
- **Repeated topic noun** in every sentence ("The method... The method... The method..."). Use "it", merge sentences, or change the subject.
- **Articles.** "We performed GWAS" should be "We performed a GWAS"; "The hypoxia induces" should be "Hypoxia induces".
- **Hedging asymmetry from 可能 / 表明 / 证明.** 证明 is rarely "prove"; usually "show". 可能 is one hedge, not "may possibly".
- **"In this paper"** should usually be "Here we" or "In this study".
- **显著** means statistically significant only when a test was run; otherwise "substantially" or "markedly".

## 9. False alarms: keep these

The script and the lists above flag patterns, not errors. Keep these unless they are overused:

- Connectors that carry logic (however, although, whereas, therefore, in contrast) and functional adverbs (slightly, consistently, approximately, respectively).
- Technical terms: robust regression, robust standard errors, statistical significance, mutational or fitness landscape, "novel loci" (standard GWAS term for loci not previously reported), leverage in regression diagnostics, harmonized summary statistics, comprehensive when coverage really is exhaustive.
- Conventions: "Here we show", "To our knowledge" after checking, "Taken together" once per paper, "consistent with" for partial support.
- The author's correct personal habits, as recorded in `voice-profile.md` if it exists.
