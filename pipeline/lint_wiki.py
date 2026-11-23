#!/usr/bin/env python3
"""Wiki lint（graph 節點 N4）：檢查 wiki/ 是否符合 CLAUDE.md 規則。

檢查項目
  L1 每條事實（條列）結尾有來源標記 [Sx] 或 [綜合: Sx,Sy]
  L2 標記的來源存在於 raw/，且列在頁首 sources
  L3 相對連結都指向存在的檔案
  L4 概念頁都有被 index.md 連到（沒有孤兒頁）
  L5 條列中的數字都能在它標記的 raw 來源裡找到（防止捏造數字）
  L6 有「⚠ 矛盾」小節的頁面，log.md 必須有對應紀錄
用法：python3 pipeline/lint_wiki.py [報告輸出路徑]
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI, RAW = ROOT / "wiki", ROOT / "raw"
TAG = re.compile(r"\[(?:綜合:\s*)?(S\d(?:\s*,\s*S\d)*)\]\s*$")
LINK = re.compile(r"\]\(([^)]+?\.md)(?:#[^)]*)?\)")
NUM = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?%?)")

raw_ids = {p.stem for p in RAW.glob("S*.md")}
raw_text = {p.stem: p.read_text(encoding="utf-8") for p in RAW.glob("S*.md")}
errors, checked = [], 0


def frontmatter_sources(text):
    m = re.search(r"^sources:\s*\[(.*?)\]", text, re.M)
    return {s.strip() for s in m.group(1).split(",")} if m else set()


def bullets(text):
    """回傳 (行號, 內容)，略過 frontmatter 與程式碼區塊。"""
    in_code, in_fm = False, False
    for i, line in enumerate(text.splitlines(), 1):
        if i == 1 and line == "---":
            in_fm = True; continue
        if in_fm:
            if line == "---": in_fm = False
            continue
        if line.startswith("```"):
            in_code = not in_code; continue
        if not in_code and re.match(r"^\s*(?:-|\d+\.)\s", line):
            yield i, line


pages = sorted(WIKI.rglob("*.md"))
for page in pages:
    rel = page.relative_to(ROOT)
    text = page.read_text(encoding="utf-8")
    fm = frontmatter_sources(text)
    is_fact_page = page.parent.name in ("concepts", "sources") or page.name == "overview.md"
    for ln, line in bullets(text):
        if not is_fact_page:
            continue
        # 「相關頁面」那種只有連結的條列不算事實
        if re.match(r"^\s*- \[[^\]]*\]\([^)]*\.md\)(、\[[^\]]*\]\([^)]*\.md\))*\s*$", line):
            continue
        checked += 1
        m = TAG.search(line)
        if not m:
            errors.append(f"L1 {rel}:{ln} 缺來源標記 → {line.strip()[:60]}")
            continue
        ids = {s.strip() for s in m.group(1).split(",")}
        for s in ids:
            if s not in raw_ids:
                errors.append(f"L2 {rel}:{ln} 來源 {s} 不存在於 raw/")
            elif s not in fm:
                errors.append(f"L2 {rel}:{ln} 來源 {s} 未列在頁首 sources {sorted(fm)}")
        body = TAG.sub("", line)
        body = re.sub(r"`[^`]*`|\([^)]*\.md\)|<https?://[^>]+>|S\d", "", body)
        for n in NUM.findall(body):
            if not any(n in raw_text[s] for s in ids if s in raw_text):
                errors.append(f"L5 {rel}:{ln} 數字「{n}」在 {sorted(ids)} 的 raw 中找不到")
    for target in LINK.findall(text):
        if target.startswith("http"):
            continue
        if not (page.parent / target).resolve().exists():
            errors.append(f"L3 {rel} 壞連結 → {target}")
    if "⚠ 矛盾" in text and page.parent.name == "concepts":
        log = (WIKI / "log.md").read_text(encoding="utf-8")
        title = re.search(r"^title:\s*(.+)$", text, re.M).group(1)
        key = title.split("（")[0].strip()
        if key not in log and page.stem not in log:
            errors.append(f"L6 {rel} 有矛盾小節，但 log.md 沒有提到「{key}」")

index = (WIKI / "index.md").read_text(encoding="utf-8")
for c in (WIKI / "concepts").glob("*.md"):
    if f"concepts/{c.name}" not in index:
        errors.append(f"L4 孤兒頁：{c.relative_to(ROOT)} 未被 index.md 連到")

report = [f"Wiki lint：{len(pages)} 頁、檢查 {checked} 條事實", f"錯誤數：{len(errors)}"] + errors
out = "\n".join(report)
print(out)
if len(sys.argv) > 1:
    pathlib.Path(sys.argv[1]).write_text(out + "\n", encoding="utf-8")
sys.exit(1 if errors else 0)
