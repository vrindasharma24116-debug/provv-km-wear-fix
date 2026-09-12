# What I checked, and what the agent got wrong

## What the agent got wrong

At first the agent used the wrong repository name — "provv" instead of "proov" — so the clone
failed and we had to correct it. That was a reminder not to trust a change just because the agent
says it is correct. I also checked the km-to-miles conversion myself because the old number
(1.609) looked suspicious — it turned out to be inverted, giving miles values that were more than
twice the real distance. The agent identified and fixed it, but I verified the new constant
(0.621371) independently before accepting the change.

## What I checked before I accepted its work

I checked that the wear calculation changed from `//` (floor division) to `/` (true division) and
confirmed that 14900 / 15000 gives about 99.3%, which is above the 80% threshold and correctly
flags the car. I also checked that the service interval was still 15000 km and the warning
threshold was still 80% — both in the code and in settings.cfg — to make sure the agent had not
accidentally changed the rules while fixing the bugs. Rather than only trusting the agent's
summary, I ran `pytest` and `python verify.py` myself and read the output line by line before
accepting the work as done.

## What the data actually said

The data showed that `km_since_service` was the strongest factor related to breakdowns
(correlation 0.40). Cars in the 10–15k km-since-service window broke down at a 43% rate,
compared to 3% for freshly-serviced cars. `avg_daily_km` and `load_factor` also showed some
relationship. `odometer_km` and `age_years` were not useful — the values were almost the same for
cars that broke down and cars that did not, so total mileage and age do not predict breakdowns in
this fleet. The obvious assumption that older, higher-mileage cars are the risky ones turned out
not to be supported by the data.
