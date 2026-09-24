(function(){ 'use strict';
  // line chart
  document.querySelectorAll('[data-line-chart]').forEach(function(el){
    var points=(el.dataset.points||'12,40,28,30,18,55,40,48,32,68,55,72,62,80').split(',').map(Number);
    var W=400,H=140;var maxv=Math.max.apply(null,points),minv=Math.min.apply(null,points);
    var step=W/(points.length-1);
    var norm=points.map(function(v){return H-8-((v-minv)/(maxv-minv||1))*(H-16);});
    var pathD=norm.map(function(y,i){return (i===0?'M':'L')+(i*step).toFixed(1)+','+y.toFixed(1);}).join(' ');
    var areaD=pathD+' L '+W.toFixed(1)+','+H+' L 0,'+H+' Z';
    var gid='lg-'+Math.random().toString(36).slice(2,8);
    el.setAttribute('viewBox','0 0 '+W+' '+H); el.setAttribute('preserveAspectRatio','none');
    var html='<defs><linearGradient id="'+gid+'" x1="0" x2="0" y1="0" y2="1">'+
      '<stop offset="0%" stop-color="#00e5ff" stop-opacity="0.4"/>'+
      '<stop offset="100%" stop-color="#00e5ff" stop-opacity="0"/></linearGradient></defs>'+
      '<g stroke="rgba(0,229,255,0.10)" stroke-width="1">'+
      '<line x1="0" y1="'+(H*0.25)+'" x2="'+W+'" y2="'+(H*0.25)+'"/>'+
      '<line x1="0" y1="'+(H*0.5)+'" x2="'+W+'" y2="'+(H*0.5)+'"/>'+
      '<line x1="0" y1="'+(H*0.75)+'" x2="'+W+'" y2="'+(H*0.75)+'"/></g>'+
      '<path d="'+areaD+'" fill="url(#'+gid+')"/>'+
      '<path d="'+pathD+'" fill="none" stroke="#00e5ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="800" stroke-dashoffset="800">'+
      '<animate attributeName="stroke-dashoffset" from="800" to="0" dur="1.8s" fill="freeze"/></path>';
    norm.forEach(function(y,i){
      html+='<circle cx="'+(i*step).toFixed(1)+'" cy="'+y.toFixed(1)+'" r="2.5" fill="#00e5ff" opacity="0">'+
        '<animate attributeName="opacity" from="0" to="1" begin="'+(0.8+i*0.05).toFixed(2)+'s" dur="0.2s" fill="freeze"/></circle>';
    });
    el.innerHTML=html;
  });
  // donut
  document.querySelectorAll('[data-donut]').forEach(function(el){
    var value=parseFloat(el.dataset.donut);
    var total=parseFloat(el.dataset.total||'100');
    var label=el.dataset.label||'';var color=el.dataset.color||'#00e5ff';
    var pct=Math.max(0,Math.min(1,value/total));
    var C=2*Math.PI*36;var dash=C*pct;
    el.setAttribute('viewBox','0 0 100 100');
    el.innerHTML='<circle cx="50" cy="50" r="36" stroke="rgba(255,255,255,0.06)" stroke-width="10" fill="none"/>'+
      '<circle cx="50" cy="50" r="36" stroke="'+color+'" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="'+C+'" stroke-dashoffset="'+C+'" transform="rotate(-90 50 50)">'+
      '<animate attributeName="stroke-dashoffset" from="'+C+'" to="'+(C-dash)+'" dur="1.6s" fill="freeze"/></circle>'+
      '<text x="50" y="46" text-anchor="middle" fill="#e6edf7" font-family="Space Grotesk, Inter, sans-serif" font-size="18" font-weight="700">'+Math.round(pct*100)+'<tspan font-size="10" fill="#00e5ff">%</tspan></text>'+
      '<text x="50" y="62" text-anchor="middle" fill="#6c7891" font-family="JetBrains Mono, monospace" font-size="6" letter-spacing="1">'+label+'</text>';
  });
  // spark
  document.querySelectorAll('[data-spark]').forEach(function(el){
    var points=(el.dataset.sparkValues || el.dataset.spark || '4,8,6,5,9,7,10,12,11,16').split(',').map(Number);
    var W=140,H=30,maxv=Math.max.apply(null,points),step=W/(points.length-1);
    var pathD=points.map(function(v,i){return (i===0?'M':'L')+(i*step).toFixed(1)+','+(H-(v/maxv)*H).toFixed(1);}).join(' ');
    el.setAttribute('viewBox','0 0 '+W+' '+H);
    el.innerHTML='<path d="'+pathD+'" fill="none" stroke="#00e5ff" stroke-width="1.5" stroke-dasharray="200" stroke-dashoffset="200">'+
      '<animate attributeName="stroke-dashoffset" from="200" to="0" dur="1.4s" fill="freeze"/></path>';
  });
  // radial
  document.querySelectorAll('[data-radial]').forEach(function(el){
    var v=parseFloat(el.dataset.radial);var pct=Math.max(0,Math.min(100,v));
    var uid=Math.random().toString(36).slice(2,7);
    el.setAttribute('viewBox','0 0 120 120');var C=2*Math.PI*50;
    el.innerHTML='<defs><linearGradient id="rg-'+uid+'" x1="0" x2="1" y1="0" y2="1">'+
      '<stop offset="0%" stop-color="#00e5ff"/><stop offset="100%" stop-color="#7c5cff"/></linearGradient></defs>'+
      '<circle cx="60" cy="60" r="50" stroke="rgba(255,255,255,0.06)" stroke-width="8" fill="none"/>'+
      '<circle cx="60" cy="60" r="50" stroke="url(#rg-'+uid+')" stroke-width="8" fill="none" stroke-linecap="round" stroke-dasharray="'+C+'" stroke-dashoffset="'+C+'" transform="rotate(-90 60 60)">'+
      '<animate attributeName="stroke-dashoffset" from="'+C+'" to="'+(C-(C*pct/100))+'" dur="2s" fill="freeze"/></circle>'+
      '<text x="60" y="58" text-anchor="middle" fill="#e6edf7" font-family="Space Grotesk, Inter, sans-serif" font-size="22" font-weight="700">'+pct+'<tspan font-size="13" fill="#00e5ff">%</tspan></text>'+
      '<text x="60" y="74" text-anchor="middle" fill="#6c7891" font-family="JetBrains Mono, monospace" font-size="7" letter-spacing="1.5">'+(el.dataset.label||'')+'</text>';
  });

  // bars vertical
  document.querySelectorAll('[data-bars]').forEach(function(el){
    var values=(el.dataset.bars||'40,60,35,80,55,72,48,90,65,82,70,95').split(',').map(Number);
    var maxv=Math.max.apply(null,values);
    el.innerHTML=values.map(function(v,i){
      var h=(v/maxv)*100;
      return '<div class="bar bar-grow" style="height:'+h+'%; animation-delay:'+(i*60)+'ms"></div>';
    }).join('');
  });

  // worldmap dots
  document.querySelectorAll('[data-worldmap]').forEach(function(el){
    var dots=(el.dataset.worldmap||'').split('|').filter(Boolean);
    el.innerHTML=dots.map(function(d,i){
      var p=d.split(',');var x=p[0],y=p[1],c=p[2]||'#00e5ff';
      return '<circle cx="'+x+'" cy="'+y+'" r="2.5" fill="'+c+'" opacity="0">'+
        '<animate attributeName="opacity" from="0" to="0.9" begin="'+(i*0.1).toFixed(2)+'s" dur="0.4s" fill="freeze"/>'+
        '<animate attributeName="r" values="2.5;4;2.5" dur="3s" begin="'+(i*0.1).toFixed(2)+'s" repeatCount="indefinite"/></circle>';
    }).join('');
  });

  // horizontal bars
  document.querySelectorAll('[data-bars-h-values]').forEach(function(el){
    var values=(el.dataset.barsH||'').split(',').map(Number);
    var labels=(el.dataset.labels||'').split(',');
    el.innerHTML=values.map(function(v,i){
      var w=Math.max(0,Math.min(100,v));
      return '<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;font-family:JetBrains Mono,monospace;font-size:.78rem;">'+
        '<span style="width:90px;color:#aab4c8;">'+(labels[i]||'')+'</span>'+
        '<div style="flex:1;height:8px;background:rgba(255,255,255,0.05);border-radius:4px;overflow:hidden;">'+
          '<div class="h-bar-fill" data-w="'+w+'" style="height:100%;width:0;background:linear-gradient(90deg,#00e5ff,#7c5cff);border-radius:4px;transition:width 1.4s cubic-bezier(.16,1,.3,1) '+(i*80)+'ms;"></div>'+
        '</div>'+
        '<span style="width:50px;text-align:right;color:#00e5ff;">'+v+'%</span>'+
      '</div>';
    }).join('');
    requestAnimationFrame(function(){
      el.querySelectorAll('.h-bar-fill').forEach(function(bar){ bar.style.width=bar.dataset.w+'%'; });
    });
  });

  // radar
  document.querySelectorAll('[data-radar]').forEach(function(el){
    var values=(el.dataset.radar||'90,75,85,95,70').split(',').map(Number);
    var labels=(el.dataset.labels||'').split(',');
    var maxv=parseFloat(el.dataset.max||'100');
    var n=values.length;var cx=100,cy=100,r=70;
    var pts=values.map(function(v,i){
      var a=(-Math.PI/2)+(2*Math.PI*i/n);
      var rr=(v/maxv)*r;
      return [cx+Math.cos(a)*rr, cy+Math.sin(a)*rr];
    });
    var pathD=pts.map(function(p,i){return (i===0?'M':'L')+p[0].toFixed(1)+','+p[1].toFixed(1);}).join(' ')+' Z';
    var ringPts=Array.from({length:n},function(_,i){
      var a=(-Math.PI/2)+(2*Math.PI*i/n);
      return [cx+Math.cos(a)*r, cy+Math.sin(a)*r];
    });
    var rings=[0.25,0.5,0.75,1].map(function(s){
      var sp=ringPts.map(function(p){
        return [(cx+(p[0]-cx)*s).toFixed(1),(cy+(p[1]-cy)*s).toFixed(1)];
      });
      return sp.map(function(p,i){return (i===0?'M':'L')+p[0]+','+p[1];}).join(' ')+' Z';
    }).join(' ');
    var html='<polygon points="'+rings.replace(/Z/g,' ').replace(/M/g,'M').replace(/L/g,'L')+'" fill="none" stroke="rgba(0,229,255,0.10)" stroke-width="1"/>';
    ringPts.forEach(function(p){ html+='<line x1="'+cx+'" y1="'+cy+'" x2="'+p[0].toFixed(1)+'" y2="'+p[1].toFixed(1)+'" stroke="rgba(0,229,255,0.10)" stroke-width="1"/>'; });
    html+='<path d="'+pathD+'" fill="rgba(0,229,255,0.20)" stroke="#00e5ff" stroke-width="2" stroke-linejoin="round" opacity="0">'+
      '<animate attributeName="opacity" from="0" to="1" dur="1.2s" fill="freeze"/></path>';
    pts.forEach(function(p){ html+='<circle cx="'+p[0].toFixed(1)+'" cy="'+p[1].toFixed(1)+'" r="3" fill="#00e5ff"/>'; });
    labels.forEach(function(l,i){
      if(!l) return;
      var a=(-Math.PI/2)+(2*Math.PI*i/n);
      var lx=cx+Math.cos(a)*(r+18);var ly=cy+Math.sin(a)*(r+18);
      html+='<text x="'+lx.toFixed(1)+'" y="'+ly.toFixed(1)+'" text-anchor="middle" fill="#aab4c8" font-family="JetBrains Mono, monospace" font-size="9">'+l+'</text>';
    });
    el.setAttribute('viewBox','0 0 200 200');el.innerHTML=html;
  });

  // heatmap (data-heatmap: comma separated values count)
  document.querySelectorAll('[data-heatmap]').forEach(function(el){
    var values=(el.dataset.heatmap||'').split(',').map(Number);
    var cols=parseInt(el.dataset.cols||'7');var rows=Math.ceil(values.length/cols);
    var html='<div style="display:grid;grid-template-columns:repeat('+cols+',1fr);gap:4px;">';
    values.forEach(function(v,i){
      var intensity=Math.min(1,v/(el.dataset.max||100));
      var r=Math.round(0+intensity*0);var g=Math.round(229+intensity*26);var b=Math.round(255-0);
      var bg='rgba('+r+','+g+','+b+','+(0.1+intensity*0.85).toFixed(2)+')';
      html+='<div style="aspect-ratio:1;background:'+bg+';border-radius:4px;border:1px solid rgba(255,255,255,0.05);"></div>';
    });
    html+='</div>';
    el.innerHTML=html;
  });

})();
