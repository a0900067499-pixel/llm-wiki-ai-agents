#!/usr/bin/env python3
"""大綱檢查（graph 節點 N6）：生成簡報『之前』先檢查大綱。
  O1 每列對應的 wiki 頁存在
  O2 9 個概念頁都至少被一張投影片使用（覆蓋率）
  O3 教學結構完整：要有 學習目標、測驗、總結
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
text = (ROOT / "slides/outline.md").read_text(encoding="utf-8")
rows = [r for r in text.splitlines() if re.match(r"^\|\s*\d+\s*\|", r)]
errors, used = [], set()
for r in rows:
    cells = [c.strip() for c in r.strip("|").split("|")]
    num, part, title, goal, pages = cells
    for p in re.split(r",\s*", pages):
        if p.startswith("多頁"):
            continue
        path = ROOT / ("wiki/" + p if p.startswith(("concepts", "sources")) else p)
        if p.endswith("/"):
            path = ROOT / "wiki" / p
        if not path.exists():
            errors.append(f"O1 第 {num} 張：wiki 頁不存在 → {p}")
        if p.startswith("concepts/"):
            used.add(pathlib.Path(p).name)
for c in sorted((ROOT / "wiki/concepts").glob("*.md")):
    if c.name not in used:
        errors.append(f"O2 概念頁沒被任何投影片使用 → {c.name}")
for need in ("學習目標", "測驗", "回顧"):
    if need not in text:
        errors.append(f"O3 教學結構缺少「{need}」")
out = "\n".join([f"大綱檢查：{len(rows)} 張投影片", f"錯誤數：{len(errors)}"] + errors)
print(out)
if len(sys.argv) > 1:
    pathlib.Path(sys.argv[1]).write_text(out + "\n", encoding="utf-8")
sys.exit(1 if errors else 0)
