# Decisions

# Week 1: the stack, the first call, and what it costs

## Week 1

**Run conditions.** Everything below was produced on:

- machine: [make: ASUS , chip: 11th Gen Intel(R) Core(TM) i5-11400F @ 2.60GHz (2.59 GHz), RAM: 16,0 GB]
- model:[NAME                       ID              SIZE      MODIFIED
        qwen3-vl:4b                1343d82ebee3    3.3 GB    23 hours ago
        qwen2.5:7b                 845dbda0ea48    4.7 GB    23 hours ago
        nomic-embed-text:latest    0a109f422b47    274 MB    25 hours ago
        qwen3:4b-instruct          0edcdef34593    2.5 GB    25 hours ago]
- served by: Ollama, one request at a time, locally
- date: [2026-09-20]

Every number in this file is meaningless without those four lines, so they
are stated once here and referred to rather than repeated.

### 1. Machine and model set

I am running the required plus optional model set.


### 2. The first call

| | |
| finish reason | stop |
| prompt tokens | 24 |
| completion tokens | 45 |
| elapsed | 3.71 s |

One sentence on the finish reason: what my program would do differently if
it came back as a truncation rather than a normal stop.

[My program would treat stop as a normal deliberate ending. If the finish reason indicated truncation, it would treat the response as incomplete rather than a successful completion.]

### 3. Variance

| cell | distinct (recording) | distinct (mine) | median latency |
| closed_short, t=0.0 | 1/12 | 1/6 | 0.07 s|
| closed_short, t=1.0 | 1/12 | 1/6 | 0.06 s|
| open_list, t=0.0 | 1/12 | 1/6 | 0.66s |
| open_list, t=1.0 | 11/12 | 6/6 | 0.64s |

Which cell still returns a single answer at temperature 1.0, and why that
one:

[At temperature 1.0, closed_short still returned a single distinct answer
because temperature changes the sampling distribution but does not guarantee
different outputs when the model strongly favors the same completion.]

Which cells a test asserting exact string equality would pass on, and what
that tells me about testing this system:

[An exact-string test would pass on closed_short|t00, closed_short|t10, and open_list|t00, but would fail on open_short|t10, open_list|t10, and open_reasoning|t10. This shows that this system's output is not always repeatable, so tests cannot always rely on one exact generated string.]

**The sentence that carries into week 10.** [Model outputs can be repeatable
for some prompts and variable for others, so we cannot assume that rerunning
a prompt will produce the same output.]

### 4. The cold start

- cold call: [ 2.65 ] s
- warm call: [ 0.06 ] s
- ratio: [ 44.17x ]

What this implies for a system that uses more than one model, and what I
will do about it:

[The first call took 2.65s, while the identical second call took only 0.06s.
This shows that loading a model into memory adds significant latency. Since
the system will use two different models, I would avoid switching between
them inside a single request when possible and instead keep the required model
loaded or structure the request to minimize model switching.]

### 5. Cost, estimated

A 200-case golden set, at the token cost of my long case:

| | one run | nightly for the semester |
| small tier | 0.0335€ | 3.28€ |
| large tier | 2.4912€ | 244.14€ |

Estimates against the price list dated [ 2026-08-10 ], not
measurements. Running locally, my actual monetary cost was zero.

Which tier I would run nightly, which I would run before a release, and why
not the same one for both:

[I would use the small tier for nightly evaluation and the large tier before
a release, because nightly evaluation runs frequently and the large tier
estimate is much higher, while a release check can justify the additional
cost. I would not use the same tier for both because their cost and
evaluation requirements are different.]


# Week 2: a structured-output extractor, measured
## Week 2

**Run conditions.** model: [ 
aNAME                       ID              SIZE      MODIFIED
qwen3-vl:4b                1343d82ebee3    3.3 GB    4 days ago
qwen2.5:7b                 845dbda0ea48    4.7 GB    4 days ago
nomic-embed-text:latest    0a109f422b47    274 MB    4 days ago
qwen3:4b-instruct          0edcdef34593    2.5 GB    4 days ago] | temperature: 0.0 | prompt version: [ week02-zero-shot-v1 ] |
served locally | date: [ 2026-09-24 ] | scored on: [the recording / my own machine]

### 1. The output contract

The conventions I chose, and why:

- due_date, when the message states no date: [ None ]
- due_date, when the message states only a relative expression: [ None ]
- quote, and what "verbatim" means in my scorer: [ quote must be a short, exact substring copied from the input message, do not paraphrase, normalize, or alter wording]
- what my scorer does with a record that failed validation: [ The record is rejected/marked as a validation failure and is not scored as a valid prediction.]

[The last one matters because a validation failure counts as wrong for every field, preventing the scorer from hiding failures and making the model appear better as it gets worse.]

### 2. Zero-shot, per field

| field | correct | of |
| category | 7 | 10 |
| urgency | 10 | 10 |
| due_date | 6 | 10 |
| quote | 10 | 10 |
| invalid records | 0 | 10 |

My prediction, written before block 3: examples will help most on [ due_date ]
because [ the examples show dates in ISO format ].

### 3. Few-shot

Examples chosen, and the job each one does:

| example | why it is in the block | field it should move |
| EX-03 | defines the boundary between hardware and facilities and also demonstrates a German message with an ISO-formatted date.| category, due_date |
| EX-05 | demonstrates a French message and a clearly stated calendar deadline, showing how a non-English message with a specific date should be handled.| due_date |
| EX-06 | demonstrates facilities issue with no stated calendar date, reinforcing that the due date should be None when no specific date is given. | due_date |

| field | zero-shot | few-shot | move |
| category | 7/10 | 6/10 | -1 |
| urgency | 10/10 | 10/10 | +0 |
| due_date | 6/10 | 8/10 | +2 |
| quote | 10/10 | 10/10 | +0 |

### 4. What got worse

[Category got worse, dropping from 7/10 in zero-shot to 6/10 in few-shot.]

### 5. What the examples cost

- extra input tokens per call: [ 200 ]
- per thousand calls: [ 200000 ]
- estimated euros per thousand calls on the small tier: [ 200,000 / 1,000,000 × 0.20€ = 0.04€ ], against the price list dated [ 2026-08-10 ]. Estimate, not a measurement.

### 6. Ship it or not

[I would keep the few-shot variant because it improved due_date from 6/10 to 8/10, while urgency and quote stayed at 10/10. However, I would not be confident that it is better overall because category dropped from 7/10 to 6/10, and ten records is too small of a sample. I would change my mind after testing on a larger set of records and seeing whether the improvements hold consistently.]

### Sensitivity variant

Variant assigned: [ reordered ]. What I changed: [ the order of the examples ]. What moved: [ nothing ].

[nothing moved]

### The gold set

Ten cases written to `artifacts/goldset.json`, tagged by language.

One thing my scorer cannot currently detect: My scorer cannot extract the correct date itself. It only checks whether the date extracted by the model matches the expected date.
