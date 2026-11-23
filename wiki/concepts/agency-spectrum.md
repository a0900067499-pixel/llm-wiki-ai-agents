---
title: 代理程度光譜（Agency Spectrum）
sources: [S1, S2]
updated: 2026-11-23
---
# 代理程度光譜

- 「是不是 agent」不是二分法，而是一個連續光譜：看 LLM 對流程有多少控制權。[S2]

| 星等 | 名稱 | LLM 的輸出控制了什麼 | 範例程式 |
|---|---|---|---|
| ☆☆☆ | Simple processor | 不影響流程 | `process_llm_output(llm_response)` |
| ★☆☆ | Router | 一個 if/else 分支 | `if llm_decision(): path_a() else: path_b()` |
| ★★☆ | Tool call | 要執行哪個函式 | `run_function(llm_chosen_tool, llm_chosen_args)` |
| ★★☆ | Multi-step agent | 是否繼續下一輪 | `while llm_should_continue(): execute_next_step()` |
| ★★★ | Multi-agent | 一個 agent 可以啟動另一個 | `if llm_trigger(): execute_agent()` |
| ★★★ | Code agent | 用程式碼行動、自己定義工具 | `def custom_tool(args): ...` |

- 上表依 smolagents 原文整理。[S2]

## ⚠ 矛盾與註記
- HF 課程的表格把 Multi-step agent 標為 ★★★，並註明表格取自 smolagents；但 smolagents 原文標 ★★☆。[綜合: S1,S2]
- 處理：以原始出處 S2 為準，保留本註記（討論後決定）。[綜合: S1,S2]

## 相關頁面
- [什麼是 AI Agent](what-is-an-agent.md)、[Workflow vs Agent](workflow-vs-agent.md)
