# mcp-consent-prompt-replay-auditor-20260730

Replay MCP tool-call logs against a consent policy to find stale approvals, missing prompt receipts, and unallowlisted tools.

## Pain point
MCP and CLI integrations are spreading quickly, but consent dialogs are hard to audit after the fact. A log can show that a dangerous tool ran, yet not whether the human saw the right prompt.

## Why now
Security discussions around MCP consent bypasses, hidden PR comments, and enterprise agent tool harnesses are prominent in current developer news.

## Install / run
```bash
python mcp_consent_prompt_replay_auditor.py --log examples/mcp_calls.jsonl --policy examples/policy.json
```

## Example
The example flags an expired approval and a high-risk filesystem write without prompt text.

## Self-check
```bash
python -m unittest discover -s tests
```

## Roadmap
- Import Claude/Codex/OpenCode style session logs.
- Produce SARIF and GitHub Actions annotations.
- Model multi-step consent replay windows.
