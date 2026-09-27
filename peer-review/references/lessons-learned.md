# Lessons learned

This file covers what happened to past comments once they reached authors, how a senior co-reviewer reshaped the user's drafts, the findings that recur across reviews, mistakes in our own reports, and what the user changed when this skill was first used on a real manuscript. Cases are anonymized. Read it before writing a revision report, when merging with a co-reviewer, or when deciding how hard to push.

## Contents

1. How authors responded to one joint report
2. What happened to comments in four other reports
3. How a senior co-reviewer edited the user's drafts
4. Recurring findings across reviews
5. Pitfalls in our own reports
6. A trial run of this skill: what the user changed
7. Rules that follow

---

## 1. How authors responded to one joint report

**Case.** An invited narrative review for a clinical-specialty journal. The user and a senior co-reviewer sent a joint report of 28 numbered comments, organized by section, with a separate block of figure and table comments. The response letter and revised manuscript came back for R1.

### Accepted: cheap, concrete, within scope

- Missing citations for factual claims were added.
- The caveat that the nearest gene is not necessarily the causal gene went into the Figure 1 legend.
- "Effect" became "odds ratio (95% CI)" in the tables.
- A confidence interval that excluded its point estimate was corrected.
- A limitation paragraph was added on the modest predictive accuracy of the subtyping approaches. It came from a terse note that the co-reviewer expanded into a full comment with questions: methods, data, or other features?
- Future-direction text and a sentence on bidirectional causal inference were added.
- A buzzword-heavy conceptual figure was **deleted** rather than redesigned.

### Declined as out of scope: the big asks

- A dedicated discussion of pleiotropy models (horizontal vs vertical, definitions). The authors said it would need a whole section and did not suit the journal's clinical readership, but offered to add it if the editor wanted it.
- A survey of statistical approaches (colocalization, multi-trait fine-mapping, local genetic correlation). The authors said the review reports the literature rather than cataloguing methods, and that a methods-heavy text would exceed the readership's interest.
- A survey of emerging non-genetic risk factors. The authors said the review is about genetics.
- A discussion of how functional experiments could dissect the shared biology. The authors called it too broad and asked the editor for guidance.

### Infeasible

- Formal colocalization for the "shared" loci in Figure 1, which had been defined by positional overlap within ±500 kb. The authors had only published lead variants, not full summary statistics, so they added a caveat to the legend instead.

### Rebutted successfully

- The comment said that soft-clustering methods "require tissue-specific information". The authors replied that clustering runs on summary statistics across traits, and that tissue information is an optional validation step. **The rebuttal was correct.** The claim came from the user's own draft. It was the only point in the report that authors refuted on the facts.

### The editor's own request

- The associate editor asked which questions the field has solved, which remain open, and what the primary goals are now. The authors answered with a scope statement in the introduction: an overview of key findings rather than a technical discussion. They did not add depth.

### Round two

- The senior co-reviewer wrote a narrowed R1 with 2 major and 3 minor points:
  1. A high-level 1–2 paragraphs on colocalization and fine-mapping. This was argued from the review's own title: a review of the shared genetic landscape cannot ignore the methods that resolve that landscape locus by locus.
  2. Functional follow-up, re-raised by number ("our previous point #22").
  3. More specific future-direction questions about shared genetics.
  4. A cautionary note in Figure 1 that nearest genes are not necessarily causal.
  5. A Manhattan plot that matched neither trait: either make it fully schematic or show the real data.
- The draft also expressed disappointment and included sarcastic asides ("if the authors dared to be a little bit thoughtful", "but I digress"). Neither helps the argument.

### Takeaways

- **Lead with the minimum.** "A section on pleiotropy models" was declined outright. "A high-level 1–2 paragraphs" is what the R1 had to fall back to. Offering the minimal version in round one saves a round.
- **Tie requests to the manuscript's own stated aim.** "Your title promises X, and X cannot be addressed without Y" is harder to decline than "the review should also discuss Y".
- **Check feasibility.** Ask whether the authors can do what you request, e.g. whether full summary statistics are public or only lead variants. Offer the caveat or limitation as the fallback in the same comment.
- **If you want a figure improved, say the smallest fix.** Otherwise deletion is the path of least resistance.
- **Separate must-fix from nice-to-have.** Scope-expanding suggestions (new risk factors, functional-genomics outlook) will be declined in a focused review; label them as optional so they don't dilute the essential points.
- **Verify technical claims** about what a method requires or does before writing them (guardrail 4 in SKILL.md).
- **Expect framing requests to be met by a scope statement.** If depth really matters, say which paragraph is missing and why the conclusions depend on it.

---

## 2. What happened to comments in four other reports

Outcomes of first-round reports on a software paper, a modeling study and a wet-lab study, and of the second round on an ML review. Each row was checked against the revised manuscript, not only the response letter.

| Request | What came back | Lesson |
|---|---|---|
| Software paper: replace an unmaintained comparator with a maintained one | Added, but only the comparator's CPU build (the authors cited limited GPU access and installation trouble). The paper then claimed consistent superiority | If the comparator's strength depends on hardware, say which configuration you expect, or ask for the caveat next to the claim |
| Software paper: a balanced limitations paragraph, with examples (scalability, algorithmic assumptions, data types) | A limitations paragraph and a future-work paragraph were added | Examples make a request easy to satisfy |
| Modeling study: an error metric and a power analysis for a small validation set | The error metric was already in the supplement. An agreement analysis in a new figure panel replaced the power analysis | Check the supplement before asking. Accept an equivalent substitute that answers the question behind the request |
| Modeling study: replace informal terms with "in silico" and "in vivo/in vitro" | The authors chose "in silico" and "ex vivo", which fit their assay better | Name the precise term for the specific assay |
| Wet-lab study: reconcile two DEG counts and justify the fold-change cutoff | The smaller count was dropped and the larger one kept. The letter says a rationale for the cutoff was added to Methods, but the revised Methods has none. Methods still says P < 0.05 where Results says adjusted P < 0.05 | Re-check a fixed number in every section where it appears, and confirm that each promised addition is really there |
| Wet-lab study: functional outcomes (behaviour, lesion size, oedema, survival) and direct functional assays | The reply called both future work. The revised manuscript nevertheless added a new figure with neurological scores and oedema and lesion measures. The functional assays were not done and became a limitation | Read the revised manuscript itself: letters can understate changes as well as overstate them |
| Wet-lab study: an implausible statistic, a copy-paste legend, misspellings | All fixed; the introduction paragraph was rewritten | Cheap, concrete fixes are nearly always made |
| ML review, second round: synthesis, length, worked case studies, professional editing, ethics subsections | Generic replies ("we acknowledged the mistake"), two of them duplicated, and typos in the letter itself. The quoted phrases were fixed but other errors remained. The ethics text gained examples but stayed two paragraphs without subsections. The body shrank from about 14k to about 12k words, and the section numbering stayed inconsistent | Make each request checkable: name the structure (e.g. three subsections and their headings), quote examples, give a target. When a reply is generic, verify every claim at line level |

### Takeaways

- **Experimental requests become limitations.** In wet-lab papers, new assays are usually answered with a limitation or a future-work paragraph. Write the fallback into the same comment, and decide beforehand whether the missing experiment is fatal to the conclusions.
- **The letter is not the record.** Build the revision tracking table from the manuscript text, then compare it with the letter.
- **Checkable requests get checkable answers.** "Improve the synthesis" invites "we compared the algorithms". "End each subsection with the conflicting findings and one take-home message" can be verified.

---

## 3. How a senior co-reviewer edited the user's drafts

Two joint reports: the clinical review above, and a methods review for a high-profile review journal. The user drafted detailed comments; the co-reviewer added terse notes and tracked edits, then restructured. What changed:

| Edit | Before (pattern) | After (pattern) |
|---|---|---|
| Directive → suggestion with an audience rationale | "The introduction should first outline the challenges." | "We suggest that an approach that might allow a broader audience to be engaged would be to first outline the broad challenges … before introducing specific methods in later sections." |
| Added the trade-off | "The review omits method X." | "…omits X. Despite its simplicity, X is widely used because it does not require an LD matrix; its weakness is that it assumes a single causal signal per locus." |
| Added the practical consequence | "Discuss trait selection." | "…in practice, methods can fail or give spurious results when all available traits are included, so guidance on selection matters." |
| Two-sided judgment when the call is close | "Remove the section on method class Y." | "The reviewers could go either way here… The authors might keep it with more context and a justification, or remove it if space does not permit." |
| Probing question instead of an assertion | "Most tagged genes may not be causal." | "How many of those genes are proven beyond reasonable doubt to be causal? If many carry uncertainty, would it not be prudent to show that uncertainty in the figures or text?" |
| Figure redesign from objectives | "Figure 3 is unclear." | "Reimagine the figure: identify the key outcomes first, work backwards, and add a 'you are here' marker plus what is needed to reach the next level of inference." |
| Structure | Flat Major/Minor list | A general-assessment paragraph, then comments by manuscript section, then a separate block for figures and tables |
| Balance | — | "The references to recent literature are commendable… however, they are highly specific and can come across as anecdotal." |
| Concrete resources | "Cite relevant work." | A named preprint DOI or PMID as an exemplar |
| Better point replaces a weaker one | How loci were counted (LD clumping) | Positional overlap within ±500 kb overstates shared biology; formal colocalization or multi-trait fine-mapping is the better test |
| Terse note → full comment | "actual accuracy is pretty modest" | A comment that states the gap, asks for its source (methods, data, other features), and explains why it matters for the field |
| Consolidation | Overlapping items | Merged; weaker points dropped |
| R1 | — | Narrowed to the two items that mattered most, with deference to the editor on scope |

What to copy: the rationale, the trade-offs, the two-sided judgments, the probing questions and the narrowing. What not to copy: the co-reviewer's edits also introduced typos and missing words ("undoubtably", "far to generous", "the start of play", "the authors to make a case") and, in R1, sarcasm. **Proofread the merged text regardless of who wrote each part.**

---

## 4. Recurring findings across reviews

Across 11 journal reports on 9 manuscripts (research, tool, modeling, case report, reviews, revisions) and 2 thesis evaluations, these came up again and again. Check for them first.

| Finding | Seen in | Typical request |
|---|---|---|
| Missing or thin limitations | software paper, modeling study, wet-lab study, case report, clinical review | A balanced limitations paragraph naming specific constraints (sample size, model, assumptions, data types) |
| Validation missing or indirect | data-mining study, wet-lab study, modeling study, methods paper, theses | Replication in independent data; orthogonal assays; at minimum qPCR in one extra dataset |
| Correlation presented as mechanism | wet-lab study, data-mining study, theses | Direct assays (binding, site mutation, rescue, RNAi); markers vs drivers |
| Outdated or narrow comparators | software paper, methods paper | Benchmark against maintained tools and alternative paradigms, with accuracy as well as speed |
| Conceptual conflations or taxonomy errors | two methods reviews, ML review, clinical review, thesis | Name both concepts and explain the distinction in one or two sentences |
| Internal numeric inconsistencies or implausible numbers | wet-lab study, clinical review, methods review | Reconcile counts; fix CIs; check prevalence vs mortality; check that probabilities sum correctly |
| Unjustified thresholds or parameters | wet-lab study, methods review | Justify cutoffs (log2FC) and hyperparameters |
| Figure problems | nearly all | Legibility, colors, significance keys, copy-paste legends, swapped references, schematic vs real data, buzzword collages |
| Organization and synthesis | ML review, methods review, clinical review | Challenges first; group by method or objective; take-home messages; condense repetition |
| Narrow evaluation | methods paper | More traits or datasets when public resources exist; systematic validation sets rather than two examples |
| Translational realism | wet-lab study, data-mining study, modeling study, case report | Delivery, off-target effects, safety; filter drug hits by phase and tractability; compare with literature benchmarks |
| Citations that do not support the statement | narrative methods review | Check the references behind the main claims against the sources. A misreported source behind a headline conclusion is a Major item; clear local mismatches go into one Minor item with 2–3 examples |
| Abbreviations, typos, citation style | nearly all | Low priority. Group real typos in one item; leave abbreviation lists and reference formatting out of the report by default |

---

## 5. Pitfalls in our own reports

The wording errors are listed in [style-guide.md §6](style-guide.md). Structural and judgment problems found in past reports:

- **Overstated technical claim.** The soft-clustering point in §1: the one factual rebuttal.
- **Vague attribution.** "Someone suggested…": either cite the source or write "It has been suggested [verify citation]".
- **Scope creep.** Asking a clinical review for a methods tutorial, or for topics outside its title, gets the whole comment declined.
- **Duplicated points.** One merged item repeated its own sentence; two items covered overlapping line ranges with the same complaint.
- **Ambiguous cross-references.** The user's solo reports restart at 1 for the minor comments, which is the user's chosen format. A bare "comment 2" is then ambiguous, so write "Major comment 2". The three reports shaped by the co-reviewer number continuously, which let the R1 cite "our previous point #22"; in joint reports, follow the co-reviewer's layout.
- **Where the decision goes.** Seven of the 11 saved reports have no recommendation line. That is the user's practice: the decision goes into the journal's form, and the tone sentence at the end of the opening carries the verdict in words. The two must agree.
- **Tone mismatch.** Harsh wording with a lenient verdict, or the reverse. Opening praise that later comments contradict. Sarcasm in a revision round.
- **Asserting citation errors without reading the source.** Say a reference is wrong only after reading it. When a source disagrees with the text, report every relevant estimate, not only the one that fits the point (one draft gave only the null drug-target estimate and left out the significant polygenic one).
- **"Not cited" when it was cited.** Search the reference list first; the study may be cited under another topic.
- **Figures judged from the text.** Figures sent as separate TIFF files were not looked at in the first draft. Convert every figure to PNG and view it.
- **"Corrections" that are wrong.** Changing "three software" to "three softwares" (both wrong: write "three software tools"). Check that every language correction is itself correct.
- **Ambiguous typo fixes.** "Correct the typo 'X with a low Y' (missing 'a')" doesn't show which text is original. Quote the original and the correction.

---

## 6. A trial run of this skill: what the user changed

**Case.** An invited narrative review of causal-inference methods applied to molecular data in a common disease. It had no line numbers, figures as separate TIFF files, and a reference list of about 60 items. The report went through six versions before the user was satisfied. The changes, in order:

1. **First draft.** The user rejected it for two reasons.
   - The figures had not been looked at.
   - Several citations were called wrong without the cited papers being read.

   The user asked for every figure to be viewed as an image and every questioned reference to be checked one by one.
2. **Second draft: style.** The user gave five rules, which now define the default format in SKILL.md:
   - Sentences were long and used uncommon words that read as machine-written. Use plain words and short sentences.
   - Drop the title. The opening paragraph is 200–300 words in three parts: what the manuscript does, its overall quality, and one sentence that sets the tone without naming the decision. It ends with "My comments are below."
   - Use two numbered lists, "Major revisions" and "Minor revisions", each starting at 1. No bold, italics or subheadings. Each item says where the problem is and what it is.
   - Major items are about research content: design, methods, results, evidence.
   - Minor items are formatting, wrong statements and similar.
3. **Deletions, round one.** The user deleted:
   - a request for a systematic search description (the manuscript called itself a narrative review);
   - all individual citation mismatches and the preprint labels;
   - the Major item on a misreported source behind a headline conclusion;
   - an uncited claim and an "unbalanced example" point;
   - the confidential note to the editor.
4. **Citation severity, revisited.** The user asked whether the citation problems were serious, and whether they might come from AI-assisted writing. The answer separated two kinds of problem:
   - A source whose findings were misreported and which carried a conclusion in the abstract. The source's main estimate contradicted the text.
   - Local mismatches, where a citation was attached to the wrong claim or a table row gave the wrong data source.

   Whether AI was involved cannot be known and does not change what the authors must fix, so it stays out of the report. The user then restored the first kind as one Major item, with all relevant estimates, and the second kind as one merged Minor item with three examples and a request to check all citations.
5. **Second opinion.** The user had another model critique the draft. Each point was checked against the manuscript and the sources, and most were accepted:
   - absolute statements about which MR sensitivity analyses can be used;
   - a wrong claim that a type of study was not cited;
   - an identifiability statement given without its conditions;
   - a suggested table wording that was itself misleading;
   - opening praise that later comments contradicted.

   One proposal was declined: moving a conceptual error into Major to cut the list short. It conflicted with the user's Major/Minor split. A proposal to re-add individual citation mismatches went to the user to decide.
6. **Deletions, round two.** From 8 Major and 14 Minor items, the user deleted:
   - two Major items, each a long list of further threats or methods to discuss;
   - a wrong table cross-reference and a framework wording point;
   - a slightly overstated phrase in a table;
   - the order of first table citation, and methods missing from a table;
   - a legend that listed fewer items than its figure;
   - figure resolution and an extra TIFF page;
   - the abbreviation list and mixed journal-name styles in the references.

   The final report had 6 Major and 7 Minor items and about 1,700 words.
7. **Reviewer form.** The decision (revise), the novelty score and the yes/no questions went into the journal's form. The comments to the editor were left blank. See report-templates §8.

**What the deletions show.** The user keeps items that change what a reader should believe: the evidence behind conclusions, incorrect statements, method assumptions, and summaries that disagree with the text. The user drops items that are correct but cost the authors time without changing the science: presentation details, cross-reference fixes, formatting, and long lists of extra topics. The leave-out list in SKILL.md comes from these deletions. Items on that list are still mentioned to the user in chat, so nothing is lost silently.

---

## 7. Rules that follow

1. For every expensive request, give the minimum acceptable version in the same comment.
2. Tie big requests to the manuscript's stated aim or title, and to the conclusions they affect.
3. Check feasibility: the data, cohorts and resources the authors can actually access. Check the supplement before asking for an analysis.
4. Verify every claim about how a method works; hedge or ask when unsure.
5. Mark optional suggestions as optional. Keep the major list to what changes the conclusions.
6. In revision rounds, verify each claimed change in the manuscript itself, credit concrete improvements, concede good rebuttals, re-raise at most a few central points by number, and defer scope disputes to the editor.
7. When merging with a co-reviewer, keep their rationale and trade-offs, remove duplicates, unify the voice, and proofread everything.
8. Make the tone sentence and the decision in the form agree. Don't name the decision in the report.
9. Make requests checkable: name the target structure, quote examples, and give numbers where they apply.
10. View every figure as an image, including separate TIFF files, before commenting on figures.
11. Check the references behind the main claims against the sources before saying they are wrong. Triage by consequence: headline conclusions → Major; clear local mismatches → one Minor item with examples; small differences in wording → leave out.
12. Leave low-value items out of the report by default, but list them for the user.
13. When the user brings a second opinion, verify each point before accepting it, and pass decisions that reverse the user's earlier choices back to the user.
14. Never speculate in the report about AI use, misconduct or carelessness. Describe the error and the fix.
