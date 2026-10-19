#!/usr/bin/env python3
"""Canonical notes navigation; preserves the existing pharmacology and slide tools."""
from pathlib import Path
from html import escape
import re,json
R=Path(__file__).resolve().parents[1]
CSS="""*{box-sizing:border-box}body{margin:0;background:#fff;color:#263445;font:16px/1.7 -apple-system,BlinkMacSystemFont,'PingFang TC',sans-serif}main{max-width:980px;margin:auto;padding:32px 24px 64px}header{padding:18px 24px;border-bottom:1px solid #dde4e9}header>div{max-width:932px;margin:auto}nav{display:flex;gap:18px;flex-wrap:wrap;font-size:13px}a{color:var(--accent,#53677c);text-decoration:none}a:hover{text-decoration:underline}a:focus-visible{outline:3px solid #b3a4bb;outline-offset:4px}h1{font-size:27px;font-weight:550;margin:12px 0 3px}header p{font-size:14px;color:#71808d;margin:0}.row{display:flex;align-items:center;justify-content:space-between;gap:24px;padding:24px 0;border-bottom:1px solid #dde4e9}.row h2{font-size:21px;font-weight:550;margin:0 0 4px}.row p{color:#71808d;font-size:14px;margin:0}.row>a{padding:10px 0;min-height:44px;white-space:nowrap}.pending{font-size:13px;color:#8a929b}.muted{font-size:14px;color:#71808d}footer{font-size:13px;color:#71808d;margin-top:30px}@media(max-width:600px){main{padding:22px 18px}header{padding:16px 18px}h1{font-size:24px}.row{align-items:flex-start;gap:12px}.row h2{font-size:19px}}"""
def write(p,s):
 f=R/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(s)
def row(title,desc,url=None):return '<section class="row"><div><h2>'+escape(title)+'</h2><p>'+escape(desc)+'</p></div>'+(f'<a href="{escape(url)}">開啟 →</a>'if url else'<span class="pending">準備中</span>')+'</section>'
def page(p,title,body,crumbs,desc='',subject=''):
 accent={'pathology':'#69758f','pharmacology':'#506e84'}.get(subject,'#53677c');nav=''.join(f'<a href="{escape(url)}">{escape(label)}</a>'for label,url in crumbs)
 write(p,f'<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}｜學習筆記</title><style>{CSS}</style><body style="--accent:{accent}"><header><div><nav aria-label="位置">{nav}</nav><h1>{escape(title)}</h1><p>{escape(desc)}</p></div></header><main>{body}</main></body></html>')
def alias(p,target):
 write(p,'<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>學習筆記</title><p><a href="'+target+'">前往新版入口</a></p><script>location.replace('+json.dumps(target)+'+location.search+location.hash)</script></html>')
page('index.html','學習筆記',row('病理 Pathology','正課與實驗','pathology/')+row('藥理 Pharmacology','機轉、藥物比較與複習','pharmacology/'),[],desc='選擇科目，進入本學期的學習內容。')
page('pathology/index.html','病理',row('正課','課程學習與複習測驗','lecture/')+row('實驗','切片導讀與認片練習','lab/'),[('筆記首頁','../')],subject='pathology')
for kind,label,desc in [('lecture','正課','整合課程'),('lab','實驗','病理切片')]:
 page(f'pathology/{kind}/index.html','病理・'+label,row('115-1',desc,'115-1/'),[('筆記首頁','../../'),('病理','../')],subject='pathology')
page('pathology/lecture/115-1/index.html','病理正課・115-1',row('Block 1','尚未整理')+row('Block 2','感染系統與腫瘤學概論','2/'),[('筆記首頁','../../../'),('病理','../../'),('正課','../')],subject='pathology')
page('pathology/lecture/115-1/2/index.html','病理正課・Block 2',row('感染性疾病總論','五個主題','00-Overview.html')+row('複習測驗','課後、間隔與考前複習','review.html')+row('後續單元','待逐堂核對後加入'),[('筆記首頁','../../../../'),('病理','../../../'),('正課','../../'),('115-1','../')],subject='pathology')
lab=''.join(row(f'第 {i} 次切片考試','切片導讀與認片練習',f'https://zi-yiii.github.io/pathology/micro/115-1/{i}/')for i in (1,2,3))
page('pathology/lab/115-1/index.html','病理實驗・115-1',lab,[('筆記首頁','../../../'),('病理','../../'),('實驗','../')],desc='依切片考試次數分類。',subject='pathology')
# Existing bookmarked semester route remains useful, with an explicit choice.
page('pathology/115-1/index.html','病理・115-1',row('正課','整合課程','../lecture/115-1/')+row('實驗','病理切片','../lab/115-1/'),[('筆記首頁','../../'),('病理','../')],subject='pathology')
page('pharmacology/index.html','藥理',row('115-1','機轉與藥物速查','115-1/'),[('筆記首頁','../')],subject='pharmacology')
page('pharmacology/115-1/index.html','藥理・115-1',row('Block 1','預留內容')+row('Block 2','機轉與藥物速查','2/'),[('筆記首頁','../../'),('藥理','../')],subject='pharmacology')
# Only the audited, source-free first lecture and its self-authored quiz are published.
S=R.parents[1]/'01_課程/01_整合課程/Block 2/05_學習輸出/病理複習媒介/第一版'
D=R/'pathology/lecture/115-1/2'
for name in ['00-Overview.html','quiz-overview.html']:
 s=(S/name).read_text().replace('本機試讀版，尚未上線。','').replace('<a href="index.html">← 病理首頁</a>','<a href="index.html">← Block 2</a>')
 if name=='quiz-overview.html':s=s.replace('href="review.html">← 複習測驗','href="index.html">← Block 2')
 (D/name).write_text(s)
alias('pathology/lecture/115-1/2/review.html','quiz-overview.html')
print('Navigation and audited lecture ready')
