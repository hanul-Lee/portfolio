"""SPANLAB: fictional structural member geometry, sensors and telemetry for public portfolio use."""
from pathlib import Path
from html import escape
from io import BytesIO
import base64
from fontTools.ttLib import TTFont
from fontTools import subset
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'src/assets/cases/public-concepts';OUT.mkdir(parents=True,exist_ok=True)
WHITE='#edf3ff';MUTED='#a1afc6';BLUE='#85aeff';BLUE_LIGHT='#b1ceff';BG='#0c121e';PANEL='#141e2e';LINE='#2b3a50'
def rect(x,y,w,h,fill=PANEL,r=18,stroke=None):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'
def t(x,y,s,size=16,fill=WHITE,weight=400,anchor=None):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}"'+(f' text-anchor="{anchor}"' if anchor else '')+'>'+escape(str(s))+'</text>'
def rule(x,y,w,color=LINE):return f'<path d="M{x} {y}h{w}" stroke="{color}"/>'
def path(d,color=BLUE,w=1.5,fill='none'):return f'<path d="{d}" stroke="{color}" stroke-width="{w}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"/>'
def icon(x,y,name,color=MUTED,size=22):
 paths={'grid':'M3 3H10V10H3ZM14 3H21V10H14ZM3 14H10V21H3ZM14 14H21V21H14Z','beam':'M3 4H21V8H15V16H21V20H3V16H9V8H3Z','sensor':'M5 5H19V19H5ZM9 2V5M15 2V5M9 19V22M15 19V22M2 9H5M2 15H5M19 9H22M19 15H22M9 9H15V15H9Z','chart':'M4 20V12M12 20V5M20 20V9','history':'M4 8C7 0 21 3 21 12C21 22 6 25 3 15M3 3V9H9M12 7V12L16 15','search':'M17 10A7 7 0 1 1 3 10A7 7 0 1 1 17 10M15 15L21 21','chevron':'M8 10L12 14L16 10','back':'M15 4L7 12L15 20','check':'M5 12L10 17L20 6','bell':'M5 17V10C5 1 19 1 19 10V17H5M9 21H15'}
 return f'<g transform="translate({x} {y}) scale({size/24})">{path(paths[name],color,1.7)}</g>'
def spark(x,y,w,h,vals,color,gap_from=None):
 n=len(vals);lo,hi=min(vals),max(vals);pts=[(x+w*i/(n-1),y+h-(v-lo)/(hi-lo or 1)*h) for i,v in enumerate(vals)]
 if gap_from is None:return '<path d="M'+' L'.join(f'{a:.1f} {b:.1f}' for a,b in pts)+f'" stroke="{color}" stroke-width="1.6" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
 live=pts[:gap_from+1];dead=pts[gap_from:]
 return '<path d="M'+' L'.join(f'{a:.1f} {b:.1f}' for a,b in live)+f'" stroke="{color}" stroke-width="1.6" fill="none" stroke-linejoin="round"/>'+f'<path d="M{dead[0][0]:.1f} {dead[0][1]:.1f}H{x+w}" stroke="{color}" stroke-width="1.4" stroke-dasharray="2 4" fill="none"/>'+f'<circle cx="{dead[0][0]:.1f}" cy="{dead[0][1]:.1f}" r="3" fill="{color}"/>'
def smooth(pts):
 d=f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
 for i in range(len(pts)-1):
  p0=pts[i-1] if i else pts[i];p1=pts[i];p2=pts[i+1];p3=pts[i+2] if i+2<len(pts) else p2
  c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6);c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
  d+=f'C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
 return d
def sensor_strip(x,y,w,states):
 # Schematic of the member with sensor positions at 1/10, 4/10, 7/10 and 9/10 of its length.
 a=rect(x,y-3,w,6,'#2b3d56',3)+rect(x-4,y+4,8,8,'#2b3d56',1)+rect(x+w-4,y+4,8,8,'#2b3d56',1)
 for f,st in zip([.1,.4,.7,.9],states):
  c={'ok':BLUE_LIGHT,'sel':'#ffffff','lost':'#f2b35b'}[st];a+=f'<circle cx="{x+w*f:.1f}" cy="{y}" r="{5 if st!="ok" else 4}" fill="#0c121e" stroke="{c}" stroke-width="2"/>'
 return a
def badge(x,y,label,w=84):return rect(x,y,w,27,'#223852',9)+t(x+w/2,y+19,label,13,'#b8d5ff',600,'middle')
def defs():return '''<defs><clipPath id="scene-cut"><rect x="252" y="204" width="930" height="482" rx="22"/></clipPath><radialGradient id="scene" cx=".55" cy=".44" r=".8"><stop stop-color="#243b5c"/><stop offset="1" stop-color="#101a29"/></radialGradient><linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#aec6e6"/><stop offset=".5" stop-color="#7699c8"/><stop offset="1" stop-color="#44658f"/></linearGradient><linearGradient id="web" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#5d80b0"/><stop offset="1" stop-color="#304a6e"/></linearGradient><linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#668ff6" stop-opacity=".35"/><stop offset="1" stop-color="#668ff6" stop-opacity="0"/></linearGradient></defs>'''
def point(x,y,z):return (720+(x-5)*51+y*34,537-(x-5)*14+y*18-z*76)
def polygon(points,fill,stroke='#9dbbe2'):
 return '<polygon points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in points)+f'" fill="{fill}" stroke="{stroke}" stroke-width="1" stroke-linejoin="round"/>'
def box(x0,x1,y0,y1,z0,z1,top='url(#metal)',side='url(#web)',end='#587ca9'):
 p=point
 return polygon([p(x0,y1,z0),p(x1,y1,z0),p(x1,y1,z1),p(x0,y1,z1)],side)+polygon([p(x0,y0,z0),p(x0,y1,z0),p(x0,y1,z1),p(x0,y0,z1)],end)+polygon([p(x0,y0,z1),p(x1,y0,z1),p(x1,y1,z1),p(x0,y1,z1)],top)
def scene():
 a='<g clip-path="url(#scene-cut)">'+rect(252,204,930,482,'url(#scene)',22,LINE)+t(278,241,'Q-24 부재 · 센서 위치',20,WHITE,650)+badge(1038,219,'3D 위치도',116)
 # A newly constructed I-section, not a scan, CAD model or real site image.
 for x in range(-1,13):
  p,q=point(x,-3,-.55),point(x,3,-.55);a+=path(f'M{p[0]} {p[1]}L{q[0]} {q[1]}','#30445e',.7)
 for y in range(-3,4):
  p,q=point(-1,y,-.55),point(12,y,-.55);a+=path(f'M{p[0]} {p[1]}L{q[0]} {q[1]}','#30445e',.7)
 a+=box(.6,1.3,-.9,.9,-.45,0,'#26394f','#1c2d40','#26394f')+box(8.7,9.4,-.9,.9,-.45,0,'#26394f','#1c2d40','#26394f')
 a+=box(0,10,-.72,.72,0,.24)+box(0,10,-.18,.18,.24,1.56)+box(0,10,-.72,.72,1.56,1.8)
 for i,x in enumerate([1,4,7,9]):
  xx,yy=point(x,.78,1.84);active=i==1
  a+=f'<circle cx="{xx}" cy="{yy}" r="{11 if active else 8}" fill="#203d60" stroke="{BLUE_LIGHT}" stroke-width="1.5"/><circle cx="{xx}" cy="{yy}" r="3.5" fill="{BLUE_LIGHT}"/>'
  if not active:a+=t(xx,yy+31,'C-0'+str(i+1),13,'#d3e7ff',600,'middle')
  else:
   a+=path(f'M{xx} {yy-12}V309H{xx+44}',BLUE_LIGHT,1)+rect(xx+44,278,166,64,'#1a2e48',14,'#5377a2')+t(xx+59,303,'C-02 · 선택됨',13,'#b6cce8')+t(xx+59,328,'+2.7 mm',21,'white',700)
 ca,cb=point(5,-1.5,.9),point(5,1.5,.9)
 a+=f'<path d="M{ca[0]:.1f} {ca[1]:.1f}L{cb[0]:.1f} {cb[1]:.1f}" stroke="#f2b35b" stroke-width="1.3" stroke-dasharray="6 4 1 4"/>'
 for q in [ca,cb]:a+=f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="10" fill="#2a2312" stroke="#f2b35b" stroke-width="1.2"/>'+t(q[0],q[1]+4.5,'A',12,'#f2c784',700,'middle')
 ox,oy=300,606;a+=path(f'M{ox} {oy}L{ox+40} {oy-11}',MUTED,1.3)+path(f'M{ox} {oy}L{ox+22} {oy+12}',MUTED,1.3)+path(f'M{ox} {oy}L{ox} {oy-38}',MUTED,1.3)
 a+=t(ox+46,oy-10,'x',11,MUTED)+t(ox+26,oy+24,'y',11,MUTED)+t(ox-4,oy-44,'z',11,MUTED)
 sx,sy=1016,470;a+=rect(sx,sy,150,156,'#0f1928',14,'#2b3a50')+t(sx+16,sy+26,'단면 A-A',13,'#d3e7ff',650)
 a+=f'<path d="M{sx+45} {sy+46}H{sx+105}V{sy+56}H{sx+80}V{sy+112}H{sx+105}V{sy+122}H{sx+45}V{sy+112}H{sx+70}V{sy+56}H{sx+45}Z" fill="url(#metal)" stroke="#9dbbe2" stroke-width="1"/>'
 a+=path(f'M{sx+124} {sy+46}V{sy+122}M{sx+120} {sy+46}H{sx+128}M{sx+120} {sy+122}H{sx+128}','#7d8ea8',1)+path(f'M{sx+45} {sy+134}H{sx+105}M{sx+45} {sy+130}V{sy+138}M{sx+105} {sy+130}V{sy+138}','#7d8ea8',1)
 a+=t(sx+132,sy+88,'h',11,MUTED)+t(sx+75,sy+150,'b',11,MUTED,400,'middle')+f'<circle cx="{sx+75}" cy="{sy+42}" r="3.5" fill="{BLUE_LIGHT}"/>'
 a+=badge(278,273,'연결 4 / 4',108)+rect(270,638,896,32,'#111e30',8)+t(278,657,'임의 제작한 부재 형상 · 실제 측정 및 안전 판정 자료가 아닙니다.',13,'#b0c4dd')
 return a+'</g>'
SPARKS=[[1.0,1.1,1.05,1.15,1.1,1.2,1.18,1.2],[2.1,2.3,2.25,2.5,2.45,2.6,2.65,2.7],[1.5,1.6,1.7,1.65,1.8,1.85,1.9,1.9],[1.2,1.25,1.2,1.3,1.35,1.3,1.4,1.4]]
# Desktop: spatial context first, live channels beside it, history below.
a=defs()+rect(0,0,1600,1000,BG,0)+rect(16,16,212,968,'#111a28',24,LINE)+icon(39,45,'beam',BLUE,27)+t(78,66,'spanlab',25,WHITE,700)+t(40,110,'구조 측정 워크스페이스',12,MUTED,500)+rule(40,136,164)
for i,(label,kind) in enumerate([('현장 현황','grid'),('부재 분석','beam'),('측정 이력','history'),('센서 관리','sensor')]):
 y=170+i*61
 if i==1:a+=rect(30,y-10,184,46,'#243955',14)+rect(208,y+1,3,23,BLUE,1)
 a+=icon(46,y,kind,WHITE if i==1 else MUTED,20)+t(80,y+17,label,16,WHITE if i==1 else MUTED,600 if i==1 else 400)
a+=t(40,899,'모래빛 제작장',15,WHITE,600)+t(40,926,'공개용 가상 워크스페이스',12,MUTED)
a+=t(252,58,'현장 / 부재 분석',16,MUTED)+rect(1072,27,305,43,PANEL,13,LINE)+icon(1087,38,'search',MUTED,19)+t(1118,54,'부재·세션 검색',14,MUTED)+rect(1394,27,174,43,PANEL,13,LINE)+t(1410,54,'이도경 · 품질관리',14,WHITE,500)
a+=t(252,124,'부재 측정 모니터',32,WHITE,700)+t(252,158,'모래빛 제작장 · B구역  /  2027.09.16  /  가상 측정 세션',16,MUTED)+rect(1330,103,238,30,'#2a2312',9,'#6b5426')+t(1449,123,'공개용 재가공 · 가상 데이터',13,'#f2c784',650,'middle')
a+=scene()+rect(1206,204,362,482,PANEL,22,LINE)+t(1230,243,'측정 세션',20,WHITE,650)+badge(1454,220,'수집 중',90)+t(1230,288,'Q-24',36,WHITE,700)+t(1230,319,'2차 측정 · SIM-318',15,MUTED)+rule(1230,341,314)
for x,num,label in [(1230,'04','연결 채널'),(1394,'76%','수집 진행')]:a+=t(x,380,num,29,WHITE,700)+t(x,408,label,13,MUTED)
a+=t(1230,451,'채널',13,MUTED)+t(1544,451,'변위 예시',13,MUTED,400,'end')
for i,(ch,v) in enumerate([('C-01','+1.2 mm'),('C-02','+2.7 mm'),('C-03','+1.9 mm'),('C-04','+1.4 mm')]):
 y=482+i*44
 if i==1:a+=rect(1220,y-24,334,36,'#20334d',10)
 a+=t(1230,y,ch,16,BLUE if i==1 else WHITE,600 if i==1 else 400)+spark(1296,y-16,120,16,SPARKS[i],BLUE_LIGHT if i==1 else '#6f86a8')+t(1544,y,v,17,BLUE_LIGHT if i==1 else WHITE,650,'end')
a+=rect(1230,646,314,5,'#2b3b51',2)+rect(1230,646,239,5,BLUE,2)
# Corresponding fictional profile curve and session history.
a+=rect(252,710,846,270,PANEL,22,LINE)+t(278,750,'변위 프로파일',20,WHITE,650)+t(1072,749,'단위 mm · 가상 곡선',13,MUTED,400,'end')
for y,val in [(792,'4'),(844,'2'),(896,'0')]:a+=rule(310,y,750,'#26364b')+t(294,y+5,val,12,MUTED,400,'end')
PTS=[(310,.4),(385,1.2),(497,2.1),(610,2.7),(722,2.35),(835,1.9),(985,1.4),(1060,.6)];PXY=[(x,896-v*26) for x,v in PTS]
a+=path('M310 792H1060','#f2b35b',1.3).replace('/>',' stroke-dasharray="6 5"/>')+t(1060,784,'가상 기준 4.0',12,'#f2c784',600,'end')
a+=path(smooth(PXY)+'L1060 896H310Z','none',0,'url(#area)')+path(smooth(PXY),BLUE,3)
for (x,v),lab in zip([PTS[1],PTS[3],PTS[5],PTS[6]],['C-01','C-02','C-03','C-04']):
 yy=896-v*26;sel=lab=='C-02';a+=path(f'M{x} {yy+6}V896','#3a4d68',1).replace('/>',' stroke-dasharray="2 3"/>')+f'<circle cx="{x}" cy="{yy}" r="{6 if sel else 4.5}" fill="#0c121e" stroke="{BLUE_LIGHT if sel else BLUE}" stroke-width="2"/>'+t(x,yy-12,lab,11,'#d3e7ff' if sel else MUTED,600 if sel else 400,'middle')
a+=t(310,937,'P-01',12,MUTED)+t(680,937,'부재 길이 방향',13,MUTED,400,'middle')+t(1060,937,'P-08',12,MUTED,400,'end')
a+=rect(1122,710,446,270,PANEL,22,LINE)+t(1146,750,'측정 이력',20,WHITE,650)+t(1544,749,'전체 보기',13,BLUE,500,'end')
for i,(session,stamp,state) in enumerate([('SIM-318','09.16 10:24','수집 중'),('SIM-317','09.16 09:40','수집 완료'),('SIM-316','09.15 16:20','수집 완료')]):
 y=800+i*59;live=i==0;a+=t(1146,y,session,16,WHITE,600)+t(1146,y+23,stamp,13,MUTED)+f'<circle cx="{1544-len(state)*13-12}" cy="{y-5}" r="4" fill="{BLUE_LIGHT if live else "#4d6180"}"/>'+(f'<circle cx="{1544-len(state)*13-12}" cy="{y-5}" r="8" fill="none" stroke="{BLUE_LIGHT}" stroke-opacity=".35"/>' if live else '')+t(1544,y,state,14,BLUE_LIGHT if live else MUTED,650 if live else 500,'end')+rect(1146,y+33,398 if not live else 302,0,'none',0)
 if i<2:a+=rule(1146,y+36,398)
# Mobile views use the same session, geometry and channel values.
def mobile_base(title,sub):
 s=defs()+rect(0,0,390,844,BG,0)+t(24,30,'9:41',14,WHITE,600)+t(323,30,'LTE',12,MUTED)+rect(350,19,19,10,WHITE,3)
 s+=rect(24,56,38,38,PANEL,12,LINE)+icon(34,65,'back',WHITE,19)+t(195,81,title,18,WHITE,600,'middle')+t(24,143,sub,26,WHITE,700)
 return s
def cta(label):return rect(24,746,342,56,'#4b7edb',14)+t(195,782,label,17,'white',650,'middle')+rect(135,833,120,4,'#e5ecf8',2)
start=mobile_base('측정 준비','연결 상태를 확인해요')+t(24,175,'모래빛 제작장 · B구역',14,MUTED)
start+=rect(24,202,342,102,PANEL,20,LINE)+icon(43,225,'beam',BLUE,31)+t(94,236,'Q-24 부재',22,WHITE,650)+t(94,267,'2차 측정 · 4개 채널',14,MUTED)+sensor_strip(254,252,92,['ok','ok','ok','ok'])
start+=t(24,348,'준비 항목',19,WHITE,650)
for i,(title,sub) in enumerate([('측정 대상 선택','Q-24 · 모래빛 제작장'),('센서 연결','4개 채널 연결 완료'),('기준점 설정','기준점 2개 확인 완료')]):
 y=374+i*93;start+=rect(24,y,342,77,PANEL,17,LINE)+rect(40,y+21,32,32,'#243955',10)+icon(47,y+28,'check',BLUE,18)+t(87,y+31,title,17,WHITE,600)+t(87,y+56,sub,14,MUTED)
start+=t(24,693,'실제 센서와 연결되지 않는 가상 화면입니다.',13,MUTED)+cta('측정 시작하기')
# Measuring: status, last reception, connected channels and the required action come before the values.
AMBER='#f2b35b'
def status_card(y,badge_label,badge_fg,badge_bg,items,stroke=LINE):
 a=rect(24,y,342,186,PANEL,20,stroke)+rect(44,y+20,len(badge_label)*14+28,28,badge_bg,9)+t(58,y+39,badge_label,14,badge_fg,700)+sensor_strip(232,y+34,112,STRIP)
 for i,(label,value,color) in enumerate(items):
  x=44+(i%2)*166;yy=y+84+(i//2)*62
  a+=t(x,yy,label,13,MUTED)+t(x,yy+27,value,18,color,700)
 return a
STRIP=['ok','ok','ok','ok']
mobile=mobile_base('실시간 측정','측정값을 수집하고 있어요')+t(24,175,'Q-24 · SIM-318 · 10:24 시작',14,MUTED)
mobile+=status_card(200,'정상 수집 중','#b8d5ff','#223852',[('마지막 수신','2초 전',WHITE),('연결 채널','4 / 4',WHITE),('진행','76% · 20초 남음',WHITE),('필요한 조치','없음 · 대기',BLUE_LIGHT)])
mobile+=t(24,428,'채널별 변위',17,WHITE,650)+t(366,428,'단위 mm',13,MUTED,400,'end')
for i,(ch,value) in enumerate([('C-01','+1.2'),('C-02','+2.7'),('C-03','+1.9'),('C-04','+1.4')]):
 y=446+i*56;mobile+=rect(24,y,342,46,PANEL,12,LINE)+rect(40,y+19,8,8,'#7fd1a0',4)+t(58,y+29,ch,15,WHITE,600)+spark(150,y+14,120,18,SPARKS[i],'#6f86a8')+t(348,y+30,value,18,WHITE,650,'end')
mobile+=t(24,708,'표시된 값은 가상이며 안전 판정과 무관합니다.',13,MUTED)+cta('측정 상세 보기')
# Proposal: one channel drops. Collected values are kept; resume or re-measure only the lost channel.
STRIP=['ok','ok','lost','ok']
drop=mobile_base('실시간 측정','C-03 신호가 끊겼어요')+t(24,175,'Q-24 · SIM-318 · 10:24 시작',14,MUTED)
drop+=status_card(200,'일부 채널 누락','#2a1c06',AMBER,[('C-03 마지막 수신','29초 전',AMBER),('연결 채널','3 / 4',AMBER),('보존된 값','3개 채널 저장',WHITE),('필요한 조치','C-03 연결 확인',AMBER)],'#7a5a2b')
drop+=t(24,428,'채널별 변위',17,WHITE,650)+t(366,428,'단위 mm',13,MUTED,400,'end')
for i,(ch,value,ok) in enumerate([('C-01','+1.2',True),('C-02','+2.7',True),('C-03','끊김',False),('C-04','+1.4',True)]):
 y=446+i*56;drop+=rect(24,y,342,46,PANEL if ok else '#2b2312',12,LINE if ok else '#7a5a2b')+rect(40,y+19,8,8,'#7fd1a0' if ok else AMBER,4)+t(58,y+29,ch,15,WHITE if ok else AMBER,600)+(spark(150,y+14,120,18,SPARKS[i],'#6f86a8') if ok else spark(150,y+14,120,18,SPARKS[i],AMBER,4))+t(348,y+30,value,18 if ok else 15,WHITE if ok else AMBER,650,'end')
drop+=rect(24,676,342,56,'#4b7edb',14)+t(195,711,'재연결 후 이어서 측정',17,'white',650,'middle')+rect(24,744,342,56,PANEL,14,'#5176a5')+t(195,779,'C-03만 다시 측정',17,'#cfe0ff',650,'middle')+rect(135,833,120,4,'#e5ecf8',2)
font=TTFont(ROOT/'src/fonts/original/SUIT-Variable.woff2');opt=subset.Options();opt.layout_features=['*'];opt.name_IDs=['*'];ss=subset.Subsetter(options=opt);ss.populate(text=Path(__file__).read_text());ss.subset(font)
for n in font['name'].names:
 if n.nameID in [1,3,4,6,16,17]:
  names={1:'Span UI',3:'SpanUI-SUITSubset-20261124',4:'Span UI Variable',6:'SpanUI-Variable',16:'Span UI',17:'Regular'};n.string=names[n.nameID].encode(n.getEncoding(),errors='replace')
font.flavor='woff2';b=BytesIO();font.save(b);data=base64.b64encode(b.getvalue()).decode();style=f"<style>@font-face{{font-family:'Span SUIT';font-style:normal;font-weight:100 900;src:url(data:font/woff2;base64,{data}) format('woff2');}}text{{font-family:'Span SUIT',sans-serif;}}</style>"
def save(name,body,label,w,h):
 (OUT/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><title>{label} · 공개용 재가공 · 모든 화면 데이터는 가상입니다</title>{style}{body}</svg>',encoding='utf-8')
save('measure-desktop',a,'SPANLAB 부재·센서 위치와 측정 현황',1600,1000)
save('measure-start',start,'SPANLAB 모바일 측정 준비',390,844)
save('measure-mobile',mobile,'SPANLAB 모바일 측정 상태',390,844)
save('measure-dropout',drop,'SPANLAB 채널 누락 상태 개선안',390,844)
print('Generated three fictional SPANLAB structural monitoring screens')
