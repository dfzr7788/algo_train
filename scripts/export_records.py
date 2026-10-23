"""白名单发布公开昵称和赛事成绩。答案、联系方式、内部点评不导出。"""
import json
import math
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def export(source):
    members, contests = [], []
    ids, contest_ids = set(), set()
    for m in source["members"]:
        mid, name = m["id"], m["name"]
        if not isinstance(mid, str) or not mid or mid in ids or not isinstance(name, str) or not name.strip():
            raise ValueError("成员 ID 必须唯一，公开昵称不能为空")
        ids.add(mid)
        members.append(dict(id=mid, name=name, role="队员", accounts={}))
    for c in source["contests"]:
        cid = c["id"]
        if not isinstance(cid, str) or not cid or cid in contest_ids:
            raise ValueError("比赛 ID 必须唯一")
        contest_ids.add(cid)
        date.fromisoformat(c["date"])
        if c["format"] not in ("ICPC", "SCORE", "OFFICIAL"):
            raise ValueError("赛制必须为 ICPC、SCORE 或 OFFICIAL")
        if not isinstance(c["title"], str) or not c["title"].strip():
            raise ValueError("比赛标题不能为空")
        results, seen = [], set()
        for r in c["results"]:
            if r["memberId"] not in ids or r["memberId"] in seen:
                raise ValueError("成绩引用未知成员或同场重复成员")
            seen.add(r["memberId"])
            clean = {"memberId": r["memberId"]}
            for field in ("solved", "score", "penalty"):
                value = r[field]
                if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                    raise ValueError(field + " 必须为有限非负数")
                if field == "solved" and type(value) is not int:
                    raise ValueError("solved 必须为整数")
                clean[field] = value
            if c["format"] == "OFFICIAL":
                value = r["officialRank"]
                if type(value) is not int or value < 1:
                    raise ValueError("官方排名必须为正整数")
                clean["officialRank"] = value
            results.append(clean)
        contests.append(dict(id=cid, title=c["title"], date=c["date"], format=c["format"], results=results))
    return dict(schemaVersion=1, members=members, contests=contests, daily=[])

if __name__ == "__main__":
    source = ROOT / "local/records.json"
    result = export(json.loads(source.read_text(encoding="utf-8-sig")))
    (ROOT / "docs/data/records.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("已导出公开成员与比赛成绩；未导出答案或个人日报")
