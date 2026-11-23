---
title: 總覽
sources: [S1, S2, S3, S4, S5, S6]
updated: 2026-11-23
---
# 總覽：AI Agents 是什麼？

- LLM（大型語言模型）是輸入文字、輸出文字的 AI 模型，例如 GPT-4；在 agent 裡當作大腦。→ [術語小辭典](concepts/glossary.md) [S1]
- AI agent 是讓 LLM 不只「回答」，而是「決定下一步做什麼、用工具去做、看結果再決定」的系統。[綜合: S1,S2,S6]
- 是不是 agent 是程度問題：LLM 控制的流程越多，代理程度越高。→ [代理程度光譜](concepts/agency-spectrum.md) [S2]
- 組成：會推理的模型＋規劃＋記憶＋工具＋指令／護欄。→ [組成元件](concepts/agent-components.md) [綜合: S3,S5,S6]
- 運作核心是迴圈：Thought → Action → Observation，直到滿足結束條件。→ [Agent Loop 與 ReAct](concepts/agent-loop-react.md) [綜合: S2,S4,S6]
- 不是所有事都需要 agent：流程固定用 workflow；要彈性才用 agent。→ [Workflow vs Agent](concepts/workflow-vs-agent.md)、[何時該用](concepts/when-to-use-agents.md) [綜合: S2,S5,S6]
- 常見架構從 prompt chaining 到 evaluator-optimizer 共五種，再往上是多代理。→ [設計模式](concepts/design-patterns.md) [綜合: S5,S6]
- 風險靠多層護欄與人工介入控制，並面對 context 有限、錯誤累積等挑戰。→ [護欄](concepts/guardrails-and-human.md)、[挑戰](concepts/challenges.md) [綜合: S3,S5,S6]
