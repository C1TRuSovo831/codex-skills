# Calibration and observability

Read this when fitting geometry/mounting, diagnosing implausible articulated motion despite low residuals, or deciding whether a calibration transfers to a new session. Select the checks relevant to the suspected ambiguity; do not turn every adapter edit into a full calibration study.

## Identify what the observations determine

Write down observed quantities, latent joint states, shared geometry/extrinsics, fixed parameters, priors and their units/frames. Identify the coordinate reference that removes arbitrary global freedoms. A low sensor residual may leave internal joint allocation or mounting/length combinations ambiguous.

Use diagnostic evidence such as parameter sensitivity, appropriately scaled Jacobian rank, multiple admissible fits, held-out motion and contact with parameter bounds. Similar residuals with different geometry or internal motion indicate weak identification; one optimizer converging repeatedly is not proof of uniqueness. Bounds and priors can select one explanation without establishing anatomical or mechanical truth.

Check whether the recorded motions excite the parameters at issue. A single-axis motion, for example, may leave mounting components along that axis unobservable; diagnose the actual measurement model before prescribing more free parameters. Inspect implausible lengths, near-zero segments, shared-base compensation and multiple parameters stuck at bounds as hypotheses, not automatic root causes.

Separate a coordinate/adapter error, wrong kinematic structure, insufficient excitation, inappropriate prior and local solver failure. Use a controlled comparison that changes the relevant assumption while keeping observation provenance and protected behavior clear. If changing the kinematic chain or frame convention, refit or transform dependent parameters consistently before judging the new model; evaluating it with incompatible old parameters confounds the comparison.

## Use independent evaluation appropriate to the claim

- Preserve raw observations, original artifacts and the association with operator, mounting, side/limb and session. Write candidates separately rather than silently updating personal geometry or the active model.
- Distinguish measured truth from pose instructions, inferred labels and priors. A requested “straight” pose is not an independent joint-angle measurement. A label or axis summary derived from a recording is not a second independent observation of that same recording.
- Choose evaluation splits for the desired claim. Adjacent frames or halves of one hold remain strongly related. Hold out distinct motions, trials, remountings or people when claiming those forms of generalization. Record when data previously used for validation becomes fitting data.
- Evaluate sensor-space residuals and the task behavior that motivated calibration: functional range, joint allocation, shape, continuity, mapping quality and protected contact/pose tasks as applicable. Improvement in the fitting objective alone is insufficient.
- Separate model plausibility from independent accuracy and downstream utility. An unmeasured parameter can remain uncertain even if a task improves; state that narrower result.

## Decide and retain provenance

Check required identity, format, finite values, dimensions, model compatibility and nominal bounds. Treat residuals and confidence according to the existing contract; do not invent runtime rejection thresholds to conceal a model problem.

Record the model/configuration, input identities, assumptions, fitting and evaluation split, intended acceptance criteria, actual tradeoffs and evidence location. Keep rejected candidates and failure evidence according to the project's retention policy. Retry a rejected mechanism only under the project's retry rules with a concrete changed condition or new evidence.

Geometric calibration, source-to-target mapping preferences and control response parameters solve different problems. Keep their ownership explicit; changing an online output offset is task compensation, not proof that the underlying geometry was identified.
