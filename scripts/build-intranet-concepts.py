"""MORROW intranet concept: original vector UI with fictional work data."""
from pathlib import Path
from html import escape
import base64
OUT=globals().get('OUT',Path(__file__).resolve().parents[1]/'src/assets/cases/public-concepts')
OUT.mkdir(parents=True,exist_ok=True)
# Light workspace palette. Deep indigo carries the primary surfaces, iris marks interaction,
# marigold is reserved for "now" and time-sensitive signals. Kept distinct from the dark navy measure concept.
INK='#1c1b2e'; MUTED='#6b6a80'; FAINT='#a09fb2'; LINE='#e8e7f0'; PAGE='#f5f4f9'; CARD='#ffffff'
INDIGO='#2b2785'; IRIS='#5a4fe0'; LILAC='#ecebfb'; LILAC_LINE='#d6d3f2'
MARIGOLD='#f2b33d'; MARI_WASH='#fdf2d9'; MARI_INK='#8a5a00'
GREEN='#1d8a5a'; GREEN_WASH='#e2f4ea'; RED='#cf3550'; RED_WASH='#fdeef1'; RED_LINE='#f3b7c2'
WHITE=INK
def rect(x,y,w,h,fill,r=18,stroke=None,op=None,sw=1):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' fill-opacity="{op}"' if op is not None else '')+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'
def text(x,y,s,size=16,fill=INK,weight=400,anchor=None,ls=None,op=None):
 if ls is None: ls=-0.6 if size>=22 else (-0.2 if size>=15 else 0)
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}"'+(f' text-anchor="{anchor}"' if anchor else '')+(f' letter-spacing="{ls}"' if ls else '')+(f' fill-opacity="{op}"' if op is not None else '')+'>'+escape(str(s))+'</text>'
def line(x1,y1,x2,y2,c,w=1,dash=None,op=None):
 return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+(f' stroke-opacity="{op}"' if op is not None else '')+'/>'
def circle(cx,cy,r,fill,stroke=None,sw=1):
 return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'
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
def defs(p):
 return f'''<defs>
 <pattern id="{p}hatchD" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0V7" stroke="#ffffff" stroke-opacity=".28" stroke-width="2.4"/></pattern>
 <pattern id="{p}hatchL" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="7" fill="#f1f0f6"/><path d="M0 0V7" stroke="#d9d8e4" stroke-width="2.4"/></pattern>
 <pattern id="{p}hatchR" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="7" fill="#fdeef1"/><path d="M0 0V7" stroke="#f3b7c2" stroke-width="2.4"/></pattern>
 <pattern id="{p}dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#ffffff" fill-opacity=".16"/></pattern>
 <radialGradient id="{p}fade" cx="1" cy="0" r="1"><stop stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
 <mask id="{p}dotmask"><rect width="390" height="844" fill="url(#{p}fade)"/></mask>
 </defs>'''
def status():
 s=text(28,31,'9:41',14,INK,650)
 for i,h in enumerate([4,7,10,13]):s+=rect(298+i*5,29-h,3,h,INK,1)
 return s+icon(323,14,'wifi',INK,14)+rect(345,18,22,11,'none',3,'#9d9cb0')+rect(347,20,16,7,INK,1)
def base(p,title=None):
 s=defs(p)+rect(0,0,390,844,PAGE,0)+status()
 if title:
  s+=circle(43,74,19,CARD,LINE)+icon(34,65,'back',INK,18)+text(195,80,title,17,INK,650,'middle',0)
 return s
def heading(y,label,sub=None):
 s=text(24,y,label,25,INK,750)
 if sub:s+=text(24,y+28,sub,14,MUTED)
 return s
def section(y,label,right=None,count=None,right_color=MUTED):
 s=text(24,y,label,17,INK,700)
 if count:s+=rect(24+len(label)*14.6+8,y-15,22,20,LILAC,10)+text(24+len(label)*14.6+19,y-1,count,12,IRIS,700,'middle')
 if right:s+=text(366,y,right,13,right_color,600,'end')
 return s
def home_bar():return rect(135,833,120,4,INK,2)
def nav(active='홈'):
 s=rect(0,744,390,100,CARD,0)+line(0,744.5,390,744.5,LINE)
 for x,label,kind in [(55,'홈','home'),(145,'회의실','room'),(245,'결재','document'),(335,'내 정보','user')]:
  on=label==active
  if on:s+=rect(x-14,744,28,3,IRIS,1.5)
  s+=icon(x-11,760,kind,IRIS if on else '#b4b3c4',22)+text(x,798,label,11,INK if on else FAINT,700 if on else 500,'middle')
 return s+home_bar()
def cta(y,label,sub=None,enabled=True):
 s=''
 if sub:s+=text(195,y-18,sub,13,MUTED,400,'middle')
 s+=rect(24,y,342,56,INDIGO if enabled else '#e6e5ee',16)+text(195,y+35,label,17,'#ffffff' if enabled else FAINT,700,'middle',0)
 return s+home_bar()
def field(y,label,value,kind=None,note=None):
 s=text(24,y,label,13,MUTED,600)+rect(24,y+12,342,52,CARD,14,LINE)+text(42,y+44,value,16,INK,600)
 if note:s+=text(348,y+44,note,13,FAINT,500,'end')
 if kind:s+=icon(330,y+28,kind,'#b4b3c4',20)
 return s
def chip(x,y,label,fg,bg,w=None,h=24):
 w=w or len(label)*12+20
 return rect(x,y,w,h,bg,8)+text(x+w/2,y+h/2+4.5,label,12,fg,700,'middle',0)
def tx(t,x0,w,s=13,e=16):return round(x0+(t-s)/(e-s)*w,1)
def floorplan(x,y,s=1):
 # Original room plan: walls, a wall monitor, a five-seat table and the door swing.
 g=rect(0,0,110,118,'#f4f3fd',12,LILAC_LINE,sw=1.4)+rect(34,7,42,4,IRIS,2)
 g+=rect(30,32,50,54,CARD,10,'#cfcbea',sw=1.2)
 for cx,cy,w,h in [(18,40,8,15),(18,63,8,15),(84,40,8,15),(84,63,8,15),(48,92,14,8)]:g+=rect(cx,cy,w,h,'#dcd8f7',3)
 g+=rect(75,116,26,5,'#f4f3fd',0)+'<path d="M76 117.5A24 24 0 0 1 100 93.5" fill="none" stroke="#bdb8e6" stroke-width="1.2" stroke-dasharray="2 3"/>'+line(100,117.5,100,93.5,'#9f99dc',1.6)
 return f'<g transform="translate({x} {y}) scale({s})">{g}</g>'
def timeline(p,x0,y,w,h,booked,selected=None,clash=None,labels_y=None,start=13,end=16):
 # A half-day strip: booked slots are hatched, the chosen slot is solid iris, overlaps turn red.
 s=rect(x0,y,w,h,CARD,12,LINE)
 for t in range(start*2+1,end*2):
  xx=tx(t/2,x0,w,start,end);s+=line(xx,y+8,xx,y+h-8,LINE if t%2 else '#dddce7',1)
 for a,b,lab in booked:
  s+=rect(tx(a,x0,w,start,end)+2,y+4,tx(b,x0,w,start,end)-tx(a,x0,w,start,end)-4,h-8,f'url(#{p}hatchL)',9)
  if lab:s+=text(tx(a,x0,w,start,end)+12,y+h/2+4.5,lab,11,'#8f8ea3',650,None,0)
 if clash:
  a,b=clash;s+=rect(tx(a,x0,w,start,end)+2,y+4,tx(b,x0,w,start,end)-tx(a,x0,w,start,end)-4,h-8,f'url(#{p}hatchR)',9,RED,sw=1.6)
  s+=text((tx(a,x0,w,start,end)+tx(b,x0,w,start,end))/2,y+h/2+4.5,f'{int(a)}:{int((a%1)*60):02d}',12,RED,750,'middle',0)
 if selected:
  a,b=selected;s+=rect(tx(a,x0,w,start,end)+2,y+4,tx(b,x0,w,start,end)-tx(a,x0,w,start,end)-4,h-8,IRIS,9)
  s+=text((tx(a,x0,w,start,end)+tx(b,x0,w,start,end))/2,y+h/2+4.5,f'{int(a)}:{int((a%1)*60):02d}',12,'#ffffff',750,'middle',0)
 ly=labels_y or y+h+18
 for i,t in enumerate(range(start,end+1)):
  s+=text(tx(t,x0,w,start,end),ly,f'{t}:00',11,FAINT,500,'start' if t==start else ('end' if t==end else 'middle'),0)
 return s

# ---------- Home: next meeting on a timeline -> quick requests -> pending requests ----------
P='ih-';home=base(P)
home+=circle(44,82,20,LILAC)+text(44,88,'도',16,IRIS,750,'middle',0)
home+=text(76,76,'6월 9일 수요일',12,MUTED,500)+text(76,98,'이도경님, 좋은 아침이에요',18,INK,700)
home+=circle(346,82,20,CARD,LINE)+icon(336,72,'bell',INK,20)+circle(356,72,4.5,MARIGOLD,CARD,2)
home+=rect(24,128,342,204,INDIGO,24)+f'<rect x="24" y="128" width="342" height="204" rx="24" fill="url(#{P}dots)" mask="url(#{P}dotmask)"/>'
home+=chip(44,148,'40분 후',INDIGO,MARIGOLD,62)+icon(252,151,'room','#b9b4f0',16)+text(346,164,'라일락 룸 3층',13,'#d5d2f7',600,'end',0)
home+=text(44,210,'아이디어 워크숍',25,'#ffffff',750)+text(44,236,'14:00 - 14:40 · 5명 참석',14,'#bdb9ef',500)
# meeting strip 13:00-16:00 with the current time marker at 13:20
x0,w=44,302
home+=rect(x0,262,w,24,'#ffffff',7,op=.09)
for t in [14,15]:home+=line(tx(t,x0,w),266,tx(t,x0,w),282,'#ffffff',1,op=.25)
home+=rect(tx(15,x0,w)+1,264,tx(16,x0,w)-tx(15,x0,w)-3,20,f'url(#{P}hatchD)',5)
home+=rect(tx(14,x0,w)+1,264,tx(14+40/60,x0,w)-tx(14,x0,w)-2,20,'#ffffff',5)
nx=tx(13+20/60,x0,w);home+=line(nx,256,nx,290,MARIGOLD,2)+circle(nx,256,4,MARIGOLD)
for t in [13,14,15,16]:home+=text(tx(t,x0,w),310,f'{t}:00',11,'#a9a5e6',500,'start' if t==13 else ('end' if t==16 else 'middle'),0)
home+=section(374,'바로 신청')
for x,label,sub,kind,tile,ink in [(24,'공간 예약','지금 빈 회의실 4곳','room',LILAC,IRIS),(201,'근태 신청','연차·반차·시간 휴가','calendar',MARI_WASH,MARI_INK)]:
 home+=rect(x,390,165,104,CARD,18,LINE)+rect(x+16,406,40,40,tile,12)+icon(x+24,414,kind,ink,24)+icon(x+139,416,'chevron','#c4c3d2',14)
 home+=text(x+16,470,label,16,INK,700)+text(x+16,486,sub,12,MUTED)
home+=section(536,'처리 중인 신청','전체 보기','2',IRIS)
home+=rect(24,552,342,94,CARD,18,LINE)+text(42,582,'오후 반차 · 6월 11일',15,INK,700)+text(348,582,'1차 검토 중',12,IRIS,700,'end',0)
xs=[58,170,282];home+=line(xs[0],610,xs[1],610,IRIS,2)+line(xs[1],610,xs[2],610,LINE,2,'2 4')
home+=circle(xs[0],610,6,IRIS)+circle(xs[1],610,7,CARD,IRIS,2.4)+circle(xs[1],610,2.6,IRIS)+circle(xs[2],610,6,CARD,'#d4d3df',2)
for x_,lab,col in zip(xs,['신청','1차 검토','최종 승인'],[MUTED,INK,FAINT]):home+=text(x_,632,lab,11,col,650 if col==INK else 500,'middle',0)
home+=rect(24,658,342,68,CARD,18,LINE)+rect(40,672,40,40,LILAC,10)+text(60,688,'6월',9,IRIS,600,'middle',0)+text(60,705,'14',15,IRIS,800,'middle',0)
home+=text(94,688,'라일락 룸 예약',15,INK,700)+text(94,706,'10:00 - 11:00 월요일',12,MUTED)+chip(304,680,'확정',GREEN,GREEN_WASH,46)
home+=nav()

# ---------- Booking: room plan, week strip, half-day timeline ----------
P='ib-';booking=base(P,'회의실 예약')+heading(140,'집중할 공간을 골라요','회의에 맞는 날짜와 시간을 선택해 주세요.')
booking+=rect(24,192,342,146,CARD,22,LINE)+floorplan(40,206,1)
booking+=text(166,232,'라일락 룸',20,INK,750)+text(166,254,'3층 동쪽 창가',13,MUTED)
cx=166
for lab in ['5명','모니터','화이트보드']:
 w_=len(lab)*12+18;booking+=chip(cx,268,lab,'#4b4a63','#f1f0f6',w_);cx+=w_+6
booking+=circle(170,311,4,GREEN)+text(181,315,'오늘 14:00 이후 예약 가능',12,GREEN,650,None,0)
booking+=section(374,'예약일','2027년 6월')
for i,(d,n) in enumerate(zip('월화수목금토일',[7,8,9,10,11,12,13])):
 x=24+i*49;on=n==9;wk=i>=5
 booking+=rect(x,388,44,60,INDIGO if on else CARD,13,None if on else LINE)
 booking+=text(x+22,409,d,11,'#c9c6f2' if on else (FAINT if wk else MUTED),500,'middle',0)+text(x+22,434,n,17,'#ffffff' if on else (FAINT if wk else INK),750,'middle',0)
 if n==8:booking+=circle(x+22,442,2,'#c4c3d2')
booking+=section(490,'시작 시간','40분 이용')
booking+=timeline(P,24,504,342,52,[(13,13.5,None),(15.5,16,'예약됨')],selected=(14,14+40/60))
booking+=field(612,'회의 제목','아이디어 워크숍',note='12/30')
booking+=cta(748,'라일락 룸 예약하기','6월 9일 수요일 14:00 - 14:40')

# ---------- Conflict: the overlap is drawn on the timeline, input is kept, alternatives offered ----------
P='ic-';conflict=base(P,'회의실 예약')+heading(140,'집중할 공간을 골라요','회의에 맞는 날짜와 시간을 선택해 주세요.')
conflict+=rect(24,192,342,84,CARD,20,LINE)+floorplan(38,203,.52)+text(112,228,'라일락 룸',18,INK,750)+text(112,250,'3층 동쪽 창가 · 6월 9일 수요일',13,MUTED)
conflict+=section(318,'시작 시간','40분 이용')
conflict+=timeline(P,24,332,342,52,[(13,13.5,None),(14,15,None),(15.5,16,None)],clash=(14,14+40/60))
conflict+=text(tx(14+40/60,24,342)+8,362,'제품 리뷰',11,'#8f8ea3',650,None,0)
conflict+=rect(24,414,342,66,RED_WASH,16,RED_LINE)+circle(48,447,11,RED)+text(48,452,'!',14,'#ffffff',800,'middle',0)
conflict+=text(70,441,'14:00 - 14:40에 다른 예약이 있어요',14,RED,700,None,0)+text(70,462,'제품 리뷰가 15:00까지 이 방을 쓰고 있어요.',12,'#a34a5c')
conflict+=section(522,'바로 예약할 수 있어요')
for y,time,end,title,sub in [(538,'15:00','15:40','라일락 룸','같은 방에서 가장 가까운 빈 시간'),(616,'14:00','14:40','세이지 룸','같은 시간 · 2층 · 최대 4명')]:
 conflict+=rect(24,y,342,66,CARD,16,LINE)+rect(36,y+10,62,46,LILAC,11)+text(67,y+31,time,14,IRIS,800,'middle',0)+text(67,y+47,end+'까지',10,'#7d75e6',600,'middle',0)
 conflict+=text(112,y+29,title,15,INK,700)+text(112,y+49,sub,12,MUTED)+chip(308,y+21,'선택',IRIS,LILAC,46)
conflict+=icon(98,712,'check',GREEN,14)+text(118,724,'입력한 회의 제목과 날짜는 그대로 유지돼요.',12,MUTED,500,None,0)
conflict+=cta(748,'시간을 다시 선택해 주세요',enabled=False)

# ---------- Leave request: segmented type, balance gauge, approval line ----------
P='ir-';request=base(P,'근태 신청')+heading(140,'잠깐의 쉼도, 간편하게','신청 내용을 확인하고 제출해 주세요.')
request+=rect(24,192,342,50,'#ebeaf2',14)
for x,label,on in [(28,'연차',False),(141,'오후 반차',True),(254,'시간 휴가',False)]:
 if on:request+=rect(x,196,108,42,CARD,11,'#dcdbe6')
 request+=text(x+54,222,label,14,IRIS if on else MUTED,700 if on else 500,'middle',0)
request+=rect(24,258,342,112,CARD,18,LINE)+text(42,286,'남은 연차',13,MUTED,600)
request+=text(42,322,'8.5',30,INK,800)+text(91,322,'일',16,INK,600)+text(348,322,'신청 후 8.0일',13,IRIS,700,'end',0)
gx,gw=42,306;u=gw/15
request+=rect(gx,338,gw,8,'#eeedf4',4)+rect(gx,338,u*8,8,IRIS,4)+rect(gx+u*8+1.5,338,u*.5,8,MARIGOLD,2)
request+=rect(gx,356,8,8,MARIGOLD,2)+text(gx+14,363,'이번 신청 0.5일',11,MUTED,500,None,0)+text(348,363,'연간 15일',11,FAINT,500,'end',0)
request+=field(398,'신청일','2027년 6월 11일 금요일','calendar')+field(494,'신청 사유','개인 일정')
request+=section(598,'결재선')
request+=rect(24,612,342,84,CARD,18,LINE)
request+=circle(62,654,20,LILAC)+text(62,659,'서',15,IRIS,750,'middle',0)+text(90,650,'최서윤',15,INK,700)+text(90,670,'1차 검토',12,MUTED)
request+=line(158,654,186,654,'#c4c3d2',1.6,'2 4')+icon(184,647,'chevron','#c4c3d2',14)
request+=circle(226,654,20,MARI_WASH)+text(226,659,'한',15,MARI_INK,750,'middle',0)+text(254,650,'한지우',15,INK,700)+text(254,670,'최종 승인',12,MUTED)
request+=cta(748,'반차 신청하기','신청 후 내 결재에서 진행 상황을 볼 수 있어요.')

FONT='SUIT UI, sans-serif'
from io import BytesIO
from fontTools.ttLib import TTFont
from fontTools import subset
_font=TTFont(Path(__file__).resolve().parents[1]/'src/fonts/original/SUIT-Variable.woff2');_opt=subset.Options();_opt.layout_features=['*'];_opt.name_IDs=['*'];_ss=subset.Subsetter(options=_opt);_ss.populate(text=Path(__file__).read_text()+'0123456789:');_ss.subset(_font)
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

# ---------- Editorial cover: left story column, phones on an indigo day-schedule panel ----------
board='''<defs><clipPath id="home-cut"><rect width="390" height="844" rx="37"/></clipPath><clipPath id="booking-cut"><rect width="390" height="844" rx="37"/></clipPath><clipPath id="panel-cut"><rect x="660" y="72" width="708" height="936" rx="40"/></clipPath>
<filter id="phone-shadow" x="-20%" y="-10%" width="140%" height="130%"><feDropShadow dx="0" dy="24" stdDeviation="28" flood-color="#0d0b3a" flood-opacity=".35"/></filter></defs>'''+rect(0,0,1440,1080,PAGE,0)
board+=rect(660,72,708,936,INDIGO,40)+'<g clip-path="url(#panel-cut)">'
for i,hh in enumerate(range(9,20)):
 y=150+i*80;board+=line(660,y,1368,y,'#ffffff',1,op=.08)+text(690,y-10,f'{hh:02d}:00',13,'#8f8ad6',500,None,0)
board+=line(660,322,1368,322,MARIGOLD,2,op=.9)+circle(668,322,5,MARIGOLD)+'</g>'
board+=f'<rect x="96" y="104" width="34" height="34" rx="10" fill="{INDIGO}"/>'+rect(105,113,16,21,MARIGOLD,3)+circle(116,124,1.8,INDIGO)
board+=text(142,130,'morrow',28,INK,750,None,-0.8)
board+=text(96,300,'하루의 업무를,',46,INK,750,None,-1.6)+text(96,358,'한곳에서.',46,INK,750,None,-1.6)
for i,l in enumerate(['회의실 예약과 근태 신청을 모바일 홈에서 바로','시작하도록, 오늘 일정과 처리 중인 신청을','가장 먼저 보여 주는 사내 워크스페이스입니다.']):board+=text(96,420+i*28,l,17,MUTED,500,None,-0.2)
for i,(kind,tile,ink,t1,t2) in enumerate([('time',MARI_WASH,MARI_INK,'오늘 일정 먼저','다음 회의와 남은 시간을 타임라인으로'),('room',LILAC,IRIS,'빈 회의실 바로 예약','평면과 시간표를 보며 공간 선택'),('document',GREEN_WASH,GREEN,'근태 신청과 결재선','남은 연차와 검토 담당을 한 화면에')]):
 y=560+i*92;board+=line(96,y-18,560,y-18,LINE)+rect(96,y,44,44,tile,12)+icon(106,y+10,kind,ink,24)+text(160,y+19,t1,18,INK,700)+text(160,y+41,t2,14,MUTED)
board+=line(96,y+74,560,y+74,LINE)
for x,y,body,clip in [(706,236,home,'home-cut'),(1010,330,booking,'booking-cut')]:
 board+=f'<g transform="translate({x} {y}) scale(.78)" filter="url(#phone-shadow)">'+rect(-10,-10,410,864,'#15142a',47)+f'<g clip-path="url(#{clip})">{body}</g></g>'
board+=text(96,1004,'공개용 재설계 / 모든 인물·일정·수치는 가상',14,FAINT,500,None,0)
save('intranet-overview',board,'MORROW 인트라넷 홈과 회의실 예약',1440,1080)
print('Generated MORROW home, booking, leave request and overview')
