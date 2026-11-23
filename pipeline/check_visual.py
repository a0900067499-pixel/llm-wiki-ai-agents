#!/usr/bin/env python3
"""視覺檢查（graph 節點 N8b）：用無頭 Chrome 開簡報，逐張截圖並偵測內容是否超出版面、壓到頁尾。
本節點是第一次實際執行後新增的（見 wiki/log.md）。
用法：python3 pipeline/check_visual.py [報告路徑]
"""
import asyncio, sys, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
SHOTS = ROOT / "pipeline/reports/shots"

async def main():
    SHOTS.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        await pg.goto((ROOT / "slides/index.html").as_uri()); await pg.wait_for_timeout(800)
        n = await pg.evaluate("slides.length"); errors = []
        for i in range(n):
            await pg.evaluate(f"show({i})")
            if await pg.evaluate("!!document.querySelector('.slide.on #stepBtn')"):
                await pg.evaluate("for(let k=0;k<20;k++) step()")   # 把互動跑完再量
            await pg.wait_for_timeout(120)
            bottom, foot = await pg.evaluate("""()=>{const s=document.querySelector('.slide.on');
              const f=document.querySelector('footer').getBoundingClientRect().top;let m=0;
              s.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.height>0)m=Math.max(m,r.bottom)});return [m,f]}""")
            if bottom > foot + 1:
                errors.append(f"V1 第 {i+1} 張內容超出版面：內容底部 {bottom:.0f}px > 頁尾 {foot:.0f}px")
            blocked = await pg.evaluate("""()=>[...document.querySelectorAll('.slide.on button')].filter(b=>{
              const r=b.getBoundingClientRect(),e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
              return e && !b.contains(e)}).map(b=>b.textContent)""")
            for t in blocked:
                errors.append(f"V2 第 {i+1} 張按鈕「{t}」被其他元素蓋住，點不到")
            await pg.screenshot(path=str(SHOTS / f"s{i+1:02d}.png"))
        await b.close()
    out = "\n".join([f"視覺檢查：{n} 張投影片（1280×720）", f"錯誤數：{len(errors)}"] + errors)
    print(out)
    if len(sys.argv) > 1: pathlib.Path(sys.argv[1]).write_text(out + "\n", encoding="utf-8")
    return 1 if errors else 0
sys.exit(asyncio.run(main()))
