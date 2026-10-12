# Bounded behavior evaluation

Use these cases when maintaining the robotics, IK, retargeting or gain skills. They exercise task selection and technical decisions without operating hardware.

Give an independent evaluator the candidate skills and [case inputs](fixtures/behavior-cases.json). Treat each case as a separate user request, complete the requested analysis, and record the actual answer and skill/reference choices. Supply only the relevant instructions and fictional artifacts; withhold the [grading rubric](behavior-rubric.json), old answers and suspected defects. Limit tools to reading the supplied skills/cases and writing an assigned result file in an isolated evaluation directory; no project writes, device commands or service operations.

After the pass, grade each answer against the rubric and retain the actual response with the candidate content hashes. If a decision fails, retain its evidence, make a justified correction and repeat only affected cases. Results describe a bounded behavioral sample, not a guarantee for every future task.

Frontmatter, UI metadata and local-link validation remain separate structural checks. Parsing these fixtures or checking that their IDs exist does not run the behavioral evaluation.
