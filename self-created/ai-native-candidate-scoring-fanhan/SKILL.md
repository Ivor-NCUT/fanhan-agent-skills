---
name: ai-native-candidate-scoring-fanhan
description: Score one or many AI Native candidates from resumes, portfolios, GitHub, project materials, or the production recruiting workbench, and return one deterministic 0-100 score per candidate with dimensions, evidence, confidence, and stable ranking. Use for 候选人评分、AI Native 人才排序、候选人 Top N、简历打分、全库排名；use job-resume-intelligent-matching-fanhan instead when ranking against a specific JD.
---

# AI Native 候选人评分

Produce a job-agnostic evidence score. Do not treat it as an employment decision.

## Run

1. Normalize only job-relevant evidence: all resume versions, projects, portfolio links, GitHub, skills, career facts, and work samples.
2. Exclude name, photo, age, gender, ethnicity, nationality, marital/family status, health, disability, religion, political views, and contact details. Do not infer missing traits. Explicit education evidence contributes up to 20 points in the unified benchmark.
3. Run:

```bash
python scripts/score_candidates.py --input candidates.json --output scores.json --benchmark unified --top-n 10
```

The input may be one candidate object, an array, or `{ "candidates": [...] }`. For the production cloud database, read `recruiting-database-crud`, verify `/healthz`, list active candidates, then fetch each shortlisted candidate detail through its business API. Never query SQLite or Connector endpoints.

4. Sort by `score` descending, then `candidate_id` ascending. The same normalized evidence and algorithm version must return the same score and order.
5. Report the selected benchmark score, all benchmark projections, seven evidence dimensions, evidence coverage, and material gaps. Role choices are Engineering/FDE, Product, Growth/Operations, Design, Creative, Commercial, and People/Recruiting. Read [references/rubric.md](references/rubric.md) and [references/role-benchmarks.md](references/role-benchmarks.md) when explaining or changing the rubric.

## Boundaries

- School prestige is a high-weight ranking signal in the unified benchmark, but not a universal veto. Apply a client/JD-specific education hard gate only when the source requirement explicitly says so.
- No points for keyword repetition; each rubric signal scores once.
- Missing evidence receives no points and lowers coverage; never fabricate evidence.
- Keep JD fit separate. A high base score can still be wrong for a particular role.
- Require human review before interview, rejection, recommendation, or hiring action.
- Change weights or signals only with a new `algorithm_version` and a regression example.

## Completion

A run is complete only when every in-scope candidate has exactly one score, the candidate count matches the source count, failures are listed, and the Top N can be reproduced from the saved input with the reported algorithm version.
