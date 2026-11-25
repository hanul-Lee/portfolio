"""Folio board: a monochrome public concept of a personal kanban workflow."""
from pathlib import Path
from html import escape
from io import BytesIO
import base64
from fontTools.ttLib import TTFont
from fontTools import subset
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'src/assets/cases/public-concepts';OUT.mkdir(parents=True,exist_ok=True)
INK='#292827';MUTED='#77736e';LINE='#e3e1de';BG='#f5f4f2';ACCENT='#292827'
def rect(x,y,w,h,fill='white',r=14,stroke=None):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'
def t(x,y,s,size=16,fill=INK,weight=400,anchor=None):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}"'+(f' text-anchor="{anchor}"' if anchor else '')+'>'+escape(str(s))+'</text>'
def rule(x,y,w):return f'<path d="M{x} {y}h{w}" stroke="{LINE}"/>'
def icon(x,y,name,color=MUTED,size=21):
 paths={'grid':'M3 3H10V10H3ZM14 3H21V10H14ZM3 14H10V21H3ZM14 14H21V21H14Z','task':'M5 3H19V21H5ZM8 9L10 11L15 6M8 16H15','plus':'M4 12H20M12 4V20','search':'M17 10A7 7 0 1 1 3 10A7 7 0 1 1 17 10M15 15L21 21','calendar':'M4 5H20V21H4ZM8 2V8M16 2V8M4 11H20','filter':'M3 6H21M6 12H18M9 18H15','sort':'M7 3V21M3 7L7 3L11 7M15 6H21M15 12H19M15 18H17','user':'M16 7A4 4 0 1 1 8 7A4 4 0 1 1 16 7M4 22C4 12 20 12 20 22','link':'M9 8L12 5C18 -1 25 6 19 12L16 15M15 16L12 19C6 25 -1 18 5 12L8 9M8 16L16 8','file':'M5 3H16L20 7V21H5ZM9 11H16M9 16H15'}
 return f'<path d="{paths[name]}" transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
def tag(x,y,label,w=66,warm=False):return rect(x,y,w,25,'#e5e3df' if warm else '#eeece8',7)+t(x+11,y+17,label,12,'#45413b' if warm else '#69635c',500)
def avatar(x,y,label):return rect(x,y,27,27,'#e8e3dc',14)+t(x+13.5,y+18,label,12,'#635b50',600,'middle')
def thumb(x,y,size,variant,category):
 # Fixed square thumbnail: a cover image when present, otherwise a quiet category tile of the same size.
 if variant is None:
  return rect(x,y,size,size,'#f1efeb',10)+icon(x+size/2-11,y+size/2-18,'file','#a29b91',22)+t(x+size/2,y+size/2+22,category,12,'#8a8379',600,'middle')
 a=rect(x,y,size,size,['#e8e5df','#393733','#dcd8d1','#efece7'][variant],10)
 if variant==0:a+=rect(x+12,y+14,size-24,10,'#c9c3ba',3)+rect(x+12,y+32,size-40,8,'#d6d1c9',3)+rect(x+12,y+size-38,size-24,24,'#393733',6)
 if variant==1:a+=rect(x+12,y+12,size-24,size-44,'#56524c',6)+rect(x+12,y+size-24,size/2,8,'#c4beb4',3)
 if variant==2:
  for i in range(3):a+=rect(x+12+i*(size-24)/3,y+16,(size-24)/3-6,size-32,'#f7f6f3',5)
 if variant==3:
  for i in range(2):
   for j in range(2):a+=rect(x+14+i*(size-28)/2,y+14+j*(size-28)/2,(size-28)/2-6,(size-28)/2-6,'#393733' if (i+j)%2==0 else '#cfc9c0',8)
 return a
def card(x,y,title,desc,category,date,name,cover=None,done=False,w=390,h=160):
 # Same height for every card: thumbnail left, one line each for title, description and tag.
 a=rect(x,y,w,h,'white',12,LINE)+thumb(x+16,y+16,96,cover,category)
 tx=x+128
 a+=rect(tx,y+22,18,18,'#34332f' if done else 'white',5,LINE)
 if done:a+='<path d="M'+str(tx+4)+' '+str(y+31)+'l3 3 6-7" fill="none" stroke="white" stroke-width="1.7"/>'
 a+=t(tx+28,y+37,title,16,INK,650)+t(tx,y+64,desc,13,MUTED)+tag(tx,y+78,category,62,category=='검토')
 a+=rule(x+16,y+h-34,w-32)+icon(x+16,y+h-24,'calendar',MUTED,15)+t(x+38,y+h-12,date,12,MUTED)+icon(x+124,y+h-24,'file',MUTED,15)+t(x+146,y+h-12,'2',12,MUTED)+avatar(x+w-43,y+h-30,name)
 return a,h
a=rect(0,0,1600,1000,'white',0)+rect(0,0,226,1000,'#f3f2ef',0)+t(28,53,'folio',28,INK,750)+rect(28,82,170,43,'#ffffff',10,LINE)+icon(42,95,'search',MUTED,18)+t(69,109,'작업 검색',14,'#98928a')
for i,(label,kind) in enumerate([('내 작업','task'),('작업 보드','grid'),('일정','calendar'),('보관함','file')]):
 y=162+i*61
 if i==1:a+=rect(16,y-11,194,45,'#e4e1db',10)
 a+=icon(31,y,kind,INK if i==1 else MUTED,21)+t(68,y+17,label,16,INK if i==1 else MUTED,600 if i==1 else 400)
a+=rule(28,423,170)+t(28,461,'워크스페이스',13,MUTED,600)+t(28,503,'개인 디자인 작업',16,INK,600)+t(28,940,'개인 프로토타입 / 공개 시안',11,MUTED)
a+=t(258,55,'작업 보드',23,INK,700)+t(434,54,'개인 디자인 작업 / 2027년 4월',14,MUTED)+avatar(1533,28,'도')+rule(226,80,1374)
a+=t(258,130,'이번 주에 집중할 일',30,INK,700)+t(258,164,'작업 분야는 태그로, 진행 상태는 컬럼으로 구분해요.',16,MUTED)+rect(1427,105,139,48,INK,12)+icon(1443,120,'plus','white',19)+t(1473,135,'새 작업',16,'white',600)
a+=t(258,221,'보드',16,INK,650)+t(329,221,'목록',16,MUTED)+t(398,221,'캘린더',16,MUTED)+f'<path d="M258 237H290" stroke="{INK}" stroke-width="3"/>'
for x,label,kind in [(1327,'필터','filter'),(1449,'정렬','sort')]:a+=rect(x,190,110,42,BG,10)+icon(x+14,202,kind,MUTED,18)+t(x+42,217,label,14,INK,500)
a+=rule(258,246,1308)
columns=[(258,'할 일','3','#b8b3ac'),(700,'진행 중','2','#45413b'),(1142,'완료','2','#69635c')]
for x,title,count,color in columns:
 a+=rect(x,269,424,707,'#f7f6f4',14)+rect(x+20,291,9,9,color,5)+t(x+43,301,title,18,INK,650)+tag(x+110,282,count,30)+icon(x+380,284,'plus',MUTED,20)
for x,y,args in [(275,326,('컴포넌트 사용 기준','입력과 선택 상태 기준 모으기','디자인','4월 23일','도',0,False)),(275,502,('자료 화면 분류','프로젝트별 자료 구분','정리','4월 24일','도',None,False)),(275,678,('다음 주 일정 초안','우선순위부터 가볍게','기획','4월 25일','도',None,False)),(717,326,('회의실 예약 흐름','예약 전후 상태 비교','검토','4월 22일','도',2,False)),(717,502,('작업 카드 정보','필요한 정보와 보조 정보','디자인','4월 23일','도',1,False)),(1159,326,('리서치 노트','이번 주 확인한 내용','정리','4월 21일','도',None,True)),(1159,502,('아이콘 스타일','작은 크기에서 알아보기','검토','4월 20일','도',3,True))]:
 a+=card(x,y,*args)[0]
# Separate creation form, not a screenshot of the earlier implementation.
b=rect(0,0,900,1120,BG,0)+rect(40,35,820,1050,'white',22,LINE)+t(78,99,'새 작업',32,INK,700)+t(78,138,'할 일을 적고, 보드에서 이어서 관리해요.',17,MUTED)+rule(78,167,744)
def field(y,label,value,h=58):return t(78,y,label,16,MUTED,500)+rect(78,y+16,744,h,'#f7f6f3',12,LINE)+t(98,y+53,value,19,INK,500)
b+=field(213,'작업 제목','컴포넌트 사용 기준 정리')+field(326,'설명','입력과 선택 상태의 기준을 한곳에 모아요.',111)+t(78,523,'진행 상태',16,MUTED,500)
for x,label,active in [(78,'할 일',True),(330,'진행 중',False),(582,'완료',False)]:b+=rect(x,541,240,56,INK if active else '#f3f1ed',12)+t(x+120,577,label,18,'white' if active else MUTED,600,'middle')
b+=field(653,'담당자','이도경')+field(770,'마감일','2027년 4월 23일')+t(78,902,'첨부 파일',16,MUTED,500)+rect(78,923,744,54,'white',12,LINE)+icon(97,939,'file',MUTED,20)+t(131,958,'표지 이미지 추가',17,MUTED)
b+=rect(78,1004,226,52,'#f0eeea',12)+t(191,1037,'취소',18,INK,600,'middle')+rect(322,1004,500,52,INK,12)+t(572,1037,'작업 만들기',18,'white',650,'middle')
# Card move states at equal size: grab, drag with drop indicator, dropped with undo.
def move_panel(mode):
 W,H=900,660;a=rect(0,0,W,H,'white',0)
 for x,title,count in [(24,'진행 중','2' if mode!='after' else '1'),(462,'완료','2' if mode!='after' else '3')]:
  a+=rect(x,24,414,612,'#f7f6f4',14)+rect(x+20,46,9,9,'#45413b' if x==24 else '#69635c',5)+t(x+43,56,title,17,INK,650)+tag(x+120,37,count,30)
 def mini(x,y,args,shadow=False):
  s=''
  if shadow:s+=rect(x+6,y+10,382,160,'#d9d5cf',14)
  return s+card(x,y,*args,w=382)[0]
 moving=('작업 카드 정보','필요한 정보와 보조 정보','디자인','4월 23일','도',1,False)
 other=('회의실 예약 흐름','예약 전후 상태 비교','검토','4월 22일','도',2,False)
 done1=('리서치 노트','이번 주 확인한 내용','정리','4월 21일','도',None,True)
 done2=('아이콘 스타일','작은 크기에서 알아보기','검토','4월 20일','도',3,True)
 if mode=='grab':
  a+=mini(40,80,other)+mini(478,80,done1)+mini(478,256,done2)
  a+=f'<rect x="40" y="256" width="382" height="160" rx="12" fill="none" stroke="#b8b3ac" stroke-width="1.5" stroke-dasharray="6 5"/>'
  a+='<g transform="rotate(-2 230 350)">'+mini(34,268,moving,True)+'</g>'
  a+=t(231,470,'원래 자리는 점선으로 남아요',13,MUTED,500,'middle')
 elif mode=='drag':
  a+=mini(40,80,other)+f'<rect x="40" y="256" width="382" height="160" rx="12" fill="none" stroke="#b8b3ac" stroke-width="1.5" stroke-dasharray="6 5"/>'
  a+=f'<path d="M478 74H860" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'+f'<circle cx="478" cy="74" r="6" fill="{INK}"/>'
  a+=mini(478,92,done1)+mini(478,268,done2)
  a+='<g transform="rotate(-2 560 200)">'+mini(400,120,moving,True)+'</g>'
  a+=t(669,470,'굵은 선 위치에 들어가요',13,MUTED,500,'middle')
 else:
  a+=mini(40,80,other)
  a+=f'<rect x="474" y="76" width="390" height="168" rx="15" fill="none" stroke="{INK}" stroke-width="2"/>'+mini(478,80,moving)+mini(478,256,done1)+mini(478,432,done2)
  a+=rect(150,592,600,52,INK,12)+t(176,624,'‘작업 카드 정보’를 완료로 옮겼어요',15,'white',500)+t(724,624,'되돌리기',15,'#f3d38b',700,'end')
 return a
font=TTFont(ROOT/'src/fonts/original/SUIT-Variable.woff2');opt=subset.Options();opt.layout_features=['*'];opt.name_IDs=['*'];ss=subset.Subsetter(options=opt);ss.populate(text=Path(__file__).read_text());ss.subset(font)
for n in font['name'].names:
 if n.nameID in [1,3,4,6,16,17]:
  names={1:'Folio UI',3:'FolioUI-SUITSubset-20261124',4:'Folio UI Variable',6:'FolioUI-Variable',16:'Folio UI',17:'Regular'};n.string=names[n.nameID].encode(n.getEncoding(),errors='replace')
font.flavor='woff2';buf=BytesIO();font.save(buf);data=base64.b64encode(buf.getvalue()).decode();style=f"<style>@font-face{{font-family:'Folio SUIT';font-style:normal;font-weight:100 900;src:url(data:font/woff2;base64,{data}) format('woff2');}}text{{font-family:'Folio SUIT',sans-serif;}}</style>"
def save(name,body,label,w,h):(OUT/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><title>{label} · 공개용 리디자인 · 가상 작업 데이터</title>{style}{body}</svg>',encoding='utf-8')
save('kanban-board',a,'FOLIO 개인 작업 칸반 보드',1600,1000);save('kanban-move-before',move_panel('grab'),'FOLIO 카드 잡기',900,660);save('kanban-move-drag',move_panel('drag'),'FOLIO 카드 이동 중',900,660);save('kanban-move-after',move_panel('after'),'FOLIO 카드 놓은 후',900,660);save('kanban-create',b,'FOLIO 새 작업 입력 화면',900,1120)
print('Generated monochrome FOLIO kanban board and task form')
