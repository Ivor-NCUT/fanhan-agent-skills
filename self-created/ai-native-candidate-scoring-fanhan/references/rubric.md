# Rubric v3

Source: the private Feishu Base `AI 招聘客户会议妙记库`, table `招聘会议妙记`, scanned 2026-01-01 through 2026-08-13. The first calibration set contained 98 recruiting-related meetings, including 11 explicit client-demand meetings and 89 records with extracted requirement or evaluation quotes.

The recurring client signals were abstracted instead of copying private transcripts into the Skill. A second calibration pass read all 2,145 messages from the 38 chats carrying the `招聘客户` Feishu tag: 64 education-related messages appeared across 18 chats, including explicit client hard gates such as undergraduate 985 and repeated rejection feedback about school level. Education therefore remains a top-tier ranking dimension.

The v3 calibration adds the headhunter industry's traditional “Five Good” model: good company, good school, core business, high performance and strong stability. The stability reference is no more than three moves within five years. Missing chronology is unknown rather than a penalty. In the AI era, company quality includes both established top companies and category-leading young AI companies; an AI startup CTO, technical leader or core-business owner can receive the same company-quality credit as a traditional large-company candidate.

| Dimension | Max | Evidence examples |
|---|---:|---|
| Company quality | 10 | Established top company or category-leading young AI company; key AI leadership also qualifies |
| School prestige | 15 | Tiered explicit evidence: C9/global top, 985/Double First Class, 211/key university, or degree-level baseline |
| Core business | 10 | Core product/business/platform, strategic AI business, or key technical/product ownership |
| High performance | 10 | M+/A+/top percentile, promotions, recognized awards, or quantified outsized results |
| Stability | 10 | Five years with no more than three moves, or explicit multi-year tenure; unknown is not penalized |
| AI-native practice | 12 | Uses agents/LLMs in real workflows; builds automation, evaluation, RAG/MCP or AI products |
| Shipped proof | 10 | Live product, GitHub, portfolio, deployment, users, adoption, measurable result |
| End-to-end ownership | 8 | Owns problem through implementation, launch and iteration; independent debugging |
| Learning and first principles | 5 | Fast learning, research, hackathons, cross-domain transfer, explicit first-principles reasoning |
| Customer and business | 10 | User research, delivery, FDE, growth, revenue, conversion, customer outcomes |

The score is the sum of capped signal points, not an LLM rating. Repeated occurrences of one signal do not add points. `evidence_coverage` is the fraction of dimensions with at least one matched signal and is reported separately from the score.

The five-good subtotal is 55. It is reported separately from the final 100-point score. The result also assigns a commercial-priority tier: internship, standard, core or high-value. Fee-multiple text is a business planning reference, not a salary recommendation or automatic employment decision.

This is a cross-role AI Native evidence score. The same evidence also produces role projections described in `role-benchmarks.md`. Use the JD matching Skill for exact role fit, location, work type, seniority, required domain, and must-have stack.
