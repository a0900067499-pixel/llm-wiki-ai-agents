#!/usr/bin/env python3
"""簡報檢查（graph 節點 N8）：簡報內容必須能在它對應的 wiki 頁找到。
  C1 每張投影片有 data-wiki，且指向存在的 wiki 頁
  C2 投影片張數、順序與 outline.md 對應頁一致
  C3 投影片文字中的數字，都要出現在對應 wiki 頁（防捏造數字）
  C4 投影片中的英文專有名詞／術語，都要出現在對應 wiki 頁（防內容漂移）
  C5 標成 illustration 的示意頁，必須有「示意」說明
  C6 術語小辭典裡的術語在整份簡報第一次出現時，要緊接括號白話說明，或該張宣告 glossary（第二輪新增）
用法：python3 pipeline/check_slides.py [報告路徑] [--only N]
  --only N：只檢查第 N 張（逐張生成時用，第一次執行後新增）
"""
import re, sys, pathlib
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
html = (ROOT / "slides/index.html").read_text(encoding="utf-8")
outline = (ROOT / "slides/outline.md").read_text(encoding="utf-8")
STOP = {"and", "the", "or", "for", "API", "LLM", "Wiki", "wiki", "memory"}  # 通用詞


class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.slides = []; self.cur = None; self.skip = 0
    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "section" and "slide" in a.get("class", ""):
            self.cur = {"wiki": a.get("data-wiki"), "kind": a.get("data-kind"), "text": ""}
            self.slides.append(self.cur)
        elif self.cur is not None and tag in ("code", "pre", "script"):
            self.skip += 1
    def handle_endtag(self, tag):
        if tag == "section": self.cur = None
        elif self.cur is not None and tag in ("code", "pre", "script") and self.skip: self.skip -= 1
    def handle_data(self, d):
        if self.cur is not None and not self.skip: self.cur["text"] += d


p = P(); p.feed(html)
rows = [[c.strip() for c in r.strip("|").split("|")] for r in outline.splitlines() if re.match(r"^\|\s*\d+\s*\|", r)]
args = sys.argv[1:]
only = int(args[args.index("--only") + 1]) if "--only" in args else None
if "--only" in args:
    i = args.index("--only"); args = args[:i] + args[i + 2:]
gl = (ROOT / "wiki/concepts/glossary.md").read_text(encoding="utf-8")
TERMS = [t for t in re.findall(r"^- \*\*([^（*]+)", gl, re.M) if t.strip() not in ("工具（tool）", "工具")]
TERMS = [re.sub(r"[（(].*", "", t).strip() for t in TERMS]
TERMS = [t for t in TERMS if t != "工具"]
seen = set()
errors = []
if only is None and len(rows) != len(p.slides):
    errors.append(f"C2 大綱 {len(rows)} 張，但簡報有 {len(p.slides)} 張")

for i, s in enumerate(p.slides, 1):
    if only and i < only:  # 逐張模式：前面的張只用來記錄「已出現過的術語」
        t0 = re.sub(r"\s+", " ", s["text"])
        seen.update(t for t in TERMS if t in t0)
        continue
    if only and i > only:
        break
    if not s["wiki"]:
        errors.append(f"C1 第 {i} 張沒有 data-wiki"); continue
    pages = [x.strip() for x in s["wiki"].split(",")]
    wiki_text = ""
    for pg in pages:
        f = ROOT / "wiki" / pg
        if not f.exists():
            errors.append(f"C1 第 {i} 張：wiki 頁不存在 → {pg}")
        else:
            wiki_text += f.read_text(encoding="utf-8")
    if i <= len(rows) and not rows[i - 1][4].startswith("多頁"):
        want = {x.strip().replace("wiki/", "") for x in rows[i - 1][4].split(",") if not x.strip().endswith("/")}
        if not want <= set(pages):
            errors.append(f"C2 第 {i} 張對應 {pages}，大綱寫的是 {sorted(want)}")
    text = re.sub(r"\s+", " ", s["text"])
    for n in re.findall(r"(?<![\w.])(\d+(?:\.\d+)?%?)", text):
        if n not in wiki_text:
            errors.append(f"C3 第 {i} 張：數字「{n}」不在 {pages}")
    for w in sorted(set(re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", text)) - STOP):
        if w.lower() not in wiki_text.lower():
            errors.append(f"C4 第 {i} 張：術語「{w}」不在 {pages}")
    for term in TERMS:
        if term in seen:
            continue
        k = text.find(term)
        if k >= 0:
            seen.add(term)
            after = text[k + len(term):k + len(term) + 2]
            if "concepts/glossary.md" not in pages and "（" not in after and "(" not in after:
                errors.append(f"C6 第 {i} 張：術語「{term}」第一次出現，沒有白話說明")
    if s["kind"] == "illustration" and "示意" not in text:
        errors.append(f"C5 第 {i} 張是示意頁但沒有標「示意」")

out = "\n".join([f"簡報檢查：{len(p.slides)} 張投影片", f"錯誤數：{len(errors)}"] + errors)
print(out)
if args:
    pathlib.Path(args[0]).write_text(out + "\n", encoding="utf-8")
sys.exit(1 if errors else 0)
