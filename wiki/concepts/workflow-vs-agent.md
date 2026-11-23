---
title: Workflow vs Agent
sources: [S2, S5]
updated: 2026-11-23
---
# Workflow vs Agent

- Anthropic 把兩者統稱為 **agentic systems**，但在架構上區分：[S5]
- **Workflow**：用「預先寫好的程式路徑」來編排 LLM 與工具。[S5]
- **Agent**：讓 LLM **自己動態決定**流程與工具使用，掌握怎麼完成任務。[S5]
- Workflow 適合定義清楚、需要可預測性的任務；agent 適合需要彈性、由模型做決策的情境。[S5]

## 衝浪旅行社的例子
- 顧客只有兩種需求（想知道行程資訊／想找業務）→ 固定流程就夠：一個搜尋框加一個聯絡表單。[S2]
- 顧客說「我週一能到，但忘了護照可能延到週三，能不能週二早上帶我和裝備去衝浪，還要取消險？」→ 條件太多、無法事先寫死，需要 multi-step agent 搭配天氣 API、地圖 API、員工排班表、知識庫 RAG。[S2]
- 判斷法則：**預先寫好的流程太常不夠用時，才需要更多彈性**。[S2]

## 相關頁面
- [代理程度光譜](agency-spectrum.md)、[五種設計模式](design-patterns.md)、[何時該用 Agent](when-to-use-agents.md)
