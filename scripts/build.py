"""仅从 local/daily.json 导出白名单汇总字段；绝不复制答案或成员标识。"""
import json
from pathlib import Path
from datetime import date
ROOT = Path(__file__).resolve().parents[1]
def aggregate(rows):
    grouped = {}
    for row in rows:
        day = row["date"]
        date.fromisoformat(day)
        members = row["participants"]
        problems = row["problems"]
        if not isinstance(members, list) or not isinstance(problems, list):
            raise ValueError("participants 与 problems 必须为列表")
        minutes, accepted = row["minutes"], row["accepted"]
        if any(type(x) is not int or x < 0 for x in (minutes, accepted)):
            raise ValueError("minutes 与 accepted 必须为非负整数")
        g = grouped.setdefault(day, {"members": set(), "problems": set(), "minutes": 0, "accepted": 0})
        g["members"].update(members)
        g["problems"].update(problems)
        g["minutes"] += minutes
        g["accepted"] += accepted
    return {"days": [{"date": day, "participants": len(g["members"]), "problems": len(g["problems"]),
                      "minutes": g["minutes"], "accepted": g["accepted"]} for day, g in sorted(grouped.items())]}
if __name__ == "__main__":
    source = ROOT / "local/daily.json"
    if not source.exists():
        raise SystemExit("请先建立 local/daily.json，格式参见 README.md；已有公开数据未改动。")
    result = aggregate(json.loads(source.read_text(encoding="utf-8-sig")))
    (ROOT / "docs/data/summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("已导出", len(result["days"]), "天汇总数据")
