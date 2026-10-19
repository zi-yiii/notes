#!/usr/bin/env python3
"""Publish only reviewed study HTML; never copy course source materials."""
from pathlib import Path
import argparse, html, re
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--mechanism-source',type=Path);args=p.parse_args()
repo=Path(__file__).resolve().parents[1]
CSS=":root{--ink:#263445;--muted:#71808d;--line:#dde4e9;--paper:#fff;--card:#fff;--purple:#506e84;--deep:#fff;--wash:#f2f6f8}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 'Helvetica Neue',Helvetica,Arial,'PingFang TC',sans-serif}header{background:#fff;color:var(--ink);border-bottom:1px solid var(--line);padding:18px 24px}header h1{font-size:23px;font-weight:500;margin:8px 0 2px}header p{color:var(--muted);font-size:13px;margin:0}nav{display:flex;gap:18px;flex-wrap:wrap;font-size:13px}nav a{color:#53677c;text-decoration:none;min-height:28px}main{max-width:980px;margin:auto;padding:32px 24px 60px}h2{font-size:20px;font-weight:500;margin:0 0 20px}a{color:var(--purple);text-decoration:none}a:hover{text-decoration:underline}a:focus-visible{outline:3px solid #af99c6;outline-offset:4px}.rows{display:grid;gap:0}.row{padding:20px 0;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:18px}.row h3{font-size:20px;font-weight:500;margin:0 0 3px}.row p{font-size:14px;color:var(--muted);margin:0}.links{display:flex;gap:18px;flex-wrap:wrap}.pending{color:var(--muted);font-size:13px}.eyebrow{font-size:12px;color:var(--muted);margin:24px 0 10px}@media(max-width:600px){header{padding:16px}main{padding:24px 16px}.row{align-items:flex-start;flex-direction:column;gap:10px}.row h3{font-size:19px}}"
COLORS={'pharmacology':'#506e84','pathology':'#69758F'}
def link(url,label):return '<a href="'+html.escape(url)+'">'+html.escape(label)+'</a>'
def page(title,body,nav='',subject=''):
 return '<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>'+CSS+':root{--purple:'+COLORS.get(subject,'#53677c')+'}</style><header><nav>'+nav+'</nav><h1>'+title+'</h1></header><main>'+body+'</main></html>'
def write(path,text):
 target=repo/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
def row(title,desc,url=None,label='Open · 開啟'):
 return '<div class="row"><div><h3>'+title+'</h3><p>'+desc+'</p></div>'+(link(url,label) if url else '<span class="pending">Reserved · 預留</span>')+'</div>'
def redirect(path,target):
 write(path,'<!doctype html><meta charset="utf-8"><title>Moved</title><a href="'+target+'">Open updated page</a><script>location.replace('+repr(target)+'+location.search+location.hash)</script>')
units=[('Autacoids · 自泌素','01-自泌素'),('Antibiotics · 抗生素','02-抗生素'),('NSAIDs & gout · 非類固醇抗炎與痛風','03-NSAIDs與痛風'),('Adrenal corticosteroids · 腎上腺類固醇','04-腎上腺類固醇'),('Antifungal agents · 抗黴菌藥','05-抗黴菌藥'),('Antiviral agents · 抗病毒藥','06-抗病毒藥'),('Immunotherapy · 免疫療法','07-免疫療法'),('Antiparasitic agents · 抗寄生蟲藥物','08-抗寄生蟲藥物')]
nav=link('../../../','Notes')+link('../../','Pharmacology')+link('../','115-1')+link('./','Block 2')
navcss='.site-nav{display:flex;gap:20px;flex-wrap:wrap;padding:12px 24px;border-bottom:1px solid #dde4e9;font:13px/1.6 Helvetica,Arial,sans-serif}.site-nav a{color:#506e84;text-decoration:none}.embed .site-nav{display:none}'
for src in args.source.glob('*.html'):
 if src.name=='開始複習.html':continue
 if args.mechanism_source and src.name[:2].isdigit() and '藥物速查' not in src.name and (args.mechanism_source/src.name).exists():src=args.mechanism_source/src.name
 text=src.read_text().replace('開始複習.html','index.html').replace('#71549a','#506e84').replace('#f6f3fa','#f2f6f8')
 text=text.replace('</style>',navcss+'</style>',1)
 text=text.replace('<body>','<body><nav class="site-nav">'+nav+'</nav>',1)
 # Some standalone documents use body attributes.
 if '<nav class="site-nav">' not in text:text=re.sub(r'(<body[^>]*>)',lambda m:m[1]+'<nav class="site-nav">'+nav+'</nav>',text,count=1)
 if '<nav class="site-nav">' not in text:text=text.replace('</style>','</style><nav class="site-nav">'+nav+'</nav>',1)
 write(Path('pharmacology/115-1/2')/src.name,text)
 redirect(Path('pharmacology/2')/src.name,'../115-1/2/'+src.name)
body=''.join(row(t,'',name+'.html','Mechanisms · 機轉')[:-6]+'<span class="links">'+link(name+'-藥物速查.html','Drug reference · 藥物速查')+'</span></div>' for t,name in units)
write(Path('pharmacology/115-1/2/index.html'),page('Pharmacology · Block 2',body,nav,'pharmacology'))
redirect(Path('pharmacology/2/index.html'),'../115-1/2/')
write(Path('pharmacology/115-1/1/index.html'),page('Pharmacology · Block 1',row('Reserved · 預留','之後補入本單元內容。'),link('../../../','Notes')+link('../../','Pharmacology')+link('../','115-1'),'pharmacology'))
redirect(Path('pharmacology/1/index.html'),'../115-1/1/')
write(Path('pharmacology/115-1/index.html'),page('Pharmacology · 115-1',row('Block 1','預留內容','1/')+row('Block 2','Mechanisms & drug reference · 機轉與藥物速查','2/'),link('../../','Notes')+link('../','Pharmacology'),'pharmacology'))
for subject,title in [('pharmacology','Pharmacology · 藥理'),('pathology','Pathology · 病理')]:
 write(Path(subject)/'index.html',page(title,row('115-1','課程複習','115-1/'),link('../','Notes'),subject))
body=''.join(row('Micro · 第'+str(i)+'次切片考試','Pathology slide practice · 病理切片','https://zi-yiii.github.io/pathology/micro/115-1/'+str(i)+'/') for i in (1,2,3))
write(Path('pathology/115-1/index.html'),page('Pathology · 115-1',body,link('../../','Notes')+link('../','Pathology'),'pathology'))
body=row('Pathology · 病理','115-1 · 切片複習','pathology/')+row('Pharmacology · 藥理','115-1 · Block 2','pharmacology/')+row('Clinical medicine · 臨床醫學','')+row('Laboratory medicine · 檢驗醫學','')+row('Master tables · 總表','跨科整合，之後補入')
write(Path('index.html'),page('Study notes · 學習筆記',body))
print('Published HTML prepared:',len(list((repo/'pharmacology/115-1/2').glob('*.html'))))

# Reapply the approved canonical site hierarchy after syncing course HTML.
import runpy
runpy.run_path(str(repo/'scripts/build-navigation.py'),run_name='__main__')
