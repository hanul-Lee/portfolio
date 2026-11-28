"""MOA WORK: original ERP portfolio illustrations, using only fictional data."""
from pathlib import Path
from html import escape
from io import BytesIO
import base64
from fontTools.ttLib import TTFont
from fontTools import subset
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'src/assets/cases/public-concepts';OUT.mkdir(parents=True,exist_ok=True)
INK='#17222a';MUTED='#66727a';LINE='#e5e8e7';BG='#f2f4f3'
def rect(x,y,w,h,fill='white',r=20,stroke=None):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'
def t(x,y,s,size=16,fill=INK,weight=400,anchor=None):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}"'+(f' text-anchor="{anchor}"' if anchor else '')+'>'+escape(str(s))+'</text>'
def rule(x,y,w,color=LINE):return f'<path d="M{x} {y}h{w}" stroke="{color}"/>'
def icon(x,y,name,color=MUTED,size=22):
 paths={'grid':'M3 3H10V10H3ZM14 3H21V10H14ZM3 14H10V21H3ZM14 14H21V21H14Z','people':'M15 7A4 4 0 1 1 7 7A4 4 0 1 1 15 7M3 21C3 12 19 12 19 21M18 4C23 4 23 11 19 11M20 15C23 16 23 18 23 21','chart':'M4 20V12M12 20V5M20 20V9','file':'M5 3H19V21H5ZM9 8H15M9 12H15M9 16H13','search':'M17 10A7 7 0 1 1 3 10A7 7 0 1 1 17 10M15 15L21 21','bell':'M5 17V10C5 1 19 1 19 10V17H5M9 21H15','chevron':'M8 10L12 14L16 10','settings':'M12 4V2M12 22V20M4 12H2M22 12H20M6 6L4 4M20 20L18 18M18 6L20 4M4 20L6 18M17 12A5 5 0 1 1 7 12A5 5 0 1 1 17 12','time':'M21 12A9 9 0 1 1 3 12A9 9 0 1 1 21 12M12 6V12L16 15','arrow':'M4 12H20M14 6L20 12L14 18','check':'M5 12L10 17L20 6'}
 return f'<path d="{paths[name]}" transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
# Ledger palette: petrol for primary surfaces, teal shades for data series, orange only for
# "over plan / over standard" signals. Kept apart from the indigo intranet and the dark measure concept.
PETROL='#0f5e6e';PETROL_DARK='#123840';TEAL='#2a9aa8';TEAL_SOFT='#dcefee';ORANGE='#e2702a';ORANGE_WASH='#fcece0'
SERIES=['#0f5e6e','#2a9aa8','#7cc3c9','#bfe0e2']
BLUE=PETROL;BLUE_DEEP=PETROL_DARK
def tt(x,y,s,size=16,fill=INK,weight=400,anchor=None,ls=None):
 if ls is None:ls=-0.8 if size>=28 else (-0.3 if size>=18 else 0)
 return t(x,y,s,size,fill,weight,anchor).replace('<text ',f'<text letter-spacing="{ls}" ',1) if ls else t(x,y,s,size,fill,weight,anchor)
def line(x1,y1,x2,y2,c,w=1,dash=None,op=None):
 return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+(f' stroke-opacity="{op}"' if op is not None else '')+'/>'
def poly(points,c,w=2,dash=None,fill='none'):
 return '<path d="M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in points)+f'" stroke="{c}" stroke-width="{w}" fill="{fill}" stroke-linejoin="round" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def dot(cx,cy,r,fill,stroke=None,sw=2):return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'
def defs():
 return '''<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#eef0ee"/><path d="M0 0V6" stroke="#d3d8d6" stroke-width="2"/></pattern></defs>'''
def badge(x,y,label,kind='blue',w=92):
 fg,bg={'blue':(PETROL,TEAL_SOFT),'gray':('#5f6b70','#eef0ef'),'review':('#a8480f',ORANGE_WASH)}[kind]
 return rect(x,y,w,28,bg,8)+t(x+w/2,y+19,label,13,fg,700,'middle')
def logo(x,y):
 return rect(x,y,38,38,PETROL,11)+rect(x+9,y+10,20,4,'#ffffff',2)+rect(x+9,y+17,14,4,'#7cc3c9',2)+rect(x+9,y+24,17,4,'#ffffff',2)
def base(title,sub,active='전체 현황'):
 a=defs()+rect(0,0,1600,1000,BG,0)+rect(16,16,70,968,'white',24)+logo(32,36)
 for i,kind in enumerate(['grid','chart','people','file']):
  y=142+i*69;on=i==(0 if active=='전체 현황' else 1)
  if on:a+=rect(28,y-12,46,46,TEAL_SOFT,14)
  a+=icon(40,y,kind,PETROL if on else '#9aa3a6',22)
 a+=icon(40,926,'settings','#9aa3a6')+tt(116,60,'모아워크',23,INK,800)+t(116,82,'비용·인원 관리',12,MUTED,500)
 for x,label in [(500,'전체 현황'),(612,'프로젝트'),(716,'인원 내역'),(828,'보고서')]:
  on=label==active;a+=t(x,62,label,16,INK if on else MUTED,750 if on else 500)
  if on:a+=rect(x,74,len(label)*16,3,PETROL,1.5)
 a+=line(500,80.5,900,80.5,LINE)
 a+=rect(1161,32,47,46,'white',14)+icon(1174,45,'search')+rect(1220,32,47,46,'white',14)+icon(1233,45,'bell')+dot(1252,44,4,ORANGE,'white',2)+rect(1280,31,282,48,'white',24)+dot(1306,55,16,TEAL_SOFT)+t(1306,61,'도',14,PETROL,700,'middle')+t(1334,61,'이도경 · 운영관리팀',15,INK,500)+icon(1521,44,'chevron',MUTED,20)
 a+=tt(116,142,title,30,INK,800)+t(116,172,sub,15,MUTED)
 a+=rect(116,194,1450,57,'white',16)+t(138,229,'조회 범위',14,MUTED,600)
 for x,w,label in [(230,145,'전사' if active=='전체 현황' else '프로젝트'),(390,235,'2027.01.01 - 06.30'),(640,172,'모든 조직')]:a+=rect(x,204,w,37,BG,10)+t(x+16,228,label,15,INK,500)+icon(x+w-30,214,'chevron',MUTED,17)
 a+=t(1300,228,'기준일 2027.06.30',13,MUTED,500)+rect(1430,204,114,37,PETROL,10)+t(1487,228,'조회하기',15,'white',700,'middle')
 return a
def burnup(x,y,w,h,title,actual,plan,maximum,sub_max,unit='단위: 백만원'):
 # Monthly execution bars plus cumulative plan (dashed) and actual (solid) lines on a second scale.
 a=rect(x,y,w,h,'white',22)+tt(x+24,y+38,title,19,INK,750)+t(x+w-24,y+37,unit,13,MUTED,400,'end')
 a+=rect(x+24,y+58,10,10,TEAL,3)+t(x+40,y+68,'월 집행',13,MUTED)+line(x+108,y+63,x+130,y+63,PETROL,2.5)+t(x+136,y+68,'누적 집행',13,MUTED)+line(x+214,y+63,x+236,y+63,'#9aa3a6',2,'4 4')+t(x+242,y+68,'누적 계획',13,MUTED)
 top=y+96;bottom=y+h-40;H=bottom-top;left=x+56;right=x+w-60;step=(right-left)/len(actual)
 for i in range(5):
  yy=bottom-H*i/4;a+=line(left,yy,right,yy,'#eef0ef')+t(left-12,yy+4,int(maximum*i/4),11,MUTED,400,'end')+t(right+12,yy+4,int(sub_max*i/4),11,'#9aa3a6',400)
 ca=cp=0;pa=[];pp=[]
 for i,(v,p) in enumerate(zip(actual,plan)):
  cx=left+step*i+step/2;hh=H*v/maximum;a+=rect(cx-11,bottom-hh,22,hh,TEAL if i<len(actual)-1 else PETROL,5)+t(cx,bottom+24,f'{i+1}월',12,MUTED,500,'middle')
  ca+=v;cp+=p;pa.append((cx,bottom-H*ca/sub_max));pp.append((cx,bottom-H*cp/sub_max))
 a+=poly(pp,'#9aa3a6',2,'5 5')+poly(pa,PETROL,2.6)
 for px,py in pa:a+=dot(px,py,3.5,'white',PETROL,2)
 ex,ey=pa[-1];gx,gy=pp[-1]
 a+=line(ex+18,ey,ex+18,gy,ORANGE,1.5)+line(ex+14,ey,ex+22,ey,ORANGE,1.5)+line(ex+14,gy,ex+22,gy,ORANGE,1.5)
 a+=rect(ex-138,(ey+gy)/2-15,112,30,ORANGE_WASH,8)+t(ex-82,(ey+gy)/2+5,f'계획 대비 -{cp-ca:.1f}',12,'#a8480f',700,'middle')
 return a
def heatmap(x,y,w,h,rows):
 a=rect(x,y,w,h,'white',22)+tt(x+24,y+38,'프로젝트별 월 투입 시간',19,INK,750)+t(x+w-24,y+37,'단위: 시간',13,MUTED,400,'end')
 cw=(w-176)/6;ch=40;top=y+86
 for j in range(6):a+=t(x+152+cw*j+cw/2,top-10,f'{j+1}월',12,MUTED,500,'middle')
 for i,(name,vals) in enumerate(rows):
  yy=top+i*ch;a+=t(x+24,yy+ch/2+5,name,14,INK,600)
  for j,v in enumerate(vals):
   k=(v-120)/(320-120);col=['#e3f1f1','#bfe0e2','#7cc3c9','#2a9aa8','#0f5e6e'][min(4,int(k*5))]
   a+=rect(x+152+cw*j+2,yy+2,cw-4,ch-4,col,7)+t(x+152+cw*j+cw/2,yy+ch/2+5,v,12,'white' if k>.6 else INK,600,'middle')
 lx=x+152;ly=top+ch*len(rows)+16
 a+=t(lx,ly+10,'적음',11,MUTED)
 for i,c in enumerate(['#e3f1f1','#bfe0e2','#7cc3c9','#2a9aa8','#0f5e6e']):a+=rect(lx+32+i*22,ly,20,12,c,3)
 return a+t(lx+148,ly+10,'많음',11,MUTED)
def overview():
 a=base('비용과 인원을 한눈에','조회 조건을 정하면 집행 비용과 프로젝트별 투입 현황을 같은 기준으로 보여 줘요.')
 projects=[('해솔 연구동',106.4,140,14,1680),('누리 문화관',88.2,115,10,1456),('여울 복합센터',68.6,95,8,1232),('모래빛 업무동',49.6,70,6,928)]
 # Budget bar: executed amount split by project, remaining budget hatched.
 a+=rect(116,275,880,126,'white',22)+t(140,306,'예산 대비 집행',14,MUTED,600)
 a+=tt(140,356,'74.5',44,INK,800,None,-1.6)+t(232,356,'%',22,INK,700)+t(276,334,'312,800,000원 집행',16,INK,700)+t(276,356,'총 예산 420,000,000원 중 잔액 107,200,000원',13,MUTED)
 bx,bw=140,832;cx=bx
 a+=rect(bx,370,bw,14,'url(#hatch)',4)
 for i,(n,v,*_) in enumerate(projects):
  ww=bw*v/420;a+=rect(cx,370,ww-2,14,SERIES[i],3);cx+=ww
 a+=t(972,356,'잔액 25.5%',13,MUTED,600,'end')
 # One supporting panel instead of three identical cards.
 a+=rect(1020,275,546,126,'white',22)
 for i,(label,value,unit,delta) in enumerate([('투입 인원','38','명','전월 대비 +2명'),('누적 투입 시간','5,296','시간','월평균 883시간')]):
  x=1044+i*262;a+=t(x,306,label,14,MUTED,600)+tt(x,352,value,32,INK,800)+t(x+sum(17.5 if c.isdigit() else 8 for c in value)+5,352,unit,16,INK,600)+t(x,380,delta,13,TEAL if i==0 else MUTED,600)
 a+=line(1290,295,1290,381,LINE)
 a+=burnup(116,425,880,285,'월별 집행과 누적 추이',[42.4,46.8,51.2,54.6,56.8,61.0],[60,65,70,70,75,80],80,420)
 a+=heatmap(1020,425,546,285,[('해솔 연구동',[240,260,280,290,300,310]),('누리 문화관',[220,230,240,250,250,266]),('여울 복합센터',[180,190,200,210,220,232]),('모래빛 업무동',[130,140,150,160,170,178])])
 # Table with inline budget-use bars.
 a+=rect(116,734,1048,260,'white',22)+tt(140,771,'프로젝트별 비용·인원',19,INK,750)+t(1140,771,'전체 보기',14,PETROL,600,'end')
 cols=[(140,'프로젝트'),(392,'투입 인원'),(510,'투입 시간'),(690,'집행 비용'),(880,'예산 소진 · 주황 선 경보 80%')]
 a+=line(140,814.5,1140,814.5,LINE)
 for x,l in cols:a+=t(x,804,l,12,MUTED,600)
 for i,(n,v,b,p,hrs) in enumerate(projects):
  yy=848+i*38;a+=rect(140,yy-11,10,10,SERIES[i],3)+t(160,yy,n,15,INK,650)+t(392,yy,f'{p}명',15,INK)+t(510,yy,f'{hrs:,}시간',15,INK)+t(690,yy,f'{int(v*1e6):,}원',15,INK,600)
  r=v/b;a+=rect(880,yy-9,170,8,'#eef0ef',4)+rect(880,yy-9,170*r,8,SERIES[i] if i<2 else TEAL,4)+line(880+170*.8,yy-13,880+170*.8,yy+3,ORANGE,1.5)+t(1140,yy,f'{r*100:.1f}%',14,INK,600,'end')
  if i<3:a+=line(140,yy+15.5,1140,yy+15.5,'#f0f1f0')
 a+=rect(1188,734,378,260,PETROL_DARK,22)+tt(1212,773,'집계 기준',19,'white',700)+t(1212,812,'조건에 맞는 기록만 합산했어요.',15,'#b9d3d6')
 for i,(k,v) in enumerate([('기간','2027.01 - 2027.06'),('범위','전사, 모든 조직'),('갱신','2027.06.30 18:00')]):a+=t(1212,852+i*30,k,14,'#7fa6ab',500)+t(1262,852+i*30,v,14,'#e2eeef',600)
 a+=line(1212,930.5,1542,930.5,'#2a5560')+rect(1212,946,208,28,'#ffffff1a',8)+t(1226,965,'공개용 재가공 · 가상 데이터',13,'#e2eeef',600)
 return a
main=overview()
def detail_page():
 a=base('해솔 연구동','프로젝트별 예산과 인원, 상세 기록을 같은 기준으로 확인해요.','프로젝트')
 a+=rect(116,275,880,126,'white',22)+t(140,306,'프로젝트 집행',14,MUTED,600)+tt(140,356,'106,400,000원',36,INK,800)+t(450,356,'예산 140,000,000원 중 76.0% 사용',14,MUTED,500)
 a+=rect(140,370,832,14,'url(#hatch)',4)+rect(140,370,832*.76,14,PETROL,4)+line(140+832*.8,364,140+832*.8,390,ORANGE,2)+t(140+832*.8+6,362,'경보 80%',11,'#a8480f',700)
 a+=rect(1020,275,546,126,'white',22)
 for i,(label,value,unit,sub) in enumerate([('투입 인원','14','명','설계·검토·관리 3개 직무'),('누적 투입 시간','1,680','시간','선택한 기간의 합계')]):
  x=1044+i*262;a+=t(x,306,label,14,MUTED,600)+tt(x,352,value,32,INK,800)+t(x+sum(17.5 if c.isdigit() else 8 for c in value)+5,352,unit,16,INK,600)+t(x,380,sub,13,MUTED)
 a+=line(1290,295,1290,381,LINE)
 a+=burnup(116,425,880,285,'프로젝트 월별 집행',[12.8,15.2,16.4,18.0,20.0,24.0],[20,22,23,24,25,26],32,140)
 a+=rect(1020,425,546,285,'white',22)+tt(1044,463,'직무별 투입 시간',19,INK,750)+t(1542,462,'합계 1,680시간',13,MUTED,500,'end')
 x=1044
 for i,(label,num,ratio) in enumerate([('설계',840,.5),('검토',504,.3),('관리',336,.2)]):
  w=498*ratio;a+=rect(x,488,w-3,40,SERIES[i],8)+t(x+12,513,f'{int(ratio*100)}%',13,'white' if i<2 else PETROL_DARK,700);x+=w
 for i,(label,num,ppl) in enumerate([('설계',840,'7명'),('검토',504,'4명'),('관리',336,'3명')]):
  yy=574+i*42;a+=rect(1044,yy-11,10,10,SERIES[i],3)+t(1064,yy,label,15,INK,600)+t(1180,yy,ppl,14,MUTED)+t(1542,yy,f'{num}시간',15,INK,650,'end')
  if i<2:a+=line(1044,yy+17.5,1542,yy+17.5,'#f0f1f0')
 a+=rect(116,734,1450,260,'white',22)+tt(140,771,'인원별 상세',19,INK,750)+t(260,771,'14명 중 4명 표시',13,MUTED,500)+t(1542,771,'전체 보기',14,PETROL,600,'end')
 a+=line(140,814.5,1542,814.5,LINE)
 for x,l in [(140,'이름·소속'),(470,'투입 시간 (월 기준 160시간)'),(940,'집행 비용'),(1200,'확인 상태')]:a+=t(x,804,l,12,MUTED,600)
 for i,(name,team,h,cost,ok) in enumerate([('이도경','설계팀',168,'11,200,000원',True),('정하준','설계팀',160,'10,400,000원',True),('윤지안','검토팀',176,'12,100,000원',False),('최서윤','관리팀',152,'9,800,000원',True)]):
  yy=848+i*38;a+=dot(152,yy-5,12,TEAL_SOFT)+t(152,yy,name[0],11,PETROL,700,'middle')+t(174,yy,name,15,INK,650)+t(234,yy,team,13,MUTED)
  over=h>160;a+=rect(470,yy-9,300,8,'#eef0ef',4)+rect(470,yy-9,300*min(h,160)/180,8,TEAL,4)
  if over:a+=rect(470+300*160/180,yy-9,300*(h-160)/180,8,ORANGE,0)
  a+=line(470+300*160/180,yy-13,470+300*160/180,yy+3,'#9aa3a6',1.2)+t(790,yy,f'{h}시간',14,'#a8480f' if h>170 else INK,700 if h>170 else 500)
  a+=t(940,yy,cost,15,INK)+(badge(1200,yy-19,'확인 완료','gray',86) if ok else badge(1200,yy-19,'확인 필요','review',86))
  if i<3:a+=line(140,yy+15.5,1542,yy+15.5,'#f0f1f0')
 return a
detail=detail_page()
# Explanatory flow: the steps really are a sequence, so they keep their numbers.
structure=defs()+rect(0,0,1600,900,BG,0)+tt(72,92,'조회 조건에서 상세 내역까지',34,INK,800)+t(72,130,'같은 조회 범위와 집계 기준을 끝까지 유지하는 정보 구조',17,MUTED)
for x,n,title,sub in [(72,'1','조회 조건','어느 범위를 볼지 정해요'),(586,'2','주요 수치','선택한 범위의 합계를 봐요'),(1100,'3','상세 내역','프로젝트와 인원을 확인해요')]:
 structure+=rect(x,195,428,610,'white',24)+dot(x+42,237,18,PETROL)+t(x+42,243,n,16,'white',800,'middle')+tt(x+24,306,title,26,INK,800)+t(x+24,340,sub,15,MUTED)
structure+=line(500,237,586,237,'#c5cfcf',1.5,'3 5')+line(1014,237,1100,237,'#c5cfcf',1.5,'3 5')
structure+=rect(96,377,380,52,BG,12)
for i,(lab,on) in enumerate([('전사',True),('프로젝트',False),('개인',False)]):
 structure+=(rect(100+i*125,381,122,44,PETROL,10) if on else '')+t(161+i*125,409,lab,16,'white' if on else MUTED,700 if on else 500,'middle')
for y,label,value in [(486,'기간','2027.01 - 2027.06'),(552,'조직','모든 조직'),(618,'프로젝트','전체 선택')]:structure+=t(96,y,label,14,MUTED,500)+t(96,y+29,value,18,INK,650)
structure+=rect(610,377,380,138,'white',18,LINE)+t(634,412,'집행 비용',15,MUTED,600)+tt(634,458,'312,800,000원',30,INK,800)+rect(634,478,332,10,'url(#hatch)',3)
cx=634
for i,v in enumerate([106.4,88.2,68.6,49.6]):structure+=rect(cx,478,332*v/420-2,10,SERIES[i],2);cx+=332*v/420
structure+=t(610,575,'투입 인원',15,MUTED,500)+tt(990,575,'38명',24,INK,800,'end')+rule(610,598,380)+t(610,646,'누적 투입',15,MUTED,500)+tt(990,646,'5,296시간',24,INK,800,'end')
for i,(title,sub,r) in enumerate([('해솔 연구동','14명 · 106,400,000원',.76),('누리 문화관','10명 · 88,200,000원',.767),('여울 복합센터','8명 · 68,600,000원',.722),('모래빛 업무동','6명 · 49,600,000원',.709)]):
 y=377+i*89;structure+=rect(1124,y,380,72,BG,13)+rect(1124,y,4,72,SERIES[i],2)+t(1144,y+28,title,17,INK,650)+t(1144,y+54,sub,14,MUTED)+t(1488,y+28,f'{r*100:.0f}%',15,PETROL,700,'end')
structure+=t(72,855,'공개용 재가공 · 실제 운영 데이터가 아닌 가상 예시입니다.',14,MUTED,500)
# Focused UI specimen: range selection and cost total.
menu=defs()+rect(0,0,900,1120,BG,0)+tt(64,87,'조회 범위와 합계',32,INK,800)+t(64,124,'선택 상태와 집계 결과를 분명하게',17,MUTED)+rect(64,167,772,305,'white',24)
menu+=t(92,209,'조회 범위',17,INK,700)+rect(92,232,716,72,BG,16)
for i,(label,selected) in enumerate([('전사',True),('프로젝트',False),('개인',False)]):
 x=98+i*236;menu+=(rect(x,238,232,60,'white',12,'#d4dcdc') if selected else '')+t(x+116,276,label,19,PETROL if selected else MUTED,750 if selected else 500,'middle')
menu+=t(92,350,'2027.01.01 - 2027.06.30',19,INK,650)+t(92,391,'모든 조직, 모든 프로젝트',16,MUTED)+badge(92,419,'조회 적용','blue',100)
menu+=rect(64,500,772,232,PETROL_DARK,24)+t(92,546,'선택 범위의 집행 비용',17,'#b9d3d6',600)+tt(92,616,'312,800,000원',48,'white',800,None,-1.6)
cx=92
for i,v in enumerate([106.4,88.2,68.6,49.6]):menu+=rect(cx,646,716*v/420-3,12,['#7cc3c9','#5fb3bb','#3f9ea8','#bfe0e2'][i],3);cx+=716*v/420
menu+=rect(cx,646,808-cx,12,'#ffffff',3).replace('/>',' fill-opacity=".12"/>')+t(92,694,'4개 프로젝트, 38명, 5,296시간',17,'#b9d3d6',500)+t(808,694,'잔액 25.5%',15,'#7fa6ab',600,'end')
menu+=rect(64,760,772,254,'white',24)+tt(92,812,'집계에서 상세로',21,INK,750)
for i,(label,value) in enumerate([('해솔 연구동','106,400,000원'),('누리 문화관','88,200,000원'),('여울 복합센터','68,600,000원')]):
 yy=865+i*51;menu+=rect(92,yy-12,10,10,SERIES[i],3)+t(112,yy,label,18,INK,550)+t(805,yy,value,18,INK,700,'end')
 if i<2:menu+=line(92,yy+20.5,805,yy+20.5,'#f0f1f0')
menu+=t(64,1073,'공개용 재가공 · 가상 데이터',14,MUTED,500)
# Status specimen: orange marks the overage, together with the number and a baseline tick.
overtime=defs()+rect(0,0,1200,760,BG,0)+tt(64,87,'기준을 넘긴 투입 시간',32,INK,800)+t(64,124,'수치, 상태, 기준을 같은 줄에서 확인해요.',17,MUTED)+rect(64,170,1072,476,'white',24)
overtime+=tt(96,215,'인원별 투입 기록',22,INK,750)+badge(1002,192,'확인 필요 1명','review',112)+line(96,242.5,1104,242.5,LINE)
for x,label in [(96,'이름·소속'),(380,'투입 시간 (기준 8시간)'),(860,'차이')]:overtime+=t(x,280,label,14,MUTED,600)
for y,name,team,h,diff,alert in [(340,'윤지안','검토팀',9,'+1시간',True),(435,'이도경','설계팀',8,'0시간',False),(530,'정하준','설계팀',7,'-1시간',False)]:
 if alert:overtime+=rect(80,y-36,1040,68,ORANGE_WASH,14)
 overtime+=t(96,y,name,20,INK,700)+t(160,y,team,15,MUTED)
 sx,sw=380,400;per=sw/10;overtime+=rect(sx,y-10,sw,10,'#eef0ef',5)+rect(sx,y-10,per*min(h,8),10,TEAL,5)
 if h>8:overtime+=rect(sx+per*8,y-10,per*(h-8),10,ORANGE,0)
 overtime+=line(sx+per*8,y-17,sx+per*8,y+7,INK,1.5)+t(sx+sw+18,y,f'{h}시간',18,'#a8480f' if alert else INK,750 if alert else 500)
 overtime+=t(860,y,diff,20,'#a8480f' if alert else MUTED,750 if alert else 500)
overtime+=line(380+40*8,560,380+40*8,580,INK,1.5)+t(380+40*8+8,575,'기준 8시간',12,MUTED,600)
overtime+=t(96,615,'초과분은 색만이 아니라 막대 길이와 수치로 함께 보여 줘요.',15,MUTED)+t(64,706,'9시간 / 기준 8시간은 화면 상태 예시이며 실제 근태 기록이 아닙니다. 공개용 재가공 · 가상 데이터',14,MUTED)

# Embed a licensed SUIT subset so standalone SVGs do not fall back to system fonts.
font=TTFont(ROOT/'src/fonts/original/SUIT-Variable.woff2');opt=subset.Options();opt.layout_features=['*'];opt.name_IDs=['*'];sub=subset.Subsetter(options=opt);sub.populate(text=Path(__file__).read_text());sub.subset(font)
for name in font['name'].names:
 if name.nameID in [1,3,4,6,16,17]:
  vals={1:'Moa UI',3:'MoaUI-SUITSubset-20261124',4:'Moa UI Variable',6:'MoaUI-Variable',16:'Moa UI',17:'Regular'};name.string=vals[name.nameID].encode(name.getEncoding(),errors='replace')
font.flavor='woff2';buf=BytesIO();font.save(buf);data=base64.b64encode(buf.getvalue()).decode()
style=f"<style>@font-face{{font-family:'Moa SUIT';font-style:normal;font-weight:100 900;src:url(data:font/woff2;base64,{data}) format('woff2');}}text{{font-family:'Moa SUIT',sans-serif;}}</style>"
def save(name,body,label,w=1600,h=1000):
 (OUT/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><title>{label} · 공개용 재가공 · 모든 데이터는 가상</title>{style}{body}</svg>',encoding='utf-8')
save('erp-overview',main,'모아워크 비용·인원 전체 현황')
save('erp-detail',detail,'모아워크 프로젝트 비용·인원 상세')
save('erp-structure',structure,'조회 조건·주요 수치·상세의 정보 구조',1600,900)
save('erp-scope',menu,'조회 범위 선택과 비용 합계',900,1120)
save('erp-overtime',overtime,'기준 시간 초과 상태 예시',1200,760)
print('Generated five MOA WORK ERP illustrations with embedded SUIT')
