---
title: Agent 的組成元件
sources: [S3, S5, S6]
updated: 2026-11-23
---
# Agent 的組成元件

## 觀點一：大腦＋三大元件（Lilian Weng）
- LLM 是 agent 的大腦，另外搭配三個元件：**規劃、記憶、工具使用**。[S3]
- **規劃**：把大任務拆成子目標（Chain of Thought「一步一步想」、Tree of Thoughts 同時探索多條思路），並透過自我反思修正過去的動作（ReAct、Reflexion）。[S3]
- **記憶**：短期記憶＝放在 context window 裡的內容（in-context learning），受長度限制；長期記憶＝外部向量資料庫，需要時再檢索。[S3]
- 長期記憶的快速檢索常用近似最近鄰演算法，例如 LSH、HNSW、FAISS、ScaNN。[S3]
- **工具使用**：呼叫外部 API 取得模型本身沒有的資訊或能力；例如 MRKL 讓 LLM 把問題轉給計算機等專家模組。[S3]
- MRKL 實驗發現 LLM 不一定抽得出正確的參數 → 「何時用、怎麼用工具」本身就是能力。[S3]

## 觀點二：Model / Tools / Instructions（OpenAI）
- **Model**：負責推理與決策的 LLM。[S6]
- **Tools**：agent 用來行動的外部函式或 API；沒有 API 的舊系統可以用 computer-use 模型操作畫面。[S6]
- **Instructions**：明確的行為準則與護欄。[S6]
- 工具三類：**資料類**（查資料庫、讀 PDF、搜尋網路）、**行動類**（寄信、更新紀錄、轉交真人）、**協調類**（把其他 agent 當工具）。[S6]

## 觀點三：Augmented LLM（Anthropic）
- 最基本的積木是「增強版 LLM」：LLM＋檢索＋工具＋記憶，並給它清楚、文件完整的介面。[S5]

## 三種觀點怎麼對應
- 三者其實說的是同一件事：一個會推理的模型，加上取得資訊與採取行動的能力，再加上規則。[綜合: S3,S5,S6]

## 相關頁面
- [Agent Loop 與 ReAct](agent-loop-react.md)、[護欄與人工介入](guardrails-and-human.md)
