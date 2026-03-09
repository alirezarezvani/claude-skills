(function() {
  document.querySelectorAll('form').forEach(function(form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var input = form.querySelector('input[type="email"]');
      var btn = form.querySelector('button[type="submit"]');
      if (input && btn && input.value && input.checkValidity()) {
        // TODO: Replace with actual newsletter API endpoint
        var originalText = btn.textContent;
        btn.textContent = "You're in!";
        btn.style.background = '#4a6741';
        input.value = '';
        setTimeout(function() {
          btn.textContent = originalText;
          btn.style.background = '';
        }, 3000);
      }
    });
  });
})();
