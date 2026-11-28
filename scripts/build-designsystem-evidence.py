"""Design-system evidence cards: explanatory reconstructions of the token JSON, the Markdown
guide, the 12 expanded menus and the fixes made to AI output. Content is illustrative and fictional."""
from pathlib import Path
from html import escape
from io import BytesIO
import base64
from fontTools.ttLib import TTFont
from fontTools import subset
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'src/assets/cases/public-concepts';OUT.mkdir(parents=True,exist_ok=True)
INK='#1f2430';MUTED='#6b7280';FAINT='#a3a9b3';LINE='#e6e8ec';BG='#f6f5f3';CARD='#ffffff'
BROWN='#b65b3a';BROWN_SOFT='#f6e7df';NAVY='#1b2f54';BEIGE='#f8e4c6';RED='#d1435b';RED_SOFT='#fdecef';GREEN='#2f7d5b';GREEN_SOFT='#e3f2ea'
CODE_BG='#1d2230';CODE_LINE='#2a3142';C_KEY='#9cc4ff';C_STR='#f2c38b';C_REF='#b9e3a8';C_PUN='#8a93a6'
W,H=800,600
def rect(x,y,w,h,fill,r=12,stroke=None,sw=1,dash=None):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def t(x,y,s,size=14,fill=INK,weight=400,anchor=None,mono=False):
 fam=' font-family="SFMono-Regular, Menlo, Consolas, monospace"' if mono else ''
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}"'+(f' text-anchor="{anchor}"' if anchor else '')+fam+'>'+escape(str(s))+'</text>'
def line(x1,y1,x2,y2,c=LINE,w=1,dash=None):
 return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def circle(cx,cy,r,fill,stroke=None):return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'
def frame(title,sub):
 return rect(0,0,W,H,BG,0)+t(40,56,title,22,INK,750)+t(40,84,sub,14,MUTED)+t(760,56,'설명용 재구성',12,FAINT,600,'end')
def badge(x,y,label,fg,bg,w=None):
 w=w or len(label)*12+18
 return rect(x,y,w,24,bg,7)+t(x+w/2,y+16.5,label,12,fg,700,'middle')

# 1. Token JSON + generated Figma variables
def tokens():
 a=frame('Tokens Studio JSON과 Figma 변수','원래 값(primitive)을 쓰임새(semantic)가 참조합니다.')
 a+=rect(40,112,448,448,CODE_BG,14)+circle(62,134,5,'#ff6b6b')+circle(80,134,5,'#ffd166')+circle(98,134,5,'#06d6a0')+t(124,139,'tokens.json',12,C_PUN,500,None,True)+line(40,154,488,154,CODE_LINE)
 rows=[(0,[('{',C_PUN)]),(1,[('"primitive"',C_KEY),(': {',C_PUN)]),(2,[('"navy.900"',C_KEY),(': ',C_PUN),('"#1B2F54"',C_STR),(',',C_PUN)]),(2,[('"beige.100"',C_KEY),(': ',C_PUN),('"#F8E4C6"',C_STR)]),(1,[('},',C_PUN)]),
       (1,[('"semantic"',C_KEY),(': {',C_PUN)]),(2,[('"action.primary"',C_KEY),(': ',C_PUN),('"{navy.900}"',C_REF),(',',C_PUN)]),(2,[('"surface.base"',C_KEY),(': ',C_PUN),('"{beige.100}"',C_REF),(',',C_PUN)]),(2,[('"surface.selected"',C_KEY),(': ',C_PUN),('"{beige.100}"',C_REF)]),(1,[('}',C_PUN)]),(0,[('}',C_PUN)])]
 y=190
 for i,(ind,parts) in enumerate(rows):
  a+=t(60,y,str(i+1),12,'#4b5468',400,'end',True)
  a+=f'<text x="{78+ind*22}" y="{y}" font-size="13" font-weight="500" font-family="SFMono-Regular, Menlo, Consolas, monospace" xml:space="preserve">'+''.join(f'<tspan fill="{c}">{escape(s_)}</tspan>' for s_,c in parts)+'</text>'
  y+=30
 a+=rect(78,y-6,390,0,'none',0)
 # highlight reference line
 a+=rect(54,348,428,26,'#ffffff',4).replace('/>',' fill-opacity=".06"/>')
 # variables panel
 a+=rect(508,112,252,448,CARD,14,LINE)+t(528,144,'Figma 변수',15,INK,700)+badge(684,128,'API 생성',BROWN,BROWN_SOFT,62)+line(528,162,740,162)
 for i,(group,name,ref,sw) in enumerate([('primitive','navy/900','값 #1B2F54',NAVY),('primitive','beige/100','값 #F8E4C6',BEIGE),('semantic','action/primary','참조 navy/900',NAVY),('semantic','surface/base','참조 beige/100',BEIGE),('semantic','surface/selected','참조 beige/100',BEIGE)]):
  y=192+i*68;a+=rect(528,y-14,32,32,sw,8,'#00000014')+t(574,y-4,group,11,BROWN,700)+t(574,y+14,name,14,INK,650)+t(574,y+31,ref,12,MUTED,500)
  if i<4:a+=line(528,y+44,740,y+44,'#f0f1f3')
 a+=t(528,546,'화면은 semantic 변수만 참조합니다',12,MUTED,500)
 return a

# 2. Markdown guide excerpt
def guide():
 a=frame('Markdown 기준 문서 일부','AI와 사람이 같은 규칙을 읽도록 레이아웃·상태·컴포넌트·용어를 적었습니다.')
 a+=rect(40,112,720,448,CARD,14,LINE)+rect(40,112,720,40,'#fafafa',14)+rect(40,138,720,14,'#fafafa',0)+line(40,152,760,152)+t(60,137,'guide/work-screen.md',12,MUTED,500,None,True)
 y=188;x=64
 def h1(s):return t(x,y,s,20,INK,800)
 a+=t(x,y,'# 업무 화면 기준',19,INK,800,None,True)
 cols=[(64,[('## 레이아웃',['조회 조건 → 요약 → 목록 순서','주요 행동 버튼은 오른쪽 위 1개','좌우 여백 32 · 블록 간격 24']),('## 상태',['읽기 전용: 회색 면, 테두리 없음','비활성: 글자 40% · 클릭 불가','오류: 칸 아래 한 줄로 이유 표시'])]),
       (420,[('## 컴포넌트',['버튼: 주요 1개, 나머지는 보조','표: 숫자는 오른쪽 정렬','빈 목록: 다음 행동 버튼 포함']),('## 용어',['‘삭제’로 통일 (제거·지우기 금지)','날짜 표기 2027.04.18','버튼은 동사로 끝냄: 저장하기'])])]
 for cx,blocks in cols:
  yy=232
  for head,items in blocks:
   a+=t(cx,yy,head,15,BROWN,750,None,True);yy+=32
   for it in items:a+=t(cx,yy,'-',14,FAINT,500,None,True)+t(cx+18,yy,it,14,INK,450);yy+=31
   yy+=28
 a+=line(400,214,400,532,'#f0f1f3')
 return a

# 3. Twelve menus from one standard
def menus():
 a=frame('같은 기준으로 확장한 12개 메뉴','기준 메뉴 1개를 직접 디자인하고, 11개는 AI가 기준 문서를 따라 만들었습니다.')
 names=['기준 메뉴','일정','공지','자료실','근태','장비','예산','인원','보고서','요청','알림','설정']
 cw,ch,gx,gy=164,134,16,16;x0,y0=40,112
 for i,n in enumerate(names):
  c,r=i%4,i//4;x=x0+c*(cw+gx);y=y0+r*(ch+gy);base=i==0
  a+=rect(x,y,cw,ch,CARD,12,BROWN if base else LINE,2 if base else 1)
  a+=rect(x+12,y+12,58,8,INK if base else '#c9ced6',4)+rect(x+cw-42,y+10,30,12,BROWN if base else '#e8d2c7',4)
  a+=rect(x+12,y+30,cw-24,14,'#f3f4f6',4)
  for k in range(3):
   yy=y+52+k*16;a+=rect(x+12,yy,cw-24,10,'#f8f8f9',3)+rect(x+12,yy+2,40+((i*7+k*13)%30),6,'#d6dae0',3)+rect(x+cw-40,yy+2,28,6,'#e3e6ea',3)
  a+=t(x+12,y+ch-14,n,13,INK,700 if base else 600)
  a+=badge(x+cw-(76 if base else 54)-10,y+ch-30,'직접 디자인' if base else 'AI 확장',BROWN if base else MUTED,BROWN_SOFT if base else '#f1f2f4',76 if base else 54)
 a+=t(40,H-26,'제목·주요 버튼·조회 칸·목록의 위치와 간격이 12개 화면에서 같게 유지됩니다.',13,MUTED,500)
 return a

# 4. Fixes made to AI output
def fixes():
 a=frame('AI 결과에서 직접 고친 부분','기준 문서와 대조해 간격·상태 표현·용어가 어긋난 곳을 고쳤습니다.')
 def panel(x,title,ok):
  s=rect(x,112,350,448,CARD,14,LINE)+t(x+20,144,title,15,INK,700)+badge(x+350-20-(64 if ok else 72),128,'기준 적용' if ok else 'AI 첫 결과',GREEN if ok else RED,GREEN_SOFT if ok else RED_SOFT,64 if ok else 72)+line(x+20,162,x+330,162)
  # header row with action button
  s+=t(x+20,196,'장비 대여 요청',16,INK,700)+(rect(x+250,180,80,28,BROWN,8)+t(x+290,199,'저장하기',12,'#fff',700,'middle') if ok else rect(x+236,180,94,28,BROWN,8)+t(x+283,199,'요청 제출',12,'#fff',700,'middle'))
  # fields
  gap=24 if ok else 12
  y=228
  for i,(lab,val,ro) in enumerate([('신청자','이도경',True),('대여 기간','2027.04.18 – 04.20',False),('장비','측정 장비 A-02',False)]):
   s+=t(x+20,y+14,lab,12,MUTED,600)
   if ro and ok:s+=rect(x+20,y+22,310,40,'#f3f4f6',8)+t(x+34,y+47,val,14,'#4b5563',500)
   else:s+=rect(x+20,y+22,310,40,CARD,8,'#cfd4db')+t(x+34,y+47,val,14,INK,500)
   y+=62+gap
  # footer link (term)
  s+=t(x+20,y+18,'선택한 장비 삭제' if ok else '선택한 장비 제거',13,RED if not ok else MUTED,600)
  return s,y
 l,ly=panel(40,'고치기 전',False);r,ry=panel(410,'고친 뒤',True);a+=l+r
 # numbered callouts on the "before" panel
 def mark(n,cx,cy):return circle(cx,cy,11,RED)+t(cx,cy+4.5,str(n),12,'#fff',800,'middle')
 a+=mark(1,28,315)+mark(2,28,250)+mark(3,28,ly+13)
 a+=line(40,295,40,335,RED,2)
 notes=[('1','필드 간격 12 → 기준 24'),('2','읽기 전용 칸을 회색 면으로'),('3','‘제거’ → ‘삭제’, 버튼 ‘저장하기’')]
 y=H-26;x=40
 for n,s_ in notes:
  a+=circle(x+8,y-4,8,RED)+t(x+8,y,n,10,'#fff',800,'middle')+t(x+22,y,s_,12,MUTED,600);x+=240
 return a

font=TTFont(ROOT/'src/fonts/original/SUIT-Variable.woff2');opt=subset.Options();opt.layout_features=['*'];opt.name_IDs=['*'];ss=subset.Subsetter(options=opt);ss.populate(text=Path(__file__).read_text()+'0123456789');ss.subset(font)
for n in font['name'].names:
 if n.nameID in [1,3,4,6,16,17]:
  n.string={1:'Guide UI',3:'GuideUI-SUITSubset-20261128',4:'Guide UI Variable',6:'GuideUI-Variable',16:'Guide UI',17:'Regular'}[n.nameID].encode(n.getEncoding(),errors='replace')
font.flavor='woff2';b=BytesIO();font.save(b);data=base64.b64encode(b.getvalue()).decode()
style=f"<style>@font-face{{font-family:'Guide SUIT';font-style:normal;font-weight:100 900;src:url(data:font/woff2;base64,{data}) format('woff2');}}text{{font-family:'Guide SUIT',sans-serif;}}</style>"
def save(name,body,label):
 (OUT/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}"><title>{label} · 설명용 재구성 · 가상 데이터</title>{style}{body}</svg>',encoding='utf-8')
save('ds-tokens-json',tokens(),'Tokens Studio JSON과 Figma 변수 목록')
save('ds-guide-md',guide(),'Markdown 기준 문서 일부')
save('ds-menus',menus(),'같은 기준으로 확장한 12개 메뉴')
save('ds-ai-fixes',fixes(),'AI 결과에서 직접 고친 부분')
print('Generated four design-system evidence cards')
