(function(){ 'use strict';
  // 3D tilt for dashboard / hero visuals
  document.querySelectorAll('[data-tilt]').forEach(function(el){
    var rect, rx=0, ry=0;
    function onMove(e){
      rect=rect||el.getBoundingClientRect();
      var px=(e.clientX-rect.left)/rect.width-0.5;
      var py=(e.clientY-rect.top)/rect.height-0.5;
      ry=px*8; rx=-py*8;
      el.style.transform='rotateX('+rx+'deg) rotateY('+ry+'deg)';
    }
    function onLeave(){ el.style.transform='rotateX(2deg) rotateY(-6deg)'; }
    el.addEventListener('mousemove',onMove);
    el.addEventListener('mouseleave',onLeave);
    el.addEventListener('mouseenter',function(){ rect=el.getBoundingClientRect(); });
  });

  // Typing effect for elements with [data-typing]
  document.querySelectorAll('[data-typing]').forEach(function(el){
    var text=el.dataset.typing||el.textContent;
    el.textContent='';
    el.classList.add('cursor');
    var i=0;
    function tick(){
      if(i<=text.length){
        el.textContent=text.slice(0,i);
        i++;
        setTimeout(tick,30+Math.random()*40);
      } else {
        setTimeout(function(){ el.classList.remove('cursor'); },900);
      }
    }
    setTimeout(tick,200);
  });

  // Parallax blobs
  document.querySelectorAll('[data-parallax]').forEach(function(el){
    var strength=parseFloat(el.dataset.parallax||'30');
    window.addEventListener('scroll',function(){
      var r=el.getBoundingClientRect();
      var y=(window.innerHeight/2 - r.top - r.height/2) / window.innerHeight;
      el.style.transform='translate3d(0,'+(y*strength).toFixed(1)+'px,0)';
    },{passive:true});
  });

  // Cursor-follow glow on hover for cards
  document.querySelectorAll('.card, .service, .pillar, .adv-card, .news-card, .contact-card').forEach(function(card){
    card.addEventListener('mousemove',function(e){
      var r=card.getBoundingClientRect();
      card.style.setProperty('--mx',((e.clientX-r.left)/r.width*100).toFixed(1)+'%');
      card.style.setProperty('--my',((e.clientY-r.top)/r.height*100).toFixed(1)+'%');
    });
  });

})();