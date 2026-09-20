# Decisions
# TODO 5
cell                       distinct   chars   median s
------------------------------------------------------
closed_short|t00               1/12      10       0.17
closed_short|t10               1/12      10       0.17
open_short|t00                 1/12     194       1.07
open_short|t10                 5/12     198       1.07
open_list|t00                  1/12     189       1.10
open_list|t10                 11/12     178       1.14
open_reasoning|t00             1/12    1003       5.41
open_reasoning|t10            12/12     973       5.41


cell                       distinct   chars   median s
------------------------------------------------------
closed_short|t00               1/6      10       0.07
closed_short|t10               1/6      10       0.06
open_list|t00                  1/6     199       0.66
open_list|t10                  6/6     188       0.64



a. At temperature 0, all recorded cells produced 1 distinct answer out of 12, and my machine also produced 1 distinct answer out of 6 for the two cells I tested, so my results agree with the recording.

b. At temperature 1.0, closed_short still returned a single distinct answer because temperature changes the sampling distribution but does not guarantee different outputs when the model strongly favors the same completion.

c. An exact-string unit test would pass consistently on closed_short|t00, closed_short|t10, and open_list|t00, but would fail or be unreliable on open_short|t10, open_list|t10, and open_reasoning|t10. This shows that this system's output is not always repeatable, so tests cannot always rely on one exact generated string.



---------------------------------------------------------------------------------
# TODO 6
Model outputs can be repeatable for some prompts and variable for others, so we cannot assume that rerunning a prompt will produce the same output.


---------------------------------------------------------------------------------
# TODO 7
The first call took 2.65s, while the identical second call took only 0.06s. This shows that loading a model into memory adds significant latency. Since the system will use two different models, I would avoid switching between them inside a single request when possible and instead keep the required model loaded or structure the request to minimize model switching.

---------------------------------------------------------------------------------
# TODO 8
For 200 cases run every night for 14 weeks, the estimated cost is €3.28 on the small tier and €244.14 on the large tier. These are estimates, not measurements, based on the 2026-08-10 price list. I would use the small tier for nightly evaluation and the large tier before a release, because nightly evaluation runs frequently and the large-tier estimate is much higher, while a release check can justify the additional cost. I would not use the same tier for both because their cost and evaluation requirements are different.

