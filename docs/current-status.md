# Current status

*Last updated: September 2026.*

Short version: the evidence infrastructure (Palace) is implemented and tested. The reasoning layer (Enigma) is experimental. It behaves correctly on synthetic probes and refuses to guess on real material, but it can't yet get the facts it needs from real literature without a human. Whether it adds value over simpler approaches hasn't been tested. That comparison, E5, is planned. No E5 results exist.

| Label | Meaning |
| --- | --- |
| **Implemented** | Code exists |
| **Tested** | Automated tests or a frozen experiment exercise it |
| **Experimental** | Exists only as experiment code under a frozen protocol |
| **Planned** | Intended; may have a written design, but no code |

## What exists

| Area | Status | Notes |
| --- | --- | --- |
| Canonical record with version control | Implemented | Plain-text notes; an accepted revision is authoritative |
| Claim-evidence ledger | Implemented, tested | Sources, hashed evidence anchors, claims, typed relations |
| Bibliographic integrity checks | Implemented, tested | Report-only; checks identity, not quality |
| Literature acquisition | Implemented, tested | Awaiting a second independent review before acceptance |
| Evidence graph | Implemented, tested | Explicit links only |
| Retrieval with line-level attribution | Implemented, tested | Candidate recall only |
| Evidence-state and provenance contract | Planned (as runtime) | Semantics fixed in a frozen design document; 24 invariants; no runtime |
| Enigma precedence rules | Experimental, tested | E3/E4 experiment code |
| Automatic fact encoding from real literature | Experimental; not achieved | See E4 |
| E5 comparison | Planned | Not run; no results |
| Transition history, gap significance, user interface | Planned | Not started |
| Public source code | Not published | Implementation lives in a private research repository |

## Experimental record

From E4 on, experiments run against a protocol that is hashed and frozen before any results exist. E4's interpretation was reviewed, then audited, separately from its execution.

### E2: standalone Enigma, stopped and repositioned

The earlier design treated Enigma as a standalone classifier with a larger vocabulary of evidence states. A kill-or-continue review (E2) stopped that design. Its findings:

1. Retrieval was not the failure. The critical evidence was surfaced.
2. The facts that decided each case lived in free text. No deterministic resolver could honestly be built from the frozen schema.
3. The full standalone pipeline showed no state-label advantage over a frontier language model given the same evidence and provenance directly.
4. The benefit of provenance didn't depend on Enigma-specific rules.

That stopped the standalone design, not the idea. Enigma was repositioned as a bounded reasoning layer inside the Palace architecture: six states instead of the larger vocabulary, deterministic rules over explicit facts, and every step justified against the direct-model baseline.

### E3: representation feasibility (synthetic)

**Question.** If the deciding facts are made explicit, can a small set of typed fields and a fixed rule order produce the right state and a complete audit trail?

**Design.** 12 synthetic, hand-authored probes, three each for uncertainty, absence, conflict, and supersession. Two conditions over identical evidence: a baseline with evidence direction and locators only, and the same plus seven typed fields.

**Result.**

| Condition | Correct state | Audit obligations present |
| --- | ---: | ---: |
| Baseline | 5 / 12 | 12 / 96 |
| With typed fields and precedence rules | 12 / 12 | 96 / 96 |

No probe got worse. Re-running produces byte-identical output.

**What it does and doesn't show.** The typed representation is sufficient to express these distinctions, and the rules apply them consistently. The probes and the rules came out of the same project, so 12/12 isn't an accuracy figure. It establishes nothing about real literature, retrieval, human usefulness, or calibration.

### E4: derivability on real material

**Question.** On a real corpus (special-education research notes), can the seven typed facts actually be derived from the records? When they can't, does the layer abstain instead of inventing a state?

**Design.** A frozen snapshot of the real corpus. A census of 20 candidate propositions, 12 of which had enough typed structure to enter the automatic path. Three conditions: the E3 baseline, a single human-confirmed reference pass working from source locators, and the deterministic extractor.

**Result.**

- The extractor derived **none** of investigation status, adequacy, conflict, or supersession for any of the 12 admitted propositions.
- It abstained on all 12 (`NOT_ASSESSABLE`). Across 80 underivable field occurrences, it never produced a substantive state: **zero fabricated dispositions.**
- The human reference pass recovered many of the same facts from the same material. For the 12 aligned propositions: investigation status in 11, conflict status in 10, adequacy in 8, supersession in 3.
- The baseline, given the same records, marked 4 propositions as supported on the strength of a typed `supports` link alone. That is precisely the shortcut the architecture forbids.

**Interpretation, with its qualifiers.** The pre-registered outcome "representation debt confirmed (expected)" was selected. The reviewers attached conditions that carry forward with it. This is one corpus, one snapshot, 12 aligned propositions, and a single reader, not a gold standard. Some recovered "conflict" statements are really qualifications, so a strict count of the gap is lower than the raw one. The finding is an inventory of facts that exist only in prose. It is not a set of resolved states. E4 shows no reasoning capability and no novelty, and it does not reopen the standalone design.

**Why it matters.** It locates the bottleneck. The rules aren't the hard part. Getting reliable, explicit facts out of real literature is. E4 also shows that neither E3 nor E4 can say whether Enigma beats simpler approaches. That needs a stronger controlled comparison.

### E5: planned decision gate

**Purpose.** A controlled comparison of simpler approaches against the Enigma reasoning approach. It answers the question E3 and E4 left open: does Enigma add enough over simpler alternatives to justify a separate reasoning layer?

**Decision it informs.** If simpler approaches perform as well, the case for Enigma as a separate layer fails. The evidence-state vocabulary and provenance model would still stand.

**Status.** Planned. E5 has not been run. **No E5 results exist**, and nothing on this page depends on E5 results. No E5 design details are published here, and no held-out evaluation material will be.

## What is not being claimed

- That Enigma is more accurate than a language model. E2 found it wasn't, in its earlier form. E5 is planned to test the current form.
- That Enigma works on real literature end to end. It doesn't yet. Fact encoding is the gap.
- That the synthetic E3 score is an accuracy figure.
- That any of this is ready for use in decisions about individual students.

## Open decisions

- License (none chosen yet).
- Whether and when to publish a reference implementation of the reasoning layer.
