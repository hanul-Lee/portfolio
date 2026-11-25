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
# Desktop is a practical document desk: persistent files, paper preview and record metadata.
def right(x,y,label,size=16,color=INK,weight=400):return t(x,y,label,size,color,weight).replace(f'x="{x}"',f'x="{x}" text-anchor="end"')
def shell(active,title,sub):
 a=rect(0,0,1600,1000,BG,0)+rect(0,0,1600,76,'white',0)+t(26,49,'fieldnote',26,'#2e6247',750)+line(0,76,1600,76)+t(223,46,title,19,INK,650)+t(1040,46,'모래빛 실증센터 / A팀',14,MUTED)+pill(1360,23,'공개용 가상 데이터','#2e6247','#e7efe5',208)
 a+=rect(0,76,180,924,'#233f30',0)+t(24,124,'현장 기록',14,'#c2d1bf',600)
 for i,(label,kind) in enumerate([('작업 준비','home'),('안전 기록','record'),('현장 문서','record'),('내 정보','user')]):
  y=163+i*62
  if label==active:a+=rect(12,y-12,156,46,'#dfe9d9',9)
  color='#294d37' if label==active else '#c8d6c3';a+=icon(25,y,kind,color,21)+t(58,y+16,label,16,color,600)
 a+=t(24,909,'FIELD WORKSPACE',10,'#bdcbb6',600)+t(24,940,'모래빛 실증센터',13,'#bdcbb6')
 return a
# Record workspace.
a=shell('안전 기록','오늘의 안전 기록','')
for x,value,label in [(202,'9명','오늘 참여 인원'),(664,'8명','확인 완료'),(1126,'1명','확인 대기')]:
 a+=rect(x,100,440,120,'white',12,LINE)+t(x+23,136,label,15,MUTED)+t(x+23,190,value,35,'#2e6247',750)
a+=rect(202,244,902,720,'white',12,LINE)+t(228,284,'작업 전 확인 일지',23,INK,700)+pill(986,260,'작성 중','#2e6247','#eaf1ec',90)+t(228,320,'2027.04.18 / 오전 작업 / A팀',15,MUTED)+line(228,343,1078,343)
for y,label,value in [(386,'작업 구분','거더 조립 준비'),(452,'공유 사항','장비 이동 동선 확인'),(518,'주요 위험 요인','작업 공간 내 이동 간섭'),(584,'예방 활동','구역 구분 및 작업 전 안내')]:
 a+=t(228,y,label,16,MUTED)+t(428,y,value,18,INK,600)+line(228,y+25,1078,y+25)
a+=t(228,674,'참여자 확인 이력',19,INK,700)
for i,(name,time,status) in enumerate([('이도경','07:42','확인 완료'),('정하준','07:45','확인 완료'),('윤지안','-','확인 대기')]):
 y=708+i*71;a+=rect(228,y,850,54,BG,8)+t(248,y+34,name,17,INK,600)+t(548,y+34,time,16,MUTED)+right(1058,y+34,status,16,'#2e6247' if i<2 else '#2e6247',600)
a+=rect(1126,244,440,338,'white',12,LINE)+t(1150,284,'확인 상태',22,INK,700)
for i,(label,state) in enumerate([('작성 담당','확인 완료'),('현장 책임자','검토 대기'),('참여자','8 / 9명 확인')]):
 y=339+i*75;a+=t(1150,y,label,16,MUTED)+right(1542,y,state,17,'#2e6247' if i==1 else '#2e6247',600)+line(1150,y+24,1542,y+24)
a+=rect(1126,606,440,358,'#e7efe3',12)+t(1150,650,'작업 전 체크',22,'#2e6247',700)
for i,label in enumerate(['보호구 착용 확인','이동 동선 공유','작업 구역 정리']):
 y=686+i*66;a+=rect(1150,y,28,28,'white',8)+icon(1154,y+4,'check','#2e6247',20)+t(1194,y+22,label,17,INK,600)
a+=t(1150,925,'가상 현장 기록 · 실제 운영 자료 아님',13,MUTED)
save('tbm-journal',1600,1000,a,'FIELDNOTE 안전 기록과 확인 상태')
# Document review workspace, inspired by an editor's three-panel organization.
a=shell('현장 문서','현장 문서 열람','')+rect(202,100,300,866,'white',12,LINE)+t(224,139,'현장 자료',22,INK,700)+right(478,139,'3개',14,MUTED)+line(224,160,478,160)
for i,(label,meta) in enumerate([('작업 전 안전 안내.pdf','2027.04.18 · 2쪽'),('작업 체크리스트.pdf','2027.04.17 · 1쪽'),('반입 장비 목록.xlsx','2027.04.15 · 12 KB')]):
 y=181+i*119;a+=rect(214,y,276,101,'#e7efe3' if i==0 else '#f6f7f3',9)+rect(229,y+17,37,46,'white',6)+t(233,y+44,'PDF' if i<2 else 'XLS',10,'#2e6247',700)+t(278,y+29,label,15,INK,650)+t(278,y+55,meta,13,MUTED)
 if i==0:a+=rect(214,y+17,3,67,'#2e6247',1)
a+=t(224,815,'관련 기록',15,MUTED,600)+rect(224,837,254,52,'#2e6247',8)+t(245,870,'오늘의 안전 기록 보기',16,'white',600)+t(224,936,'공개용으로 작성한 가상 문서',12,MUTED)
a+=rect(524,100,680,866,'#e6ebe2',12)+rect(544,116,640,52,'white',9)+t(563,148,'작업 전 안전 안내.pdf',16,INK,650)+right(1166,148,'1 / 2  ·  100%',14,MUTED)
a+=rect(578,191,572,730,'white',2)+t(618,239,'FIELDNOTE / 안전관리팀',12,'#2e6247',700)+t(618,294,'작업 전 안전 안내',30,INK,750)+t(618,331,'모래빛 실증센터 · A팀',15,MUTED)+line(618,354,1110,354)
for i,(title,body) in enumerate([('01  작업 준비','보호구와 장비의 상태를 확인합니다.'),('02  동선 공유','장비와 보행자의 이동 구역을 구분합니다.'),('03  작업 구역 확인','작업 공간의 간섭 요소를 함께 확인합니다.')]):
 y=404+i*115;a+=t(618,y,title,20,INK,700)+t(618,y+37,body,15,MUTED)
a+=rect(618,754,492,83,'#f1f5ed',7)+t(638,787,'기록 안내',16,'#2e6247',650)+t(638,816,'실제 문서가 아닌 공개용 예시입니다.',14,MUTED)+t(618,883,'FICTIONAL DOCUMENT / 01',11,MUTED)
a+=rect(1226,100,340,866,'white',12,LINE)+t(1250,141,'문서 정보',22,INK,700)+line(1250,163,1542,163)
for i,(label,value) in enumerate([('현장','모래빛 실증센터'),('문서 구분','안전 안내'),('등록일','2027.04.18'),('등록 담당','이도경'),('열람 상태','문서 선택됨')]):
 y=203+i*88;a+=t(1250,y,label,14,MUTED)+t(1250,y+31,value,18,'#2e6247' if i==4 else INK,600)
a+=rect(1250,670,292,52,'#2e6247',8)+t(1276,703,'문서 편집 화면으로 이동',16,'white',600)+rect(1250,735,292,48,'#f1f4ed',8,LINE)+t(1320,766,'파일 다운로드',16,INK,600)+line(1250,815,1542,815)+t(1250,851,'열람과 편집을 구분해',15,MUTED)+t(1250,879,'다음 행동을 확인합니다.',15,MUTED)+pill(1250,912,'가상 문서','#2e6247','#e7efe3',120)
save('tbm-documents',1600,1000,a,'FIELDNOTE 현장 문서 선택·열람·편집 진입')
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
