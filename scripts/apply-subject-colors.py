from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
# Reusable color normalization; no font prototype or chooser is published.
for subject,c in [('pathology','#637b90'),('pharmacology','#507b78')]:
 for p in (R/subject).rglob('*.html'):
  if 'notes' in p.parts:continue
  s=p.read_text()
  if 'location.replace' in s:continue
  patch=f'<style data-subject-palette>:root{{--accent:{c};--purple:{c}}}a,.site-nav a{{color:{c}}}h2,.members h2{{color:{c}}}.drug{{fill:{c}}}.topic-tabs button[aria-selected="true"]{{color:{c};border-color:{c}}}</style>'
  s=re.sub(r'<style data-subject-palette>.*?</style>','',s,flags=re.S)
  s=s.replace('</style>','</style>'+patch,1)
  s=re.sub(r'<a[^>]+href=[\"\'][^\"\']*(?:review|quiz)[^\"\']*[\"\'][^>]*>.*?</a>', '',s,flags=re.S)
  p.write_text(s)
print('Quiz entries removed; palettes applied')
