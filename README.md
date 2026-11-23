# 用 LLM Wiki 做一份教學 HTML 簡報：AI Agents

網站：<https://a0900067499-pixel.github.io/llm-wiki-ai-agents/>

## 1. LLM Wiki 主題與簡介

**主題：AI Agents。** 依照 Karpathy 的 LLM Wiki 模式，把 6 篇關於 AI Agents 的資料 ingest 成一個由 LLM 維護、互相連結的 markdown 知識庫。內容涵蓋：定義、代理程度光譜、組成元件、Agent Loop／ReAct、Workflow vs Agent、五種設計模式、何時該用、護欄與人工介入、挑戰。

- 三層結構：`raw/`（原始筆記，不可改）→ `wiki/`（LLM 維護的概念頁與來源頁）→ `CLAUDE.md`（規則檔）
- 每條事實都標來源 `[S1]`–`[S6]`，可以一路追回 raw
- 採「先討論、後生成」：先把 6 篇的重點、2 個來源矛盾、Wiki 結構整批列出來討論，我決定後才生成；簡報初稿完成後，再以「新手看不看得懂」做第二輪討論（紀錄在 `wiki/log.md`）

| 編號 | 來源 |
|---|---|
| S1 | Hugging Face Agents Course〈What is an Agent?〉 |
| S2 | smolagents〈Introduction to Agents〉 |
| S3 | Lilian Weng〈LLM Powered Autonomous Agents〉(2023) |
| S4 | Yao et al.〈ReAct: Synergizing Reasoning and Acting in Language Models〉(ICLR 2023) |
| S5 | Anthropic〈Building Effective Agents〉(2024) |
| S6 | OpenAI〈A Practical Guide to Building Agents〉 |

## 2. LLM Wiki 連結

- 10 個概念頁（含術語小辭典）、6 個來源頁
- Wiki 索引：<https://a0900067499-pixel.github.io/llm-wiki-ai-agents/wiki/index.html>
- 原始 markdown（repo 內）：`wiki/`、`raw/`、`CLAUDE.md`

## 3. 教學 HTML 簡報

<https://a0900067499-pixel.github.io/llm-wiki-ai-agents/slides/>

共 17 張，結構為：比喻 → 定義 → 構造 → 運作 → 選擇（workflow 還是 agent）→ 設計模式 → 風險 → 小測驗 → 回顧。術語第一次出現時都附白話說明。每張頁尾都連回它所根據的 Wiki 頁。第 9 張可以一步一步執行 agent loop，第 16 張是互動小測驗。用鍵盤 ← → 或頁尾按鈕翻頁。

## 4. Loop / Graph 設計

取得資料 → 討論確認（人）→ Ingest → 編譯 Wiki ⇄ Wiki lint → 查詢 Wiki 產生大綱 ⇄ 大綱檢查 → 逐張生成投影片 ⇄ 內容檢查 → 視覺檢查 → 發布

流程圖與完整說明：<https://a0900067499-pixel.github.io/llm-wiki-ai-agents/docs/process.html>

## 5. 實際執行與檢查紀錄

- 執行紀錄表與截圖：見上面流程頁第 4 節
- 每次檢查的原始輸出：<https://a0900067499-pixel.github.io/llm-wiki-ai-agents/pipeline/reports/>
- 檢查程式：`pipeline/lint_wiki.py`、`check_outline.py`、`check_slides.py`、`check_visual.py`

重現方式：

```
python3 pipeline/lint_wiki.py
python3 pipeline/check_outline.py
python3 pipeline/check_slides.py
python3 pipeline/check_visual.py   # 需要 playwright 與 Chrome
python3 pipeline/build_site.py     # 把 .md 轉成 .html
```

## 6. 反思（摘要）

- **最常出錯的節點：生成投影片（N7）。** 第一次內容檢查有 19 個錯：18 個是投影片借用了沒宣告的 Wiki 頁，1 個是捏造的測驗選項。視覺檢查另外發現 10 張超出版面，還有 1 個按鈕被文字蓋住、點不到。
- **把檢查往前移：** 對應頁的宣告和版面預算移到「大綱」階段；內容檢查從整份寫完改成逐張檢查。
- **第二輪討論：** 檢視簡報初稿後，發現「新手看不懂的術語」是原本的檢查都抓不到的。所以新增術語小辭典，並加上 C6 術語門檻檢查，把這個問題也變成自動檢查。
- **修改 graph：** 新增「視覺檢查」節點，因為按鈕點不到這種錯，文字檢查看不出來。另外把生成迴圈改成逐張進行，讓重做的範圍變小。
