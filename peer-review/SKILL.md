---
name: peer-review
description: Draft, revise, merge, and quality-check peer-review reports for scientific manuscripts and theses in the user's own reviewing style (statistical genetics, functional genomics, bioinformatics, ML for omics, translational biomedicine), and answer the journal's reviewer-form questions consistently with the report. Use this skill whenever the user wants to review a manuscript, paper, or submission; write referee or reviewer comments for a journal; check whether a manuscript's citations support its statements; fill in a journal reviewer form (recommendation, novelty score, yes/no questions); assess a revised manuscript (R1/R2) against the authors' response letter; merge their notes with a co-reviewer's into one combined report; weigh a second opinion on a draft review; polish or tone-check a draft review; or write a Chinese thesis evaluation (学位论文评阅意见, 博士/硕士论文评审). Trigger even on terse requests such as "审稿", "写审稿意见", "看看这篇稿子", "帮我 review 这篇文章", "回答审稿表格", or "评阅意见", and whenever a folder with a manuscript PDF/DOCX, figures, or a journal reviewer PDF is shared for evaluation.
---

# Peer Review

Write reviews the way the user does: an opening paragraph that proves the manuscript was understood and sets the tone, then numbered, anchored, actionable Major and Minor revisions. These patterns were distilled from the user's past reports: journal reviews of research articles, software and methods papers, a case report, and narrative and methods reviews (including revision rounds), plus Chinese PhD and master's thesis evaluations. The authors' responses and a senior co-reviewer's edits were studied too, and so was a full trial run of this skill that the user corrected line by line.

The report format below is the user's current format. It replaces the title, bold headings, continuous numbering and closing Recommendation line of older reports.

## What a review in this style looks like

- **No title, plain text.** The report is an opening paragraph, then "Major revisions" and "Minor revisions", each a numbered list starting at 1. No title, bold, italics, subheadings, or bullet lists inside items. The decision goes in the journal's form, not in the text.
- **The opening paragraph has three parts and 200–300 words.**
  1. What the manuscript does: data, design, methods, key numbers and main claims, in your own words.
  2. Overall quality: specific strengths, then the two or three areas that need work. Both must agree with the comments that follow; don't praise something that a later comment criticizes.
  3. One sentence that sets the tone without naming a decision: the manuscript is well written and needs only small changes; it needs further improvement in named areas; or it has substantial problems. Then "My comments are below."
- **Each item gives the location first, then the comment.** Use line numbers when the manuscript has them. Otherwise use the section title in quotes plus the paragraph number, the table and row, or the figure and panel. A Major item runs: where → what is wrong or missing → why it matters for the conclusions → what to do.
- **Major is substance; Minor is wrong statements and formatting.**
  - Major: research design, methods, results, the evidence behind the conclusions, and questions about any of these.
  - Minor: incorrect or unsupported single statements, missing citations for single claims, errors in tables and figures, and a few visible formatting fixes.
- **Plain, short sentences.** Use common academic words and one point per sentence. The user rejected a draft because its long sentences and unusual word choices read as machine-written (see [style-guide §1](references/style-guide.md)).
- **Focused.** Usually 5–8 Major and 5–8 Minor items, about 1,500–1,800 words in total. Merge related points and leave out low-value items (step 6).
- **Domain precision.** Catch conceptual conflations, for example:
  - conditional analysis vs fine-mapping;
  - colocalization vs multi-trait fine-mapping;
  - nearest gene vs causal gene;
  - OR vs "effect";
  - total vs direct effect;
  - deep learning vs learning paradigms.

  Also catch outdated or unmaintained comparators and missing standard analyses.
- **Numbers are checked**, for example:
  - counts that disagree between sections;
  - CIs that exclude their point estimate;
  - probabilities that sum above 1;
  - implausible statistics;
  - copy-pasted legends;
  - swapped figure references;
  - summary-table entries that disagree with the cited study.
- **Polite, specific, and firm when warranted.** Use "Please …", "I suggest …" and "It would be helpful …". When the evidence supports it, say plainly that the problems are fundamental.

## Guardrails

1. **Confidentiality.** A manuscript under review is confidential, so keep its content local:
   - Don't paste manuscript text, unpublished results or identifying details into web searches or external services.
   - Don't publish the report or a summary of the manuscript as a web page.
   - Looking up the published papers the manuscript cites is fine: search PubMed or PMC by title, DOI or PMID, never with the manuscript's own sentences. Generic lookups are fine too, e.g. "is this tool still maintained?".
2. **Journal AI policy.** Many publishers restrict AI assistance in peer review or require it to be disclosed. If the user hasn't already dealt with this, add one line, once per conversation, reminding them to check the journal's reviewer policy. The user is the reviewer of record and vets every comment.
3. **No fabricated references.** Cite only papers, tools and URLs you are confident exist, and give the DOI, PMID or URL when you have it. If unsure, name the method without a citation or mark it `[verify citation]`. A wrong citation costs more credibility than a missing one.
4. **Verify before asserting.**
   - Check every claim about how another method works, what the field "always" does, or what the manuscript says, against the manuscript text, your own knowledge, or a quick generic lookup.
   - State the conditions under which a technical statement holds instead of writing it as absolute ("with only one or two independent instruments, MR-Egger cannot be used", not "MR-Egger cannot be used").
   - Before writing that something "is not cited" or "is missing", search the manuscript's own reference list and supplements.
   - If still uncertain, ask it as a question or hedge ("as far as I know…").

   In past reviews, the one point authors successfully rebutted was an overstated technical claim.
5. **No speculation about AI use or misconduct in the report.** A manuscript may show patterns typical of AI drafting: real references carrying wrong content, table details that match no source, tables that contradict the text, thin synthesis. The pattern is not proof, and careless human citation produces the same pattern. Describe each problem factually and ask for the fix. If the user asks what you think, discuss it in chat only.
6. **Double-blind etiquette.** Don't try to identify anonymized authors, for example from file metadata.

## Workflow

### 1. Scope the task

Work these out from the request and the files; ask only if they can't be inferred.

- **Mode**: initial review, revision review (R1/R2), co-reviewer merge, second opinion on a draft, polishing the user's own draft, or thesis evaluation. See [Modes](#modes).
- **Venue and article type**: which journal and audience, and whether it is a research article, methods/software paper, resource/database, review, case report or thesis. The venue sets what you can reasonably request. PLOS ONE judges rigor, not novelty. A clinical journal's invited review will decline deep method detail. A case report is judged on its educational value. A self-declared narrative review should not be asked for a systematic search.
- **Constraints**: the reviewer-form questions, word limits, and whether the user wants a full draft or only the key issues.

The user's review folders are usually named `YYYY-MM-DD <Journal>/` or `YYYY-MM-DD/`. Each holds:
- the journal's `*_reviewer.pdf` or a DOCX manuscript, sometimes in a subfolder;
- any figures, tables and supplements;
- after the review, `comments.docx`.

### 2. Read everything

Extract the text into a scratch directory (the session scratchpad or a temp dir), not into the manuscript folder:

```bash
python3 <skill-dir>/scripts/extract_manuscript.py "<manuscript folder or file>" --outdir "<scratch>/extract" --figures-to-png --render-figure-pages
```

It writes one text file per input plus `MANIFEST.txt`, and handles:
- PDF: on journal reviewer PDFs each line keeps its line number (`212  were retained after QC…`), so anchors can be checked; highlights and sticky notes are listed; pages that look like figures are flagged and, with `--render-figure-pages` or `--render-pages 12,14-15`, rendered to PNG;
- DOCX: tracked changes as `{+[author] …+}` / `{-[author] …-}`, Word comments with their anchored text, replies and resolved state, and embedded images (converted with `--figures-to-png`);
- DOC/RTF, PPTX, XLSX, CSV and code files; ZIP archives with `--unzip`;
- TIFF and other figures, converted to PNG (`--figures-to-png`) so you can view them.

Author names in file metadata are printed only with `--meta`; leave it off for double-blind review.

Then read in full:
- the abstract, methods, results and discussion;
- figure legends and tables;
- supplements;
- the data and code availability statements;
- the reference list;
- the journal's reviewer questions.

Look at every figure as an image. TIFF and most other figure files can't be read directly: open the converted PNGs, and compare the separate figure files with the images embedded in the manuscript. In the trial run, comments on figures that had not really been viewed were wrong, and the user caught them. Don't comment on a figure you haven't opened.

As you read, keep anchored notes (line or section and paragraph, page, table row, figure panel) on:
- the central claims and the examples offered as evidence for them;
- every number that appears in more than one place;
- each method and its parameters;
- the references behind the main claims and the summary tables;
- anything surprising.

### 3. Write the opening paragraph first

Summarize the study in your own words before critiquing it. If you can't state the central claim clearly in two sentences, that is itself a finding about clarity or organization. Write the quality and tone parts after the critical pass, so they match the comments.

### 4. Critical pass

Evaluate through these lenses, roughly in priority order:

1. Does the evidence support the central claims? Watch for association presented as causation, overclaiming, alternative explanations, and conclusions that rest on a few examples.
2. Methods: are they appropriate, current, fully described and reproducible? Are their assumptions stated? Are standard analyses missing?
3. Statistics and internal consistency: sample sizes, tests, multiple testing, CIs, and numbers that should match across sections.
4. Confounding and bias: batch or platform effects, cell-type composition, population structure, selection.
5. Validation: replication, independent data, orthogonal experiments, and benchmarking against current, maintained tools.
6. Limitations, scope and translational realism.
7. Presentation: structure, figures, terminology, language.

Load the matching checklists:
- by article type (research, wet-lab, data-mining, methods/software, database, review, case report, thesis): [references/checklists-article-types.md](references/checklists-article-types.md);
- by domain (GWAS and shared genetics, MR, fine-mapping, functional annotation, QTL and TWAS, transcriptomics, drug repurposing, ML, modeling, wet-lab, clinical, statistics, causal graphs): [references/checklists-domains.md](references/checklists-domains.md).

Treat the checklists as prompts for thought, not a form to fill in. Raise only the items that apply to this manuscript.

### 5. Check the references behind the main claims

Reviews and discussion sections often cite papers that don't say what the text claims. Check them, but check your own reading first. An earlier draft asserted many citation errors without looking the papers up; the user doubted that so many errors were likely, and several of the claims did not hold.

1. Pick the references that carry weight: those behind the abstract's conclusions, those behind each row of a summary table (estimates, data sources, methods), and any statement that looks surprising.
2. Look each one up on PubMed or PMC by title, DOI or PMID. Read the abstract, or the full text when the claim concerns methods, data sources or numbers. Note the design, data, exposure and outcome, and the main estimates with CIs.
3. Before calling a citation wrong, re-read the manuscript sentence and check whether another cited reference covers it.
4. Triage what you find:
   - **A mismatch that supports a main or abstract conclusion** becomes a Major item. Give what the source actually reports, with every relevant estimate, not only the one that fits your point. For example, if a study reports a null drug-target estimate and a significant polygenic estimate, give both. Ask the authors to revise the conclusion that rests on it, including in the abstract.
   - **Clear local mismatches** (wrong study design, data type, data source, method or sample) go into one Minor item. Give 2–3 concrete examples and ask the authors to check all citations and table entries.
   - **Imprecise wording or interpretation-level differences**: leave them out.

### 6. Triage and calibrate

- **Major vs minor.** Major items concern design, methods, results and whether the conclusions hold. Minor items are wrong or unsupported single statements, table and figure errors, and a few formatting fixes. When in doubt, ask: "would fixing this change what a reader believes?"
- **Keep the report focused.** Aim for 5–8 Major and 5–8 Minor items and about 1,500–1,800 words. Merge related points into one item and drop weak ones. Order Major items by importance, so the decision hinges on the first two.
- **Leave out low-value items by default.** The user deleted these kinds of items from a recent report:
  - lists of undefined or unused abbreviations;
  - reference-list formatting, such as mixed full and abbreviated journal names, or preprints not marked;
  - figure file resolution, image size, or extra pages in a TIFF;
  - the order in which tables are first cited, or methods missing from a summary table;
  - legends that list fewer items than the figure shows;
  - a wrong cross-reference to a part of a table;
  - examples that are unbalanced, e.g. only positive trials;
  - the literature-search description of a self-declared narrative review;
  - fine points of how a framework or guideline is worded;
  - softening a single table phrase that is only slightly overstated;
  - long lists of extra threats or extra methods to discuss (e.g. every bias that could affect MR, or adding g-methods and Granger examples to a section that only mentions them).

  Raise one of these only if it causes a real error or misunderstanding. Give the user the list of what you left out, in chat, so they can add items back.
- **Give fallbacks for expensive requests.** When asking for new experiments, new cohorts, or data the authors may not have, give the ideal fix *and* a minimum acceptable alternative, e.g. "at minimum, discuss this limitation". Authors decline requests that look out of scope or infeasible; a fallback keeps the point alive.
- **Calibrate to the audience.** For a review aimed at a clinical readership, ask for "a high-level 1–2 paragraphs", not a methods tutorial.

### 7. Draft the report

Use the templates in [references/report-templates.md](references/report-templates.md). They cover:
- the journal report (research, methods, software, resource and review articles);
- the revision report;
- the co-reviewer merge;
- confidential comments to the editor (only on request);
- the tone sentence and the form's decision;
- the Chinese thesis form;
- the journal reviewer form.

Defaults:
- Order: opening paragraph → `Major revisions` → `Minor revisions`. No title and no Recommendation section.
- Number each list from 1. When one item refers to another, write "Major comment 1", not "comment 1".
- A solo report uses "I" ("I suggest…"); a joint report uses "we".
- Start each item with its anchor, as described above.
- Plain text only: no bold, italics, headings inside the lists, or bullets inside items.
- When you suggest replacement wording, check it as hard as the original. A suggested fix that carries its own error undermines the comment.
- Write in the venue's language, whatever language the conversation is in: English for journals, Chinese for Chinese thesis forms.
- Exception: a joint report follows the structure the co-reviewer sets, e.g. organized by manuscript section.

For voice, wording to avoid, and exemplars, see [references/style-guide.md](references/style-guide.md).

### 8. Self-check before delivering

- [ ] No title; plain text; "Major revisions" and "Minor revisions" each numbered from 1.
- [ ] The opening paragraph is 200–300 words, has the three parts, and ends with "My comments are below." Its praise doesn't contradict any later comment.
- [ ] The tone sentence matches the severity of the Major items and the decision the user will pick in the form.
- [ ] Every item starts with its location. Every Major item says why it matters and what to do; none is a vague "improve the discussion".
- [ ] Every anchor, number and quote has been checked against the manuscript; every statement about a cited paper has been checked against that paper.
- [ ] No fabricated or unverifiable references; URLs and DOIs are correct.
- [ ] Technical statements carry their conditions; nothing is called "not cited" without checking the reference list; suggested wording is itself correct.
- [ ] Requests are feasible for this venue and article type, with fallbacks for the expensive ones.
- [ ] No duplicated points; about 5–8 Major and 5–8 Minor items; roughly 1,500–1,800 words.
- [ ] Short sentences and plain words. If the `paper-prose` skill is installed, run its `scripts/prose_check.py` on the draft and fix what it flags. Language corrections in the report are themselves correct (e.g. "three software tools", never "three softwares").
- [ ] Nothing insulting or ad hominem, and nothing about AI use; the criticism targets the work.

[references/lessons-learned.md](references/lessons-learned.md) covers what authors accepted, disputed and declined, how a senior co-reviewer edited the user's drafts, and what the user changed in the trial run. Read it before writing a revision report, or when unsure how hard to push.

### 9. Deliver

- Show the report in chat as Markdown. Then, in the conversation language, tell the user the decisive issues, anything you couldn't verify, and the items you left out.
- Save a Word copy in the manuscript folder, following the user's archive convention (`comments.docx`). The script never overwrites: if the file exists, it writes `_v2`, `_v3`, and so on. It also blanks the author field in the file's metadata.

  ```bash
  python3 <skill-dir>/scripts/md_to_docx.py "<scratch>/comments.md" -o "<manuscript folder>/comments.docx"
  ```

  HTML comments (`<!-- … -->`) in the Markdown are dropped during conversion, so private working notes can stay in the draft. When the user settles on a version, keep that one and, if they ask to clean up, move the others to the Trash rather than deleting them.
- Don't write confidential comments to the editor by default; the user leaves that box empty. If the user asks for one, offer one or two neutral sentences (report-templates §5).
- If the user shares the journal's reviewer form (pasted questions or a screenshot), answer each question consistently with the report (report-templates §8).
- Flag anything you couldn't check, such as unreadable figure details or supplementary files that wouldn't open.

## Modes

### Initial review

Follow the workflow above.

### Iterating on the user's edits

The user usually revises by deleting items ("delete Major 3 and Minor 1, 2, 7") or by rejecting a style.

1. Apply exactly what was asked, renumber, and keep all other text verbatim.
2. Save the result as a new version; don't overwrite the previous one.
3. Treat the kinds of items the user deleted as preferences for the rest of this report and for later reports. If a kind is new, suggest adding it to the leave-out list in step 6.
4. If the user deletes an item you think is central (e.g. the one citation problem that undercuts the main conclusion), say so once, briefly, with the reason; then follow their decision.

### Second opinion

Use this when the user brings another reviewer's or another model's critique of the draft and asks what you think.

1. Check each point against the manuscript and the sources, not against your earlier draft.
2. Tell the user which points you accept and which you reject, with the reason for each, before revising.
3. Accept correct points plainly. In the trial run, most of a second model's points were right: over-absolute technical statements, a "not cited" claim that the reference list disproved, an identifiability statement given without its conditions, a suggested wording that introduced a new error, and opening praise that later comments contradicted.

### Revision review (R1/R2)

Inputs: the previous comments (ours and, if available, the other reviewers'), the response letter, and the revised manuscript (tracked or clean).

1. Build a tracking table for each previous comment. Record the authors' response and what actually changed in the manuscript. Verify each change in the text itself: letters overstate ("we revised the whole manuscript") and also understate (new data added for another reviewer and never mentioned to you). Journal PDFs for a revision often bundle the previous manuscript, the revised one and a tracked version, so check which one you are reading. Then assign a status (resolved / partially / not addressed / declined) and a next action.
2. Use the same report format. The opening paragraph acknowledges the effort and the concrete improvements, then names what remains. Raise only the unresolved important items and any new issues the revision introduced, narrowed to the few that matter most. Refer to earlier points by list and number ("our previous Major comment 3").
3. Accept reasonable declines gracefully. If a declined point is central:
   - restate briefly why it matters;
   - propose a minimal version (e.g. "a high-level 1–2 paragraphs");
   - defer to the editor on scope.
4. Don't move the goalposts. Raise new major issues on unchanged material only if they are serious, and label genuinely new problems as new.

### Co-reviewer merge

Use this when the user drafts jointly with a co-reviewer, for example detailed comments from the user plus terse notes or tracked edits from a senior colleague.

1. Extract both documents; the script preserves tracked changes and Word comments.
2. Pick one structure. Prefer the co-reviewer's if they set one. Otherwise use the user's format above.
3. Merge the notes into one text:
   - merge overlapping points, keeping the most specific evidence and combining the rationales;
   - expand terse notes into full sentences without changing their intent;
   - unify the voice to "we"/"the reviewers";
   - renumber.
4. Don't silently resolve disagreements; list them for the user to settle with the co-reviewer.
5. Give the user a short provenance note alongside the merged report: which comments came from whom, and what was reworded.

### Polishing the user's draft

Keep the user's points and voice. Improve clarity, specificity and tone, fix grammar, and add anchors or concrete suggestions where the draft is vague. List substantive changes separately (e.g. "softened Major comment 3", "hedged the claim in Minor comment 2; please confirm"). If a technical statement looks wrong, flag it rather than silently rewriting it.

### Chinese thesis evaluation (学位论文评阅意见)

Write in Chinese, following the user's form:
- 评分;
- 学术评语: one paragraph with a fixed arc;
- 论文的不足之处及建议: grouped as 格式上 / 语言表达上 / 内容上.

If the university supplies a form, map the content into its fields. The template, stock phrases and score guidance are in [references/report-templates.md](references/report-templates.md), section 7.
