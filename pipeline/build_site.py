#!/usr/bin/env python3
"""把所有 .md 轉成同名 .html（給 GitHub Pages 瀏覽），.md 原檔保留，作為 LLM Wiki 本體。"""
import re, pathlib, html, markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = """
:root{--paper:#EEF2F4;--ink:#1C2B3A;--muted:#5E6E7D;--line:#C9D3DA;--think:#4A4DB8;--act:#C27C0E;--obs:#0E7A70}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.75 "Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif}
header{border-bottom:1px solid var(--line);background:#fff}header div{max-width:58rem;margin:0 auto;padding:.7rem 1.5rem;display:flex;gap:1.4rem;flex-wrap:wrap}
header a{color:var(--ink);text-decoration:none;font-weight:500}header a:hover{color:var(--think)}
main{max-width:58rem;margin:0 auto;padding:1.5rem 1.5rem 4rem}
h1,h2,h3{font-family:"LXGW WenKai TC","Kaiti TC",serif;line-height:1.3}h1{font-size:2.2rem;margin:.4rem 0 1rem}h2{margin-top:2.2rem}
a{color:var(--think)}p,li{max-width:46rem}
table{border-collapse:collapse;width:100%;margin:1rem 0;background:#fff;font-size:.95rem}th,td{border:1px solid var(--line);padding:.45rem .7rem;text-align:left;vertical-align:top}th{background:#F6F8F9}
code{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:.9em;background:#fff;padding:.05em .3em}
pre{background:#fff;border-left:4px solid var(--think);padding:1rem;overflow:auto}pre code{padding:0}
.meta{font-size:.88rem;color:var(--muted);background:#fff;border:1px solid var(--line);padding:.5rem .8rem;margin-bottom:1rem}
.meta b{color:var(--ink);font-weight:500}
.src{color:var(--obs);font-size:.85em;font-weight:500;white-space:nowrap}
.path{font-size:.85rem;color:var(--muted)}
"""
NAV = [("首頁", "index.html"), ("教學簡報", "slides/index.html"), ("Wiki 索引", "wiki/index.html"),
       ("流程與反思", "docs/process.html"), ("規則檔", "CLAUDE.html"), ("檢查報告", "pipeline/reports/index.html")]


def page(title, body, rel_root, path):
    nav = "".join(f'<a href="{rel_root}{h}">{t}</a>' for t, h in NAV)
    return f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — AI Agents LLM Wiki</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@700&family=Noto+Sans+TC:wght@400;500&display=swap">
<style>{CSS}</style></head><body><header><div>{nav}</div></header><main><p class="path">{html.escape(path)}{"　<a href=" + chr(34) + pathlib.Path(path).name + chr(34) + ">看 Markdown 原檔</a>" if path.endswith(".md") else ""}</p>{body}</main></body></html>"""


def render(md_path):
    text = md_path.read_text(encoding="utf-8")
    meta, title = "", md_path.stem
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        text = text[m.end():]
        rows = [l.split(":", 1) for l in m.group(1).splitlines() if ":" in l and not l.startswith(" ")]
        meta = '<div class="meta">' + "　".join(f"<b>{html.escape(k.strip())}</b>：{html.escape(v.strip())}" for k, v in rows) + "</div>"
        t = dict((k.strip(), v.strip()) for k, v in rows).get("title")
        if t: title = t.strip('"')
    h = re.search(r"^# (.+)$", text, re.M)
    if h: title = h.group(1)
    body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    body = re.sub(r'href="([^":#]+?)\.md(#[^"]*)?"', lambda x: f'href="{x.group(1)}.html{x.group(2) or ""}"', body)
    body = re.sub(r"\[((?:綜合:\s*)?S\d(?:\s*,\s*S\d)*)\]", r'<span class="src">[\1]</span>', body)
    rel = md_path.relative_to(ROOT)
    rel_root = "../" * (len(rel.parts) - 1)
    if "<h1" in body and meta:
        body = body.replace("</h1>", "</h1>" + meta, 1)
    else:
        body = meta + body
    md_path.with_suffix(".html").write_text(page(title, body, rel_root, str(rel)), encoding="utf-8")


def reports_index():
    d = ROOT / "pipeline/reports"
    items = "".join(f'<li><a href="{f.name}">{f.name}</a> — {html.escape(f.read_text(encoding="utf-8").splitlines()[1] if len(f.read_text(encoding="utf-8").splitlines())>1 else "")}</li>'
                    for f in sorted(d.glob("*.txt")))
    body = f"<h1>檢查報告</h1><p>每次執行檢查節點的原始輸出，依時間順序編號（run1、run2…）。逐張截圖會在執行 check_visual.py 時產生於 shots/；為了符合 GitHub 網頁上傳的檔案數上限沒有上傳，代表性截圖請見流程頁。</p><ul>{items}</ul>"
    (d / "index.html").write_text(page("檢查報告", body, "../../", "pipeline/reports/"), encoding="utf-8")


n = 0
for p in list(ROOT.rglob("*.md")):
    if ".git" in p.parts: continue
    render(p); n += 1
reports_index()
print(f"rendered {n} markdown files")
