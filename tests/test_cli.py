import tempfile, json, unittest
from pathlib import Path
from datetime import datetime, timezone, timedelta
import mcp_consent_prompt_replay_auditor as m
class T(unittest.TestCase):
 def test_flags(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d); (p/'pol.json').write_text(json.dumps({'allowed_tools':[],'consent_ttl_hours':1}))
   (p/'log.jsonl').write_text('{"server":"s","tool":"t","scopes":["filesystem.write"]}\n')
   out=m.audit(p/'log.jsonl',p/'pol.json',datetime(2026,1,1,tzinfo=timezone.utc))
   self.assertEqual(out[0]['status'],'review')
 def test_future_approval_requires_review(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d); now=datetime(2026,1,1,tzinfo=timezone.utc)
   (p/'pol.json').write_text(json.dumps({'allowed_tools':[{'server':'s','tool':'t'}]}))
   event={'server':'s','tool':'t','approved_at':(now+timedelta(minutes=1)).isoformat()}
   (p/'log.jsonl').write_text(json.dumps(event))
   out=m.audit(p/'log.jsonl',p/'pol.json',now)
   self.assertEqual(out[0]['status'],'review')
   self.assertIn('future',out[0]['reasons'][0])
if __name__=='__main__': unittest.main()
