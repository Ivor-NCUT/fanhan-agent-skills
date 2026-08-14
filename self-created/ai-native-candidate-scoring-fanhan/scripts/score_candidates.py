#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path

VERSION = "ai-native-five-good-v3.0.0"

RUBRIC = {
    "company_quality": (10, []),
    "school_prestige": (15, []),
    "core_business": (10, [
        (6, r"(?:核心业务|核心产品|核心团队|核心部门|主航道|战略业务|抖音|douyin|基础模型|大模型平台|AI应用)"),
        (4, r"(?:技术负责人|技术leader|tech lead|CTO|首席技术官|业务负责人|产品负责人).{0,40}(?:AI|大模型|智能体|生成式|AIGC)"),
    ]),
    "high_performance": (10, [
        (6, r"(?:M\+|E\+|S级|A\+|高绩效|绩效.{0,8}(?:优秀|卓越|top)|top\s*\d+%|前\s*\d+%)"),
        (4, r"(?:晋升|破格晋升|优秀员工|最佳员工|年度.{0,8}(?:奖|优秀)|连续.{0,8}(?:优秀|高绩效))"),
        (4, r"(?:营收|收入|GMV|用户|活跃|留存|转化|成本).{0,24}\d+(?:\.\d+)?\s*(?:%|万|亿|k|w|人|家|元|美元)"),
    ]),
    "stability": (10, []),
    "ai_native_practice": (12, [
        (7, r"(?:ai|llm|agentic|agent|大模型|智能体)"),
        (6, r"(?:claude|cursor|codex|copilot|chatgpt|gemini)"),
        (6, r"(?:rag|mcp|prompt|向量|embedding|微调|fine[- ]?tun|多模态|评测|eval)"),
        (6, r"(?:自动化|automation|workflow|工作流|数字员工)"),
    ]),
    "shipped_proof": (10, [
        (7, r"(?:github|开源|open source|作品集|portfolio|demo|个人网站)"),
        (7, r"(?:上线|发布|部署|launch|ship|deployed|production|落地)"),
        (6, r"(?:用户|客户|活跃|留存|转化|收入|营收|增长).{0,24}\d+(?:\.\d+)?\s*(?:%|万|千|k|w|人|家|元|美元)?"),
        (5, r"(?:产品|项目|系统|平台|应用|插件|工具).{0,32}(?:从0到1|0\s*[-到]\s*1|独立|主导|上线|发布|落地)"),
    ]),
    "end_to_end_ownership": (8, [
        (6, r"(?:端到端|全流程|闭环|end[- ]?to[- ]?end|需求.*上线|从需求.*交付)"),
        (5, r"(?:独立|主导|负责|owner|牵头|带领)"),
        (5, r"(?:架构|技术选型|系统设计|排障|debug|故障|性能优化|迭代)"),
        (4, r"(?:结果负责|业务结果|交付结果|复盘|验证|反馈)"),
    ]),
    "learning_first_principles": (5, [
        (3, r"(?:第一性|first principles?|底层逻辑|拆解问题)"),
        (3, r"(?:自学|快速学习|快速上手|跨领域|跨学科|通才)"),
        (2, r"(?:黑客松|hackathon|比赛|竞赛)"),
        (2, r"(?:研究|research|论文|paper|实验|探索)"),
    ]),
    "customer_business": (10, [
        (3, r"(?:客户|用户|user research|用户调研|需求访谈)"),
        (3, r"(?:交付|实施|fde|解决方案|客户成功|售前)"),
        (2, r"(?:商业化|营收|收入|销售|成交|付费|成本|roi)"),
        (2, r"(?:增长|转化|留存|获客|市场|运营)"),
    ]),
}

BENCHMARK_WEIGHTS = {
    "unified": {name: maximum for name, (maximum, _) in RUBRIC.items()},
    "engineering": {"company_quality": 10, "school_prestige": 15, "core_business": 10, "high_performance": 10, "stability": 10, "ai_native_practice": 20, "shipped_proof": 10, "end_to_end_ownership": 10, "learning_first_principles": 3, "customer_business": 2},
    "product": {"company_quality": 10, "school_prestige": 15, "core_business": 12, "high_performance": 10, "stability": 10, "ai_native_practice": 15, "shipped_proof": 10, "end_to_end_ownership": 8, "learning_first_principles": 3, "customer_business": 7},
    "growth_operations": {"company_quality": 10, "school_prestige": 12, "core_business": 12, "high_performance": 15, "stability": 10, "ai_native_practice": 10, "shipped_proof": 10, "end_to_end_ownership": 8, "learning_first_principles": 3, "customer_business": 10},
    "design": {"company_quality": 10, "school_prestige": 12, "core_business": 10, "high_performance": 10, "stability": 10, "ai_native_practice": 12, "shipped_proof": 18, "end_to_end_ownership": 8, "learning_first_principles": 5, "customer_business": 5},
    "creative": {"company_quality": 8, "school_prestige": 10, "core_business": 10, "high_performance": 10, "stability": 8, "ai_native_practice": 18, "shipped_proof": 20, "end_to_end_ownership": 8, "learning_first_principles": 5, "customer_business": 3},
    "commercial": {"company_quality": 12, "school_prestige": 12, "core_business": 12, "high_performance": 15, "stability": 12, "ai_native_practice": 8, "shipped_proof": 8, "end_to_end_ownership": 8, "learning_first_principles": 3, "customer_business": 10},
    "people_recruiting": {"company_quality": 12, "school_prestige": 15, "core_business": 10, "high_performance": 12, "stability": 12, "ai_native_practice": 8, "shipped_proof": 5, "end_to_end_ownership": 8, "learning_first_principles": 5, "customer_business": 13},
}

TRADITIONAL_TOP_COMPANIES = r"(?:字节跳动|ByteDance|腾讯|Tencent|阿里巴巴|Alibaba|蚂蚁集团|美团|京东|百度|Huawei|华为|Microsoft|微软|Google|谷歌|Meta|Amazon|亚马逊|Apple|苹果|Netflix|NVIDIA|英伟达)"
AI_ERA_COMPANIES = r"(?:LiblibAI|Liblib|哩布哩布|Machine|MiniMax|月之暗面|Kimi|智谱|百川智能|零一万物|阶跃星辰|DeepSeek|深度求索|字节豆包|飞书多维表格|HeyGen|VAST|Tripo|RockFlow|硅基流动|生数科技|即梦|可灵)"

ROLE_SIGNALS = {
    "engineering": [(5, r"(?:软件工程|工程师|developer|backend|frontend|full.?stack|后端|前端|全栈|FDE|field deployment engineer)"), (5, r"(?:代码|编程|Python|Java|JavaScript|TypeScript|Go|C\+\+|React|Node\.js)"), (5, r"(?:架构|系统设计|性能优化|debug|排障|测试|CI/CD|code review|PR Review)"), (5, r"(?:Agent SDK|tool calling|RAG|MCP|模型训练|SFT|评测|benchmark|解决方案落地|客户现场|实施交付)")],
    "product": [(5, r"(?:产品经理|产品负责人|product manager|PM)"), (5, r"(?:用户访谈|需求分析|需求拆解|PRD|原型|Figma)"), (5, r"(?:产品规划|路线图|roadmap|产品设计|功能设计)"), (5, r"(?:埋点|指标体系|A/B|用户反馈|产品迭代)")],
    "growth_operations": [(5, r"(?:增长|growth|运营|operations|GTM)"), (5, r"(?:投放|获客|转化|留存|DAU|GMV|ROI|漏斗|A/B)"), (5, r"(?:小红书|抖音|TikTok|YouTube|社媒|内容运营|KOL|KOC)"), (5, r"(?:活动策划|用户运营|社区运营|商业化|电商)")],
    "design": [(5, r"(?:UI|UX|交互设计|视觉设计|产品设计|设计师)"), (5, r"(?:Figma|Sketch|Adobe|Photoshop|Illustrator)"), (5, r"(?:作品集|portfolio|原型|动效|设计系统)"), (5, r"(?:用户体验|信息架构|品牌设计|可用性|设计规范)")],
    "creative": [(5, r"(?:创意|creative|内容创作|艺术|导演|编剧)"), (5, r"(?:After Effects|Blender|Unity|视频|动画|3D|影像)"), (5, r"(?:作品集|portfolio|短片|展览|广告创意)"), (5, r"(?:AIGC|AI 视频|生成艺术|创意技术|叙事)")],
    "commercial": [(5, r"(?:销售|商务|BD|商业化|成交|合同|回款)"), (5, r"(?:客户需求|业务诊断|PoC|方案设计|定价|投标)"), (5, r"(?:售前|客户成功|解决方案|渠道|GTM)"), (5, r"(?:客户沟通|跨团队推进|项目管理|业务落地)")],
    "people_recruiting": [(5, r"(?:招聘|猎头|HRBP|人力资源|人才发展)"), (5, r"(?:寻访|sourcing|面试|候选人|人才盘点)"), (5, r"(?:组织发展|绩效|薪酬|员工关系|培训)"), (5, r"(?:业务伙伴|用人部门|招聘漏斗|人才策略)")],
}

TEXT_FIELDS = ("resume_text", "material_text", "profile_text", "portfolio_text", "summary", "direction")
DEGREE = r"(?:本科|学士|硕士|博士|Ph\.?D|Bachelor|Master)"
SCHOOL_TIERS = (
    (15, r"(?:清华大学|北京大学|复旦大学|上海交通大学|浙江大学|中国科学技术大学|南京大学|哈尔滨工业大学|西安交通大学|麻省理工|MIT|Stanford|斯坦福|Harvard|哈佛|Berkeley|伯克利|Cambridge|剑桥|Oxford|牛津|Princeton|普林斯顿|Yale|耶鲁|Caltech|加州理工|Carnegie Mellon|卡内基梅隆|ETH Zurich|苏黎世联邦理工|Imperial College|帝国理工|UCL|伦敦大学学院|National University of Singapore|新加坡国立大学|Nanyang Technological University|南洋理工)"),
    (12, r"(?:中国人民大学|北京航空航天大学|北京理工大学|北京师范大学|南开大学|天津大学|同济大学|东南大学|武汉大学|华中科技大学|厦门大学|中山大学|四川大学|电子科技大学|重庆大学|山东大学|吉林大学|大连理工大学|西北工业大学|兰州大学|中南大学|湖南大学|华南理工大学|中国农业大学|中央民族大学|国防科技大学)"),
)


def candidate_text(candidate):
    values = [candidate.get(key) for key in TEXT_FIELDS]
    values += candidate.get("skills") or []
    values += candidate.get("portfolio") or candidate.get("links") or []
    values += candidate.get("career_facts") or []
    for resume in candidate.get("resumes") or []:
        values.append(resume.get("resume_text"))
    return "\n".join(_string(value) for value in values if value)


def _string(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)


def display_name(candidate):
    name = str(candidate.get("name") or "").strip()
    if name and not re.fullmatch(r"[+\d\s-]{7,}", name):
        return name
    for resume in candidate.get("resumes") or []:
        filename = str(resume.get("file_name") or resume.get("filename") or resume.get("original_filename") or resume.get("name") or "")
        match = re.search(r"(?:^|[_-])([\u4e00-\u9fff]{2,4})(?=(?:的)?(?:AI|产品|个人|求职|运营)?简历|[_\-.\s])", filename)
        if match:
            return match.group(1)
    text = candidate_text(candidate)[:1000]
    match = re.search(r"(?:^|\n)([\u4e00-\u9fff]{2,4})(?=\s+(?:1\d{10}|[\w.+-]+@))", text)
    return match.group(1) if match else "未命名候选人"


def evidence(text, match):
    start = max(0, match.start() - 50)
    end = min(len(text), match.end() + 90)
    return re.sub(r"\s+", " ", text[start:end]).strip()[:180]


def school_score(text):
    for points, school in SCHOOL_TIERS:
        match = re.search(rf"(?:{school}.{{0,80}}{DEGREE}|{DEGREE}.{{0,80}}{school})", text, re.I | re.S)
        if match:
            return points, [evidence(text, match)]
    match = re.search(rf"(?<!非)(?:(?:985|双一流).{{0,40}}{DEGREE}|{DEGREE}.{{0,40}}(?:985|双一流))", text, re.I | re.S)
    if match:
        return 12, [evidence(text, match)]
    match = re.search(rf"(?<!非)(?:(?:211|一本|重点大学).{{0,40}}{DEGREE}|{DEGREE}.{{0,40}}(?:211|一本|重点大学))", text, re.I | re.S)
    if match:
        return 9, [evidence(text, match)]
    match = re.search(DEGREE, text, re.I)
    return (5, [evidence(text, match)]) if match else (0, [])


def company_score(text):
    for pattern in (TRADITIONAL_TOP_COMPANIES, AI_ERA_COMPANIES):
        match = re.search(pattern, text, re.I)
        if match:
            return 10, [evidence(text, match)]
    match = re.search(r"(?:CTO|首席技术官|技术负责人|技术leader|tech lead|创始人|联合创始人).{0,50}(?:AI|大模型|智能体|生成式|AIGC)|(?:AI|大模型|智能体|生成式|AIGC).{0,50}(?:CTO|首席技术官|技术负责人|技术leader|tech lead|创始人|联合创始人)", text, re.I | re.S)
    if match:
        return 10, [evidence(text, match)]
    match = re.search(r"(?:世界500强|上市公司|独角兽|行业头部|头部公司|知名公司)", text, re.I)
    return (7, [evidence(text, match)]) if match else (0, [])


def stability_score(text):
    unstable = re.search(r"(?:5|五)年.{0,24}(?:超过|多于).{0,8}(?:3|三)(?:次|跳)|(?:5|五)年.{0,24}(?:4|四)(?:次|跳)", text, re.I | re.S)
    if unstable:
        return 0, [evidence(text, unstable)]
    explicit = re.search(r"(?:5|五)年.{0,24}(?:不超过|至多|最多).{0,8}(?:3|三)(?:次|跳)", text, re.I | re.S)
    if explicit:
        return 10, [evidence(text, explicit)]
    tenure = re.search(r"(?:任职|在职|就职|工作|负责).{0,24}([1-9](?:\.\d+)?)\s*年|([1-9](?:\.\d+)?)\s*年.{0,24}(?:任职|在职|就职|工作|负责)", text, re.I | re.S)
    if not tenure:
        return 0, []
    years = float(tenure.group(1) or tenure.group(2))
    return (10 if years >= 3 else 7 if years >= 2 else 4), [evidence(text, tenure)]


def talent_value(score, five_good_score, text):
    if re.search(r"(?:实习生|实习岗位|internship|\bintern\b)", text, re.I):
        return {"tier": "intern", "headhunting_priority": "low", "fee_multiple": "项目制或低客单"}
    if score >= 75 and five_good_score >= 35:
        return {"tier": "high_value", "headhunting_priority": "high", "fee_multiple": "2-3个月工资"}
    if score >= 60:
        return {"tier": "core", "headhunting_priority": "medium", "fee_multiple": "约1个月工资"}
    return {"tier": "standard", "headhunting_priority": "low", "fee_multiple": "约1个月工资或按项目定价"}


def role_fit_scores(text):
    scores = {}
    for role, signals in ROLE_SIGNALS.items():
        scores[role] = min(20, sum(points for points, pattern in signals if re.search(pattern, text, re.I | re.S)))
    return scores


def score_candidate(candidate, benchmark="unified"):
    text = candidate_text(candidate)
    if re.search(r"(?:合成测试信息|仅供 Allen Agent .*测试|非真实候选人|test candidate)", text, re.I):
        empty = {name: {"score": 0, "max": maximum, "evidence": []} for name, (maximum, _) in RUBRIC.items()}
        return {"candidate_id": str(candidate.get("id") or candidate.get("candidate_id") or ""), "candidate_name": display_name(candidate), "score": 0, "benchmark": benchmark, "benchmark_scores": {key: 0 for key in BENCHMARK_WEIGHTS}, "role_fit_scores": {key: 0 for key in ROLE_SIGNALS}, "algorithm_version": VERSION, "eligible": False, "evidence_coverage": 0, "dimensions": empty, "five_good": {"score": 0, "max": 55}, "talent_value": {"tier": "excluded", "headhunting_priority": "none", "fee_multiple": "不适用"}, "input_hash": hashlib.sha256(text.encode()).hexdigest(), "evidence": [], "material_gaps": ["测试或合成候选人，不进入真实候选人排序"]}
    dimensions = {}
    all_evidence = []
    for name, (maximum, signals) in RUBRIC.items():
        if name == "company_quality":
            points, found = company_score(text)
            dimensions[name] = {"score": points, "max": maximum, "evidence": found}
            all_evidence.extend(found)
            continue
        if name == "school_prestige":
            points, found = school_score(text)
            dimensions[name] = {"score": points, "max": maximum, "evidence": found}
            all_evidence.extend(found)
            continue
        if name == "stability":
            points, found = stability_score(text)
            dimensions[name] = {"score": points, "max": maximum, "evidence": found}
            all_evidence.extend(found)
            continue
        points, found = 0, []
        for value, pattern in signals:
            match = re.search(pattern, text, re.I | re.S)
            if match:
                points += value
                found.append(evidence(text, match))
        dimensions[name] = {"score": min(maximum, points), "max": maximum, "evidence": found}
        all_evidence.extend(found)
    role_scores = role_fit_scores(text)
    benchmark_scores = {}
    for key, weights in BENCHMARK_WEIGHTS.items():
        base = sum(dimensions[name]["score"] / dimensions[name]["max"] * weight for name, weight in weights.items())
        benchmark_scores[key] = round(base if key == "unified" else base * 0.8 + role_scores[key])
    covered = sum(bool(item["evidence"]) for item in dimensions.values())
    five_good_dimensions = ["company_quality", "school_prestige", "core_business", "high_performance", "stability"]
    five_good_score = sum(dimensions[name]["score"] for name in five_good_dimensions)
    value = talent_value(benchmark_scores["unified"], five_good_score, text)
    return {
        "candidate_id": str(candidate.get("id") or candidate.get("candidate_id") or ""),
        "candidate_name": display_name(candidate),
        "score": benchmark_scores[benchmark],
        "benchmark": benchmark,
        "benchmark_scores": benchmark_scores,
        "role_fit_scores": role_scores,
        "algorithm_version": VERSION,
        "eligible": True,
        "evidence_coverage": round(covered / len(RUBRIC), 2),
        "dimensions": dimensions,
        "five_good": {"score": five_good_score, "max": 55, "dimensions": {name: dimensions[name] for name in five_good_dimensions}},
        "talent_value": value,
        "input_hash": hashlib.sha256(text.encode()).hexdigest(),
        "evidence": list(dict.fromkeys(all_evidence))[:12],
        "material_gaps": [] if text.strip() else ["无可评分的简历、项目或作品材料"],
    }


def load_candidates(path):
    payload = json.loads(Path(path).read_text())
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("candidates"), list):
        return payload["candidates"]
    if isinstance(payload, dict):
        return [payload]
    raise ValueError("input must be a candidate object, array, or {candidates:[...]}")


def rank(candidates, top_n=None, benchmark="unified"):
    scores = [score_candidate(item, benchmark) for item in candidates]
    scores.sort(key=lambda item: (-item["score"], item["candidate_id"]))
    for index, item in enumerate(scores, 1):
        item["rank"] = index
    return scores if top_n is None else scores[:top_n]


def self_test():
    strong = {"id": "b", "resume_text": "清华大学本科毕业，在字节跳动抖音核心业务任职3年，M+绩效；用第一性原理研究问题，用 Claude 和 Agent 工作流独立从0到1开发并上线产品，GitHub 开源；完成客户访谈和交付，复盘用户增长 35%。"}
    weak = {"id": "a", "resume_text": "负责日常行政事务。"}
    first = rank([weak, strong])
    second = rank([strong, weak])
    assert first == second and first[0]["candidate_id"] == "b"
    assert first[0]["score"] > first[1]["score"]
    assert all(item["score"] > 0 for item in first[0]["dimensions"].values())
    assert score_candidate(strong)["score"] == score_candidate(strong)["score"]
    assert score_candidate(strong, "engineering")["benchmark"] == "engineering"
    fde = score_candidate({"id": "c", "resume_text": "FDE 工程师，负责客户现场 Python 实施交付和解决方案落地。"}, "engineering")
    assert fde["role_fit_scores"]["engineering"] >= 15
    assert {"design", "creative", "commercial", "growth_operations"} <= set(BENCHMARK_WEIGHTS)
    ai_leader = score_candidate({"id": "d", "resume_text": "LiblibAI 技术leader，负责 AI 应用核心业务，在职3年，连续高绩效。"})
    assert ai_leader["dimensions"]["company_quality"]["score"] == 10
    assert ai_leader["five_good"]["score"] >= 30
    assert all(sum(weights.values()) == 100 for weights in BENCHMARK_WEIGHTS.values())
    print("self-test ok")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--top-n", type=int)
    parser.add_argument("--benchmark", choices=BENCHMARK_WEIGHTS, default="unified")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.input:
        parser.error("--input is required")
    candidates = load_candidates(args.input)
    results = rank(candidates, args.top_n, args.benchmark)
    output = {"algorithm_version": VERSION, "benchmark": args.benchmark, "source_candidate_count": len(candidates), "returned_count": len(results), "scores": results}
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
