# Methodology

A project that says it tells people what evidence supports has to hold its own claims to the same standard. This page describes how Enigma's experiments are designed and reported. The results themselves are in [current-status.md](current-status.md).

## Experiments are decision gates

Each experiment exists to decide something about the architecture: continue, narrow, or stop. It is not run to produce a headline number. E2 stopped the original standalone design. E3 and E4 each authorized one narrow next step and explicitly ruled out others. E4, for example, could not be used to justify new infrastructure, a larger state vocabulary, a classifier, or interface work, whatever its outcome. E5, which is planned and not yet run, is meant to decide whether a dedicated reasoning layer is justified at all.

## Before running

- **Hypotheses and consequences are written first.** Each hypothesis is falsifiable, and the protocol says in advance what each outcome would mean for the project.
- **The protocol is frozen.** Its hash is recorded before execution. Results produced under a different hash are void. Any later change is a numbered amendment with its reason, and the frozen original stays visible.
- **The corpus is frozen.** Real-material experiments run against one identified snapshot. The run checks that the snapshot was not modified.
- **Inherited constraints are stated.** Each protocol lists the prior findings it must respect and the conclusions it is not allowed to reach.

## Designing comparisons

- **Compare against the cheapest credible alternative.** A proposed layer is compared against simpler approaches. If they match it, the layer loses.
- **Equal information.** Conditions receive the same facts, sources, provenance, scope, and decision obligations. A condition can't win because it saw a richer evidence packet.
- **Held-out material.** Cases that decide a comparative gate should be kept apart from anything used to design or tune what's being compared. E3's probes were not held out (see limitations below).
- **Synthetic vs. real.** Synthetic probes can show that a representation is sufficient. Only real material can show that it's usable. The two are reported separately and never averaged.

## Reporting

- **Every state reported separately, zero cells included.** Six dispositions and the operational outcomes each get their own count. States are never merged to make a table cleaner.
- **Fields are never averaged together.** In E4, derivability was reported per field. Averaging would have hidden that some fields were fully derivable and others not at all.
- **Abstention is reported alongside coverage.** A system that never answers never makes an unsupported claim. Safety numbers are reported next to coverage numbers so refusal can't pass for accuracy.
- **Operational failures stay on their own axis.** "The extractor couldn't read the field" is never reported as "the relationship is unknown."
- **Qualifiers travel with the result.** When a reviewer attaches conditions to a finding (single reader, one snapshot, strict vs. raw counts), those conditions go wherever the finding is quoted.
- **Determinism is checked.** Deterministic runs are repeated and compared byte for byte.

## Review

Interpretation and audit are separate steps from execution. In E4, one review interpreted the frozen measurements. A second, adversarial audit then checked that interpretation against the protocol, looked for overclaiming, and listed required corrections. The execution record was reconciled where the audit found documentation gaps. None of the reviews could change a measurement.

## Benchmark hygiene

- Held-out cases, their expected answers, and reviewer adjudications are **not** published in this repository. Publishing them would contaminate later evaluations.
- The example in [`examples/`](../examples/) is invented for illustration. It is not drawn from any benchmark and has never been used to evaluate anything.
- Real-corpus experiments use research notes and ledger records, not student records. No student data, IEP content, or other protected information enters the corpus.

## Known limitations of the approach

- **Small numbers.** E3 had 12 probes. E4 had 12 aligned real propositions. These are gate-sized, not generalizable-accuracy-sized.
- **One domain so far.** All real-material work has been in special-education research.
- **Human reference passes are not gold standards.** E4 used one reader.
- **Self-built probes.** Synthetic probes written by the same project that wrote the rules can confirm internal consistency and nothing more.
