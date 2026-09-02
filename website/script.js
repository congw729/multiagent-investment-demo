/* ============================================================
   US Equity Research Multi-Agent Teaching Demo — script.js
   Vanilla JS only: sticky-nav scrollspy + reveal-on-scroll.
   No frameworks, no CDN. Degrades gracefully if disabled.
   ============================================================ */
(function () {
  'use strict';

  var navLinks = Array.prototype.slice.call(document.querySelectorAll('nav a'));
  var sections = navLinks
    .map(function (a) {
      var id = a.getAttribute('href');
      return id && id.charAt(0) === '#' ? document.querySelector(id) : null;
    })
    .filter(function (s) { return s; });

  // Scrollspy: highlight the nav link of the section in view.
  function onScroll() {
    var pos = window.scrollY + 120;
    var current = null;
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].offsetTop <= pos) current = sections[i];
    }
    navLinks.forEach(function (a) {
      a.classList.remove('active');
      if (current && a.getAttribute('href') === '#' + current.id) {
        a.classList.add('active');
      }
    });
  }

  // Reveal-on-scroll: fade blocks in as they enter the viewport.
  var revealEls = document.querySelectorAll('.member, .tl-item, .scard, .scen, .sum, .del');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.style.opacity = '1';
          e.target.style.transform = 'translateY(0)';
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(function (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(18px)';
      el.style.transition = 'opacity .6s ease, transform .6s ease';
      io.observe(el);
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
