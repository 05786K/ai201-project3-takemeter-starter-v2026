# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---
<!-- Added five criterias below -->
These five criteria define what “working” means for the four-label classifier.

1. **Overall accuracy:** The classifier must achieve at least **0.70 accuracy on each of the three seeds**.

   **Why this target:** My labels aren't evenly split — `question`, `personal_experience`, and `opinion` each make up about 32% of the data, with `analysis` at only 3%. That means a baseline that always guesses one of the three big labels already clears roughly 32%, and one that can tell `analysis`-shaped posts apart and guesses randomly among the rest lands closer to 35%. 0.70 is roughly double that realistic baseline — a bar that actually means something, not a coin flip dressed up as a target. Requiring it on all three seeds, rather than just one favorable split, guards against a result that only looks good because of which posts happened to land in test.

2. **Per-label performance:** The `question`, `personal_experience`, and `opinion` labels must each achieve an **F1 score of at least 0.70 on all three seeds**. For `analysis`, I'm tracking F1 but not holding it to the same per-seed bar: with only 6 total examples, each seed's test split contains roughly **one** `analysis` post, so a single seed's F1 is either 0.0 or 1.0 — essentially a coin flip, not a measurement. Instead, I require the `analysis` F1s **averaged across all three seeds to be at least 0.40** — still thin, but less purely luck-based than any single seed alone.

   **Why this target:** The first three labels have roughly 65 examples each (≈10 in test per seed), enough for F1 to mean something at 0.70. `analysis` doesn't have that luxury — the honest move is to say so and measure it differently, not apply the same bar and hope.

3. **Labeling consistency:** On a separate review of **30 randomly selected posts**, I must agree with my original labels on at least **90%** of them.

   **Why this target:** The taxonomy includes potentially overlapping labels. For example, a post can ask a question while also explaining a view; this check helps reveal whether the label definitions and boundary rule are clear enough to apply consistently.

4. **Boundary-case performance:** The classifier must correctly classify at least **75% of 20 preselected borderline posts on each seed**.

   **Why this target:** Borderline examples are especially useful for this taxonomy because the distinction between asking for input (`question`), supporting a conclusion (`analysis`), and expressing a judgment (`opinion`) can be subtle. A 75% target is demanding without requiring near-perfect performance on the hardest examples.

5. **Confidence:** Among the test predictions on each seed, **accuracy on the most-confident third of predictions must be at least 15 percentage points higher than accuracy on the least-confident third**.

   **Why this target:** This is exactly what the notebook's `confidence_report` already computes (`accuracy_most_confident_third` / `accuracy_least_confident_third`), so it's measurable with no extra code. A gap of zero would mean the model's confidence carries no signal at all; I didn't pick something larger because several of my labels sit on genuinely ambiguous boundaries (the `question`/`personal_experience` boundary especially), so I'd expect real, defensible uncertainty on some correct guesses too — a model that's never unsure about the hard cases would worry me more than reassure me.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
