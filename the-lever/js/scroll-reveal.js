(function() {
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) { if (e.isIntersecting) e.target.classList.add('reveal--show'); });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
  document.querySelectorAll('.reveal').forEach(function(el) { obs.observe(el); });

  // Footer lever tip animation
  var leverObs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) { if (e.isIntersecting) e.target.classList.add('lever-anim--tipped'); });
  }, { threshold: 0.5 });
  var lever = document.getElementById('footer-lever');
  if (lever) leverObs.observe(lever);
})();
