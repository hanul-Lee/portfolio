"""MOA WORK: original ERP portfolio illustrations, using only fictional data."""
from pathlib import Path
from html import escape
from io import BytesIO
import base64
from fontTools.ttLib import TTFont
from fontTools import subset
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'src/assets/cases/public-concepts';OUT.mkdir(parents=True,exist_ok=True)
INK='#202435';MUTED='#707789';BLUE='#5069df';BLUE_DEEP='#354fb8';LINE='#e9ebf3';BG='#f5f6fa'
def rect(x,y,w,h,fill='white',r=20,stroke=None):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'
def t(x,y,s,size=16,fill=INK,weight=400,anchor=None):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}"'+(f' text-anchor="{anchor}"' if anchor else '')+'>'+escape(str(s))+'</text>'
def rule(x,y,w,color=LINE):return f'<path d="M{x} {y}h{w}" stroke="{color}"/>'
def icon(x,y,name,color=MUTED,size=22):
 paths={'grid':'M3 3H10V10H3ZM14 3H21V10H14ZM3 14H10V21H3ZM14 14H21V21H14Z','people':'M15 7A4 4 0 1 1 7 7A4 4 0 1 1 15 7M3 21C3 12 19 12 19 21M18 4C23 4 23 11 19 11M20 15C23 16 23 18 23 21','chart':'M4 20V12M12 20V5M20 20V9','file':'M5 3H19V21H5ZM9 8H15M9 12H15M9 16H13','search':'M17 10A7 7 0 1 1 3 10A7 7 0 1 1 17 10M15 15L21 21','bell':'M5 17V10C5 1 19 1 19 10V17H5M9 21H15','chevron':'M8 10L12 14L16 10','settings':'M12 4V2M12 22V20M4 12H2M22 12H20M6 6L4 4M20 20L18 18M18 6L20 4M4 20L6 18M17 12A5 5 0 1 1 7 12A5 5 0 1 1 17 12','time':'M21 12A9 9 0 1 1 3 12A9 9 0 1 1 21 12M12 6V12L16 15','arrow':'M4 12H20M14 6L20 12L14 18','check':'M5 12L10 17L20 6'}
 return f'<path d="{paths[name]}" transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
def badge(x,y,label,kind='blue',w=92):
 fg,bg={'blue':('#4058b6','#edf1ff'),'gray':('#687187','#f0f2f7'),'review':('#354fb8','#edf1ff')}[kind]
 return rect(x,y,w,29,bg,9)+t(x+w/2,y+20,label,14,fg,600,'middle')
def pill(x,y,w,label,active=False):return rect(x,y,w,40,INK if active else 'white',20)+t(x+w/2,y+26,label,15,'white' if active else MUTED,600 if active else 400,'middle')
def base(title,sub,active='전체 현황'):
 a=rect(0,0,1600,1000,BG,0)+rect(16,16,70,968,'white',28)+rect(32,36,38,38,BLUE,13)+t(51,62,'m',25,'white',700,'middle')
 for i,kind in enumerate(['grid','chart','people','file']):
  y=142+i*69
  if (i==0 and active=='전체 현황') or (i==1 and active=='프로젝트'):a+=rect(28,y-13,46,46,'#edf1ff',16)
  a+=icon(40,y,kind,BLUE if i==(0 if active=='전체 현황' else 1) else '#9299aa',22)
 a+=icon(40,926,'settings','#9299aa')+t(116,57,'모아워크',23,INK,750)+t(116,81,'COST & PEOPLE',11,MUTED,600)
 a+=rect(475,31,522,48,'white',24)
 for x,label,w in [(482,'전체 현황',126),(608,'프로젝트',112),(720,'인원 내역',112),(832,'보고서',104)]:a+=pill(x,35,w,label,label==active)
 a+=rect(1161,32,47,46,'white',16)+icon(1174,45,'search')+rect(1220,32,47,46,'white',16)+icon(1233,45,'bell')+rect(1280,31,282,48,'white',24)+rect(1290,39,32,32,'#e8ecfa',16)+t(1306,61,'도',14,BLUE,650,'middle')+t(1334,61,'이도경 · 운영관리팀',15,INK,500)+icon(1521,44,'chevron',MUTED,20)
 a+=t(116,139,title,30,INK,750)+t(116,171,sub,16,MUTED)
 a+=rect(116,194,1450,57,'white',18)+t(138,229,'조회 범위',14,MUTED,600)
 for x,w,label in [(230,145,'전사' if active=='전체 현황' else '프로젝트'),(390,235,'2027.01.01 - 06.30'),(640,172,'모든 조직')]:a+=rect(x,204,w,37,'#f5f6fa',11)+t(x+16,228,label,15,INK,500)+icon(x+w-30,214,'chevron',MUTED,17)
 a+=rect(1430,204,114,37,BLUE,11)+t(1487,228,'조회하기',15,'white',650,'middle')
 return a
def kpi(x,label,value,sub,primary=False):
 a=rect(x,275,346,126,BLUE if primary else 'white',23)
 a+=t(x+22,308,label,15,'#e0e7ff' if primary else MUTED,500)+t(x+22,353,value,31,'white' if primary else INK,750)+t(x+22,380,sub,13,'#e0e7ff' if primary else MUTED)
 return a
def bars(x,y,w,h,title,values,budgets=None):
 a=rect(x,y,w,h)+t(x+24,y+37,title,20,INK,700)+t(x+w-24,y+36,'단위: 백만원',13,MUTED,400,'end')
 if budgets:a+=rect(x+24,y+57,10,10,BLUE,3)+t(x+42,y+67,'집행',13,MUTED)+rect(x+100,y+57,10,10,'#dfe3f0',3)+t(x+118,y+67,'계획',13,MUTED)
 top=y+92;bottom=y+h-39;height=bottom-top;maximum=80 if budgets else 30
 for tick in [0,maximum/2,maximum]:
  yy=bottom-height*tick/maximum;a+=rule(x+54,yy,w-80,'#eef0f6')+t(x+38,yy+5,int(tick),12,MUTED,400,'end')
 step=(w-104)/6
 for i,value in enumerate(values):
  xx=x+67+i*step
  if budgets:
   hh=height*budgets[i]/maximum;a+=rect(xx,bottom-hh,21,hh,'#dfe3f0',6)
  hh=height*value/maximum;a+=rect(xx+(27 if budgets else 0),bottom-hh,21,hh,BLUE if i!=5 else BLUE_DEEP,6)+t(xx+25,bottom+25,str(i+1)+'월',13,MUTED,400,'middle')
 return a
def table(x,y,w,heading,rows,columns,widths):
 a=rect(x,y,w,260)+t(x+24,y+37,heading,20,INK,700)+t(x+w-24,y+37,'전체 보기',14,BLUE,500,'end')+rect(x+16,y+57,w-32,35,'#f7f8fb',10)
 for dx,label in zip(widths,columns):a+=t(x+dx,y+80,label,13,MUTED,500)
 for i,row in enumerate(rows):
  yy=y+121+i*40
  for j,(dx,value) in enumerate(zip(widths,row)):a+=t(x+dx,yy,value,15,'#354fb8' if value=='확인 필요' else INK if j!=len(row)-1 else BLUE,600 if j==0 else 400)
  if i<3:a+=rule(x+24,yy+16,w-48)
 return a
def overview():
 a=base('비용과 인원을 한눈에','조회를 선택하면 집행 비용과 프로젝트별 투입 현황을 함께 볼 수 있어요.')
 # One primary indicator to judge first; the rest become compact supporting figures.
 a+=rect(116,275,714,126,BLUE,23)+t(138,308,'예산 대비 집행률',15,'#e0e7ff',600)+t(138,362,'74.5%',44,'white',750)+t(300,350,'312,800,000원 집행',17,'white',650)+t(300,375,'총 예산 420,000,000원 · 잔액 107,200,000원',13,'#e0e7ff')
 a+=rect(138,384,670,6,'#7d90ea',3)+rect(138,384,670*.745,6,'white',3)
 for x,label,value,sub in [(852,'예산 잔액','1.07억원','25.5% 남음'),(1095,'투입 인원','38명','4개 프로젝트'),(1338,'누적 투입 시간','5,296시간','선택 기간 합계')]:
  a+=rect(x,275,228,126,'white',23)+t(x+20,307,label,14,MUTED,500)+t(x+20,350,value,25,INK,700)+t(x+20,378,sub,13,MUTED)
 a+=bars(116,425,858,285,'월별 비용 집행',[42.4,46.8,51.2,54.6,56.8,61.0],[60,65,70,70,75,80])
 a+=rect(998,425,568,285)+t(1022,462,'프로젝트별 집행 비중',20,INK,700)
 colors=[BLUE,BLUE_DEEP,'#97a8e9','#c5cdef']
 for i,(name,v,ratio) in enumerate([('해솔 연구동','106.4백만원',34.0),('누리 문화관','88.2백만원',28.2),('여울 복합센터','68.6백만원',21.9),('모래빛 업무동','49.6백만원',15.9)]):
  yy=489+i*48;a+=rect(1022,yy+1,10,10,colors[i],3)+t(1044,yy+11,name,15,INK,500)+t(1538,yy+11,v,15,INK,600,'end')+rect(1044,yy+22,340,5,'#f0f2f7',2)+rect(1044,yy+22,340*ratio/34,5,colors[i],2)
 a+=table(116,734,1048,'프로젝트별 비용·인원',[['해솔 연구동','14명','1,680시간','106,400,000원'],['누리 문화관','10명','1,456시간','88,200,000원'],['여울 복합센터','8명','1,232시간','68,600,000원'],['모래빛 업무동','6명','928시간','49,600,000원']],['프로젝트','투입 인원','투입 시간','집행 비용'],[24,360,535,780])
 a+=rect(1188,734,378,260,'#222c49')+t(1212,773,'집계 기준',20,'white',650)+t(1212,815,'조건에 맞는 기록만 합산했어요.',16,'#c1cce4')+t(1212,858,'기간  2027.01 - 2027.06',15,'#c1cce4')+t(1212,893,'범위  전사 · 모든 조직',15,'#c1cce4')+rule(1212,916,330,'#3a4563')+t(1212,953,'공개용 가상 데이터',14,'#aebff0',500)
 return a
main=overview()
detail=base('해솔 연구동','프로젝트별 예산과 인원, 상세 기록을 같은 기준으로 확인해요.','프로젝트')
for x,args in zip([116,484,852,1220],[('프로젝트 집행','106,400,000원','예산 140,000,000원',True),('예산 잔액','33,600,000원','집행률 76.0%',False),('투입 인원','14명','3개 직무 참여',False),('누적 투입 시간','1,680시간','선택한 기간의 합계',False)]):detail+=kpi(x,*args)
detail+=bars(116,425,858,285,'프로젝트 월별 비용',[12.8,15.2,16.4,18.0,20.0,24.0])
detail+=rect(998,425,568,285,'#222c49')+t(1022,464,'직무별 투입 시간',20,'white',650)
for i,(label,num,ratio) in enumerate([('설계','840시간',.5),('검토','504시간',.3),('관리','336시간',.2)]):
 yy=504+i*59;detail+=t(1022,yy,label,16,'#dae3f5')+t(1538,yy,num,17,'white',600,'end')+rect(1022,yy+14,516,7,'#3a4563',3)+rect(1022,yy+14,516*ratio,7,['#8198ff','#9aaff0','#bdc6e7'][i],3)
detail+=table(116,734,1450,'인원별 상세 · 14명 중 4명 표시',[['이도경 · 설계팀','168시간','11,200,000원','확인 완료'],['정하준 · 설계팀','160시간','10,400,000원','확인 완료'],['윤지안 · 검토팀','176시간','12,100,000원','확인 필요'],['최서윤 · 관리팀','152시간','9,800,000원','확인 완료']],['이름·소속','투입 시간','집행 비용','확인 상태'],[24,480,800,1200])
# Explanatory flow, using the same components and actual synthetic totals.
structure=rect(0,0,1600,900,BG,0)+t(72,92,'조회 조건에서 상세 내역까지',34,INK,750)+t(72,130,'같은 조회 범위와 집계 기준을 유지하는 정보 구조',18,MUTED)
for x,n,title,sub in [(72,'01','조회 조건','어느 범위를 볼지 정해요'),(586,'02','주요 수치','선택한 범위의 합계를 봐요'),(1100,'03','상세 내역','프로젝트와 인원을 확인해요')]:
 structure+=rect(x,195,428,610)+badge(x+24,219,n,w=48)+t(x+24,292,title,27,INK,700)+t(x+24,330,sub,16,MUTED)
structure+=rect(96,377,380,52,'#edf1ff',14)+t(116,410,'전사 / 프로젝트 / 개인',18,BLUE,650)
for y,label,value in [(486,'기간','2027.01 - 2027.06'),(552,'조직','모든 조직'),(618,'프로젝트','전체 선택')]:structure+=t(96,y,label,15,MUTED)+t(96,y+29,value,18,INK,600)
structure+=rect(610,377,380,138,BLUE,18)+t(634,414,'집행 비용',16,'#e1e8ff')+t(634,463,'312,800,000원',30,'white',750)+t(634,492,'선택한 기간의 합계',14,'#e1e8ff')+t(610,575,'투입 인원',16,MUTED)+t(965,575,'38명',25,INK,700,'end')+rule(610,598,380)+t(610,646,'누적 투입',16,MUTED)+t(965,646,'5,296시간',25,INK,700,'end')
for i,(title,sub) in enumerate([('해솔 연구동','14명 · 106,400,000원'),('누리 문화관','10명 · 88,200,000원'),('여울 복합센터','8명 · 68,600,000원'),('모래빛 업무동','6명 · 49,600,000원')]):
 y=377+i*89;structure+=rect(1124,y,380,72,'#f6f7fb',13)+t(1140,y+28,title,18,INK,600)+t(1140,y+55,sub,15,MUTED)
structure+=icon(527,477,'arrow',BLUE,30)+icon(1041,477,'arrow',BLUE,30)+t(72,855,'공개용 재설계 · 실제 운영 데이터가 아닌 가상 예시입니다.',15,MUTED)
# Focused UI specimen: range selection and cost total.
menu=rect(0,0,900,1120,BG,0)+t(64,87,'조회 범위와 합계',32,INK,750)+t(64,124,'선택 상태와 집계 결과를 분명하게',17,MUTED)+rect(64,167,772,305)
menu+=t(92,209,'조회 범위',18,INK,650)
for x,label,selected in [(92,'전사',True),(330,'프로젝트',False),(568,'개인',False)]:menu+=rect(x,238,210,62,BLUE if selected else '#f2f4f9',15)+t(x+105,277,label,20,'white' if selected else MUTED,650 if selected else 400,'middle')
menu+=t(92,350,'2027.01.01 - 2027.06.30',19,INK,600)+t(92,391,'모든 조직 · 모든 프로젝트',17,MUTED)+badge(92,419,'조회 적용','blue',108)
menu+=rect(64,500,772,232,'#222c49')+t(92,548,'선택 범위의 집행 비용',19,'#c1cce4')+t(92,619,'312,800,000원',47,'white',750)+t(92,688,'4개 프로젝트 · 38명 · 5,296시간',19,'#c1cce4')+rect(64,760,772,254)+t(92,812,'집계에서 상세로',22,INK,650)
for i,(label,value) in enumerate([('해솔 연구동','106,400,000원'),('누리 문화관','88,200,000원'),('여울 복합센터','68,600,000원')]):menu+=t(92,865+i*51,label,19,INK,500)+t(805,865+i*51,value,19,BLUE,650,'end')
menu+=t(64,1073,'가상 데이터 · 공개용 재설계',15,MUTED)
# Status specimen: one blue accent; text and weight also distinguish review states.
overtime=rect(0,0,1200,760,BG,0)+t(64,87,'기준을 넘긴 투입 시간',32,INK,750)+t(64,124,'수치·상태·기준을 같은 영역에서 확인해요.',18,MUTED)+rect(64,170,1072,476)
overtime+=t(96,215,'인원별 투입 기록',23,INK,650)+badge(988,190,'확인 필요','review',116)+rule(96,242,1008)
for x,label in [(96,'이름·소속'),(388,'투입 시간'),(655,'기준'),(892,'차이')]:overtime+=t(x,280,label,16,MUTED,500)
for y,name,hours,basev,diff,alert in [(340,'윤지안 · 검토팀','9시간','8시간','+1시간',True),(435,'이도경 · 설계팀','8시간','8시간','- ',False),(530,'정하준 · 설계팀','7시간','8시간','-1시간',False)]:
 if alert:overtime+=rect(80,y-33,1040,66,'#edf1ff',14)
 for x,value in [(96,name),(388,hours),(655,basev),(892,diff)]:overtime+=t(x,y,value,21,'#354fb8' if alert and x!=96 else INK,700 if alert and x==388 else 500)
overtime+=t(96,611,'초과 상태는 색과 수치를 함께 표시합니다.',16,MUTED)+t(64,706,'9시간 / 기준 8시간은 화면 상태 예시이며 실제 근태 기록이 아닙니다.',16,MUTED)
# Embed a licensed SUIT subset so standalone SVGs do not fall back to system fonts.
font=TTFont(ROOT/'src/fonts/original/SUIT-Variable.woff2');opt=subset.Options();opt.layout_features=['*'];opt.name_IDs=['*'];sub=subset.Subsetter(options=opt);sub.populate(text=Path(__file__).read_text());sub.subset(font)
for name in font['name'].names:
 if name.nameID in [1,3,4,6,16,17]:
  vals={1:'Moa UI',3:'MoaUI-SUITSubset-20261124',4:'Moa UI Variable',6:'MoaUI-Variable',16:'Moa UI',17:'Regular'};name.string=vals[name.nameID].encode(name.getEncoding(),errors='replace')
font.flavor='woff2';buf=BytesIO();font.save(buf);data=base64.b64encode(buf.getvalue()).decode()
style=f"<style>@font-face{{font-family:'Moa SUIT';font-style:normal;font-weight:100 900;src:url(data:font/woff2;base64,{data}) format('woff2');}}text{{font-family:'Moa SUIT',sans-serif;}}</style>"
def save(name,body,label,w=1600,h=1000):
 (OUT/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><title>{label} · 공개용 재설계 · 모든 데이터는 가상</title>{style}{body}</svg>',encoding='utf-8')
save('erp-overview',main,'모아워크 비용·인원 전체 현황')
save('erp-detail',detail,'모아워크 프로젝트 비용·인원 상세')
save('erp-structure',structure,'조회 조건·주요 수치·상세의 정보 구조',1600,900)
save('erp-scope',menu,'조회 범위 선택과 비용 합계',900,1120)
save('erp-overtime',overtime,'기준 시간 초과 상태 예시',1200,760)
print('Generated five MOA WORK ERP illustrations with embedded SUIT')
