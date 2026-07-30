#!/usr/bin/env python
"""Replay MCP tool calls against a simple consent policy and flag missing or stale approvals."""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone, timedelta

def dt(s):
    if not s: return None
    try:
        x=datetime.fromisoformat(str(s).replace('Z','+00:00'))
        return x if x.tzinfo else x.replace(tzinfo=timezone.utc)
    except ValueError: return None

def load_jsonl(path):
    with open(path,encoding='utf-8') as f:
        for i,line in enumerate(f,1):
            line=line.strip()
            if line: yield i,json.loads(line)

def audit(log_path, policy_path, now=None):
    policy=json.load(open(policy_path,encoding='utf-8'))
    ttl_hours=int(policy.get('consent_ttl_hours',24))
    allowed={(x['server'],x['tool']) for x in policy.get('allowed_tools',[])}
    risky=set(policy.get('high_risk_scopes',['filesystem.write','network.external','secrets.read']))
    now=now or datetime.now(timezone.utc)
    findings=[]
    for line,e in load_jsonl(log_path):
        server=e.get('server',''); tool=e.get('tool',''); scopes=set(e.get('scopes',[]))
        approved=dt(e.get('approved_at'))
        reasons=[]
        if (server,tool) not in allowed: reasons.append('tool is not in policy allowlist')
        if not approved: reasons.append('call has no approved_at timestamp')
        elif now-approved>timedelta(hours=ttl_hours): reasons.append(f'approval older than {ttl_hours}h')
        if scopes & risky and not e.get('human_prompt_text'):
            reasons.append('high-risk scope lacks captured human consent prompt text')
        status='pass' if not reasons else 'review'
        findings.append({'line':line,'status':status,'server':server,'tool':tool,'scopes':sorted(scopes),'reasons':reasons})
    return findings

def main(argv=None):
    ap=argparse.ArgumentParser(description='Replay MCP calls and audit whether consent prompts would still be valid.')
    ap.add_argument('--log', required=True); ap.add_argument('--policy', required=True)
    ap.add_argument('--format', choices=['json','table'], default='table')
    args=ap.parse_args(argv)
    out=audit(args.log,args.policy)
    if args.format=='json': print(json.dumps(out,indent=2))
    else:
        print('status server tool reasons')
        for f in out: print(f"{f['status']} {f['server']} {f['tool']} {'; '.join(f['reasons']) or '-'}")
    return 1 if any(f['status']=='review' for f in out) else 0
if __name__=='__main__': raise SystemExit(main())
