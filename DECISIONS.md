# Decisions

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
Model outputs can be repeatable for some prompts and variable for others, so we cannot assume that rerunning a prompt will produce the same output.


