# mcp-consent-prompt-replay-auditor-20260730

根据策略回放 MCP 工具调用日志，发现过期授权、缺少提示记录、未在 allowlist 中的工具。

## 痛点
MCP/CLI 集成快速普及，但事后很难证明用户是否看到了正确的授权提示。

## 为什么现在值得做
近期开发者社区持续讨论 MCP consent bypass、隐藏 PR 评论劫持 Agent、企业级工具 harness 安全。

## 安装/运行
```bash
python mcp_consent_prompt_replay_auditor.py --log examples/mcp_calls.jsonl --policy examples/policy.json
```

## 示例
示例会标记过期授权，以及没有人类提示文本的高风险写文件调用。

## 路线图
- 导入 Claude/Codex/OpenCode 会话日志。
- 输出 SARIF/GitHub Actions 注释。
- 支持多步授权窗口建模。
