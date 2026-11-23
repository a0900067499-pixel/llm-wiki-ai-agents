# 簡報大綱（N5 query 產物：只讀 wiki/ 產生）

觀眾：有一點程式基礎的初學者。教學結構：引起動機 → 定義 → 構造 → 運作 → 設計 → 判斷 → 風險 → 檢核 → 總結。

| # | 段落 | 投影片標題 | 學習目標 | 對應 Wiki 頁 |
|---|---|---|---|---|
| 1 | 開場 | AI Agents 是什麼？ | — | wiki/overview.md |
| 2 | 開場 | 今天的學習目標 | 知道今天要學什麼 | wiki/index.md, wiki/overview.md |
| 3 | 動機 | 從管家 Alfred 說起 | 用比喻理解 agent 在做什麼 | concepts/what-is-an-agent.md |
| 4 | 定義 | Agent 的定義與「不是 agent」 | 能說出定義並分辨反例 | concepts/what-is-an-agent.md |
| 5 | 構造 | 大腦＋規劃、記憶、工具 | 說出 agent 的組成元件 | concepts/agent-components.md |
| 6 | 構造 | 工具三類與 Instructions | 分辨資料／行動／協調類工具 | concepts/agent-components.md |
| 7 | 定義 | 代理程度光譜 | 理解 agent 是程度問題 | concepts/agency-spectrum.md |
| 8 | 運作 | ReAct：想、做、看 | 理解 Thought→Action→Observation | concepts/agent-loop-react.md |
| 9 | 運作 | 把迴圈寫成程式（互動示意） | 看懂 agent loop 虛擬碼與結束條件 | concepts/agent-loop-react.md, concepts/what-is-an-agent.md |
| 10 | 設計 | Workflow vs Agent | 分辨兩者，舉衝浪例子 | concepts/workflow-vs-agent.md |
| 11 | 設計 | 五種設計模式 | 認得五種模式 | concepts/design-patterns.md |
| 12 | 設計 | 多代理：Manager 與 Handoff | 知道何時拆成多 agent | concepts/design-patterns.md |
| 13 | 判斷 | 何時該用 agent？ | 用三個訊號判斷 | concepts/when-to-use-agents.md |
| 14 | 風險 | 護欄與人工介入 | 列出常見護欄與介入時機 | concepts/guardrails-and-human.md |
| 15 | 風險 | 挑戰與限制 | 知道 agent 的弱點 | concepts/challenges.md |
| 16 | 檢核 | 小測驗 | 自我檢查 | 多頁（每題標註） |
| 17 | 總結 | 重點回顧與延伸閱讀 | 帶走 5 個重點 | wiki/overview.md, wiki/index.md |

## 覆蓋檢查要求（N6）
- 9 個概念頁每頁至少被 1 張投影片使用。
- 每張投影片只能用它對應的 wiki 頁內容；需要 wiki 沒有的內容 → 記為「缺口」，回 N3 補 wiki。
