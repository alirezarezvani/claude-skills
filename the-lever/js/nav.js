(function() {
  var btn = document.querySelector('.site-nav__hamburger');
  var menu = document.querySelector('.mobile-menu');
  if (btn && menu) {
    btn.addEventListener('click', function() {
      menu.classList.toggle('mobile-menu--open');
      btn.setAttribute('aria-expanded', menu.classList.contains('mobile-menu--open'));
    });
  }
})();
