---
title: Agent Loop 與 ReAct
sources: [S2, S3, S4, S5, S6]
updated: 2026-11-23
---
# Agent Loop 與 ReAct

## ReAct：想一下、做一下、看結果
- 過去「推理」（如 chain-of-thought）和「行動」（如產生行動計畫）大多被分開研究。[S4]
- ReAct 把推理軌跡（Thought）和實際行動（Action）**交錯進行**，再讀取行動結果（Observation）。[S4]
- 推理幫助模型建立、追蹤、更新計畫並處理例外；行動讓模型從外部（知識庫、環境）取得新資訊。[S4]
- 在 HotpotQA、FEVER 上，ReAct 透過簡單的 Wikipedia API 查資料，減少了 chain-of-thought 的幻覺與錯誤累積。[S4]
- 在 ALFWorld 與 WebShop 上，成功率比模仿學習／強化學習方法分別絕對提升 34% 與 10%，而且只用一兩個範例提示。[S4]
- ALFWorld 是文字遊戲，WebShop 是網頁操作任務（兩者都是互動決策任務）。[S4]

## 把 ReAct 寫成程式：multi-step loop
- smolagents 給出的最小迴圈（記憶不斷累積「動作＋觀察」）：[S2]

```python
memory = [user_defined_task]
while llm_should_continue(memory):          # 要不要繼續？由 LLM 決定
    action = llm_get_next_action(memory)    # 下一步做什麼？（tool call）
    observations = execute_action(action)   # 真的去執行
    memory += [action, observations]        # 把結果記下來
```

- 原始程式沒有 `thought` 變數；Thought 發生在 `llm_get_next_action` 這一步：LLM 先推理，再決定 action。教學時以註解補充，不改原始程式。[綜合: S2,S4]

## 迴圈什麼時候停？
- 常見的結束條件：呼叫了「最終輸出」工具、模型回覆時不再呼叫工具、發生錯誤、達到最大回合數。[S6]
- 自主 agent 通常就是「LLM 在迴圈中使用工具」，並設停止條件如最大迭代次數；每一步都從環境取得「真實結果」（工具結果、程式執行結果）。[S5]

## 要做成框架需要什麼
- 一旦有工具呼叫或多步迴圈，就需要：解析輸出格式、記憶、錯誤處理（記錄與重試）。[S2]
- 自主 agent 早期案例 AutoGPT 有很大比例程式碼是在解析模型輸出，可靠度是問題。[S3]

## 相關頁面
- [Agent 的組成元件](agent-components.md)、[挑戰與限制](challenges.md)
