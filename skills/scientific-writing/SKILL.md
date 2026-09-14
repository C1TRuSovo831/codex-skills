---
name: scientific-writing
description: Draft, revise, or audit scientific manuscripts and reports with traceable evidence. Use for manuscript prose, references, declarations, displays, reporting coverage, or submission preparation.
license: MIT
compatibility: Requires Python 3.11+ only for optional dependency-free local CLIs; core guidance is platform-neutral. Bundled tools are offline and require no API keys.
metadata:
  version: "2.1"
  skill-author: K-Dense Inc.
---

# Scientific Writing

## Purpose

Produce clear scientific prose without inventing evidence or concealing uncertainty.
Keep drafting, evidence verification, and submission approval as separate stages.

The accountable human authors control scientific decisions and final approval. AI is
not an author, and generated fluency is never evidence [SW-S01, SW-S03].

## Non-negotiable safety rules

### Confidentiality

Do not send unpublished manuscripts, peer-review or editorial material, sensitive or
restricted data, PHI or other personal data, proprietary content, or source documents
to an external service without:

1. explicit authorization from a person or body empowered to grant it; and
2. a documented review of journal, institutional, funder, consent, ethics, contractual,
   legal, and data-use policy.

When authorization or policy is unclear, keep processing local and use only the minimum
metadata needed. De-identification requires expert review; removing obvious names is
not sufficient. See `references/authorship_ai_confidentiality.md`.

### No fabrication

Never invent or complete:

- citations, references, DOI, PMID, PMCID, ISBN, URLs, or quotations;
- results, data values, denominators, sample sizes, units, effect estimates,
  uncertainty, statistical tests, or significance claims;
- methods, materials, protocol details, software versions, analysis choices, or
  deviations;
- registrations, approvals, consent, ethics statements, participant details, or dates;
- authors, author order, CRediT roles, acknowledgments, or permissions;
- funding, sponsor roles, conflicts, data or code availability, or AI disclosures.

Use an explicit missing, unverified, or not-applicable state. Do not substitute plausible
boilerplate.

### Evidence binding

Every factual or numeric manuscript claim must map to verified evidence IDs. A human
verifier must open the source, confirm the proposition and locator, verify bibliographic
metadata, and record who verified it and when.

Search snippets, generated summaries, memory, and another work's bibliography may aid
discovery but do not verify a claim. See `references/evidence_workflow.md`.

### Scientific fidelity

- Preserve uncertainty and alternative explanations.
- Distinguish confirmatory, exploratory, descriptive, and post hoc work.
- Keep methods and results consistent.
- Reconcile units, denominators, sample sizes, populations, time points, and labels.
- Report negative, null, adverse, unexpected, failed, and inconclusive findings when
  they belong to the study record.
- State concrete limitations and bound generalizability.
- Do not convert association into causation or non-significance into equivalence.

## Route by the requested work

Apply the relevant workflow to the requested document or section. Mark missing
evidence and policy inputs unresolved while completing authorized local drafting
and audits; preserve the human verification and approval requirements below.

| Work | Read |
| --- | --- |
| New manuscript, substantive drafting, or a complete evidence audit | [Manuscript workflow](references/manuscript_workflow.md), including intake, evidence IDs, consistency checks, and completion gates |
| Source/claim verification or citation audit | [Evidence workflow](references/evidence_workflow.md); [CLI reference](references/cli_reference.md) for local validators |
| Writing or revising prose/section structure | [Writing principles](references/writing_principles.md) and, when appropriate, [IMRAD](references/imrad_structure.md) |
| Study-design reporting requirements or coverage | [Reporting guidelines](references/reporting_guidelines.md), then current official guidance and target-journal instructions |
| Authorship, AI disclosure, restricted content, or external processing | [Authorship, AI, and confidentiality](references/authorship_ai_confidentiality.md) |
| Ethics, registration, funding, conflicts, or data/code availability statements | [Research integrity and open science](references/research_integrity_open_science.md) |
| Retained figures or tables | [Figures and tables](references/figures_tables.md), including provenance, reconciliation, and manual review at final size |
| Reviewer response, final formatting, journal policy, or submission preparation | [Revision and submission](references/revision_submission.md) |

Use only the relevant references; an editorial change does not require creating an
unrelated manuscript workspace. Preserve evidence IDs during drafting and reconcile
affected registries before prose when facts change. Re-run affected audits.

## Completion and approval

Local scripts are deterministic, bounded, dependency-free, and network-free. They
check structure and consistency; they do not verify source support, certify guideline
adherence, or authorize submission. Use [CLI reference](references/cli_reference.md)
for exact commands and [the workflow inventory](references/manuscript_workflow.md#bundled-files)
for scaffold assets and supporting resources.

Only accountable humans may:

- resolve scientific ambiguities;
- approve author order and declarations;
- approve external disclosure or transfer;
- set `submission_ready` to true;
- remove the draft banner;
- authorize submission.

Formatting cannot convert an incomplete evidence record into a submission-ready paper.
Keep unresolved claims, policies, and approvals explicit in the deliverable. Do not ask
for restricted source material if metadata or a local user-run audit is sufficient.

Policy evidence labels such as `SW-S01` resolve in the [source ledger](references/source_ledger.md).

When this skill materially contributes to a manuscript, report, presentation, or code
release, follow [the current-version citation procedure](references/revision_submission.md#citing-scientific-agent-skills).
