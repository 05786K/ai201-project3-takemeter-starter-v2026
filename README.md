# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts self-text posts from r/bayarea, the San Francisco Bay Area subreddit, into four categories based on the post's primary purpose rather than its topic. `question` posts ask the community for information or advice; `personal_experience` posts recount something the author personally went through; `analysis` posts argue a conclusion from specific, checkable evidence; `opinion` posts state a judgment without backing it up. Two posts about the exact same topic — say, the cost of living — can land in any of the four, depending on whether the author is asking, narrating, arguing, or just venting.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `question`

**Definition:** The post's primary purpose is to ask readers for information, advice, or opinions.

**Example 1:**
> "Will the Bay Area ever have some kind of rail transit along the major Freeways?"

**Example 2:**
> "Is 85k a livable salary for North Oakland?"

### `personal_experience`

**Definition:** The post's primary purpose is to describe a specific situation or experience the author personally went through.

**Example 1:**
> "I have 'tech envy' as a non-tech worker."

**Example 2:**
> "My first-hand experience with Bay Area tech snobbery."

### `analysis`

**Definition:** The post's primary purpose is to explain or defend a conclusion using specific evidence or a clear chain of reasoning.

**Example 1:**
> "California's 'affordable housing' tax break is letting investors charge market-rate rents while avoiding property taxes."

**Example 2:**
> "PGE rates are getting higher regardless of consumption? How they are getting away with it?"

### `opinion`

**Definition:** The post's primary purpose is to express a judgment or position without providing specific supporting evidence or developing a clear argument.

**Example 1:**
> "Bay Area FB Marketplace is full of backyard breeders — stop buying from them!"

**Example 2:**
> "[Rant/Vent] Quit your bullshit with bringing your pets everywhere. Quit the fake 'emotional support animal' quasi-service online certifications."

### The Hardest Boundary

**Which two labels:** `question` and `personal_experience`

**The decision rule I used every time:**
Remove the explicit ask from the post. If a complete, stand-alone account of what happened to the author is left over, I label it `personal_experience` — the ask is just a hook inviting reaction. If removing the ask leaves nothing but a thin fact pattern that only exists to make the ask answerable, I label it `question`.

> *"FasTrak hasn't billed me in 5+ months... should I be worried about a huge bill later?"* → `question`. Strip the ask and there's no story left, just a billing detail.
>
> *"Has anyone else felt a big difference between living in New York and the Bay Area?"* → `personal_experience`. Two full paragraphs of the author's own NY timeline stand on their own; the question is a hook, not the point.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** r/bayarea, using Reddit's own `self:true` search (text posts only) across several sort orders (New, Hot, Top all-time, Comment count). Collected by hand — Reddit's current anti-scraping measures block automated collection, confirmed by testing.

**How I labelled them:** Mixed. About 30 posts were labelled cold. Most were pre-labelled from the title and then corrected (or confirmed) after reading the full post — several flipped on that second read. Disclosed per-row in the `note` column (`cold` vs `pre-label`).

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| personal_experience | 68 | 33.8% |
| opinion | 65 | 32.3% |
| question | 62 | 30.8% |
| analysis | 6 | 3.0% |
| **Total** | 201 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "Lets be honest... how am I suppose to survive on 'Entry Level jobs' in the bay area?" — walks through real rent and take-home numbers toward an implicit conclusion that entry-level pay doesn't work here.
>
> *Could have been:* `question` or `analysis`.
>
> *I chose `question`, because:* it reads as rhetorical venting, not an explicit ask — but the numbers are doing the same load-bearing work as my `analysis` example. Close call.

**2.**
> *The post:* "To the idiot who drives at 130+ mph on 280 south... F*** You!" — a direct-address rant at one specific car, encountered three times.
>
> *Could have been:* `personal_experience` or `opinion`.
>
> *I chose `personal_experience`, because:* it stays narrow — one car, three sightings — instead of generalizing to a category of drivers, unlike my Tesla-drivers `opinion` example which makes the same rant shape into a sweeping claim.

**3.**
> *The post:* "San Jose has carried the Bay Area during the World Cup and emerged the biggest Winner" — cites a specific $600M economic estimate.
>
> *Could have been:* `opinion` or `analysis`.
>
> *I chose `opinion`, because:* the number is decoration on a celebratory, boosterish post, not the engine of an argument — the fact isn't load-bearing.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased` (the notebook default).

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, seed 42 — all defaults.

**Anything I changed from the defaults, and why:** Nothing yet. I ran Section 5 once with the defaults to get a real baseline reading before deciding whether anything was worth tuning, rather than changing settings before seeing how the defaults actually behaved.

**Split sizes:** train 139 / val 31 / test 31 (201 total). Test, per label: `question` 10, `personal_experience` 10, `opinion` 10, `analysis` 1. `analysis` has only 1 example in test — far below the ~8 floor — so its F1 (0.0 on this seed) is close to a coin flip and will swing hard across the three seeds; that's expected, not a bug.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Had Claude triage a large batch of r/bayarea post titles into my four labels before I'd read any of the bodies, to speed up finding candidates.
- *What came back:* Confident title-only guesses, several of which were wrong — e.g. "A Warning on E-Bikes" was guessed `opinion` from the title, but the full post turned out to be a first-hand account of an e-bike collision the author personally witnessed.
- *What I changed:* Read the full text of every flagged post myself and corrected the label before it went into `labels.csv`. Several flipped this way, including a post that looked like `analysis` from its title (specific numbers) but turned out to just be a link to a news article with no argument of its own.

**Moment 2**

- *What I asked for:* Asked Claude to find real posts that would stress-test my original `question`/`analysis` decision rule.
- *What came back:* It surfaced a different, more common boundary I was actually hitting — `question` vs. `personal_experience` — and proposed a "remove the ask" decision rule, checked against real examples from my data.
- *What I changed:* Replaced my original hardest-boundary writeup with that rule, since the evidence showed it was the boundary I ran into far more often than the one I'd first picked.

**Pre-labelling disclosure:** Most of my 201 posts were pre-labelled by AI from the title alone as a fast first pass, then I read the full post myself and corrected the label before it went into the dataset — marked `pre-label` vs. `cold` in the `note` column. This caught several wrong guesses before they ever reached the dataset, and a full re-read afterward still found three more mislabels that had slipped through.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
