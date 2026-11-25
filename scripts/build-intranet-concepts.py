"""MORROW intranet concept: original vector UI with fictional work data."""
from pathlib import Path
from html import escape
import base64
OUT=globals().get('OUT',Path(__file__).resolve().parents[1]/'src/assets/cases/public-concepts')
OUT.mkdir(parents=True,exist_ok=True)
WHITE='#f5f8ff'; MUTED='#b0bdd2'; BLUE='#82adff'; BORDER='#30415b'
def rect(x,y,w,h,fill,r=18,stroke=None):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="1"' if stroke else '')+'/>'
def text(x,y,s,size=16,fill=WHITE,weight=400,anchor=None):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}"'+(f' text-anchor="{anchor}"' if anchor else '')+'>'+escape(str(s))+'</text>'
def rule(x,y,w=342):return f'<path d="M{x} {y}h{w}" stroke="#2a3550"/>'
def icon(x,y,name,color=WHITE,size=22):
 # Filled silhouettes, softened corners and negative-space details at a 24px grid.
 paths={
 'home':'M3 9.3L10.7 3.1Q12 2 13.3 3.1L21 9.3Q22.6 10.7 21 12Q20.5 12.4 19.7 12V20Q19.7 22 17.7 22H14V15H10V22H6.3Q4.3 22 4.3 20V12Q3.5 12.4 3 12Q1.4 10.7 3 9.3Z',
 'calendar':'M6 3Q6 1.5 7.5 1.5Q9 1.5 9 3V4H15V3Q15 1.5 16.5 1.5Q18 1.5 18 3V4H19Q22 4 22 7V19Q22 22 19 22H5Q2 22 2 19V7Q2 4 5 4H6ZM5 10V12H19V10ZM6 15V18H9V15ZM11 15V18H14V15Z',
 'document':'M6 2H18Q21 2 21 5V20Q21 23 18 23H6Q3 23 3 20V5Q3 2 6 2ZM7 7V9H17V7ZM7 12V14H17V12ZM7 17V19H14V17Z',
 'user':'M17 7A5 5 0 1 1 7 7A5 5 0 1 1 17 7ZM3 21Q3 13 12 13Q21 13 21 21Q21 23 19 23H5Q3 23 3 21Z',
 'bell':'M10.5 3Q10.5 1 12 1Q13.5 1 13.5 3Q19 4 19 10V14L21 17Q22 19 19.5 19H4.5Q2 19 3 17L5 14V10Q5 4 10.5 3ZM9 21H15Q14.5 24 12 24Q9.5 24 9 21Z',
 'room':'M7 2H17Q20 2 20 5V21H21Q22 21 22 22Q22 23 21 23H3Q2 23 2 22Q2 21 3 21H4V5Q4 2 7 2ZM14 11Q13 11 13 12.5Q13 14 14 14H15Q16 14 16 12.5Q16 11 15 11Z',
 'time':'M22 12A10 10 0 1 1 2 12A10 10 0 1 1 22 12ZM11 5V13L16.4 16.5L17.7 14.5L13 11.6V5Z',
 'chevron':'M8 4Q9 3 10 4L17 11Q18 12 17 13L10 20Q9 21 8 20Q7 19 8 18L14 12L8 6Q7 5 8 4Z',
 'back':'M16 4Q15 3 14 4L7 11Q6 12 7 13L14 20Q15 21 16 20Q17 19 16 18L10 12L16 6Q17 5 16 4Z',
 'check':'M3 12Q4 11 5 12L10 17L19 6Q20 5 21 6Q22 7 21 8L11 20Q10 21 9 20L3 14Q2 13 3 12Z',
 'plus':'M10 4Q10 2 12 2Q14 2 14 4V10H20Q22 10 22 12Q22 14 20 14H14V20Q14 22 12 22Q10 22 10 20V14H4Q2 14 2 12Q2 10 4 10H10Z',
 'leave':'M12 22Q10 22 10 20V13Q2 13 2 4Q2 2 4 2Q13 2 13 11Q13 5 20 5Q22 5 22 7Q22 15 14 15V20Q14 22 12 22Z',
 'grid':'M5 2H8Q11 2 11 5V8Q11 11 8 11H5Q2 11 2 8V5Q2 2 5 2ZM16 2H19Q22 2 22 5V8Q22 11 19 11H16Q13 11 13 8V5Q13 2 16 2ZM5 13H8Q11 13 11 16V19Q11 22 8 22H5Q2 22 2 19V16Q2 13 5 13ZM16 13H19Q22 13 22 16V19Q22 22 19 22H16Q13 22 13 19V16Q13 13 16 13Z',
 'wifi':'M2 7Q12 -1 22 7L20 10Q12 4 4 10ZM6 12Q12 7 18 12L16 15Q12 12 8 15ZM9 18Q12 15 15 18L12 22Z',
 }
 return f'<path d="{paths[name]}" transform="translate({x} {y}) scale({size/24})" fill="{color}" fill-rule="evenodd"/>'
def defs(prefix):
 return f'''<defs>
 <linearGradient id="{prefix}bg" x1="0" y1="0" x2="0.4" y2="1"><stop stop-color="#172a65"/><stop offset=".47" stop-color="#0a1025"/><stop offset="1" stop-color="#080c18"/></linearGradient>
 <radialGradient id="{prefix}glow" cx=".78" cy="0" r=".9"><stop stop-color="#327bff" stop-opacity=".32"/><stop offset=".55" stop-color="#294bd1" stop-opacity=".12"/><stop offset="1" stop-color="#122249" stop-opacity="0"/></radialGradient>
 <linearGradient id="{prefix}glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#34486d" stop-opacity=".62"/><stop offset="1" stop-color="#1a2038" stop-opacity=".76"/></linearGradient>
 <linearGradient id="{prefix}feature" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#365b94"/><stop offset=".48" stop-color="#2b4b7c"/><stop offset="1" stop-color="#233d65"/></linearGradient>
 <linearGradient id="{prefix}button" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#528cff"/><stop offset="1" stop-color="#3268eb"/></linearGradient>
 <linearGradient id="{prefix}nav" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#27324a"/><stop offset="1" stop-color="#151b2a"/></linearGradient>
 </defs>'''
def glass(prefix,x,y,w,h,r=22):return rect(x,y,w,h,f'url(#{prefix}glass)',r,BORDER)
def pill(x,y,s,color='#c4d9ff',bg='#30456d',w=70):return rect(x,y,w,26,bg,10)+text(x+w/2,y+17,s,12,color,600,'middle')
def status():
 s=text(28,31,'9:41',14,WHITE,600)
 for i,h in enumerate([4,7,10,13]):s+=rect(298+i*5,29-h,3,h,WHITE,1)
 return s+icon(323,14,'wifi',WHITE,14)+rect(345,18,22,11,'none',3,'#d8e3ff')+rect(347,20,16,7,WHITE,1)
def base(prefix,title=None,sub=None):
 s=defs(prefix)+rect(0,0,390,844,f'url(#{prefix}bg)',0)+rect(0,0,390,600,f'url(#{prefix}glow)',0)+status()
 if title:
  s+=glass(prefix,24,55,38,38,19)+icon(34,64,'back',WHITE,19)+text(195,80,title,18,WHITE,600,'middle')
  s+=rect(24,132,6,6,BLUE,3)+text(38,143,sub,26,WHITE,700)
 return s
def nav(prefix,active='홈'):
 s=rect(24,749,342,70,'#121e31',20,'#34445e')
 for x,label,kind in [(78,'홈','home'),(156,'회의실','room'),(234,'결재','document'),(312,'내 정보','user')]:
  selected=label==active
  if selected:s+=rect(x-34,759,68,50,'#293f60',12)
  s+=icon(x-11,766,kind,'#91b9ff' if selected else '#b0bdd2',22)+text(x,802,label,11,WHITE if selected else '#b0bdd2',650 if selected else 500,'middle')
 return s+rect(135,833,120,4,'#e5eaf6',2)
def cta(prefix,y,label,sub=None):
 s=rect(24,y,342,56,'#3975f0',14)+text(195,y+35,label,18,'white',700,'middle')
 if sub:s+=text(195,y-17,sub,14,MUTED,400,'middle')
 return s+rect(135,833,120,4,'#e5eaf6',2)
def section(y,label,more=None):
 return rect(24,y-10,6,6,BLUE,3)+text(38,y,label,19,WHITE,700)+(text(366,y,more,14,'#9cc0ff',500,'end') if more else '')
def input_block(prefix,y,label,value,kind=None):
 s=text(24,y,label,14,MUTED)+glass(prefix,24,y+14,342,54,16)+text(42,y+48,value,17,WHITE,600)
 if kind:s+=icon(326,y+31,kind,MUTED,20)
 return s
# Home priority: next meeting -> quick requests -> pending requests. Leave balance lives on the request screen.
P='ih-'; home=base(P)
home+=rect(24,61,42,42,'#d8e4fb',21)+text(45,88,'도',16,'#233e70',600,'middle')+text(78,77,'좋은 아침이에요',13,'#c9d6ee')+text(78,100,'이도경님',20,WHITE,650)+rect(326,61,40,40,'#1b2944',20,'#3a4c6b')+icon(336,71,'bell',WHITE,20)
home+=text(24,152,'다음 일정',14,'#c9d6ee',600)
home+=rect(24,166,342,150,'#1c3c73',20,'#4f73ad')+pill(44,186,'40분 후','#ffffff','#3a64b0',64)+text(346,204,'14:00 - 14:40',15,'white',600,'end')
home+=text(44,250,'아이디어 워크숍',24,'white',700)+icon(44,272,'room','#cfe0ff',18)+text(70,287,'라일락 룸 · 3층',15,'#e3ecff')
home+=text(24,356,'바로 신청',14,'#c9d6ee',600)
for x,label,sub,kind in [(24,'공간 예약','빈 회의실 찾기','room'),(201,'근태 신청','연차·반차·시간 휴가','calendar')]:
 home+=rect(x,370,165,112,'#16233b',18,'#3a4c6b')+rect(x+18,386,38,38,'#2b4f8c',12)+icon(x+25,393,kind,'#ffffff',24)+text(x+18,450,label,17,WHITE,700)+text(x+18,470,sub,12,'#c3cee0')+text(x+147,410,'›',24,'#9cc0ff',600,'end')
home+=section(540,'처리 중인 신청','전체 보기')
for y,title,sub,state,color in [(562,'오후 반차 · 6월 12일','운영지원팀 1차 검토','검토 중','#c4d9ff'),(645,'라일락 룸 · 6월 14일','10:00 - 11:00 · 예약 확인','확정','#bfe8cf')]:
 home+=rect(24,y,342,72,'#16233b',18,'#33445f')+text(42,y+31,title,16,WHITE,650)+text(42,y+54,sub,13,'#c3cee0')+rect(282,y+22,66,28,'#24365a',10)+text(315,y+41,state,12,color,650,'middle')
home+=nav(P)
# Booking: room summary with a visible selected slot.
P='ib-';booking=base(P,'회의실 예약','집중할 공간을 골라요')+text(24,173,'회의에 맞는 시간과 공간을 선택해 주세요.',14,'#bdc9e2')
booking+=glass(P,24,200,342,96,24)+rect(42,220,54,54,'#2c487b',17)+icon(56,234,'room','#c6dcff',26)+text(112,233,'라일락 룸',22,WHITE,650)+text(112,260,'3층 · 최대 5명 · 모니터',13,MUTED)+pill(280,217,'예약 가능','#c9ddff','#28476d',70)
booking+=input_block(P,332,'예약일','2027년 6월 9일','calendar')+section(446,'시작 시간','40분 이용')
for x,label,selected in [(24,'13:00',False),(142,'14:00',True),(260,'15:00',False)]:
 booking+=(rect(x,466,106,48,'#28466f',12,'#8bb3f9') if selected else glass(P,x,466,106,48,16))+text(x+53,496,label,16,WHITE if selected else '#c0cae0',600 if selected else 400,'middle')
booking+=input_block(P,554,'회의 제목','아이디어 워크숍')+glass(P,24,651,342,58,18)+icon(42,669,'time','#afcaff',22)+text(78,687,'14:00 - 14:40',16,WHITE,500)+text(348,687,'총 40분',14,MUTED,400,'end')+cta(P,748,'회의실 예약하기')
# Conflict: input is preserved, overlap explained under the time field, nearest alternatives offered.
P='ic-';conflict=base(P,'회의실 예약','집중할 공간을 골라요')+text(24,173,'회의에 맞는 시간과 공간을 선택해 주세요.',14,'#bdc9e2')
conflict+=glass(P,24,200,342,96,24)+rect(42,220,54,54,'#2c487b',17)+icon(56,234,'room','#c6dcff',26)+text(112,233,'라일락 룸',22,WHITE,650)+text(112,260,'3층 · 최대 5명 · 모니터',13,MUTED)
conflict+=section(336,'시작 시간','40분 이용')
for x,label,state in [(24,'13:00','free'),(142,'14:00','clash'),(260,'15:00','free')]:
 if state=='clash':conflict+=rect(x,356,106,48,'#3a2030',12,'#ff9aa8')+text(x+53,386,label,16,'#ffd5db',650,'middle')
 else:conflict+=glass(P,x,356,106,48,16)+text(x+53,386,label,16,'#c0cae0',400,'middle')
conflict+=rect(24,416,342,64,'#2a1a26',14,'#7a3a4c')+text(42,442,'14:00 - 14:40에 다른 예약이 있어요',15,'#ffd5db',650)+text(42,466,'제품 리뷰 · 14:00 - 15:00',13,'#e7b8c1')
conflict+=section(526,'바로 예약할 수 있어요')
for y,title,sub in [(546,'라일락 룸 · 15:00 - 15:40','같은 회의실 · 가장 가까운 빈 시간'),(624,'세이지 룸 · 14:00 - 14:40','같은 시간 · 2층 · 최대 4명')]:
 conflict+=rect(24,y,342,66,'#16233b',16,'#3a4c6b')+text(42,y+28,title,16,WHITE,650)+text(42,y+50,sub,13,'#c3cee0')+text(348,y+40,'선택',14,'#9cc0ff',650,'end')
conflict+=text(195,724,'입력한 회의 제목과 날짜는 그대로 유지돼요.',13,MUTED,400,'middle')+rect(24,748,342,56,'#2a3a58',14)+text(195,783,'시간을 다시 선택해 주세요',17,'#9fb0cc',650,'middle')+rect(135,833,120,4,'#e5eaf6',2)
# Leave request: clear segmentation, a compact form and reviewer identity.
P='ir-';request=base(P,'근태 신청','잠깐의 쉼도, 간편하게')+text(24,173,'신청 내용을 확인하고 제출해 주세요.',14,'#bdc9e2')
request+=glass(P,24,202,342,58,22)
for x,label,selected in [(30,'연차',False),(142,'오후 반차',True),(254,'시간 휴가',False)]:
 if selected:request+=rect(x,208,106,46,'#28466f',12,'#8bb3f9')
 request+=text(x+53,237,label,15,WHITE if selected else '#aebbd5',600 if selected else 400,'middle')
request+=rect(24,276,342,36,'#1b2c4a',10)+text(40,299,'남은 연차 8.5일 · 반차 신청 후 8.0일',14,'#d6e4ff',600)+input_block(P,344,'신청일','2027년 6월 12일','calendar')+input_block(P,446,'신청 사유','개인 일정')+section(560,'검토 담당')
request+=glass(P,24,580,342,82,22)+rect(42,601,40,40,'#38466a',20)+text(62,628,'서',15,'#d8e6ff',600,'middle')+text(98,613,'최서윤',17,WHITE,550)+text(98,638,'운영지원팀 · 리더',13,MUTED)+pill(284,607,'1차 검토','#c7d9ff','#2a3b61',64)
request+=cta(P,748,'반차 신청하기','신청 후 내 결재에서 진행 상황을 볼 수 있어요.')
FONT='SUIT UI, sans-serif'
from io import BytesIO
from fontTools.ttLib import TTFont
from fontTools import subset
_font=TTFont(Path(__file__).resolve().parents[1]/'src/fonts/original/SUIT-Variable.woff2');_opt=subset.Options();_opt.layout_features=['*'];_opt.name_IDs=['*'];_ss=subset.Subsetter(options=_opt);_ss.populate(text=Path(__file__).read_text());_ss.subset(_font)
for _n in _font['name'].names:
 if _n.nameID in [1,3,4,6,16,17]:
  _n.string={1:'SUIT UI',3:'MorrowUI-SUITSubset-20261124',4:'SUIT UI Variable',6:'SUITUI-Variable',16:'SUIT UI',17:'Regular'}[_n.nameID].encode(_n.getEncoding(),errors='replace')
_font.flavor='woff2';_buf=BytesIO();_font.save(_buf);FONT_DATA=base64.b64encode(_buf.getvalue()).decode('ascii')
FONT_STYLE=f"<style>@font-face{{font-family:'SUIT UI';font-style:normal;font-weight:100 900;src:url(data:font/woff2;base64,{FONT_DATA}) format('woff2');}}text{{font-family:'SUIT UI',sans-serif;}}</style>"
def save(name,body,label,w=390,h=844):
 (OUT/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><title>{label} · 공개용 재설계 · 모든 데이터는 가상</title>{FONT_STYLE}<g font-family="{FONT}">{body}</g></svg>',encoding='utf-8')
save('intranet-home',home,'MORROW 모바일 인트라넷 홈')
save('intranet-booking',booking,'MORROW 회의실 예약')
save('intranet-request',request,'MORROW 근태 신청')
save('intranet-conflict',conflict,'MORROW 회의실 예약 시간 충돌')
# Editorial cover uses two original UI screens, without a third-party device image.
board='''<defs><radialGradient id="board-bg" cx=".68" cy=".1" r="1"><stop stop-color="#244ca2"/><stop offset=".5" stop-color="#111d42"/><stop offset="1" stop-color="#080d1e"/></radialGradient><clipPath id="home-cut"><rect width="390" height="844" rx="37"/></clipPath><clipPath id="booking-cut"><rect width="390" height="844" rx="37"/></clipPath></defs>'''+rect(0,0,1440,1080,'url(#board-bg)',0)
board+=text(80,84,'morrow',32,WHITE,650)+text(1358,82,'MOBILE WORKSPACE',15,'#b0c3ed',500,'end')+text(80,141,'하루의 업무를, 한곳에서.',35,WHITE,600)
for x,y,body,clip in [(283,188,home,'home-cut'),(816,245,booking,'booking-cut')]:
 board+=f'<g transform="translate({x} {y}) scale(.86)">'+rect(-10,-10,410,864,'#070b14',47,'#75809a')+f'<g clip-path="url(#{clip})">{body}</g></g>'
board+=text(80,1004,'결재 현황 · 공간 예약 · 근태 신청',19,'#b0c3ed')+text(1358,1004,'공개용 재설계 / 가상 데이터',15,'#9baccc',400,'end')
save('intranet-overview',board,'MORROW 인트라넷 홈과 회의실 예약',1440,1080)
print('Generated MORROW home, booking, leave request and overview')
