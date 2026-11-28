"""Reproducible portfolio UI illustrations. Run with .venv-fonts/bin/python. All content is fictional; no source screenshots."""
from pathlib import Path
from html import escape
from io import BytesIO
import base64
from fontTools.ttLib import TTFont
from fontTools import subset
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'src/assets/cases/public-concepts'
OUT.mkdir(parents=True, exist_ok=True)
INK='#23372c'; MUTED='#68756c'; LINE='#e3e8df'; BG='#f3f5f0'
def rect(x,y,w,h,fill='white',r=12,stroke=None):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'
def t(x,y,s,size=16,fill=INK,weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}">{escape(str(s))}</text>'
def line(x,y,x2,y2,color=LINE):
    return f'<path d="M{x} {y}H{x2}" stroke="{color}"/>' if y==y2 else f'<path d="M{x} {y}L{x2} {y2}" stroke="{color}"/>'
def pill(x,y,s,c='#2e6247',bg='#e7efe5',w=76):
    return rect(x,y,w,28,bg,8)+t(x+12,y+19,s,12,c,600)
def button(y,s,c):
    return rect(24,y,342,52,c,14)+t(195,y+33,s,16,'white',700).replace(f'x="195"', 'x="195" text-anchor="middle"')
def field(y,label,value):
    return t(24,y,label,14,MUTED,600)+rect(24,y+14,342,52,'white',12,LINE)+t(40,y+47,value,16)
def card(y,h,title,sub='',accent='#2e6247'):
    a=rect(24,y,342,h)+t(42,y+32,title,17,INK,700)
    if sub:a+=t(42,y+57,sub,13,MUTED)
    return a
def mobile(name,brand,title,subtitle,content,accent='#2e6247',tab='홈'):
    a=rect(0,0,390,844,BG,0)+rect(0,0,390,100,'white',0)+t(24,29,'9:41',14,INK,600)+t(302,29,'LTE  ▰',12,INK,600)+t(24,76,brand,22,accent,800)+pill(270,52,'DEMO',accent,BG,96)
    a+=t(24,142,title,26,INK,750)+t(24,170,subtitle,14,MUTED)+content
    a+=rect(0,758,390,86,'white',0)+line(0,758,390,758)
    for x,s in zip([42,140,238,336],['홈','기록' if brand=='FIELDNOTE' else '업무','알림','내 정보']):
        a+=rect(x-7,776,14,14,accent if s==tab else '#c5cec0',4)+t(x,816,s,12,accent if s==tab else MUTED,600).replace(f'x="{x}"',f'x="{x}" text-anchor="middle"')
    save(name,390,844,a,'가상의 '+brand+' '+title)

font=TTFont(ROOT/'src/fonts/original/SUIT-Variable.woff2');opt=subset.Options();opt.layout_features=['*'];opt.name_IDs=['*'];ss=subset.Subsetter(options=opt);ss.populate(text=Path(__file__).read_text());ss.subset(font)
for n in font['name'].names:
 if n.nameID in [1,3,4,6,16,17]:
  names={1:'Field UI',3:'FieldUI-SUITSubset-20261124',4:'Field UI Variable',6:'FieldUI-Variable',16:'Field UI',17:'Regular'};n.string=names[n.nameID].encode(n.getEncoding(),errors='replace')
font.flavor='woff2';b=BytesIO();font.save(b);data=base64.b64encode(b.getvalue()).decode();FONT_STYLE=f"<style>@font-face{{font-family:'Field SUIT';font-style:normal;font-weight:100 900;src:url(data:font/woff2;base64,{data}) format('woff2');}}text{{font-family:'Field SUIT',sans-serif;}}</style>"

def save(name,w,h,body,label):
    (OUT/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}"><title>{escape(label)} · 공개용 재설계 · 모든 데이터는 가상</title>{FONT_STYLE}<g>{body}</g></svg>',encoding='utf-8')
# Mobile screens use task-specific list rows, forms and one primary action.
GREEN='#2e6247'; BLUE='#2e6247'; blue=BLUE
def icon(x,y,name,color=MUTED,size=22):
    paths={
      'home':'M3 10 L12 3 L21 10 L21 21 L15 21 L15 14 L9 14 L9 21 L3 21 Z',
      'record':'M7 3 H17 L21 7 V21 H3 V3 H7 M8 10 H16 M8 14 H16 M8 18 H13',
      'bell':'M5 17 V10 C5 1 19 1 19 10 V17 H5 M9 21 H15',
      'user':'M16 7 C16 12 8 12 8 7 C8 2 16 2 16 7 M4 22 C4 12 20 12 20 22',
      'chevron':'M9 5 L16 12 L9 19',
      'check':'M5 12 L10 17 L20 6',
      'room':'M4 21 V3 H20 V21 M9 21 V14 H15 V21 M8 7 H10 M14 7 H16',
      'calendar':'M3 5 H21 V21 H3 Z M7 2 V8 M17 2 V8 M3 11 H21',
      'arrow':'M15 4 L7 12 L15 20',
      'sensor':'M4 4 H20 V20 H4 Z M8 16 V12 M12 16 V8 M16 16 V10',
    }
    return f'<path d="{paths[name]}" transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
def row(y,title,sub,right='',kind='record',color=GREEN):
    return rect(24,y,40,40,'#edf1eb',12)+icon(33,y+9,kind,color)+t(80,y+16,title,16,INK,600)+t(80,y+39,sub,13,MUTED)+(t(366,y+26,right,14,color,600).replace('x="366"','x="366" text-anchor="end"') if right else icon(341,y+10,'chevron','#a6aea3',18))
def info(y,label,value):
    return t(24,y,label,15,MUTED)+t(366,y,value,16,INK,600).replace('x="366"','x="366" text-anchor="end"')
def input_field(y,label,value):
    return t(24,y,label,14,MUTED)+rect(24,y+14,342,56,'#f3f5f0',12)+t(42,y+50,value,17,INK,500)
def header_section(y,title,more=''):
    return t(24,y,title,20,INK,700)+(t(366,y,more,14,MUTED).replace('x="366"','x="366" text-anchor="end"') if more else '')
def mobile(name,brand,title,subtitle,content,accent=GREEN,tab='홈',back=False):
    a=rect(0,0,390,844,'white',0)+t(24,29,'9:41',14,INK,600)+t(306,29,'LTE',12,INK,600)+rect(339,18,22,10,INK,3)
    a+=(icon(24,59,'arrow',INK) if back else t(24,77,brand,20,INK,750))+icon(340,58,'bell',INK)
    a+=t(24,134,title,26,INK,700)+t(24,165,subtitle,15,MUTED)+content
    if not back:
      a+=rect(0,755,390,89,'white',0)+line(0,755,390,755)
      for x,label,kind in [(48,'홈','home'),(146,'기록' if brand=='fieldnote' else '업무','record'),(244,'알림','bell'),(342,'내 정보','user')]:
        color=accent if label==tab else '#929b8e';a+=icon(x-11,772,kind,color)+t(x,813,label,11,color,600).replace(f'x="{x}"',f'x="{x}" text-anchor="middle"')
    a+=rect(132,832,126,4,'#191f28',2)
    save(name,390,844,a,brand+' '+title)
# Safety home: the next action, not an overview dashboard.
a=rect(24,196,342,152,'#eef4eb',20)+pill(44,214,'작성 전',GREEN,'#e4eddf',70)+t(44,276,'모래빛 실증센터',23,INK,700)+t(44,309,'A팀 · 조립 준비 · 참여 9명',15,MUTED)
a+=header_section(396,'작업 전 확인','2 / 3 완료')
for y,title,sub in [(422,'보호구 착용','안전모·안전화 착용을 확인했어요'),(500,'이동 동선 공유','장비 이동 구역을 함께 확인했어요')]:a+=row(y,title,sub,'완료','check',GREEN)
a+=row(578,'작업 구역 정리','아직 확인하지 않은 항목이에요','확인 필요','record','#2e6247')+button(678,'안전 기록 시작하기',GREEN)
mobile('tbm-home','fieldnote','작업 전, 함께 확인해요','4월 18일 · 오전 작업',a)
a=rect(24,194,342,86,'#f3f5f0',16)+t(42,226,'모래빛 실증센터 · A팀',17,INK,600)+t(42,255,'2027. 04. 18  ·  참여 예정 9명',14,MUTED)+header_section(324,'작업 전 확인 항목')
for y,title,sub,done in [(352,'보호구 착용','안전모와 안전화를 확인했어요',True),(437,'이동 동선 공유','장비와 보행자의 동선을 구분했어요',True),(522,'작업 구역 정리','주변의 장애물을 확인해 주세요',False)]:
 a+=rect(25,y+5,25,25,GREEN if done else 'white',8,LINE)+(icon(27,y+7,'check','white',21) if done else '')+t(68,y+20,title,17,INK,600)+t(68,y+48,sub,14,MUTED)
a+=line(24,602,366,602)+info(636,'책임자 확인','확인 대기')+button(716,'기록 내용 작성',GREEN)
mobile('tbm-record','fieldnote','오늘의 안전 기록','확인한 항목을 선택해 주세요.',a,back=True)
a=rect(24,196,342,92,'#f3f5f0',16)+rect(44,216,48,48,'#e1ebdd',24)+icon(57,229,'user',GREEN)+t(110,233,'이도경',18,INK,700)+t(110,260,'안전관리팀 · 기록 담당',14,MUTED)+header_section(337,'기록 확인에 쓸 표시')+t(24,370,'직접 서명 대신 예시 기호를 등록해요.',15,MUTED)+rect(24,400,342,174,'#f6f7f3',16,LINE)+t(195,495,'SAMPLE',30,'#a6aea3',500).replace('x="195"','x="195" text-anchor="middle"')+t(24,609,'등록한 표시는 기록 확인 단계에 사용돼요.',14,MUTED)+button(716,'확인 표시 저장하기',GREEN)
mobile('tbm-profile','fieldnote','내 확인 표시','필요할 때 언제든 바꿀 수 있어요.',a,back=True)
a=rect(158,248,74,74,'#e8efe4',37)+icon(178,268,'check',GREEN,34)+t(195,381,'확인 표시를 저장했어요',25,INK,700).replace('x="195"','x="195" text-anchor="middle"')+t(195,420,'이제 오늘의 안전 기록을 작성할 수 있어요.',15,MUTED).replace('x="195"','x="195" text-anchor="middle"')+rect(24,486,342,104,'#f3f5f0',16)+t(44,527,'오늘의 기록',14,MUTED)+t(44,560,'모래빛 실증센터 · A팀',17,INK,600)+button(716,'안전 기록으로 돌아가기',GREEN)
mobile('tbm-saved','fieldnote','저장 완료','',a,back=True)
# Desktop: dark bento workspace. Display numerals, glowing confirmation flow, gauge and toggles —
# every element visualises data the journal already holds (participants, times, checks, fields).
D0='#0a0e0c'; D1='#121815'; D2='#18201c'; DL='#25302a'; DT='#eef3ef'; DM='#8d9a92'; DG='#46d38b'; DGD='#1c3a2b'; DA='#f4a52a'; DAD='#3b2b12'
def right(x,y,label,size=16,color=DT,weight=400):return t(x,y,label,size,color,weight).replace(f'x="{x}"',f'x="{x}" text-anchor="end"')
def center(x,y,label,size=16,color=DT,weight=400):return t(x,y,label,size,color,weight).replace(f'x="{x}"',f'x="{x}" text-anchor="middle"')
def hl(x,y,x2,color=DL):return f'<path d="M{x} {y}H{x2}" stroke="{color}"/>'
def vline(x,y,y2,color=DL):return f'<path d="M{x} {y}V{y2}" stroke="{color}"/>'
DESK_ICONS={
 'list':'M4 6 H20 M4 12 H20 M4 18 H20','pages':'M4 4 H10 V20 H4 Z M14 4 H20 V20 H14 Z',
 'search':'M10.5 17 A6.5 6.5 0 1 1 10.5 4 A6.5 6.5 0 1 1 10.5 17 M15.5 15.5 L20 20',
 'download':'M12 4 V15 M7 10 L12 15 L17 10 M5 20 H19','pen':'M4 20 L5 15 L15 5 L19 9 L9 19 Z M13 7 L17 11',
 'info':'M12 21 A9 9 0 1 1 12 3 A9 9 0 1 1 12 21 M12 11 V16 M12 8 V8.2','close':'M6 6 L18 18 M18 6 L6 18',
 'plus':'M12 5 V19 M5 12 H19','minus':'M5 12 H19','left':'M15 5 L8 12 L15 19','rightc':'M9 5 L16 12 L9 19',
 'file':'M6 3 H14 L19 8 V21 H6 Z M14 3 V8 H19','sun':'M12 16 A4 4 0 1 1 12 8 A4 4 0 1 1 12 16 M12 2 V4 M12 20 V22 M2 12 H4 M20 12 H22 M5 5 L6.5 6.5 M17.5 17.5 L19 19 M5 19 L6.5 17.5 M17.5 6.5 L19 5',
 'shield':'M12 3 L19 6 V11 C19 16 16 19.5 12 21 C8 19.5 5 16 5 11 V6 Z M9 12 L11 14 L15 10',
 'clock':'M12 21 A9 9 0 1 1 12 3 A9 9 0 1 1 12 21 M12 7 V12 L15 14','grid':'M4 4 H10 V10 H4 Z M14 4 H20 V10 H14 Z M4 14 H10 V20 H4 Z M14 14 H20 V20 H14 Z',
}
def dicon(x,y,name,color=DM,size=20):
 return f'<path d="{DESK_ICONS[name]}" transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
DEFS=('<defs><filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
 '<linearGradient id="band" x1="0" x2="1"><stop offset="0" stop-color="#46d38b" stop-opacity="0"/><stop offset="1" stop-color="#46d38b" stop-opacity=".35"/></linearGradient>'
 '<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#18201c"/><stop offset="1" stop-color="#121815"/></linearGradient>'
 '<linearGradient id="paperfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121815" stop-opacity="0"/><stop offset="1" stop-color="#121815" stop-opacity=".95"/></linearGradient><radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#46d38b" stop-opacity=".22"/><stop offset="1" stop-color="#46d38b" stop-opacity="0"/></radialGradient></defs>')
def tile(x,y,w,h,r=18):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#tile)" stroke="{DL}"/>'
def tag(x,y,label,fg=DG,bg=DGD,w=None):
 w=w or sum(6 if c==' ' else (8 if c.isascii() else 13) for c in label)+24
 return rect(x,y,w,26,bg,13)+center(x+w/2,y+18,label,12,fg,700)
def toggle(x,y,on=True):
 return rect(x,y,52,28,DGD if on else '#222b26',14,DG if on else DL)+f'<circle cx="{x+38 if on else x+14}" cy="{y+14}" r="9" fill="{DG if on else DM}"/>'
def shell(active,title,meta):
 a=rect(0,0,1600,1000,D0,0)+DEFS
 a+=rect(0,0,76,1000,D1,0)+vline(76,0,1000)+rect(18,22,40,40,DG,12)+center(38,50,'f',22,D0,800)
 for i,(label,kind) in enumerate([('준비','home'),('기록','record'),('문서','record'),('정보','user')]):
  y=124+i*84;on=label==active;color=DG if on else '#6f7b74'
  if on:a+=rect(12,y-10,52,64,DGD,14)+rect(0,y+2,3,40,DG,1)
  a+=icon(27,y,kind,color,22)+center(38,y+42,label,11,color,600)
 a+=center(38,970,'v1.4',10,'#56615a',600)
 a+=t(100,46,title,24,DT,700)+t(100,72,meta,13,DM)
 a+=rect(1150,28,150,32,D2,16,DL)+dicon(1164,34,'sun',DA,20)+t(1192,50,'맑음 · 18°',13,DT,600)+right(1286,50,'',13)
 a+=rect(1316,28,176,32,D2,16,DL)+f'<circle cx="1336" cy="44" r="4" fill="{DG}"/>'+t(1350,49,'공개용 가상 데이터',12,DM,600)
 a+=rect(1508,28,32,32,D2,16,DL)+dicon(1514,34,'search',DT,20)+rect(1548,28,32,32,D2,16,DL)+dicon(1554,34,'info',DT,20)
 return a
# ── Record workspace (homepage hero) ──
a=shell('기록','오늘의 안전 기록','2027.04.18 · 오전 작업 · 모래빛 실증센터 A팀 · 작성 담당 이도경')
# Flow tile
a+=tile(100,100,1000,500)+t(132,160,'참여자',36,DT,300)+t(132,204,'확인 흐름',36,DT,700)
a+=tag(132,228,'작성 중')
a+=f'<rect x="100" y="318" width="380" height="64" fill="url(#band)"/>'+t(132,345,'작업 전 확인 일지',16,DT,700)+t(132,368,'07:30 공유 · 항목 4개',12,DM)
a+=f'<rect x="436" y="318" width="64" height="64" rx="12" fill="{DG}"/>'+icon(452,334,'check',D0,32)
rows=[('이도경','07:42',True),('정하준','07:45',True),('한서윤','07:46',True),('오민재','07:48',True),('윤지안','미확인',False)]
for i,(name,time,ok) in enumerate(rows):
 y=150+i*78;c=DG if ok else '#3a4640';path=f'M500 350 C640 350 660 {y+28} 800 {y+28}'
 if ok:a+=f'<path d="{path}" stroke="{DG}" stroke-width="10" fill="none" opacity=".45" filter="url(#glow)"/>'
 a+=f'<path d="{path}" stroke="{c}" stroke-width="{5 if ok else 4}" fill="none" stroke-linecap="round"/>'
 a+=rect(800,y+8,3,40,c,1)+t(822,y+24,name,15,DT if ok else DM,700)+t(822,y+44,time,12,DM)
 a+=toggle(1018,y+14,ok)
a+=t(822,560,'외 4명 · 4명 확인 완료',13,DM,600)
a+=t(132,512,'8',64,DT,300)+t(176,512,'/ 9명',22,DM,500)+t(132,548,'확인 완료',13,DM,600)
a+=vline(300,470,556)+t(328,500,'최근 확인',12,DM,600)+t(328,530,'07:48',26,DT,600)+t(328,552,'오민재',12,DM)
# Gauge tile
a+=tile(1120,100,456,500)+center(1348,160,'확인률',18,DT,700)+f'<circle cx="1348" cy="350" r="150" fill="url(#halo)"/>'
import math
def arc(cx,cy,r,f):
 a0=math.pi;a1=math.pi+math.pi*f;x0=cx+r*math.cos(a0);y0=cy+r*math.sin(a0);x1=cx+r*math.cos(a1);y1=cy+r*math.sin(a1)
 return f'M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}'
a+=f'<path d="{arc(1348,370,140,1)}" stroke="#26302a" stroke-width="26" fill="none" stroke-linecap="round"/>'
a+=f'<path d="{arc(1348,370,140,8/9)}" stroke="{DG}" stroke-width="26" fill="none" stroke-linecap="round" opacity=".5" filter="url(#glow)"/>'
a+=f'<path d="{arc(1348,370,140,8/9)}" stroke="{DG}" stroke-width="26" fill="none" stroke-linecap="round"/>'
a+=dicon(1336,282,'shield',DG,24)+center(1348,356,'89%',52,DT,300)+center(1208,404,'0%',12,DM)+center(1488,404,'100%',12,DM)
a+=hl(1152,440,1544)
for i,(label,state,ok) in enumerate([('작성 담당','확인 완료',True),('현장 책임자','검토 대기',False)]):
 y=482+i*54;a+=t(1152,y,label,14,DM)+(tag(1544-86,y-18,state,DG,DGD,86) if ok else tag(1544-86,y-18,state,DA,DAD,86))
# Journal fields tile
a+=tile(100,620,520,356)+t(132,668,'일지 내용',18,DT,700)+right(588,668,'4 / 4 작성',12,DM,600)
for i,(label,value,ic) in enumerate([('작업 구분','거더 조립 준비','grid'),('공유 사항','장비 이동 동선','list'),('위험 요인','이동 간섭','shield'),('예방 활동','구역 구분 안내','record' )]):
 col,row=i%2,i//2;x=132+col*236;y=716+row*116
 a+=rect(x,y,220,96,D2,12,DL)+t(x+18,y+32,label,12,DM,600)+t(x+18,y+66,value,16,DT,700)
 a+=(dicon(x+186,y+16,ic,DM,18) if ic!='record' else icon(x+186,y+16,'record',DM,18))
# Checklist tile
a+=tile(640,620,460,356)+t(672,668,'작업 전 체크',18,DT,700)+right(1068,668,'3 / 3',12,DG,700)
for i,label in enumerate(['보호구 착용 확인','이동 동선 공유','작업 구역 정리']):
 y=704+i*82;a+=rect(672,y,396,66,D2,12,DL)+icon(690,y+21,'check',DG,24)+t(728,y+40,label,15,DT,600)+toggle(1000,y+19,True)
# Timeline tile
a+=tile(1120,620,456,356)+t(1152,668,'기록 타임라인',18,DT,700)
tl=[('07:30','일지 공유','이도경',DG),('07:42','확인','이도경',DG),('07:45','확인','정하준',DG),('07:48','확인','오민재 외 5명',DG),('—','확인 대기','윤지안',DA)]
a+=vline(1166,712,928,'#2c3832')
for i,(tm,what,who,c) in enumerate(tl):
 y=712+i*54;a+=f'<circle cx="1166" cy="{y}" r="6" fill="{D1}" stroke="{c}" stroke-width="3"/>'+t(1188,y+5,tm,14,DT,600)+t(1256,y+5,what,14,c if c==DA else DT,600)+right(1544,y+5,who,13,DM)
save('tbm-journal',1600,1000,a,'FIELDNOTE 안전 기록과 확인 상태')
# ── Document review workspace ──
def paper_thumb(x,y,w,h,tag_,active=False):
 a=''
 if active:a+=f'<rect x="{x-4}" y="{y-4}" width="{w+8}" height="{h+8}" rx="8" fill="none" stroke="{DG}" stroke-width="2"/>'
 a+=rect(x,y,w,h,'#f3f5f1',4)
 for i in range(5):a+=f'<path d="M{x+8} {y+14+i*9}H{x+w-8-(10 if i%2 else 0)}" stroke="#cdd5cc"/>'
 return a+rect(x+6,y+h-18,28,12,'#dfeee4',3)+t(x+10,y+h-9,tag_,8,'#2e6247',700)
a=shell('문서','작업 전 안전 안내','현장 자료 3개 · PDF 2쪽 · 등록 2027.04.18 · 이도경')
Y=96;a+=tile(100,Y,1476,56,14)
for x,name,on in [(100,'list',True),(156,'pages',False)]:
 if on:a+=rect(x+8,Y+8,40,40,DGD,10)
 a+=dicon(x+18,Y+18,name,DG if on else DM,20)
a+=vline(212,Y+14,Y+42)
a+=rect(640,Y+10,320,36,D2,18,DL)+dicon(656,Y+18,'left',DT,20)+center(800,Y+34,'1  /  2',14,DT,600)+dicon(924,Y+18,'rightc',DT,20)
a+=rect(980,Y+10,180,36,D2,18,DL)+dicon(994,Y+18,'minus',DT,20)+center(1070,Y+34,'100%',14,DT,600)+dicon(1126,Y+18,'plus',DT,20)
a+=rect(1300,Y+10,120,36,D2,18,DL)+dicon(1316,Y+18,'download',DT,18)+t(1342,Y+33,'다운로드',13,DT,600)
a+=rect(1430,Y+10,136,36,DG,18)+dicon(1448,Y+18,'pen',D0,18)+t(1474,Y+33,'문서 수정',13,D0,700)
# Files
a+=tile(100,168,320,808)+t(128,214,'현장 자료',17,DT,700)+rect(214,198,28,22,DGD,11)+center(228,214,'3',12,DG,700)+dicon(384,200,'close',DM,18)+hl(100,238,420)
for i,(label,meta,tg) in enumerate([('작업 전 안전 안내.pdf','2027.04.18 · 2쪽','PDF'),('작업 체크리스트.pdf','2027.04.17 · 1쪽','PDF'),('반입 장비 목록.hwp','2027.04.15 · 3쪽','HWP')]):
 y=258+i*124;on=i==0
 if on:a+=rect(112,y-6,296,112,DGD,12)
 a+=paper_thumb(128,y+8,64,84,tg,on)+t(212,y+36,label,15,DT,700 if on else 500)+t(212,y+60,meta,12,DM)
 if on:a+=tag(212,y+72,'열람 중')
a+=t(128,948,'공개용으로 작성한 가상 문서',12,'#5d6962')
# Paper
a+=f'<rect x="440" y="168" width="760" height="808" rx="18" fill="{D1}" stroke="{DL}"/>'+f'<ellipse cx="820" cy="560" rx="340" ry="360" fill="url(#halo)" opacity=".5"/>'
a+=f'<clipPath id="pc"><rect x="440" y="168" width="760" height="808" rx="18"/></clipPath><g clip-path="url(#pc)">'
a+=rect(490,204,660,736,'white',6);X=556
a+=t(X,262,'FIELDNOTE / 안전관리팀',12,'#2e6247',700)+right(1084,262,'01',12,'#a6aea3',600)+t(X,314,'작업 전 안전 안내',30,'#1d2a22',750)+t(X,346,'모래빛 실증센터 · A팀 · 오전 작업',14,'#68756c')+f'<path d="M{X} 372H1084" stroke="#e3e8df"/>'
a+=t(X,416,'1',19,'#2e6247',700)+t(X+28,416,'작업 전 확인 사항',19,'#1d2a22',700)
y=460
for no,body,subs in [('1.','작업 시작 전, 보호구와 장비의 상태를 함께 확인합니다.',['a) 안전모·안전화·장갑 착용 여부','b) 공구와 장비의 파손·누락 여부']),('2.','장비와 보행자의 이동 구역을 나누어 공유합니다.',['a) 장비 이동 경로와 대기 위치','b) 보행 통로와 출입 제한 구역']),('3.','작업 공간의 간섭 요소를 확인하고 정리합니다.',[]),('4.','확인한 내용은 오늘의 안전 기록에 남깁니다.',[])]:
 a+=t(X,y,no,15,'#1d2a22',500)+t(X+30,y,body,15,'#3a4a40');y+=34
 for s in subs:a+=t(X+58,y,s,14,'#68756c');y+=30
 y+=12
a+=t(X,y+24,'2',19,'#2e6247',700)+t(X+28,y+24,'공유와 기록',19,'#1d2a22',700)+t(X,y+68,'1.',15,'#1d2a22',500)+t(X+30,y+68,'작업 책임자는 공유 내용을 참여자 모두에게 안내합니다.',15,'#3a4a40')
a+='</g>'
# Info
a+=tile(1220,168,356,808)+t(1248,214,'문서 정보',17,DT,700)+dicon(1540,200,'close',DM,18)+hl(1220,238,1576)
for i,(label,value) in enumerate([('현장','모래빛 실증센터'),('문서 구분','안전 안내'),('형식','PDF · 2쪽'),('등록일','2027.04.18'),('등록 담당','이도경')]):
 y=282+i*46;a+=t(1248,y,label,14,DM)+right(1548,y,value,14,DT,600)
a+=hl(1248,506,1548)+t(1248,544,'관련 기록',13,DM,600)
a+=rect(1248,562,300,150,D2,14,DL)+rect(1266,580,36,36,DGD,18)+icon(1274,588,'record',DG,20)+t(1316,596,'오늘의 안전 기록',15,DT,700)+t(1316,616,'2027.04.18 · 오전 작업',12,DM)
a+=rect(1266,636,264,58,D1,10,DL)+dicon(1282,654,'file',DG,20)+t(1312,661,'작업 전 확인 일지',14,DT,600)+t(1312,681,'참여 9명 · 확인 8명',11,DM)
a+=rect(1248,836,300,116,DGD,14)+dicon(1268,858,'info',DG,18)+t(1296,872,'열람 모드',14,DG,700)+t(1268,904,'열람 중에는 문서가 바뀌지 않아요.',13,'#b9cbbf')+t(1268,928,'수정은 상단 ‘문서 수정’에서 시작합니다.',13,'#b9cbbf')
save('tbm-documents',1600,1000,a,'FIELDNOTE 현장 문서 선택·열람·편집 진입')
# ── Equal-size state panels: only guidance, list emphasis and the bar change between states ──
def state_panel(mode):
 W,H=900,620;a=rect(0,0,W,H,D0,0)+DEFS+rect(0,0,W,58,D1,0)+hl(0,58,W)+rect(18,13,32,32,DG,10)+center(34,35,'f',18,D0,800)+t(64,36,'현장 문서 열람',15,DT,700)
 dim=mode=='edit'
 a+=tile(16,74,262,530,14)+t(34,106,'현장 자료',16,DT,700)+right(260,106,'3개',12,DM)+hl(16,122,278)
 for i,(label,meta,tg) in enumerate([('작업 전 안전 안내.pdf','2027.04.18 · 2쪽','PDF'),('작업 체크리스트.pdf','2027.04.17 · 1쪽','PDF'),('반입 장비 목록.hwp','2027.04.15 · 3쪽','HWP')]):
  y=136+i*86;sel=(i==0 and mode!='empty')
  if sel:a+=rect(26,y,242,74,DGD,10)+rect(26,y+12,3,50,DG,1)
  a+=rect(40,y+14,32,42,'#f3f5f1',4)+t(44,y+50,tg,8,'#2e6247',700)+t(84,y+32,label,13,DT,700 if sel else 500)+t(84,y+53,meta,11,DM)
 if dim:a+=f'<rect x="16" y="74" width="262" height="530" rx="14" fill="{D0}" opacity=".86"/>'+rect(34,512,226,72,D2,12,DL)+center(147,542,'수정 중에는',13,DT,600)+center(147,564,'다른 문서로 이동하지 않아요',13,DM,500)
 a+=tile(294,74,590,530,14)
 if mode=='empty':
  a+=rect(310,88,558,46,D2,10,DL)+t(328,117,'선택한 문서 없음',14,DM)+f'<circle cx="589" cy="310" r="110" fill="url(#halo)"/>'
  a+=rect(549,262,80,96,D2,10,DL)+hl(569,292,609,'#3a4640')+hl(569,310,609,'#3a4640')+hl(569,328,595,'#3a4640')
  a+=center(589,404,'왼쪽에서 문서를 선택해 주세요',19,DT,700)+center(589,434,'PDF·HWP 문서를 이 자리에서 바로 볼 수 있어요.',14,DM)
  return a
 if mode=='view':
  a+=rect(310,88,558,46,D2,10,DL)+t(328,117,'작업 전 안전 안내.pdf',14,DT,650)+right(690,117,'1 / 2  ·  100%',12,DM)+rect(706,97,70,28,D1,14,DL)+center(741,116,'다운로드',12,DT,600)+rect(784,97,70,28,DG,14)+center(819,116,'수정',12,D0,700)
 else:
  a+=rect(310,88,558,46,DGD,10,DG)+tag(322,98,'수정 중',D0,DG,64)+t(398,117,'작업 전 안전 안내.pdf',14,DT,650)+rect(706,97,70,28,D1,14,DL)+center(741,116,'취소',12,DT,600)+rect(784,97,70,28,DG,14)+center(819,116,'저장',12,D0,700)
 a+=rect(344,150,490,440,'white',4)+t(376,190,'FIELDNOTE / 안전관리팀',10,'#2e6247',700)+t(376,228,'작업 전 안전 안내',22,'#1d2a22',750)+t(376,254,'모래빛 실증센터 · A팀',12,'#68756c')+'<path d="M376 272H802" stroke="#e3e8df"/>'
 for i,(title,body) in enumerate([('01  작업 준비','보호구와 장비의 상태를 확인합니다.'),('02  동선 공유','장비와 보행자의 이동 구역을 구분합니다.'),('03  작업 구역 확인','작업 공간의 간섭 요소를 함께 확인합니다.')]):
  y=310+i*82;a+=t(376,y,title,15,'#1d2a22',700)+t(376,y+27,body,12,'#68756c')
 if mode=='edit':
  a+='<rect x="366" y="374" width="446" height="56" rx="6" fill="#eef8f1" stroke="#2e9a63" stroke-dasharray="5 4"/><path d="M640 410V424" stroke="#2e9a63" stroke-width="2"/>'
  a+=rect(600,532,222,40,D1,20,DL)
  for x,label,on in [(616,'텍스트',False),(684,'펜',True),(732,'지우개',False)]:
   if on:a+=rect(x-10,538,44,28,DGD,14)
   a+=t(x,557,label,12,DG if on else DT,600)
 return a
for name,mode,label in [('tbm-state-empty','empty','문서 선택 전'),('tbm-state-view','view','문서 열람'),('tbm-state-edit','edit','문서 수정')]:
 save(name,900,620,state_panel(mode),'FIELDNOTE '+label+' 상태')
print('Generated FIELDNOTE views (dark desktop, light mobile)')
