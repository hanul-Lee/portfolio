const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),assert=require('node:assert/strict');
const {withChrome,navigate,pages:allPages}=require('./helpers/site.cjs');
(async()=>{await withChrome(async({send,evaluate:evalJS})=>{
const report=[];
const pages=process.env.AUDIT_PAGES?.split(',') || allPages;
const widths=process.env.AUDIT_WIDTHS?.split(',').map(Number) || [320,390,600,800,801,989,1010,1024,1057,1100,1101,1280,1440,1920,2560];
for(const width of widths){
await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});
for(const file of pages){
await navigate({send,evaluate:evalJS},file);
const info=await evalJS(`(()=>{
const stacks=document.body.classList.contains('portfolio-home')?[[document.querySelector('main'),':scope > section'],[document.querySelector('.featured-projects'),':scope > .work-case']]:[[document.querySelector('.case-main'),':scope > section'],[document.querySelector('.case-body'),':scope > .case-context, :scope > .gallery, :scope > .next'],[document.querySelector('.gallery'),':scope > .story-section']];
const gaps=[];for(const [parent,selector]of stacks){const nodes=[...parent.querySelectorAll(selector)];for(let i=1;i<nodes.length;i++){const a=nodes[i-1],b=nodes[i];const as=getComputedStyle(a),bs=getComputedStyle(b);if(parent.className==='featured-projects') continue;gaps.push({stack:parent.className||'main',from:a.id||a.className,to:b.id||b.className,actual:+(b.getBoundingClientRect().top-a.getBoundingClientRect().bottom).toFixed(2),previousMargin:as.marginBottom,nextMargin:bs.marginTop});}}
return{width:innerWidth,gapToken:getComputedStyle(document.documentElement).getPropertyValue('--section-gap').trim(),gaps,overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth,missing:[...document.images].filter(i=>!i.naturalWidth).length};})()`);
assert.equal(info.overflow,false,file+' overflow '+width);assert.equal(info.missing,0,file+' missing images');
// Home sections use the section gap token; detail pages stack release panels with one tight rhythm.
const min=file==='index.html'?(width<=800?80:128):(width<=800?12:20),max=min;
for(const gap of info.gaps){assert.ok(gap.actual>=min-.1&&gap.actual<=max+.1,JSON.stringify({file,width,...gap}));assert.equal(gap.previousMargin,'0px');assert.equal(gap.nextMargin,'0px');}
if(file === 'index.html') {
  const releases = await evalJS(`(()=>[...document.querySelectorAll('.work-case')].map(e=>({title:e.querySelector('h3').getBoundingClientRect().top,decisions:e.querySelector('.work-decisions').getBoundingClientRect().top,link:e.querySelector('.case-text-link').getBoundingClientRect().top,visual:e.querySelector('.work-visual').getBoundingClientRect().height})))()`);
  assert.equal(releases.length,3,'three version history releases '+width);
  for(const card of releases){assert.ok(card.visual>0,'release visual '+width);assert.ok(card.decisions>card.title,'project decisions after title '+width);assert.ok(card.link>card.decisions,'project link after decisions '+width);}
}
if(file !== 'index.html') {
  const visualCards = await evalJS(`(()=>{
    const measure=element=>{const bounds=element.getBoundingClientRect();return {top:bounds.top,bottom:bounds.bottom,height:bounds.height,width:bounds.width};};
    return [...document.querySelectorAll('.project-visual-grid')].map(grid=>[...grid.querySelectorAll('figure')].map(figure=>({card:measure(figure),frame:measure(figure.querySelector('.visual-frame')),caption:measure(figure.querySelector('figcaption')),portrait:figure.classList.contains('portrait'),maxHeight:parseFloat(getComputedStyle(figure.querySelector('.visual-frame')).maxHeight)})));
  })()`);
  for(const cards of visualCards) for(const card of cards) {
    const matchingFrame = cards.find(other => other.portrait === card.portrait);
    assert.ok(Math.abs(card.frame.height-matchingFrame.frame.height)<1,file+' equal image frame heights '+width);
    if (Math.abs(card.card.top-cards[0].card.top)<1) assert.ok(Math.abs(card.card.height-cards[0].card.height)<1,file+' equal visual card heights '+width);
    const fixedHeight = file === 'project-dashboard.html' ? (width <= 600 ? 220 : 280) : ['project-intranet.html','project-measure.html'].includes(file) ? (width <= 600 ? 380 : 440) : null;
    if (fixedHeight) assert.ok(Math.abs(card.frame.height-fixedHeight)<1,file+' fixed visual frame '+width);
    else {
      const ratio = file === 'project-tbm.html' && card.portrait ? 390/810 : 16/9;
      const expected = Math.min(card.frame.width/ratio, card.maxHeight || Infinity);
      assert.ok(Math.abs(card.frame.height-expected)<1,file+' compact visual frame '+width);
    }
    assert.ok(card.caption.top>=card.frame.bottom,file+' caption below image '+width);
    if(Math.abs(card.card.top-cards[0].card.top)<1) assert.ok(Math.abs(card.caption.top-cards[0].caption.top)<1,file+' aligned visual captions '+width);
  }
  const comparisonCards = await evalJS(`(()=>{const cards=[...document.querySelectorAll('.iteration-compare > div')];return cards.map(card=>{const bounds=card.getBoundingClientRect(),frame=card.querySelector('.comparison-image, .wireframe').getBoundingClientRect();return {top:bounds.top,height:bounds.height,frameTop:frame.top,frameHeight:frame.height};});})()`);
  if(comparisonCards.length>1) {
    assert.ok(Math.abs(comparisonCards[0].frameHeight-comparisonCards[1].frameHeight)<1,file+' equal comparison image heights '+width);
    if(width>800) for(const key of ['top','height','frameTop']) assert.ok(Math.abs(comparisonCards[0][key]-comparisonCards[1][key])<1,file+' aligned comparison '+key+' '+width);
  }
  const heroGroups = await evalJS(`(()=>{const hero=document.querySelector('.case-hero'),overview=hero.querySelector(':scope > .case-hero-overview'),copy=overview.querySelector(':scope > .case-hero-copy'),cover=overview.querySelector(':scope > .case-cover'),meta=hero.querySelector(':scope > .case-meta');const h=hero.getBoundingClientRect(),o=overview.getBoundingClientRect(),c=copy.getBoundingClientRect(),v=cover.getBoundingClientRect(),m=meta.getBoundingClientRect();return {groups:hero.children.length,actions:copy.querySelectorAll('.case-hero-actions a').length,actionsInside:!!copy.querySelector('.case-result + .case-hero-actions'),metaOutside:!overview.contains(meta),overviewBottom:o.bottom,metaTop:m.top,heroWidth:h.width-parseFloat(getComputedStyle(hero).paddingLeft)-parseFloat(getComputedStyle(hero).paddingRight),metaWidth:m.width,copyTop:c.top,copyBottom:c.bottom,copyRight:c.right,coverTop:v.top,coverLeft:v.left,coverBottom:v.bottom,coverRight:v.right};})()`);
  assert.equal(heroGroups.groups,2,file+' two hero groups');
  assert.equal(heroGroups.actions,file==='project-pet.html'?3:2,file+' hero shortcuts');
  assert.equal(heroGroups.actionsInside,true);
  assert.equal(heroGroups.metaOutside,true);
  assert.ok(heroGroups.metaTop>=heroGroups.overviewBottom+(file==='project-kanvan.html'?27:31),file+' metadata below overview');
  assert.ok(Math.abs(heroGroups.heroWidth-heroGroups.metaWidth)<1,file+' full-width metadata');
  if(width<=800)assert.ok(heroGroups.coverTop>=heroGroups.copyBottom+31,file+' stacked overview');
  else {assert.ok(heroGroups.coverLeft>=heroGroups.copyRight+(width<=1100?31:47),file+' side-by-side overview');assert.ok(Math.abs(heroGroups.copyTop-heroGroups.coverTop)<1,file+' image stays top-aligned');}
  assert.ok(heroGroups.coverRight<=width,file+' cover fits viewport');

  const solution = await evalJS(`(()=>{const e=document.querySelector('#solution'),copy=e.querySelector('.solution-copy, header').getBoundingClientRect(),stage=e.querySelector('.ui-stage, .tbm-primary-screen').getBoundingClientRect();return {minHeight:getComputedStyle(e).minHeight,direction:getComputedStyle(e).flexDirection,copyBottom:copy.bottom,stageTop:stage.top,topSpace:copy.top-e.getBoundingClientRect().top};})()`);
  assert.equal(solution.minHeight,'0px');
  if(width<=1100){if(file!=='project-tbm.html')assert.equal(solution.direction,'column');assert.ok(solution.stageTop>=solution.copyBottom,'text before solution image');assert.ok(solution.topSpace<=49,'compact solution padding (panel padding only)');}
  const arrow = await evalJS(`({old:getComputedStyle(document.querySelector('.next > a:first-child'),'::after').content,margin:getComputedStyle(document.querySelector('.next h3'),'::after').marginLeft,position:getComputedStyle(document.querySelector('.next h3'),'::after').position})`);
  assert.equal(arrow.old,'none');assert.equal(arrow.margin,'8px');assert.equal(arrow.position,'static');
  const nextPreview=await evalJS(`(()=>{const link=document.querySelector('.next-project'),preview=link.querySelector('.next-preview').getBoundingClientRect(),copy=link.querySelector('.next-copy').getBoundingClientRect();return {cardWidth:link.getBoundingClientRect().width,containerWidth:link.parentElement.getBoundingClientRect().width,display:getComputedStyle(link).display,width:preview.width,right:preview.right,copyLeft:copy.left,summary:link.querySelector('p').textContent};})()`);
  assert.equal(nextPreview.display,'grid',file+' next preview grid '+width);
  assert.ok(Math.abs(nextPreview.cardWidth-nextPreview.containerWidth)<1,file+' full-width next preview '+width);
  assert.ok(Math.abs(nextPreview.width-(width<=600?96:160))<1,file+' next preview width '+width);
  assert.ok(nextPreview.right<nextPreview.copyLeft&&nextPreview.summary.length>0,file+' next preview beside summary '+width);


  const numbers = await evalJS(`Array.from(document.querySelectorAll('.gallery > .story-section > header > p, .gallery > .story-section > .solution-copy > p')).map(x => x.textContent.match(/^([0-9]{2}) /)?.[1]).filter(Boolean).map(Number)`);
  assert.deepEqual(numbers, numbers.map((_, i) => i + (file==='project-tbm.html'?1:2)), file + ' section sequence');
  assert.equal(await evalJS(`document.querySelectorAll('.user-voice').length`), 0);
}
if(width <= 1024) {
  await evalJS(`document.querySelector('.menu').click()`);
  const menu = await evalJS(`(()=>{const n=document.querySelector('#primary-nav').getBoundingClientRect(),b=document.querySelector('.menu').getBoundingClientRect();return {width:n.width,right:n.right,buttonRight:b.right,expanded:document.querySelector('.menu').getAttribute('aria-expanded')};})()`);
  assert.equal(menu.expanded,'true');
  assert.ok(menu.width < width - 48, file + ' compact menu');
  assert.ok(Math.abs(menu.right-menu.buttonRight)<2, file + ' menu right alignment');
  await evalJS(`document.querySelector('.menu').click()`);
}
if(file==='index.html' && [390,1280].includes(width)) {
  const hero=await evalJS(`({image:document.querySelector('.release-screen img').getAttribute('src'),scope:document.querySelector('.release-latest .release-role').textContent,status:document.querySelector('.release-latest .release-version').textContent,planets:document.querySelectorAll('img[src*="assets/planets/"]').length})`);
  assert.ok(hero.image.includes('assets/cases/pet-screens'));
  assert.ok(hero.scope.includes('공동 기획') && hero.scope.includes('입력 흐름'));
  assert.ok(hero.status.includes('iOS 출시') && hero.status.includes('2026.08.17'));
  assert.equal(hero.planets,0);
  const rows=await evalJS(`[...document.querySelectorAll('.featured-projects > .work-case')].map(e=>e.getBoundingClientRect()).map(r=>({top:r.top,bottom:r.bottom}))`);
  for(let r=1;r<rows.length;r++)assert.ok(Math.abs(rows[r].top-rows[r-1].bottom-24)<1,'release spacing '+width);
  const shot=await send('Page.captureScreenshot');fs.writeFileSync(path.join(os.tmpdir(),'hanul-home-'+width+'.png'),Buffer.from(shot.data,'base64'));
  await evalJS(`document.documentElement.style.scrollBehavior='auto';document.querySelector('#work').scrollIntoView({behavior:'instant'})`);
  const workShot=await send('Page.captureScreenshot');fs.writeFileSync(path.join(os.tmpdir(),'hanul-work-'+width+'.png'),Buffer.from(workShot.data,'base64'));

}
if(width===1010 && (file==='index.html'||file==='project-platform.html'||file==='project-tbm.html')) {
  const selector=file==='index.html'?'.work-case:nth-child(3)':file==='project-platform.html'?'#solution':'.next';
  await evalJS(`document.documentElement.style.scrollBehavior='auto';document.querySelector('${selector}').scrollIntoView({behavior:'instant'})`);
  const shot=await send('Page.captureScreenshot');fs.writeFileSync(path.join(os.tmpdir(),file.replace('.html','')+'-alignment.png'),Buffer.from(shot.data,'base64'));
}
if(['project-platform.html','project-tbm.html'].includes(file) && [390,1057,1280].includes(width)) {
  await evalJS(`document.documentElement.style.scrollBehavior='auto';window.scrollTo(0,0)`);
  const shot=await send('Page.captureScreenshot');fs.writeFileSync(path.join(os.tmpdir(),file.replace('.html','')+'-hero-'+width+'.png'),Buffer.from(shot.data,'base64'));
}
report.push({file,...info});
if(file==='index.html'&&width===390){await evalJS(`document.documentElement.style.scrollBehavior='auto'; document.querySelector('.selected-work').scrollIntoView({behavior:'instant'})`);const shot=await send('Page.captureScreenshot');fs.writeFileSync('/tmp/section-gap-home.png',Buffer.from(shot.data,'base64'));}
if(file==='project-dashboard.html'&&width===1280){await evalJS(`document.documentElement.style.scrollBehavior='auto'; document.querySelector('#context').scrollIntoView({behavior:'instant'})`);const shot=await send('Page.captureScreenshot');fs.writeFileSync('/tmp/section-gap-detail.png',Buffer.from(shot.data,'base64'));}
}
console.log('PASS',width+'px',pages.length+' pages: home gaps '+(width<=800?'80':'128')+'px, detail panels '+(width<=800?'12':'20')+'px, zero adjacent margins, no overflow or missing images');
}
fs.writeFileSync(process.env.AUDIT_REPORT || path.join(os.tmpdir(),'section-spacing-validation.json'),JSON.stringify({date:new Date().toLocaleDateString('sv-SE',{timeZone:'Asia/Seoul'}),method:'Chrome DevTools Protocol + getBoundingClientRect + computed styles',results:report},null,2));
});})().catch(e=>{console.error(e);process.exitCode=1;});
