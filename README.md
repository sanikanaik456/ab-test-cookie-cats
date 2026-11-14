\# A/B test analysis: moving the first gate in Cookie Cats



Does moving the first gate (a forced wait) in a mobile game from level 30 to level 40 change how many players come back? This project analyses a public A/B test and reports what the data can and cannot show.



\## Data

The public "Cookie Cats" A/B test dataset: 90,189 players, randomly shown the first gate at level 30 (gate\_30) or level 40 (gate\_40). Columns: user id, version, number of game rounds played in the first 14 days, and whether the player came back 1 day and 7 days after installing. The data is not included here. To download it:



&#x20;   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ryanschaub/Mobile-Games-A-B-Testing-with-Cookie-Cats/master/cookie\_cats.csv" -OutFile cookie\_cats.csv



\## Data checks

No missing values and no duplicate user ids. One player has 49,854 rounds, far above everyone else, so I report medians and use a rank test for game rounds. 3,994 players have 0 rounds.



\*\*Warning: the two groups are not the same size\*\* (44,700 and 45,489). A chi-square test for a 50/50 split gives p = 0.009, which would be unlikely by chance. This can mean the assignment of players had a problem, so the results below should be checked before anyone acts on them.



\## Methods

\- Retention (1 day and 7 days): difference in proportions with a 95% confidence interval and a chi-square test.

\- Game rounds: medians and a Mann-Whitney U test, because the metric is very skewed.

\- A bootstrap check (2,000 resamples) for 7-day retention.

\- Three metrics were tested, so I compare p-values with a Bonferroni threshold of 0.0167 (0.05 divided by 3).



\## Results



| Metric | gate\_30 | gate\_40 | Difference (40 minus 30) | p-value | Significant after adjustment |

|---|---|---|---|---|---|

| 1-day retention | 44.82% | 44.23% | -0.59 points (95% CI -1.24 to +0.06) | 0.074 | No |

| 7-day retention | 19.02% | 18.20% | -0.82 points (95% CI -1.33 to -0.31) | 0.0016 | Yes |

| Game rounds (median) | 17 | 16 | n/a | 0.050 | No |



In 99.9% of bootstrap resamples, gate\_40 had lower 7-day retention than gate\_30.



\## What I found

Moving the gate to level 40 lowered 7-day retention by about 0.8 percentage points (roughly 4% of the players who would otherwise return). On this metric, keeping the gate at level 30 looks better. The effect is small, and the other two metrics show no clear difference.



\## Limits

\- The unequal group sizes are a warning about how players were assigned. I could not check why.

\- I only have retention at 1 and 7 days and game rounds. There is no revenue or longer-term data, so this does not show which version is better for the business overall.

\- The effect is small, and a practical decision would need the cost of the change as well.

\- I chose the metrics that came with the dataset. I did not plan them in advance.



\## Run it

&#x20;   pip install -r requirements.txt

&#x20;   python ab\_analysis.py



Data source: the Cookie Cats mobile game A/B test dataset (public).

