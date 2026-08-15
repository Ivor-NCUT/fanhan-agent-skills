# Role benchmarks v3.1

Every benchmark is deterministic. Unified uses the ten evidence dimensions directly. Each role benchmark combines an 80-point weighted evidence score with a 20-point role-fit evidence score. All roles retain the Five Good signals, then change the emphasis of AI-native, shipped, ownership and customer evidence.

Unified weights are: company 10, school 15, core business 10, performance 10, stability 10, AI-native 12, shipped 10, ownership 8, learning 5 and customer/business 10. Role weights live in the scorer as versioned executable policy and always sum to 100 before the 80/20 role-fit mix.

The role-fit component looks for direct role evidence. FDE belongs to engineering and adds customer-site implementation and solution delivery evidence. Design focuses on user experience, interaction, visual systems and craft; creative focuses on original concepts, narrative, content, art and AI-generated media. Growth / operations remains one benchmark. Commercial covers sales, BD, customer success and commercialization without FDE. Exact JD must-haves remain a separate matching gate.

## Engineering interview benchmark

The engineering benchmark is calibrated with [AI-Native 工程师招聘面试官手册](https://vorojar.github.io/ai-native-hiring-guide/). Resume scoring is only pre-screen evidence. In interviews, use the guide's two tracks:

- Builder: Issues quality 20%, solution review 10%, AI driving 25%, product instinct 25%, prototype driving 20%.
- Reviewer: Issues quality 15%, solution review 20%, AI driving 25%, PR review 20%, systems thinking and decisions 20%.
- Interview threshold: 35/50 with no veto; 30-34 hold; below 30 fail.

Do not infer interview-only behavior from resume keywords. Verify AI driving live, inspect actual Issues/PRs/work samples, and record concrete evidence.

## Client/JD overrides

Role benchmarks are defaults. Exact client hard gates override ranking: for example, `本科 985` must be checked against the undergraduate institution rather than replaced by a prestigious master's degree. Keep such gates in the JD-specific matching stage, not in the universal benchmark.
