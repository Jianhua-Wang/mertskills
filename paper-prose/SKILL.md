---
name: paper-prose
description: Draft, revise, de-AI, and check English scientific manuscript prose (bioinformatics, statistical genetics, genomics) so it reads like a careful human scientist wrote it, with specific and calibrated claims, varied rhythm, correct and consistent language, and no AI tells. Covers every section from title to figure legends, tense and grammar, numbers, statistics and nomenclature, cover letters, and responses to reviewers. Use this skill whenever the user asks to write, polish, edit, shorten, humanize, proofread, or check any part of a paper; says the text sounds like AI or scored high on an AI detector such as GPTZero or Turnitin; wants Chinese notes turned into paper English; or whenever you are about to write manuscript text for the user as part of a larger task, such as turning analysis output into a Results paragraph. Trigger even on terse requests such as "写论文", "润色", "去AI味", "降AI率", "AI检测率太高", "改稿", "改语法", "改写这段", "polish this", or "make it sound less like AI".
---

# Paper Prose

The user writes English papers in bioinformatics, statistical genetics, and genomics, and text drafted with AI help has been flagged as machine-written. This skill serves two aims that turn out to be the same aim: make the science easy to follow, and remove the habits that mark text as generated. AI-sounding text fails for the reasons weak human text fails. It makes generic claims, inflates significance, leans on stock connectors, repeats one sentence shape, and picks words that sound academic instead of words that are precise.

Detector-only tricks (planted typos, odd synonyms, broken grammar, random short sentences) make the paper worse, and Turnitin and Pangram are now trained to catch humanizer output. Write for the reviewer and the reader. Lower detector scores follow from specific, varied, honest prose; they are a side effect, not the target.

## Guardrails

1. **Never invent science.** No new numbers, citations, sample sizes, P values, datasets, method details, or results. When a sentence needs something the source lacks, leave a visible placeholder: `[N?]`, `[P?]`, `[cite]`, `[verify citation]`, `[detail?]`. A fabricated detail in a manuscript is far worse than an AI-sounding one.
2. **Keep the meaning.** Revision changes how a claim is said, not what is claimed. If a claim looks wrong or too strong, flag it for the user instead of silently weakening or strengthening it.
3. **Do not write the argument from nothing.** If the user wants a section but has not given the finding, the evidence, or the point, ask one focused question, or give an outline with placeholders. Filling the gap with plausible filler is exactly how AI-sounding text is made.
4. **Readers over detectors.** Never degrade the text to game a detector.
5. **Keep manuscripts local.** Do not paste unpublished text into web search, online detectors, paraphrasers, or other external services unless the user asks. The bundled script runs locally.
6. **Disclosure.** Once per manuscript, remind the user that most journals ask authors to disclose AI assistance in writing. Do not repeat it every turn.

## Modes

| Mode | When | Output |
|---|---|---|
| Revise (default when text is supplied) | "polish", "去AI味", "改稿", a pasted paragraph or file | Revised text, short change log, author items |
| Draft | Notes, results tables, figures, or Chinese text to turn into paper English | New text with placeholders, plus the plan it follows |
| Check | "看看哪里像AI", "check this", diagnosis only | Ranked problem list with quotes and fixes; no rewrite unless asked |
| Letters | Cover letter, response to reviewers | The letter, following the Letters section |

Peer-review reports belong to the `peer-review` skill. The sentence-level rules here still apply to their wording.

## Revise

1. **Read the whole passage and name its job** (what the paragraph or section must make the reader believe). For a whole section, check it against its guide in `references/sections.md` first, and its tense and voice against `references/language.md`. Fix problems top-down, because a sentence-level polish of a paragraph that should not exist is wasted work: argument, then section job, then paragraph job, then claim/evidence/boundary, then terminology, then sentences, then words.
2. **Measure.** Run `python3 <skill-dir>/scripts/prose_check.py FILE` (.txt, .md, .tex, .docx, .pdf, or `-` for stdin; use a scratch file for pasted text). It reports sentence-length spread, repeated openers, connector-initial sentences, AI vocabulary, stock phrases, -ing tails, em dashes, stacked hedges, overclaims, and "significant" without a test, with the flagged sentences. A separate Language block reports usage errors (uncountable plurals, "Although..., but", "compared to", E-notation P values, missing unit spaces, and similar), mixed US/UK spelling, and abbreviations used before their definition or defined twice. The numbers are diagnostic proxies, not a detector score. Pass two files (`BEFORE AFTER`) to compare versions.
3. **Cut before rephrasing.** Delete stock openers, paragraph-closing morals, content-free verdicts, repeated restatements, and filler. Much AI prose is a real sentence wrapped in two decorative ones.
4. **Make it specific from the source only.** Replace vague praise and vague quantities with the actual comparison, number, dataset, or mechanism that the user's material contains. If the material does not contain it, use a placeholder.
5. **Restructure for rhythm; do not swap synonyms.** Merge two short related sentences, split an overloaded one, move the new information to the end, let a key finding stand as a short sentence. Replacing "utilize" with "use" helps because the plain word is better. Replacing "crucial" with "critical" changes nothing.
6. **Stop after one or two passes.** Re-running the script and polishing again tends to flatten the voice and introduce new tells.
7. **Deliver:** the revised text, then a change log of 3–8 bullets (the main kinds of change, not every edit), then author items (placeholders to fill, claims to verify, citations to check). Write the change log and notes in the language the user is using; the manuscript text stays English. Make targeted edits and keep passages that were already fine verbatim, so the user can review the diff.

For files: do not overwrite the input unless asked. Write the revision next to it (for example `intro_revised.tex`). Preserve LaTeX commands, citation keys (`\cite{...}`, `[@key]`), cross-references, math, gene and variant IDs, numbers, and units exactly.

### Example

Before:

> In recent years, polygenic risk scores (PRS) have emerged as a powerful tool for disease risk prediction. However, their performance remains limited in non-European populations, highlighting the critical need for more equitable approaches. In this study, we propose a novel framework that leverages multi-ancestry GWAS data to enhance PRS accuracy. Our results demonstrate that the proposed method significantly outperforms existing approaches across diverse populations, paving the way for more inclusive precision medicine.

After:

> Polygenic risk scores (PRS) built from European-ancestry GWAS predict disease less accurately in other ancestries [cite]. We developed [Method], which estimates ancestry-specific effects jointly from [K] GWAS. In [cohort], [Method] raised the variance explained for [trait] in African-ancestry participants from [x]% to [y]% (P = [P?]) without reducing accuracy in European-ancestry participants. [One sentence on the limit the results show, e.g., which traits gained least.]

What changed: the stock opener, both -ing tails, "novel", "leverages", and the untested "significantly outperforms" are gone; the vague comparison became a specific one with placeholders for the numbers; a boundary sentence was added as a placeholder; sentence lengths now vary with the content.

## Draft

1. **Intake.** Establish the section, the target journal, and the one-sentence argument: "In [system or problem], we show [advance] using [approach], supported by [evidence], within [boundary]." If the user has not given it, ask once; otherwise write with placeholders. When drafting inside a larger task (for example, writing up an analysis you just ran), take the argument from the results at hand and do not stop to ask.
2. **Terminology ledger.** Fix one name and one abbreviation per concept (method, cohort, trait, variant set) before writing, and use them identically everywhere, legends included. Cycling through synonyms for variety is itself an AI tell and confuses reviewers.
3. **Paragraph plan.** Read the section's guide in `references/sections.md`, then give each paragraph one job (context, gap, approach, result, comparison, mechanism, implication, or limitation) and write the plan as one line per paragraph. Show the plan with the draft for longer sections.
4. **Write, then self-check** against the Final check below and run the script on the draft.

**From Chinese notes.** Extract the propositions first, then rebuild the logical links in English explicitly (because, although, which means), then check terminology and hedging. Watch for topic-comment openings ("For this dataset, its quality..."), comma-joined clauses that need a full stop or a conjunction, uncited "many studies have shown", a topic noun repeated in every sentence, and article errors ("The hypoxia induces..." should be "Hypoxia induces..."). The full list, with set phrases such as "Among them" and "As we all know", is in `references/language.md` section 4.

## Check

Run the script, read the passage, then list the problems in the fix order above (argument and structure first, words last). Quote each problem and give a concrete fix. Do not rewrite the whole passage unless the user asks.

## Sections

Every paragraph should carry a claim, the evidence for it, and its boundary (the condition or limit under which it holds). Most AI text has the claim and a decorated restatement of it, but no evidence and no boundary.

Before drafting or revising a whole section, read that section's guide in `references/sections.md`. It covers the Introduction, Methods, Results, and Discussion in depth (paragraph shape, what reviewers check, methods-paper versus analysis-paper differences, section-specific AI failures, before/after examples), plus title, abstract, figure legends, availability statements, Key Points, and notes for NAR, Bioinformatics, Briefings in Bioinformatics, and Nature Communications. The short version:

| Section | Its job | Typical AI failure |
|---|---|---|
| Title | State the finding, or what the method does | Gerund opener ("Unveiling..."), hype after a colon, "novel" |
| Abstract | Context, gap, approach, results with numbers, implication with its boundary | Results given as adjectives; most words spent on context |
| Introduction | Lead the reader to the exact unknown and why it is worth answering; end with "Here we..." and the main findings | Prior work listed paper by paper; gap as "remains a challenge" or "no method exists"; contribution bullet lists |
| Methods | Let a reader reproduce every number and judge every choice | "Rigorous QC" instead of thresholds, versions, and n; invented parameter values |
| Results | Evidence in the order that builds the argument; numbers with effect sizes and tests | "To investigate X, we..." on every paragraph; inflated closing verdicts; hiding where the method lost |
| Discussion | Meaning, trustworthiness, relation to prior work, specific limitations and next steps | Re-summarizing the results; generic limitations; "further studies are needed" |
| Figure legends | Title sentence, panels, statistics; present tense | Interpretation and hype inside the legend |

## Claims and calibration

- **Verb ladder.** "show/demonstrate" for direct evidence, "indicate/suggest" for indirect or partial evidence, "may/could" for speculation. Do not promote "consistent with" to "demonstrates", or "comparable" to "superior".
- **Association is not causation.** GWAS, eQTL, colocalization, TWAS, and most MR results support "associated with", "implicates", or "prioritizes", not "causes", "drives", or "regulates", unless there is experimental evidence.
- **"Significant(ly)"** only with a named test or threshold; otherwise use "substantially", "markedly", or the number.
- **One hedge per claim.** "may suggest a possible role" stacks three; pick the one that matches the evidence.
- **Overclaim sweep.** Check every prove, conclusive(ly), unprecedented, groundbreaking, paradigm, first (verify it, and prefer "to our knowledge"), best, superior, unique, comprehensive, novel, always, never.

## Language

Correct, consistent English is part of reading as carefully written. AI drafts are usually grammatical but drift between tenses, spellings, and number formats in ways a careful author would not, and text drafted from Chinese has its own recurring errors. `references/language.md` covers tense, voice, and claim strength for each section; sentence clarity; word usage; grammar traps for Chinese-L1 writers; numbers, units, and statistics; abbreviations; nomenclature; spelling, hyphens, and punctuation; and concision. Read it when drafting or revising a whole section, and when the script's Language block reports problems. The essentials:

- **Tense.** Present for established knowledge, for what a figure shows, and for what a model or tool does; past for what this study, or one cited study, did and found. Methods: past for procedures, present for model definitions. Results: past. Discussion: present for interpretation.
- **Voice.** Active "we" for claims and choices; passive for routine procedures; data and methods as subjects in Results.
- **Consistency.** One spelling convention, one form per name and abbreviation, one format for numbers, P values, and figure citations.
- **Mechanics.** Numerals with units, separated by a space (10 kb); no numeral at the start of a sentence; P = 3.2 × 10⁻⁸, never E-notation or "P = 0.000"; effect sizes with 95% CI; human genes italic (*BRCA1*), proteins roman; the genome build stated once.
- **Chinese-English traps.** Missing articles, "evidences" and "softwares", "Although..., but" and "Because..., so", "Compared with X, the..." danglers, and "higher than X" where "higher than that of X" is meant.

**Connectors.** Counts from Nature Communications papers (a CS and AI sample, so treat as a guide): "However" is the most frequent sentence connector; "Furthermore" is used more than "Moreover"; "In addition", "In contrast", "Therefore", and "Overall" are normal. Most sentences need no connector at all, because the logic is carried by the content. Use "Notably", "Importantly", and "Interestingly" at most once per section, and only when the point really is surprising or important.
## AI tells

The full catalogue with genomics examples is in `references/ai-tells.md`. Read it when revising or checking a passage longer than a paragraph or two, or when the script flags patterns you want to fix well.

- **Words:** delve, intricate, pivotal, crucial, vital, paramount, underscore, showcase, leverage (verb), harness, utilize, facilitate, bolster, foster, unlock, unveil, elucidate, shed light on, pave the way, landscape, realm, tapestry, interplay, multifaceted, nuanced, holistic, seamless, meticulous, noteworthy, "a testament to", "plays a crucial role", "it is worth noting that".
- **Structures:** "not only X but also Y" and "not X but Y" framing; reflexive triplets ("fast, accurate, and scalable"); significance inflation; -ing tails (", highlighting the..."); vague attribution ("studies have shown" with no citation); stock openers ("In recent years"); paragraph-closing morals ("Taken together, these findings underscore..."); content-free verdicts and paraphrastic repeats ("In other words..."); "serves as" or "stands as" instead of "is"; false ranges ("from X to Y" that are not a range); vague quantifiers ("a wide range of", "numerous"); ornamental intensifiers and fillers ("remarkably", "in order to"); em dashes (en dashes in number ranges are fine); formatting leakage (Markdown bold or bullets in prose, Title Case headings where the journal uses sentence case, curly quotes in LaTeX, chat residue such as "Here is the revised text").

## Rhythm and word choice

In local detector experiments reported by others, making sentence rhythm less uniform gave most of the score reduction that could be achieved; swapping words gave little. Aim for rhythm that follows the content, not a quota: a key result can be one short sentence, a method with its conditions can take a long one.

- Vary sentence length. Break up any run of three or more sentences of similar length and shape. A short sentence has to earn its place; random short sentences read as a trick.
- Vary sentence openers. Not every sentence should start with "The", "We", "This", or a connector.
- Prefer verbs over nominalizations ("we evaluated" over "an evaluation was performed") and short common words (use, show, help, need, about). A high density of long Latinate words is itself a signal.
- When removing an adverb or connector, rebuild the sentence. Deleting "Additionally," and leaving the rest makes the text choppier and, in the same experiments, raised detector scores.
- Put known information first and new information last in each sentence, so sentences chain naturally.
- Check each paragraph's last sentence (the favourite place for a moral or summary) and every sentence over about 30 words.
- Link paragraphs through content, not through "This suggests..." or "These results..." openings.

## Leave alone

Not everything the script flags is a problem. Keep these unless they are overused:

- Logical connectors that carry real logic: however, although, whereas, thus, therefore, in contrast, furthermore, as expected, based on these results; an occasional "additionally".
- Functional adverbs: slightly, consistently, modestly, approximately, respectively, and "significantly" with a test.
- Technical senses: robust regression, statistical significance, fitness or epigenetic landscape, leverage in regression diagnostics, "novel loci" in GWAS, "comprehensive" when coverage really is exhaustive.
- Journal conventions: "Here we show", one "Taken together" per paper, structured abstract headings.
- The author's own correct habits. A consistent personal style is a feature; flattening it into generic prose makes text more machine-like, not less.

## Voice calibration

If `references/voice-profile.md` exists, read it before revising or drafting. Where it conflicts with the generic rules here, the profile wins, because the goal is to sound like this author, not like an average author.

To build it, ask the user for 2–3 of their papers written before 2023 (before AI drafting), run the script on each, and record: sentence-length distribution, favourite connectors and verbs, hedging habits, typical paragraph length, common openers, spelling convention, and 5–10 representative sentences. Use the profile to calibrate style only, never claims or content.

## Letters

- **Cover letter:** one page. State the main result, why it fits this journal specifically (its scope and readership, not flattery), and the required confirmations (originality, no concurrent submission, author approval, conflicts). No superlatives.
- **Response to reviewers:** thank each reviewer once, not at the start of every reply ("We thank the reviewer for this insightful comment" repeated 20 times is a tell). Quote each comment, answer it directly, and state exactly what changed and where (section, page and line, figure). Disagree politely and with evidence. Every addition requested by a reviewer should prompt a check for something that can be cut.

## Final check

- [ ] No invented numbers, citations, or results; every placeholder is visible
- [ ] Verbs match the evidence; no causal wording for associations
- [ ] "Significant" only with a test
- [ ] One name per concept; each abbreviation defined once
- [ ] Tense and voice fit the section; one spelling convention; numbers, units, P values, and gene names follow `references/language.md`
- [ ] No unexplained AI tells from the list above
- [ ] Sentence lengths and openers vary; no run of uniform 20–30-word sentences
- [ ] No em dashes, Markdown in prose, or chat residue
- [ ] LaTeX, citation keys, cross-references, numbers, and units intact
- [ ] Meaning preserved (revise) or every claim traceable to the user's material (draft)
