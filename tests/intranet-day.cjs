const assert=require('node:assert/strict');
const {withSite,withBrowsers}=require('./helpers/browser.cjs');
(async()=>withSite(async(base)=>withBrowsers(async(engine,browser)=>{
 const page=await browser.newPage({reducedMotion:'reduce'}),errors=[],failed=[],requests=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)failed.push(r.url())});page.on('request',r=>requests.push(r.url()));
 for(const [width,height]of [[1440,900],[1280,720],[1024,768],[768,1024],[390,844],[320,700]]){
  await page.setViewportSize({width,height});await page.goto(`${base}/assets/demos/intranet-day/index.html`);
  await page.evaluate(()=>localStorage.clear());await page.reload();await page.getByRole('button',{name:'가상 계정으로 체험하기'}).click();
  await page.getByRole('button',{name:'출근',exact:true}).click();await page.getByRole('button',{name:'퇴근',exact:true}).waitFor();
  const layout=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,clipped:[...document.querySelectorAll('.dashboard .dash-panel')].filter(e=>e.scrollHeight>e.clientHeight+2).map(e=>e.querySelector('h2')?.textContent),titleWidth:document.querySelector('.project-header strong').getBoundingClientRect().width}));
  assert.equal(layout.overflow,false,`${engine} ${width} horizontal overflow`);assert.deepEqual(layout.clipped,[],`${engine} ${width} clipped cards`);assert.ok(layout.titleWidth>80,`${engine} ${width} project title collapsed`);
 }
 await page.setViewportSize({width:1280,height:900});await page.getByRole('textbox',{name:'프로젝트 코드 선택'}).click();await page.getByRole('dialog',{name:'코드검색'}).waitFor();await page.keyboard.press('Escape');
 await page.locator('.portal-nav').getByRole('button',{name:'전자결재',exact:true}).click();await page.getByRole('button',{name:'문서작성',exact:true}).click();assert.ok(await page.locator('input[type="file"]').isDisabled());
 await page.locator('.portal-nav').getByRole('button',{name:'팀관리',exact:true}).click();await page.getByRole('searchbox').fill('윤다온');assert.equal(await page.locator('tbody tr').count(),1);
 await page.reload();await page.getByRole('button',{name:'가상 계정으로 체험하기'}).click();assert.ok(await page.getByRole('button',{name:'퇴근',exact:true}).isVisible());
 await page.getByRole('button',{name:'데모 초기화'}).click();await page.getByRole('button',{name:'가상 계정으로 체험하기'}).click();assert.ok(await page.getByRole('button',{name:'출근',exact:true}).isVisible());
 assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);assert.ok(!requests.some(url=>new URL(url).origin!==new URL(base).origin||new URL(url).pathname.startsWith('/api/')),'unexpected network request');
 console.log(`PASS: ${engine} intranet at six widths: cards, project title, code search, approval form, member search, persistence, reset and local-only requests`);
 await page.close();
})))().catch(e=>{console.error(e);process.exit(1)});
