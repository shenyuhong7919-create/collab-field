<!-- 侧栏注入模板：由 src/build.py 读入，替换 __LEDGER__ 后插到 </body> 前 -->
<style id="sideStyle">
#side{position:fixed;top:64px;right:14px;width:362px;z-index:60;display:flex;flex-direction:column;
  background:rgba(7,6,3,.84);border:1px solid rgba(255,212,0,.35);
  backdrop-filter:blur(3px);font:10.5px/1.62 "SF Mono",Menlo,monospace;color:#E8DCBB;
  box-shadow:0 0 26px rgba(255,150,20,.10) inset}
#side .hd{display:flex;justify-content:space-between;align-items:center;flex:0 0 auto;
  padding:6px 8px;border-bottom:1px solid rgba(255,212,0,.22);letter-spacing:.14em;font-size:9.5px;color:#FFD400}
#side .hd b{font-weight:600}
#side .hd i{font-style:normal;color:#8a7a4a}
#side .sec{display:flex;flex-direction:column;min-height:0;flex:0 0 auto;
  padding:6px 9px 7px;border-bottom:1px solid rgba(255,212,0,.10)}
#side .lb{flex:0 0 auto;font-size:8.6px;letter-spacing:.18em;color:#7d6a34;margin-bottom:3px;
  display:flex;justify-content:space-between}
#side .lb b{color:#FFD400;font-weight:600}
#side .log{display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden;max-height:5.4em;
  -webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 16px);
  mask-image:linear-gradient(to bottom,transparent 0,#000 16px)}
#side .e{flex:0 0 auto;white-space:pre-wrap;word-break:break-word;min-height:1.62em;
  padding-left:5.9em;text-indent:-5.9em}
#side .e.old{opacity:.5}
#side .sec.th .e+.e{margin-top:2px}
#side .sec.cd .e+.e{margin-top:5px}
#side .ts{font-style:normal;color:#6f5f30;margin-right:5px}
#side .th .tx{color:#cfc6a8}
#side .cd .tx{color:#FFD400}
#side .rs .tx{color:#FFF0C0}
#side .rs .e .tx{color:#FFF0C0}
#side .e.typing .tx::after{content:"▍";color:#FFD400;margin-left:1px;animation:sbl .55s steps(1) infinite}
@keyframes sbl{50%{opacity:0}}
#side .ft{display:flex;justify-content:space-between;padding:5px 9px;font-size:8.4px;color:#7d6a34;flex:0 0 auto}
/* 系统遥测 */
#side .sys{border-top:1px solid rgba(255,212,0,.22);padding:7px 9px 8px;flex:0 0 auto}
#side .sys .t{font-size:8.6px;letter-spacing:.16em;color:#7d6a34;display:flex;justify-content:space-between}
#side .sys .t b{color:#FFD400;font-weight:600}
#side .spec{font-size:8.4px;color:#8a7a4a;margin:3px 0 4px;line-height:1.5}
#side .spark{display:none;margin:2px 0 5px}
#side .spark .lg{display:flex;gap:12px;font-size:8px;color:#7d6a34;letter-spacing:.1em;margin-bottom:3px}
#side .spark .lg b{font-weight:500;color:#cfc6a8}
#side .spark .lg s{display:inline-block;width:12px;height:2px;vertical-align:2px;margin-right:4px}
#side canvas{display:block;width:100%;height:26px}
#side .row{display:grid;grid-template-columns:36px minmax(0,1fr) 112px;gap:6px;align-items:center;
  font-size:8.8px;margin:3px 0;color:#bda67a}
#side .row .k{color:#8a7a4a;letter-spacing:.06em}
#side .row .v{display:flex;justify-content:flex-end;align-items:baseline;gap:6px;white-space:nowrap;
  text-align:right;color:#E8DCBB}
#side .row .v b{font-weight:500;color:#FFE9A8}
#side .row .v em{font-style:normal;font-size:7.8px;color:#7d6a34}
#side .bar{position:relative;height:6px;background:rgba(255,212,0,.10);overflow:hidden}
#side .bar i{position:absolute;left:0;top:0;bottom:0;width:0%;background:linear-gradient(90deg,#7a5a00,#FFD400);transition:width .3s linear}
#side .bar.hot i{background:linear-gradient(90deg,#FF8A1F,#FF5A1F)}
#side .bar.crit i{background:linear-gradient(90deg,#FF5A1F,#E23A3A)}
#side .mini{display:grid;grid-template-columns:1fr 1fr;gap:2px 10px;font-size:8.2px;color:#8a7a4a;margin-top:5px}
#side .mini .wide{grid-column:1 / -1}
#side .mini b{color:#cfc6a8;font-weight:500}
.music.wait em{animation:none!important;opacity:1!important}
</style>
<aside id="side">
  <div class="hd"><b>LIVE / AGENT BUS</b><i id="sideClk">--:--:--</i></div>
  <div class="sec th"><div class="lb"><b>THOUGHT</b> 思考过程<span id="sideThN">—</span></div><div class="log" id="sideTh"></div></div>
  <div class="sec cd"><div class="lb"><b>CODE</b> 实时构建</div><div class="log" id="sideCd"></div></div>
  <div class="sec rs"><div class="lb"><b>RESULT</b> 结果<span id="sideRsN">—</span></div><div class="log" id="sideRs"></div></div>
  <div class="sys">
    <div class="t"><b>SYSTEM</b><span>CLOUD NODE 07</span></div>
    <div class="spec">16 vCPU / 24C GPU · 64 GB 内存 · 1.2 TB NVMe<br>LINUX 24.04 · 容器 · 远程构建</div>
    <div class="spark">
      <div class="lg"><span><s style="background:#FFD400"></s><b>CPU</b></span><span><s style="background:#FF8A1F"></s><b>GPU</b></span><span style="margin-left:auto">30S</span></div>
      <canvas id="spark" width="720" height="52"></canvas>
    </div>
    <div class="row"><span class="k">CPU</span><span class="bar" id="bCpu"><i></i></span><span class="v" id="vCpu">—</span></div>
    <div class="row"><span class="k">GPU</span><span class="bar" id="bGpu"><i></i></span><span class="v" id="vGpu">—</span></div>
    <div class="row"><span class="k">MEM</span><span class="bar" id="bMem"><i></i></span><span class="v" id="vMem">—</span></div>
    <div class="row"><span class="k">SSD</span><span class="bar" id="bSsd"><i></i></span><span class="v" id="vSsd">—</span></div>
    <div class="mini">
      <span>温度 <b id="vTmp">—</b></span><span>功耗 <b id="vPwr">—</b></span>
      <span>风扇 <b id="vFan">—</b></span><span>UPS <b id="vBat">—</b></span>
      <span class="wide">网络 <b id="vNet">—</b></span>
      <span>负载 <b id="vLd">—</b></span><span>进程 <b id="vPrc">—</b></span>
      <span class="wide">运行 <b id="vUp">—</b> · 交换 <b id="vSwp">—</b></span>
    </div>
  </div>
  <div class="ft"><span id="sidePt">BUS</span><span id="sideQ">QUEUE</span></div>
</aside>
<script id="sideJs">
(function(){
  var L = __LEDGER__;
  var thEl=document.getElementById('sideTh'), cdEl=document.getElementById('sideCd'),
      rsEl=document.getElementById('sideRs'), clk=document.getElementById('sideClk'),
      pt=document.getElementById('sidePt'), q=document.getElementById('sideQ'),
      thN=document.getElementById('sideThN'), rsN=document.getElementById('sideRsN'),
      spEl=document.getElementById('spark'), sc=spEl.getContext('2d');
  var S={cpu:58,gpu:71,mem:52,ssd:11,tmp:57,pwr:38,fan:2450,bat:96,net:12.4,ld:3.2,prc:412,swp:.4};
  var H1=[],H2=[],MAXH=116;
  var t0=Date.now()-(3*86400+7*3600+12*60)*1000;
  var pad=function(n){return String(n).padStart(2,'0');};
  var clock=function(d){return pad(d.getHours())+':'+pad(d.getMinutes())+':'+pad(d.getSeconds());};
  var tsAgo=function(sec){return clock(new Date(Date.now()-sec*1000));};
  var wait=function(ms){return new Promise(function(r){setTimeout(r,ms);});};
  var walk=function(c,st,lo,hi){return Math.max(lo,Math.min(hi,c+(Math.random()-0.48)*st));};
  var bar=function(id,v){var b=document.getElementById(id);b.firstElementChild.style.width=v.toFixed(1)+'%';
    b.className='bar'+(v>90?' crit':v>76?' hot':'');};
  function add(host,ts,cls,txt){
    var d=document.createElement('div'), t=document.createElement('span');
    d.className='e'+(cls?' '+cls:'');
    d.innerHTML='<i class="ts">'+ts+'</i>';
    t.className='tx'; t.textContent=txt||''; d.appendChild(t);
    host.appendChild(d);
    while(host.children.length>90) host.removeChild(host.firstElementChild);
    return t;
  }
  function typeTx(tx,text,per){
    return new Promise(function(res){
      var n=0; tx.parentNode.classList.add('typing');
      (function step(){
        n+=4; tx.textContent=text.slice(0,n);
        if(n<text.length) setTimeout(step,per);
        else { tx.textContent=text; tx.parentNode.classList.remove('typing'); res(); }
      })();
    });
  }
  function evLine(t){return (t.ev==='session')?('会话 '+t.rows+' 行'):'索引登记';}
  function codeOf(t){
    return 'const t = ledger.get('+t.id+');\nt.tool = "'+t.tool+'";\nt.sector = "'+t.sector+'";\nbus.emit("indexed", t);';
  }
  /* 预填历史：底部对齐的终端回滚，顶部自然裁掉 */
  function seedLogs(){
    var n=Math.min(11,L.tasks.length);
    for(var k=0;k<n;k++){
      var t=L.tasks[k], ts=tsAgo((n-k)*6+4);
      add(thEl,ts,'old','▸ 取队列 task#'+t.id+' · '+t.date+' · '+t.tool+'\n◂ 证据 '+evLine(t)+' · 工作流 '+t.sector+' '+(L.sect[t.sector]||0));
      if(k%2===1) add(cdEl,ts,'old',codeOf(t));
      add(rsEl,ts,'old','✓ #'+t.id+' 入库 · '+t.sector+' '+(L.sect[t.sector]||0)+' · 凭据 '+L.proof+'/'+L.proofTotal);
      add(rsEl,tsAgo((n-k)*6+3),'old','· 索引 '+(L.tasksN-1)+'/'+L.tasksN+' · '+evLine(t)+' · 缺口 '+L.gaps);
    }
  }
  /* CPU / GPU 走势 */
  function pushH(a,v){a.push(v);if(a.length>MAXH)a.shift();}
  function drawSpark(){
    var w=spEl.width,h=spEl.height,x,y,k;
    sc.clearRect(0,0,w,h);
    sc.strokeStyle='rgba(255,212,0,.10)';sc.lineWidth=1;
    for(k=1;k<4;k++){y=h*k/4;sc.beginPath();sc.moveTo(0,y);sc.lineTo(w,y);sc.stroke();}
    var line=function(a,col){
      if(a.length<2)return;
      sc.beginPath();
      for(k=0;k<a.length;k++){x=k*(w-2)/(MAXH-1)+1;y=h-3-(a[k]/100)*(h-6);if(k)sc.lineTo(x,y);else sc.moveTo(x,y);}
      sc.strokeStyle=col;sc.lineWidth=2;sc.stroke();
    };
    line(H2,'#FF8A1F');line(H1,'#FFD400');
  }
  function sysTick(){
    S.cpu=walk(S.cpu,13,6,96);S.gpu=walk(S.gpu,15,10,98);S.mem=walk(S.mem,5,38,74);S.ssd=walk(S.ssd,.5,8,17);
    S.tmp=walk(S.tmp,3,44,82);S.pwr=walk(S.pwr,7,22,72);S.fan=walk(S.fan,160,1500,4200);
    S.bat=Math.max(52,S.bat-(Math.random()<.15?.1:0));S.net=walk(S.net,4,.4,88);S.ld=walk(S.ld,.7,.6,12);
    S.prc=walk(S.prc,9,380,520);S.swp=walk(S.swp,.08,0,2.4);
    bar('bCpu',S.cpu);bar('bGpu',S.gpu);bar('bMem',S.mem);bar('bSsd',S.ssd);
    document.getElementById('vCpu').innerHTML='<b>'+Math.round(S.cpu)+'%</b><em>16 vCPU</em>';
    document.getElementById('vGpu').innerHTML='<b>'+Math.round(S.gpu)+'%</b><em>24 核</em>';
    document.getElementById('vMem').innerHTML='<b>'+Math.round(S.mem)+'%</b><em>'+(S.mem*.64).toFixed(1)+'/64G</em>';
    document.getElementById('vSsd').innerHTML='<b>'+(Math.round(S.ssd*10)/10)+'%</b><em>'+(S.ssd*12).toFixed(0)+'G/1.2T</em>';
    document.getElementById('vTmp').textContent=Math.round(S.tmp)+'°C';
    document.getElementById('vPwr').textContent=Math.round(S.pwr)+'W';
    document.getElementById('vFan').textContent=Math.round(S.fan/10)*10+' rpm';
    document.getElementById('vBat').textContent=Math.round(S.bat)+'% · 在线';
    document.getElementById('vNet').textContent='↓'+S.net.toFixed(1)+' ↑'+(S.net*.28).toFixed(1)+' MB/s';
    document.getElementById('vLd').textContent=S.ld.toFixed(2);
    document.getElementById('vPrc').textContent=Math.round(S.prc);
    var s=Math.floor((Date.now()-t0)/1000);
    document.getElementById('vUp').textContent=Math.floor(s/86400)+'d '+pad(Math.floor(s%86400/3600))+'h '+pad(Math.floor(s/60)%60)+'m';
    document.getElementById('vSwp').textContent=S.swp.toFixed(1)+' GB';
    pushH(H1,S.cpu);pushH(H2,S.gpu);drawSpark();
  }
  for(var z=0;z<MAXH;z++){
    H1.push(Math.max(8,Math.min(94,54+Math.sin(z/8)*11+Math.random()*10)));
    H2.push(Math.max(12,Math.min(96,68+Math.cos(z/6)*9+Math.random()*12)));
  }
  seedLogs(); sysTick();
  pt.textContent='BUS · TOOLS '+L.tools+' · '+L.span;
  q.textContent='QUEUE '+L.tasksN;
  setInterval(sysTick,260);
  setInterval(function(){clk.textContent=clock(new Date());},1000);
  var i=0;
  async function run(){
    for(;;){
      var t=L.tasks[i%L.tasks.length]; i++;
      thN.textContent='#'+t.id; rsN.textContent='#'+t.id;
      var tx=add(thEl,clock(new Date()),'','');
      await typeTx(tx,'▸ 取队列 task#'+t.id+' · '+t.date+' · '+t.tool+'\n◂ 证据 '+evLine(t)+' · 工作流 '+t.sector+' '+(L.sect[t.sector]||0),2);
      await wait(30);
      var cx=add(cdEl,clock(new Date()),'','');
      await typeTx(cx,codeOf(t),1.4);
      await wait(20);
      add(rsEl,clock(new Date()),'ok','✓ #'+t.id+' 入库 · '+t.sector+' '+(L.sect[t.sector]||0)+' · 索引 '+(L.tasksN-1)+'/'+L.tasksN+' · 凭据 '+L.proof+'/'+L.proofTotal);
      add(rsEl,clock(new Date()),'','· '+evLine(t)+' · 缺口 '+L.gaps+' · 工作流累计 '+(L.sect[t.sector]||0));
      pt.textContent='BUS · TOOLS '+L.tools+' · '+L.span;
      q.textContent='QUEUE '+L.tasksN+' · #'+t.id;
      await wait(110);
    }
  }
  run();
})();
</script>
<style id="layoutFix">
/* 列表行不许被压扁（原版 14 行在矮面板里会叠字） */
.feed>div,.code>div{flex:0 0 auto}
/* —— 常规比例：右上角控件左移，让开右侧栏 —— */
.ov.console{right:386px}
.ov.music{right:476px}
/* —— 超宽屏（≥21:10）：底栏改为右侧竖栏，画布占满左侧 —— */
@media (min-aspect-ratio: 21/10){
  .app{grid-template-columns:minmax(0,1fr) 820px;grid-template-rows:auto minmax(0,1fr)}
  header{grid-column:1;grid-row:1}
  .stage{grid-column:1;grid-row:2}
  .panels{grid-column:2;grid-row:1 / span 2;
    grid-template-columns:minmax(0,1fr);align-content:start;
    border-top:none;border-left:1px solid var(--line);
    padding:8px 412px 14px 12px;overflow-y:auto;gap:9px}
  /* 8 块面板 + 7 道 9px 间隔 + 上下 22px 内边距，正好铺满右栏高度 */
  .p{height:calc((100vh - 85px) / 8);min-height:132px}
  .ov.console{right:14px}
  .ov.music{right:104px}
  #side{top:0;right:0;width:398px;height:100vh;font-size:11.2px;
    border-left:1px solid rgba(255,212,0,.28);border-top:none;border-right:none;border-bottom:none}
  #side .sec{flex:1 1 0;overflow:hidden}
  #side .log{max-height:none;flex:1 1 auto;min-height:0}
  #side .spark{display:block}
  #side canvas{height:30px}
  #side .spec{font-size:8.8px}
  #side .row{font-size:9.4px}
  #side .mini{font-size:8.8px}
}
</style>
