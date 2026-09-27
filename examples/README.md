# Example: a synthetic evidence set

> [!IMPORTANT]
> **Everything in this folder is invented.** "Paired Rehearsal Routine" is a fictional intervention. The studies, samples, numbers, and findings are made up. The output was written by hand to show the shape of an Enigma result. No released implementation produced it. Don't cite any of this as evidence about any real practice.

## The setup

Question: *Does the Paired Rehearsal Routine improve reading outcomes for students with mild intellectual disability in grades 3–5?*

[`example_input.json`](example_input.json) contains eight synthetic reports. They were chosen to trip the usual failure points:

| Report | Trap |
| --- | --- |
| S-01, S-08 | Positive, but the students have learning disabilities, not intellectual disability (**population mismatch**) |
| S-02 | Positive, direct, n = 4 |
| S-03 | The same four students written up again (**duplicate lineage**, not replication) |
| S-04 | Randomized, direct, finds no difference (**conflict** with S-02) |
| S-05 → S-06 | A positive comprehension result, later **corrected** to a non-significant, imprecise one |
| S-07 | Says "improved reading" but measured teacher-rated engagement (**construct mismatch**) |

The question is split into five **scoped propositions**, because "does it work" isn't one question. Each proposition carries the typed facts Enigma needs: investigation status, adequacy criterion, conflict record, supersession records, and each evidence item's relation (`SUPPORTS`, `AFFIRMATIVE_NEGATIVE`, `QUALIFIES`). In this example those facts are marked as recorded by a human annotator. That matches the project today: fact encoding is done by people (see [current status](../docs/current-status.md)).

## The result

[`example_output.json`](example_output.json):

| Proposition | Disposition | Deciding rule |
| --- | --- | --- |
| P-1 fluency, mild ID | `CONTRADICTORY_EVIDENCE` | explicit conflict |
| P-2 comprehension, mild ID | `MISSING_EVIDENCE` | supersession removes S-05; adequacy not met |
| P-3 maintenance, mild ID | `MISSING_EVIDENCE` | adequacy not met: nobody measured it |
| P-4 fluency, learning disability | `SUPPORTED_RELATIONSHIP` | scoped support |
| P-5 fluency, AAC users | `UNEXPLORED_RELATIONSHIP` | investigation not started |

Things worth looking at in the output:

- **P-1** keeps both sides. S-03 is listed but flagged as the same study as S-02. S-01 and S-07 appear under `qualifying_not_counted` with the reason, not silently dropped.
- **P-2** shows why "not significant" isn't `NO_RELATIONSHIP`. S-05 moves to `historical_evidence`, because a correction explicitly replaces it, not because it's older.
- **P-3 vs. P-5** is the difference between *looked and found nothing* and *hasn't been looked at*.
- **P-4** is supported, but only for its own population. The `question_view` refuses to carry that over to the ID question.
- Every result has a `precedence_trace` listing the rules checked in order and the one that fired.
- The top-level `provenance` block states that no model was involved and nothing from outside the declared corpus was used.

## Schema

`enigma-example/0.1` is an illustrative format for this example. It is not a stable interface.
