import tempfile, json, unittest
from pathlib import Path
from datetime import datetime, timezone
import mcp_consent_prompt_replay_auditor as m
class T(unittest.TestCase):
 def test_flags(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d); (p/'pol.json').write_text(json.dumps({'allowed_tools':[],'consent_ttl_hours':1}))
   (p/'log.jsonl').write_text('{"server":"s","tool":"t","scopes":["filesystem.write"]}\n')
   out=m.audit(p/'log.jsonl',p/'pol.json',datetime(2026,1,1,tzinfo=timezone.utc))
   self.assertEqual(out[0]['status'],'review')
if __name__=='__main__': unittest.main()
