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
    return rect(24,y,40,40,'#edf1eb',12)+icon(33,y+9,kind,color)+t(80,y+16,title,16,INK,600)+t(80,y+39,sub,13,MUTED)+(t(336,y+22,right,14,color,600).replace('x="336"','x="336" text-anchor="end"') if right else icon(341,y+10,'chevron','#a6aea3',18))
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
a=rect(158,248,74,74,'#e8efe4',37)+icon(178,268,'check',GREEN,34)+t(195,381,'확인 표시를 저장했어요',25,INK,700).replace('x="195"','x="195" text-anchor="middle"')+t(195,420,'이제 오늘의 안전 기록을 작성할 수 있어요.',15,MUTED).replace('x="195"','x="195" text-anchor="middle"')+rect(24,486,342,104,'#f3f5f0',16)+t(44,521,'오늘의 기록',14,MUTED)+t(44,556,'모래빛 실증센터 · A팀',17,INK,600)+button(716,'안전 기록으로 돌아가기',GREEN)
mobile('tbm-saved','fieldnote','저장 완료','',a,back=True)
# Desktop: a calm document desk — slim icon rail, metadata header, tool strip and hairline-divided panes.
# Layout language follows a three-pane reader (files · paper · info); only features the service had are drawn.
def right(x,y,label,size=16,color=INK,weight=400):return t(x,y,label,size,color,weight).replace(f'x="{x}"',f'x="{x}" text-anchor="end"')
def center(x,y,label,size=16,color=INK,weight=400):return t(x,y,label,size,color,weight).replace(f'x="{x}"',f'x="{x}" text-anchor="middle"')
def vline(x,y,y2,color=LINE):return f'<path d="M{x} {y}V{y2}" stroke="{color}"/>'
DESK_ICONS={
 'list':'M4 6 H20 M4 12 H20 M4 18 H20',
 'pages':'M4 4 H10 V20 H4 Z M14 4 H20 V20 H14 Z',
 'search':'M10.5 17 A6.5 6.5 0 1 1 10.5 4 A6.5 6.5 0 1 1 10.5 17 M15.5 15.5 L20 20',
 'download':'M12 4 V15 M7 10 L12 15 L17 10 M5 20 H19',
 'pen':'M4 20 L5 15 L15 5 L19 9 L9 19 Z M13 7 L17 11',
 'info':'M12 21 A9 9 0 1 1 12 3 A9 9 0 1 1 12 21 M12 11 V16 M12 8 V8.2',
 'close':'M6 6 L18 18 M18 6 L6 18',
 'plus':'M12 5 V19 M5 12 H19',
 'minus':'M5 12 H19',
 'left':'M15 5 L8 12 L15 19',
 'file':'M6 3 H14 L19 8 V21 H6 Z M14 3 V8 H19',
 'down':'M6 9 L12 15 L18 9',
}
def dicon(x,y,name,color=MUTED,size=20):
 return f'<path d="{DESK_ICONS[name]}" transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
def chip(x,y,kind,label,color=GREEN):
 return rect(x,y+1,10,12,color,2)+t(x+17,y+12,label,11,color,700)
def paper_thumb(x,y,w,h,tag,active=False):
 a=rect(x,y,w,h,'white',4,GREEN if active else LINE)
 if active:a+=f'<rect x="{x-2}" y="{y-2}" width="{w+4}" height="{h+4}" rx="6" fill="none" stroke="{GREEN}" stroke-width="2"/>'
 for i in range(5):a+=line(x+8,y+14+i*9,x+w-8-(10 if i%2 else 0),y+14+i*9,'#d6ddd2')
 return a+rect(x+6,y+h-18,26,12,'#e7efe3',3)+t(x+10,y+h-9,tag,8,GREEN,700)
def shell(active,title,meta,chips):
 a=rect(0,0,1600,1000,'white',0)
 # Icon rail
 a+=rect(0,0,76,1000,'white',0)+vline(76,0,1000)+rect(18,22,40,40,GREEN,11)+center(38,50,'f',22,'white',800)
 for i,(label,kind) in enumerate([('작업 준비','home'),('안전 기록','record'),('현장 문서','record'),('내 정보','user')]):
  y=112+i*84;on=label==active;color=GREEN if on else '#8d978a'
  if on:a+=rect(10,y-8,56,64,'#eaf1e6',12)+rect(0,y+4,3,40,GREEN,1)
  a+=icon(27,y+2,kind,color,22)+center(38,y+44,label.replace('작업 ','').replace('안전 ','').replace('현장 ','').replace('내 ',''),11,color,600)
 a+=center(38,970,'v1.4',10,'#a6aea3',600)
 # Header: title, counters, context line
 a+=line(76,88,1600,88)+t(108,40,title,22,INK,650)
 cx=108+sum(7 if ch==' ' else 22 for ch in title)+20
 for kind,label in chips:a+=chip(cx,27,kind,label);cx+=sum(4 if ch==' ' else 11 for ch in label)+34
 a+=t(108,70,meta,14,MUTED)
 a+=rect(1306,30,170,30,'#eef3eb',15)+center(1391,50,'공개용 가상 데이터',12,GREEN,700)
 a+=dicon(1500,35,'search',INK,20)+dicon(1546,35,'info',INK,20)
 return a
def tool(x,y,w,name,label='',on=False,color=INK):
 a=''
 if label:a+=dicon(x+(w-len(label)*13-28)//2,y+16,name,color,18)+t(x+(w-len(label)*13-28)//2+26,y+30,label,13,color,600)
 else:a+=dicon(x+w//2-10,y+16,name,GREEN if on else color,20)
 if on:a+=rect(x,y+50,w,2,GREEN,0)
 return a
# Document review workspace.
a=shell('현장 문서','작업 전 안전 안내',"모래빛 실증센터 · A팀 · 등록 2027.04.18 · 이도경",[('file','자료 3개'),('pages','PDF · 2쪽')])
# Tool strip (88–140): panel tabs · page nav · zoom · actions
Y=88;a+=line(76,140,1600,140)
a+=tool(76,Y,64,'list',on=True)+vline(140,Y,140)+tool(140,Y,64,'pages')+vline(204,Y,140)+vline(392,Y,140)
for x,name in [(600,'left')]:a+=vline(x,Y,140)+dicon(x+22,Y+16,'left',INK,20)
a+=vline(664,Y,140)+center(752,Y+32,'1  /  2',15,INK,600)+vline(840,Y,140)
a+=f'<g transform="translate({840+42} {Y+26}) scale(-1 1) translate(-10 -10)">{dicon(0,0,"left",INK,20)}</g>'+vline(904,Y,140)
a+=tool(904,Y,64,'minus')+vline(968,Y,140)+center(1016,Y+32,'100%',15,INK,600)+vline(1064,Y,140)+tool(1064,Y,64,'plus')+vline(1128,Y,140)
a+=vline(1228,Y,140)+tool(1228,Y,148,'download','다운로드')+vline(1376,Y,140)+rect(1392,Y+9,128,34,GREEN,8)+dicon(1410,Y+17,'pen','white',18)+t(1436,Y+31,'문서 수정',14,'white',650)+vline(1536,Y,140)+tool(1536,Y,64,'info',on=True)
# Left pane: files with paper thumbnails
a+=vline(392,140,1000)+t(108,184,'현장 자료',17,INK,650)+rect(190,168,26,20,'#eef3eb',10)+center(203,183,'3',12,GREEN,700)+dicon(354,170,'close',MUTED,18)+line(76,206,392,206)
for i,(label,meta,tag) in enumerate([('작업 전 안전 안내.pdf','2027.04.18 · 2쪽','PDF'),('작업 체크리스트.pdf','2027.04.17 · 1쪽','PDF'),('반입 장비 목록.hwp','2027.04.15 · 3쪽','HWP')]):
 y=226+i*122;on=i==0
 if on:a+=rect(88,y-8,292,108,'#f2f6ef',10)
 a+=paper_thumb(104,y+4,64,84,tag,on)+t(188,y+32,label,15,INK,650 if on else 500)+t(188,y+56,meta,13,MUTED)
 if on:a+=t(188,y+80,'열람 중',12,GREEN,700)
a+=t(108,970,'공개용으로 작성한 가상 문서',12,'#97a094')
# Centre: paper on a quiet canvas, cut off at the fold like a real reader
a+=rect(392,140,836,860,'#f4f6f2',0)+f'<rect x="460" y="172" width="700" height="860" fill="white" stroke="#e1e6dd"/>'
X=540;a+=t(X,236,'FIELDNOTE / 안전관리팀',12,GREEN,700)+right(1080,236,'01',12,'#a6aea3',600)
a+=t(X,290,'작업 전 안전 안내',30,INK,750)+t(X,324,'모래빛 실증센터 · A팀 · 오전 작업',14,MUTED)+line(X,352,1080,352)
a+=t(X,398,'1',19,GREEN,700)+t(X+28,398,'작업 전 확인 사항',19,INK,700)
items=[('1.','작업 시작 전, 보호구와 장비의 상태를 함께 확인합니다.',['a) 안전모·안전화·장갑 착용 여부','b) 공구와 장비의 파손·누락 여부']),
       ('2.','장비와 보행자의 이동 구역을 나누어 공유합니다.',['a) 장비 이동 경로와 대기 위치','b) 보행 통로와 출입 제한 구역']),
       ('3.','작업 공간의 간섭 요소를 확인하고 정리합니다.',[]),
       ('4.','확인한 내용은 오늘의 안전 기록에 남깁니다.',[])]
y=444
for no,body,subs in items:
 a+=t(X,y,no,15,INK,500)+t(X+30,y,body,15,'#3a4a40')
 y+=34
 for s in subs:a+=t(X+58,y,s,14,MUTED);y+=30
 y+=12
a+=t(X,y+26,'2',19,GREEN,700)+t(X+28,y+26,'공유와 기록',19,INK,700)
a+=t(X,y+72,'1.',15,INK,500)+t(X+30,y+72,'작업 책임자는 공유 내용을 참여자 모두에게 안내합니다.',15,'#3a4a40')
a+=t(X,y+114,'2.',15,INK,500)+t(X+30,y+114,'참여자는 내용을 확인한 뒤 확인 표시를 남깁니다.',15,'#3a4a40')
# Right pane: document info, related record, actions
a+=vline(1228,140,1000)+t(1252,184,'문서 정보',17,INK,650)+dicon(1562,170,'close',MUTED,18)+line(1228,206,1600,206)
for i,(label,value) in enumerate([('현장','모래빛 실증센터'),('문서 구분','안전 안내'),('형식','PDF · 2쪽'),('등록일','2027.04.18'),('등록 담당','이도경')]):
 y=250+i*46;a+=t(1252,y,label,14,MUTED)+right(1576,y,value,15,INK,600)
a+=line(1252,474,1576,474)+t(1252,512,'관련 기록',14,MUTED,600)
a+=rect(1252,530,324,150,'white',10,LINE)+rect(1272,550,36,36,'#eaf1e6',18)+icon(1280,558,'record',GREEN,20)+t(1322,566,'오늘의 안전 기록',15,INK,650)+t(1322,586,'2027.04.18 · 오전 작업',12,MUTED)
a+=rect(1520,553,40,22,'#eef3eb',11)+center(1540,568,'작성 중',10,GREEN,700)
a+=rect(1272,606,284,54,'#f6f8f4',8,LINE)+dicon(1288,623,'file',GREEN,20)+t(1318,630,'작업 전 확인 일지',14,INK,600)+t(1318,648,'참여 9명 · 확인 8명',11,MUTED)
a+=rect(1252,860,324,112,'#f4f6f2',10)+dicon(1272,880,'info',GREEN,18)+t(1300,894,'열람 모드',14,GREEN,700)+t(1272,926,'열람 중에는 문서가 바뀌지 않아요.',13,MUTED)+t(1272,950,'수정은 상단 ‘문서 수정’에서 시작합니다.',13,MUTED)
save('tbm-documents',1600,1000,a,'FIELDNOTE 현장 문서 선택·열람·편집 진입')
# Record workspace: same shell, stats strip and two divided panes.
a=shell('안전 기록','오늘의 안전 기록','2027.04.18 · 오전 작업 · A팀 · 작성 담당 이도경',[('record','작성 중'),('pages','참여 9명')])
a+=rect(76,89,1524,911,'#f4f6f2',0)
a+=rect(108,120,1460,108,'white',12,LINE)
for i,(value,label) in enumerate([('9명','오늘 참여 인원'),('8명','확인 완료'),('1명','확인 대기')]):
 x=108+i*487
 if i:a+=vline(x,140,208)
 a+=t(x+32,160,label,14,MUTED)+t(x+32,206,value,32,GREEN if i<2 else '#b4772e',750)
a+=rect(108,252,980,716,'white',12,LINE)+t(140,300,'작업 전 확인 일지',21,INK,700)+rect(980,280,76,26,'#eef3eb',13)+center(1018,298,'작성 중',12,GREEN,700)+t(140,330,'2027.04.18 / 오전 작업 / A팀',14,MUTED)+line(108,356,1088,356)
for i,(label,value) in enumerate([('작업 구분','거더 조립 준비'),('공유 사항','장비 이동 동선 확인'),('주요 위험 요인','작업 공간 내 이동 간섭'),('예방 활동','구역 구분 및 작업 전 안내')]):
 y=402+i*60;a+=t(140,y,label,15,MUTED)+t(330,y,value,16,INK,600)+line(140,y+24,1056,y+24)
a+=t(140,686,'참여자 확인 이력',17,INK,700)+right(1056,686,'8 / 9명',14,MUTED,600)
for i,(name,time,status) in enumerate([('이도경','07:42','확인 완료'),('정하준','07:45','확인 완료'),('윤지안','-','확인 대기')]):
 y=708+i*80;a+=rect(140,y,916,64,'white',10,LINE)+rect(160,y+16,32,32,'#eaf1e6',16)+center(176,y+37,name[0],13,GREEN,700)+t(208,y+38,name,15,INK,600)+t(520,y+38,time,14,MUTED)
 a+=rect(966,y+20,72,24,'#eef3eb' if i<2 else '#f8efe2',12)+center(1002,y+37,status,11,GREEN if i<2 else '#9a6224',700)
a+=rect(1112,252,456,330,'white',12,LINE)+t(1144,300,'확인 상태',19,INK,700)+line(1112,326,1568,326)
for i,(label,state) in enumerate([('작성 담당','확인 완료'),('현장 책임자','검토 대기'),('참여자','8 / 9명 확인')]):
 y=376+i*66;a+=t(1144,y,label,15,MUTED)+right(1536,y,state,15,'#9a6224' if i==1 else GREEN,650)
 if i<2:a+=line(1144,y+26,1536,y+26)
a+=rect(1112,606,456,362,'white',12,LINE)+t(1144,654,'작업 전 체크',19,INK,700)+right(1536,654,'3 / 3',14,MUTED,600)+line(1112,680,1568,680)
for i,label in enumerate(['보호구 착용 확인','이동 동선 공유','작업 구역 정리']):
 y=712+i*62;a+=rect(1144,y,26,26,GREEN,7)+icon(1147,y+3,'check','white',20)+t(1186,y+19,label,16,INK,600)
a+=t(1144,940,'가상 현장 기록 · 실제 운영 자료 아님',12,'#97a094')
save('tbm-journal',1600,1000,a,'FIELDNOTE 안전 기록과 확인 상태')
# Equal-size state panels: only the guidance, list emphasis and header change between states.
def state_panel(mode):
 W,H=900,620;a=rect(0,0,W,H,BG,0)+rect(0,0,W,58,'white',0)+line(0,58,W,58)+t(22,37,'fieldnote',20,'#2e6247',750)+t(150,36,'현장 문서 열람',15,INK,650)
 dim=mode=='edit'
 a+=rect(16,74,262,530,'white',12,LINE)+t(34,106,'현장 자료',17,INK,700)+right(260,106,'3개',12,MUTED)+line(34,122,260,122)
 for i,(label,meta) in enumerate([('작업 전 안전 안내.pdf','2027.04.18 · 2쪽'),('작업 체크리스트.pdf','2027.04.17 · 1쪽'),('반입 장비 목록.hwp','2027.04.15 · 3쪽')]):
  y=136+i*86;sel=(i==0 and mode!='empty')
  a+=rect(26,y,242,74,'#e7efe3' if sel else '#f6f7f3',9)+rect(40,y+14,30,38,'white',5)+t(44,y+38,'PDF' if i<2 else 'HWP',9,'#2e6247',700)+t(82,y+30,label,13,INK,650)+t(82,y+52,meta,12,MUTED)
  if sel:a+=rect(26,y+12,3,50,'#2e6247',1)
 if dim:a+=rect(16,74,262,530,'#f3f5f0',12)+t(147,330,'수정 중에는',14,MUTED,600).replace('x="147"','x="147" text-anchor="middle"')+t(147,354,'다른 문서로 이동하지 않아요',14,MUTED,600).replace('x="147"','x="147" text-anchor="middle"')
 a+=rect(294,74,590,530,'#e6ebe2',12)
 if mode=='empty':
  a+=rect(310,88,558,46,'white',9)+t(328,117,'선택한 문서 없음',14,MUTED)
  a+=rect(549,262,80,96,'white',10,LINE)+line(569,292,609,292,'#c5cec0')+line(569,310,609,310,'#c5cec0')+line(569,328,595,328,'#c5cec0')
  a+=t(589,404,'왼쪽에서 문서를 선택해 주세요',19,INK,700).replace('x="589"','x="589" text-anchor="middle"')+t(589,434,'PDF·HWP 문서를 이 자리에서 바로 볼 수 있어요.',14,MUTED).replace('x="589"','x="589" text-anchor="middle"')
  return a
 if mode=='view':
  a+=rect(310,88,558,46,'white',9)+t(328,117,'작업 전 안전 안내.pdf',14,INK,650)+right(690,117,'1 / 2  ·  100%',12,MUTED)+rect(706,97,70,28,'#f1f4ed',7,LINE)+t(741,116,'다운로드',12,INK,600).replace('x="741"','x="741" text-anchor="middle"')+rect(784,97,70,28,'white',7,'#2e6247')+t(819,116,'수정',12,'#2e6247',650).replace('x="819"','x="819" text-anchor="middle"')
 else:
  a+=rect(310,88,558,46,'#2e6247',9)+pill(322,97,'수정 중','#2e6247','#e7efe5',64)+t(398,117,'작업 전 안전 안내.pdf',14,'white',650)+rect(706,97,70,28,'#3d7457',7)+t(741,116,'취소',12,'white',600).replace('x="741"','x="741" text-anchor="middle"')+rect(784,97,70,28,'white',7)+t(819,116,'저장',12,'#2e6247',700).replace('x="819"','x="819" text-anchor="middle"')
 a+=rect(344,150,490,440,'white',2)+t(376,190,'FIELDNOTE / 안전관리팀',10,'#2e6247',700)+t(376,228,'작업 전 안전 안내',22,INK,750)+t(376,254,'모래빛 실증센터 · A팀',12,MUTED)+line(376,272,802,272)
 for i,(title,body) in enumerate([('01  작업 준비','보호구와 장비의 상태를 확인합니다.'),('02  동선 공유','장비와 보행자의 이동 구역을 구분합니다.'),('03  작업 구역 확인','작업 공간의 간섭 요소를 함께 확인합니다.')]):
  y=310+i*82;a+=t(376,y,title,15,INK,700)+t(376,y+27,body,12,MUTED)
 if mode=='edit':
  a+=f'<rect x="366" y="374" width="446" height="56" rx="6" fill="#eef4eb" stroke="#2e6247" stroke-dasharray="5 4"/>'+f'<path d="M640 410V424" stroke="#2e6247" stroke-width="2"/>'
  a+=rect(612,532,210,40,'#233f30',9)
  for x,label in [(628,'텍스트'),(692,'펜'),(740,'지우개')]:a+=t(x,557,label,12,'white',600)
 return a
for name,mode,label in [('tbm-state-empty','empty','문서 선택 전'),('tbm-state-view','view','문서 열람'),('tbm-state-edit','edit','문서 수정')]:
 save(name,900,620,state_panel(mode),'FIELDNOTE '+label+' 상태')
print('Generated six forest-green FIELDNOTE views')
