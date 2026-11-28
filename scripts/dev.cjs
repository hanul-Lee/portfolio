// Local development server: rebuilds dist/ when src/ or build scripts change and reloads open pages.
// It wraps the hardened preview server and only adds a same-origin reload script, so the CSP stays unchanged.
const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),{spawn}=require('node:child_process');
const {root,src}=require('./lib/paths.cjs');
const serve=require('./lib/server.cjs');
const port=Number(process.env.PORT)||4173;
const clients=new Set();
const reloadScript=`(()=>{const e=new EventSource('/__dev/events');e.addEventListener('reload',()=>location.reload());e.addEventListener('failed',m=>console.error('[dev] build failed\\n'+m.data));})();`;

let building=false,pending=false;
function build(){
 if(building){pending=true;return Promise.resolve();}
 building=true;const started=Date.now();let log='';
 console.log('[dev] building…');
 return new Promise(resolve=>{
  const child=spawn(process.execPath,[path.join(__dirname,'build-site.cjs')],{cwd:root});
  child.stdout.on('data',d=>log+=d);child.stderr.on('data',d=>log+=d);
  child.on('close',code=>{
   building=false;
   if(code===0){console.log(`[dev] built in ${((Date.now()-started)/1000).toFixed(1)}s, reloading ${clients.size} page(s)`);broadcast('reload','');}
   else{console.error('[dev] build failed\n'+log);broadcast('failed',log.slice(-2000));}
   resolve(code);
   if(pending){pending=false;build();}
  });
 });
}
function broadcast(event,data){for(const res of clients)res.write(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);}

let timer;
const ignored=file=>/(^|[\\/])\.|\.css$|\.css\.map$|\.DS_Store$|~$|__pycache__/.test(file);
// Tools that rewrite files with identical bytes (concept generators, tests) must not trigger a rebuild.
const hashes=new Map();
const hashOf=full=>{try{return require('node:crypto').createHash('sha1').update(fs.readFileSync(full)).digest('hex');}catch{return null;}};
const changed=full=>{const hash=hashOf(full);if(hash!==null&&hashes.get(full)===hash)return false;hashes.set(full,hash);return true;};
function seed(dir){
 for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
  const full=path.join(dir,entry.name);
  if(ignored(entry.name))continue;
  if(entry.isDirectory())seed(full);else if(entry.isFile())hashes.set(full,hashOf(full));
 }
}
function watch(dir){
 seed(dir);
 fs.watch(dir,{recursive:true},(_,file)=>{
  if(!file||ignored(file))return;
  if(!changed(path.join(dir,file)))return;
  clearTimeout(timer);timer=setTimeout(()=>{console.log('[dev] changed: '+path.relative(root,path.join(dir,file)));build();},150);
 });
}

(async()=>{
 const first=await build();
 if(first!==0&&!fs.existsSync(path.join(root,'dist/index.html'))){console.error('[dev] first build failed; fix the error and save again.');}
 const inner=await serve(0);
 const innerPort=new URL(inner.url).port;
 const server=http.createServer((req,res)=>{
  const host=req.headers.host?.toLowerCase();
  if(!new Set(['127.0.0.1:'+port,'localhost:'+port]).has(host)){res.writeHead(403).end();return;}
  if(req.url==='/__dev/events'){
   res.writeHead(200,{'Content-Type':'text/event-stream','Cache-Control':'no-cache','Connection':'keep-alive'});
   res.write(': connected\n\n');clients.add(res);req.on('close',()=>clients.delete(res));return;
  }
  if(req.url==='/__dev/reload.js'){res.writeHead(200,{'Content-Type':'text/javascript; charset=utf-8','Cache-Control':'no-cache'}).end(reloadScript);return;}
  const proxy=http.request({host:'127.0.0.1',port:innerPort,path:req.url,method:req.method,headers:{...req.headers,host:'127.0.0.1:'+innerPort}},up=>{
   const isHtml=(up.headers['content-type']||'').startsWith('text/html');
   if(!isHtml||req.method==='HEAD'){res.writeHead(up.statusCode,up.headers);up.pipe(res);return;}
   const chunks=[];up.on('data',c=>chunks.push(c));up.on('end',()=>{
    const body=Buffer.from(Buffer.concat(chunks).toString('utf8').replace(/<\/body>/i,'<script src="/__dev/reload.js"></script></body>'));
    const headers={...up.headers,'content-length':body.length};res.writeHead(up.statusCode,headers).end(body);
   });
  });
  proxy.on('error',()=>{if(!res.headersSent)res.writeHead(502);res.end();});
  req.pipe(proxy);
 });
 server.listen(port,'127.0.0.1',()=>console.log(`[dev] http://127.0.0.1:${port} (watching src/ and scripts/; saves rebuild and reload automatically)`));
 watch(src);watch(__dirname);
})();
