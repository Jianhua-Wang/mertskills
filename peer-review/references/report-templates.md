# Report templates

Fill the bracketed parts. Delete optional parts that don't apply. The structures follow the user's current format; wording can adapt to the manuscript. The report itself has no title and no bold, italics or subheadings: the only headings are the plain lines "Major revisions" and "Minor revisions".

## Contents

1. Journal report: research, methods, software, resource and review articles
2. What review-article comments cover
3. Revision report (R1/R2)
4. Co-reviewer combined report and provenance note
5. Confidential comments to the editor
6. The tone sentence and the form's decision
7. Chinese thesis evaluation (学位论文评阅意见)
8. Journal reviewer forms

---

## 1. Journal report: research, methods, software, resource and review articles

```
[Opening paragraph, 200–300 words, in three parts]
[Part 1, content, 4–6 sentences] This manuscript [presents / investigates / reviews] [what] using [data: source, n, design, platform]. The authors [main methods, in order]. They report that [main findings, with the key numbers]. They conclude that [main conclusion].
[Part 2, quality, 2–3 sentences] [Specific strengths, e.g. "The topic is timely, and the manuscript is clearly written and well organized. The benchmark on X is useful for readers who choose between tools."]
[Part 3, tone, one sentence; see §6] [e.g. "However, several parts of the manuscript need further improvement, mainly A, B and C."] My comments are below.

Major revisions

1. [Location]. [What is wrong or missing]. [Why it matters for the conclusions]. [Specific request: analysis, tool, experiment, citation or text change]. [Optional: At minimum, [a cheaper acceptable alternative].]

2. ...

Minor revisions

1. [Location]. [Issue]. [Exact fix].

2. ...
```

Notes:
- **Locations.** "Lines 212–215." when the manuscript has line numbers. Otherwise `Section "Title of section", paragraph 2.`, `Table 2, LDL cholesterol row.`, `Figure 2, Panel B.` Several locations for one point go in one item, separated by semicolons.
- **Numbering.** Each list starts at 1. When one item refers to another, write "Major comment 1". In a later round, write "our previous Major comment 3".
- **Areas named in the opening** should be the themes of the first Major items, in the same order.
- **Methods and software papers** almost always need a comment on benchmarking against the *current, maintained* state of the art, and one on limitations and scope. Check the software itself too: availability, documentation, license, and supported input types.
- **Case reports**: ask for:
  - the rationale for each treatment decision and its sequencing;
  - quantified claims, e.g. what counts as "long survival" compared with the survival reported in the literature;
  - the discussion of molecular findings in *this* tumor type specifically;
  - explicit take-home lessons;
  - CARE-guideline items such as the timeline and patient consent.
- **A positive report can still carry one or two Major items**, such as a missing benchmark. Don't invent Major items to fill space. If there is nothing substantive, leave out "Major revisions" and say in the tone sentence that only small changes are needed.

---

## 2. What review-article comments cover

A solo report on a review uses the §1 format, anchored by section title and paragraph. A joint report may instead follow the co-reviewer's layout: a general-assessment paragraph, then comments by manuscript section with Major and Minor points inside each, then a block on figures and tables.

What review-article comments typically cover:
- **The evidence behind the headline conclusions.** Find the examples the abstract's conclusions rest on, and check them against the cited studies (SKILL.md step 5). A conclusion that rests on one or two mis-cited examples is the most important Major item.
- **Synthesis over description.** Most findings mentioned in one sentence, without effect sizes, is a common weakness. Ask for a short summary at the end of each method section: what the method has shown in this disease, and what is still unclear. A table or box of examples where methods gave different results helps, with the reason for each difference. A difference is not always a conflict: univariable and multivariable MR estimate different effects, and a drug-target estimate can differ from a polygenic one.
- **Assumptions and the kind of claim each method supports.** For each method, the identifying assumptions, when they fail, and whether the output is causal, prioritization or association.
- **Summary tables.** Effect estimates with 95% CIs and units, the number of instruments, the data sources, and methods that match the cited studies. Tables must not contradict the text.
- **Framing.** Lay out the challenges the field must solve before introducing specific methods. Make clear which questions are solved and which remain open.
- **Conceptual precision.** Separate concepts that have different objectives, e.g. conditional analysis vs fine-mapping, multi-trait fine-mapping vs colocalization, horizontal vs vertical pleiotropy, nearest gene vs causal gene, total vs direct effect.
- **Coverage gaps.** Look for widely used methods, QC tools, practical post-hoc filters or alternative strategies that are missing. Name 1–3 concrete examples and say why each matters, including its weakness. Keep this short; long lists of extra methods were deleted by the user.
- **Practical guidance.** Cover hyperparameter choices, how to select data sources, and trade-offs such as summary-level vs individual-level methods.
- **Future directions.** Keep them specific to the review's theme, e.g. "How can we discover more shared loci between X and Y?". Include downstream applications.
- **Figures.** Check their accuracy (probabilities, CIs, arrows that match the legend's definitions) and clarity. A figure built on buzzwords should be reimagined around key outcomes, with a "you are here" marker.
- **Readership.** Calibrate to the audience. In a clinical journal, ask for "a high-level 1–2 paragraphs", not a methods tutorial.
- **Not for narrative reviews:** a systematic search description, or balanced lists of positive and negative examples.

---

## 3. Revision report (R1/R2)

First build a tracking table for the user; it is not part of the report sent to the journal:

| Previous point | Original comment (short) | Authors' response | Verified change in manuscript | Status | Action |
|---|---|---|---|---|---|
| Major 3 | Discuss colocalization/fine-mapping | Out of scope for readership | None | Declined | Ask for a high-level 1–2 paragraphs; defer to editor |
| Minor 2 | Cite the genetic-correlation claim | Reference added | Line 86 now cites it | Resolved | — |
| Minor 6 | "Effect" → "OR (95% CI)" | Changed | Tables 1–2 updated | Resolved | — |
| Major 5 | Formal colocalization for Fig. 1 | Data unavailable | Caveat added to legend | Partially | Accept; optionally note the limitation |

Then write the report:

```
[Opening paragraph, 150–300 words] The authors have revised the manuscript carefully, and the new version is clearer, particularly [concrete improvements]. [What remains, in one sentence.] [Tone sentence; see §6.] My comments are below.

Major revisions

1. Our previous Major comment 3. [In 1–2 sentences, acknowledge the authors' reason and restate why the point matters.] [The minimal acceptable version, e.g. "I agree that a detailed discussion is beyond the scope of this review, but a high-level 1–2 paragraphs on … would still help."] [If the dispute is about scope: "I defer to the editor on how much of this is relevant to the readership."]

2. ...

Minor revisions

1. [Remaining or new small items; say which are new.]
```

Rules of thumb:
- Check every claimed change in the manuscript itself, not only in the response letter.
- Don't reopen resolved points or reasonable declines. Narrow the report to what matters most, which in the user's past R1 reports was two major items.
- If the authors convincingly rebutted a point, concede it briefly. It buys credibility for the points that remain.
- If a scope disagreement persists, make the case once, propose the minimal version, and defer to the editor.
- Label new issues as new. Raise new majors on unchanged material only if they are serious.
- Stay collegial even when disappointed. State disagreement factually; sarcasm weakens the argument with both authors and editor.

---

## 4. Co-reviewer combined report and provenance note

The combined report uses the agreed structure: the co-reviewer's layout if they set one, otherwise §1. Write it in the "we" voice.

Alongside it, give the user a provenance note. It is for them only and is never submitted:

```
Provenance (internal — do not submit)
- Structure: follows [co-reviewer]'s section layout.
- From the user's draft: #2, #3, #6–#9, #21–#26 (lightly edited).
- From [co-reviewer]: #1, #11 (bullets 2–3), #12, #19.
- Merged: #4 (user's credible-set filters + co-reviewer's calibration metrics).
- Reworded: #14 ("Someone suggested…" → "It has been suggested…" [verify citation]).
- Dropped as duplicates: user's #X (covered by #Y).
- Open disagreements: [list] — settle with [co-reviewer] before submission.
- Please proofread: #10 contains a garbled sentence in the co-reviewer's addition.
```

---

## 5. Confidential comments to the editor

Default: none. The user leaves this box empty, and a note that only repeats the report adds nothing.

Write one only when the user asks, or when there is a concern that belongs with the editor alone:
- suspected image manipulation, duplicate publication or plagiarism, stated factually and with locations;
- ethics or consent issues, or undisclosed conflicts of interest;
- the limits of the reviewer's expertise (e.g. "I am not able to assess the clinical staging details.").

Keep it to one or two neutral sentences, and never harsher or softer than the report. Don't speculate about how the manuscript was written, including AI use. If the user asks for a generic note: "My main concerns are [A] and [B], described in the comments to the authors. I believe they can be addressed in a revision."

---

## 6. The tone sentence and the form's decision

The text never names the decision. The third part of the opening paragraph sets the tone, and the user picks the decision in the journal's form. The two must agree.

| Decision in the form | Use when | Tone sentence (then "My comments are below.") |
|---|---|---|
| Accept | Nothing substantive remains | "The manuscript is well written, and I have only a few small corrections." |
| Minor revision | The conclusions are sound; fixes are to presentation, clarity or small analyses | "Overall, this is a well-prepared manuscript, and my comments should be easy to address." |
| Major revision / Revise | The conclusions may change, or key analyses, evidence or validation are missing but can be fixed | "However, several parts of the manuscript need further improvement, mainly [A], [B] and [C]." |
| Major revision, serious | As above, but several Major items undercut the main conclusions | "However, the manuscript has several substantial problems, mainly [A] and [B], that need to be addressed." |
| Reject | Fundamental flaws that a revision cannot fix | "However, the manuscript has fundamental problems in [A] and [B], which in my view a revision cannot resolve." |

- Having Major items is not the same as recommending major revision. A positive report can list one or two Major items and still fit minor revision.
- Map the decision onto the form's options, which vary by journal: Accept / Revise / Reject, Minor / Major revision, "Reconsider after major revision", or interactive-review stages. A three-option form with any Major item usually means "Revise".

---

## 7. Chinese thesis evaluation (学位论文评阅意见)

Write the output in Chinese. The fields and the arc of the 学术评语 paragraph follow the user's past evaluations:

```
论文题目：[题目]
评分：[分数]

学术评语：
[研究背景与意义，1–2 句]。本文通过[研究对象/样本/数据]，采用[主要方法]，[主要研究内容]，[主要发现]。该论文的创新之处在于[创新点]。该论文层次分明，具有一定的论证逻辑性，实验设计较为合理，表明该生基础学科知识较为扎实，有一定的科学素养。论文的不足之处在于[主要不足，1–2 条概括]；此外，论文中存在一些[格式/标点/表述]问题。总之，该论文已经达到了[博士/硕士]论文水平，同意该生将论文做适当修正后参加毕业答辩。

论文的不足之处及建议：
格式上
- [具体问题 + 位置 + 修改建议]
语言表达上
- …
内容上
- （1）…
- （2）…
```

Choose the conclusion sentence by severity:
- 同意答辩: "总之，该论文已经达到了[博士/硕士]学位论文水平，同意该生将论文做适当修正后参加毕业答辩。"
- 修改后答辩: "该论文基本达到[博士/硕士]学位论文水平，但在[主要问题]方面仍需完善，建议认真修改后再参加答辩。"
- 不同意答辩: "该论文在[研究设计/数据可靠性/结论支撑]方面存在较严重的问题，尚未达到[博士/硕士]学位论文的要求，不同意答辩。"

The score must agree with the comments. Confirm the bands against the university's rubric; a common scheme is 90–100 优秀, 80–89 良好, 70–79 中等, 60–69 合格, below 60 不合格. The user's past scores were:
- 75 for a PhD thesis: substantial clinical association work, weak mechanistic follow-up, some writing issues;
- 80 for a master's thesis: solid experiments, with weaknesses in results/discussion and formatting.

Items that recur in each category:
- **格式上**
  - blank pages, inconsistent fonts, tables not formatted to the school's requirements;
  - blurry figures or small figure text;
  - abbreviations not written out at first use (e.g. PNNs);
  - typos (e.g. lncRAN → lncRNA) and mixed Chinese/English punctuation;
  - exact P values not marked for significant group differences.
- **语言表达上**
  - colloquial or literal-translation phrasing (quote examples);
  - technical terms left unexplained;
  - non-academic, literary statements in the Discussion.
- **内容上**
  - an abstract whose purpose is verbose or whose results are vague (name the groups and give numbers);
  - missing methods detail, e.g. an RNA-seq pipeline without QC, alignment, DE software and plotting tools; unclear cell sources and culture conditions; plasmid construction not explained;
  - conceptual errors, e.g. transcriptome sequencing described as genome sequencing;
  - results not described: how many genes were detected, how many were up- or down-regulated, enrichment results;
  - figures that don't support the stated conclusions (explain the mismatch);
  - an unstructured discussion that doesn't go through the results one by one with literature;
  - claims of significance without P values;
  - selection bias in how risk-allele groups were defined;
  - mechanism left at prediction level, e.g. a transcription-factor binding site predicted but not tested. Suggest direct evidence: ChIP-qPCR or EMSA for binding, a luciferase assay with the site mutated, Co-IP for a protein–protein interaction.

---

## 8. Journal reviewer forms

Journals ask a fixed set of questions next to the free-text report. The user pastes the questions or sends a screenshot of the form. Answer in the form's language (English), in the form's order, using the exact option labels shown. For a screenshot, name the option to select for each question and give any free text ready to paste.

Answer each question literally; it is not a second vote on the whole report. But no answer may contradict the report: if one does, change the answer or the report before submitting.

| Question | How to answer |
|---|---|
| Recommendation | The decision that matches the tone sentence (§6). A report with Major items is usually "Revise". |
| Is the study design appropriate, and are the conclusions supported by the evidence? | If Major items concern the evidence behind the conclusions but can be fixed: the option meaning "No, but these points can be addressed with revisions". "Yes" only when no Major item touches the conclusions. |
| Novelty (1–5) | Rate the contribution, not the quality. A review that brings established methods together for a new field is usually 3. Add one or two plain sentences, e.g. "The methods discussed are established, but an overview of their use in [field] is useful. The novelty lies in the synthesis rather than in new methods or data." |
| Language and grammar | "Acceptable" unless errors hinder reading. Pick a lower option only if the report asks for language editing. |
| Title, abstract, keywords, introduction | Answer what is asked. "Does the abstract reflect the content?" can be Yes even when the report asks the authors to re-check a conclusion in the abstract; that problem is handled in the report. |
| Methods described well enough to repeat | Research articles: judge from the Methods and the Major items. Narrative reviews: Yes (or N/A if offered); there are no experiments to repeat. |
| RRIDs | "Not applicable" for reviews and for papers without antibodies, cell lines, model organisms or registered tools. |
| Statistics and treatment of uncertainty | For a review with no analyses of its own: "Not relevant to this manuscript" or N/A. Otherwise answer from the Major items. |
| Images free from manipulation (gels, blots) | "Not applicable" when there are only schematics and plots. For gels and blots, look at them; raise any doubt with the user first, and only factually. |
| Tables and figures well designed and necessary | Yes when they are useful and the needed fixes are in the report; No when they are misleading or unnecessary. |
| References appropriate and up to date | No when the report raises citations that don't support their statements; otherwise Yes. |
| Comments to the editor (confidential) | Leave blank by default (§5). |
