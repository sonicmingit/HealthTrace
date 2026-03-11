import json
import os

with open("../data/health_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)["healthData"]

def get_risk(item, val):
    if item == "BMI":
        if val < 18.5: return "偏瘦", 1
        elif val <= 23.9: return "正常", 0
        elif val <= 27.9: return "偏胖", 1
        else: return "肥胖", 2
    if item == "血压收缩压":
        if val <= 130: return "正常", 0
        elif val <= 139: return "偏高", 1
        elif val <= 159: return "轻度高血压", 2
        else: return "中重度高血压", 3
    if item == "空腹血糖":
        if val <= 6.1: return "正常", 0
        elif val < 7.0: return "空腹血糖受损", 1
        else: return "糖尿病风险", 3
    if item == "总胆固醇":
        if val < 5.2: return "正常", 0
        elif val < 6.2: return "边缘升高", 1
        else: return "升高", 2
    if item == "甘油三酯":
        if val < 1.7: return "正常", 0
        elif val < 2.3: return "边缘升高", 1
        else: return "升高", 2
    if item == "尿酸":
        if val <= 420: return "正常", 0
        elif val <= 480: return "轻度偏高", 1
        elif val <= 540: return "中度偏高", 2
        else: return "重度偏高", 3
    if item == "ALT":
        if val <= 40: return "正常", 0
        elif val <= 80: return "轻度偏高", 1
        else: return "偏高", 2
    return "正常", 0

# Collect trends and risks
latest = data[-1]["items"]
latest_year = data[-1]["year"]
prev = data[-2]["items"] if len(data) > 1 else {}

risks = []
for item, val in latest.items():
    desc, level = get_risk(item, val)
    if level > 0:
        trend = "➖"
        if item in prev:
            diff = val - prev[item]
            if diff > val*0.05: trend = "📈"
            elif diff < -val*0.05: trend = "📉"
        risks.append({"item": item, "val": val, "desc": desc, "level": level, "trend": trend})

risks.sort(key=lambda x: -x["level"])

# Score Calculation
score = 100
for r in risks:
    score -= r["level"] * 3
if score < 0: score = 0

chart_data = {"charts": {}}
for item in ["体重", "BMI", "血压收缩压", "空腹血糖", "总胆固醇", "甘油三酯", "尿酸", "ALT"]:
    chart_data["charts"][item] = []
    for d in data:
        if item in d["items"]:
            chart_data["charts"][item].append({"year": d["year"], "value": d["items"][item]})
with open("../data/chart_data.json", "w", encoding="utf-8") as f:
    json.dump(chart_data, f, ensure_ascii=False, indent=2)

report = f"""# 个人体检健康趋势分析报告

## 基本信息
- 分析年份范围: {data[0]["year"]} - {data[-1]["year"]}
- 报告基准年份: {latest_year}

## 健康总体评价
- **健康评分**: {score} / 100
- **总体结论**: {"良好" if score >= 85 else "需注意" if score >= 70 else "需改善"}。发现 {len(risks)} 项偏高/风险指标，需要优先关注生活方式的调整和后续复查。

## 关键健康风险
"""
if not risks:
    report += "暂未发现明显高风险指标。\n"
for i, r in enumerate(risks[:3]):
    report += f"{i+1}️⃣ **{r['item']} {r['desc']}** ({r['val']} {r['trend']})\n"
    report += f"- 变化趋势: 最近一次指标呈现 {r['trend']} 状态。\n"
    report += f"- 潜在健康风险: 可能增加心血管、代谢紊乱等慢性病风险，需引起重视。\n\n"

for cat, items in [("体重与BMI变化", ["体重", "BMI"]), ("血压变化", ["血压收缩压", "血压舒张压"]), ("血脂变化", ["总胆固醇", "甘油三酯", "HDL", "LDL"]), ("血糖变化", ["空腹血糖"]), ("尿酸变化", ["尿酸"]), ("肝功能变化", ["ALT", "AST", "GGT"])]:
    report += f"## {cat}\n- "
    has_data = False
    for it in items:
        if it in latest:
            report += f"{it}: {latest[it]}  "
            has_data = True
    if not has_data:
        report += "暂无最新年度数据"
    report += "\n\n"

report += """
## 趋势图数据配置
详细的可视化数据见 `data/chart_data.json` 文件供前端图表渲染参考。

## 健康改善建议

### 饮食建议
* **控制精制碳水**: 减少白面、白米比例，增加粗粮。
* **控制高嘌呤食物**: 注意海鲜、动物内脏和肉汤的摄入（针对尿酸偏高）。
* **少油少糖**: 减少油炸食品及含糖饮料，帮助改善血脂与体重。

### 运动建议
* **规律有氧**: 每周至少 150 分钟中等强度有氧运动（如快走、慢跑、游泳）。
* **力量训练**: 每周进行 2-3 次力量训练，提高基础代谢改善血糖、血脂。

### 生活习惯
* **饮水充足**: 每天至少 2000ml，有利于尿酸排泄。
* **规律作息**: 避免熬夜，戒烟限酒。

### 医疗建议
* 针对异常指标（如尿酸、血脂、血糖等），建议3-6个月后复查。
* 如有头晕、乏力或关节不适等症状，请及时就医。
* *本分析基于历史数据趋势总结，仅供健康生活方式管理参考，不能代替专业医疗诊断。*
"""
with open("../docs/health_report.md", "w", encoding="utf-8") as f:
    f.write(report)

print("Report generated to ../docs/health_report.md")
