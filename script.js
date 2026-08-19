/**
 * SURAKSHA AI — Interactive Core Logic & Navigation Controller
 */

document.addEventListener('DOMContentLoaded', () => {
  // --- 1. THEME TOGGLE (DARK / LIGHT) ---
  const themeToggleBtn = document.getElementById('themeToggle');
  const htmlElement = document.documentElement;

  // Check saved preference or default to dark
  const savedTheme = localStorage.getItem('suraksha_theme') || 'dark';
  htmlElement.setAttribute('data-theme', savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = htmlElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      htmlElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('suraksha_theme', newTheme);
    });
  }

  // --- 2. STICKY NAVBAR SCROLL STATE ---
  const navbar = document.getElementById('mainNavbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      navbar?.classList.add('scrolled');
    } else {
      navbar?.classList.remove('scrolled');
    }
  });

  // --- 3. MOBILE DRAWER NAVIGATION ---
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const drawerCloseBtn = document.getElementById('drawerCloseBtn');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

  const toggleDrawer = (open) => {
    if (mobileDrawer) {
      if (open) {
        mobileDrawer.classList.add('open');
        document.body.style.overflow = 'hidden';
      } else {
        mobileDrawer.classList.remove('open');
        document.body.style.overflow = '';
      }
    }
  };

  hamburgerBtn?.addEventListener('click', () => toggleDrawer(true));
  drawerCloseBtn?.addEventListener('click', () => toggleDrawer(false));
  mobileDrawer?.addEventListener('click', (e) => {
    if (e.target === mobileDrawer) toggleDrawer(false);
  });
  mobileNavLinks.forEach(link => {
    link.addEventListener('click', () => toggleDrawer(false));
  });

  // --- 4. PARTICLE CANVAS ANIMATION ---
  const canvas = document.getElementById('particleCanvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    const colors = ['#8b5cf6', '#ec4899', '#06b6d4', '#3b82f6', '#10b981'];
    const particleCount = 45;
    const particles = Array.from({ length: particleCount }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r: Math.random() * 2 + 1,
      color: colors[Math.floor(Math.random() * colors.length)],
      alpha: Math.random() * 0.4 + 0.15
    }));

    function animateParticles() {
      ctx.clearRect(0, 0, width, height);
      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.fill();
      });

      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.hypot(dx, dy);
          if (dist < 110) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = particles[i].color;
            ctx.globalAlpha = (1 - dist / 110) * 0.12;
            ctx.lineWidth = 0.6;
            ctx.stroke();
          }
        }
      }
      requestAnimationFrame(animateParticles);
    }
    animateParticles();
  }

  // --- 5. QUICK SUGGESTION CHIPS & SEARCH BAR ---
  const destinationInput = document.getElementById('destinationInput');
  const chipItems = document.querySelectorAll('.chip-item');
  const findSafeRouteBtn = document.getElementById('findSafeRouteBtn');
  const useGpsBtn = document.getElementById('useGpsBtn');

  chipItems.forEach(chip => {
    chip.addEventListener('click', () => {
      const dest = chip.getAttribute('data-dest');
      if (destinationInput && dest) {
        destinationInput.value = dest;
        destinationInput.focus();
      }
    });
  });

  useGpsBtn?.addEventListener('click', () => {
    if (destinationInput) {
      destinationInput.value = "📍 Current GPS (Connaught Place, New Delhi)";
      destinationInput.style.color = "#a78bfa";
    }
  });

  findSafeRouteBtn?.addEventListener('click', () => {
    const dest = destinationInput?.value.trim();
    if (!dest) {
      destinationInput?.focus();
      destinationInput?.setAttribute('placeholder', '⚠️ Please enter a destination first!');
      setTimeout(() => {
        destinationInput?.setAttribute('placeholder', 'Where are you going? (e.g. Lajpat Nagar, Saket)');
      }, 2500);
      return;
    }
    // Smooth scroll to Safe Routes section
    document.getElementById('safe-routes')?.scrollIntoView({ behavior: 'smooth' });
  });

  // --- 6. AREA SELECTOR & CRIME DATA INTERACTION ---
  const areaSelect = document.getElementById('areaSelect');
  const timeRangeSelect = document.getElementById('timeRangeSelect');

  const areaDataMap = {
    'south-delhi': { low: 78, mod: 18, high: 4, theft: '24%', har: '7%', ass: '4%', oth: '12%', trend: '+14.2% Safe' },
    'bengaluru':   { low: 84, mod: 13, high: 3, theft: '18%', har: '5%', ass: '2%', oth: '9%', trend: '+18.5% Safe' },
    'mumbai':      { low: 82, mod: 15, high: 3, theft: '20%', har: '6%', ass: '3%', oth: '11%', trend: '+16.1% Safe' },
    'kolkata':     { low: 76, mod: 20, high: 4, theft: '22%', har: '8%', ass: '4%', oth: '14%', trend: '+11.8% Safe' }
  };

  function updateCrimePanel(areaKey) {
    const data = areaDataMap[areaKey] || areaDataMap['south-delhi'];
    const barFills = document.querySelectorAll('.crime-data-block .bar-fill');
    if (barFills.length >= 3) {
      barFills[0].style.width = `${data.low}%`;
      barFills[1].style.width = `${data.mod}%`;
      barFills[2].style.width = `${data.high}%`;
    }
    const catPcts = document.querySelectorAll('.cat-pct');
    if (catPcts.length >= 4) {
      catPcts[0].textContent = data.theft;
      catPcts[1].textContent = data.har;
      catPcts[2].textContent = data.ass;
      catPcts[3].textContent = data.oth;
    }
    const trendHl = document.querySelector('.trend-highlight');
    if (trendHl) trendHl.textContent = `Safety Index ${data.trend}`;
  }

  areaSelect?.addEventListener('change', (e) => updateCrimePanel(e.target.value));
  timeRangeSelect?.addEventListener('change', () => {
    updateCrimePanel(areaSelect?.value || 'south-delhi');
  });

  // --- 7. ROUTE CARD SELECTION LOGIC ---
  window.selectRoute = function(routeKey) {
    const cards = [
      document.getElementById('routeCardA'),
      document.getElementById('routeCardB'),
      document.getElementById('routeCardC')
    ];
    cards.forEach(c => c?.classList.remove('recommended-card'));

    const activeCard = document.getElementById(`routeCard${routeKey}`);
    if (activeCard) {
      activeCard.classList.add('recommended-card');
      activeCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  };

  // --- 8. SMART TRAVEL TIPS ROTATOR ---
  const safetyTips = [
    "“Before starting your journey, check the safety score and crime activity around your destination.”",
    "“Stick to primary illuminated arterial roads and avoid unverified shortcuts at night.”",
    "“Keep your live location sharing enabled with trusted contacts before entering isolated transit corridors.”",
    "“Use the 1-tap SOS Emergency Beacon if you ever feel uncomfortable or notice suspicious tracking.”",
    "“Look for Suraksha-verified safe havens and 24/7 police kiosks along your daily commute.”"
  ];
  let tipIndex = 0;
  const tipText = document.getElementById('tipText');
  const nextTipBtn = document.getElementById('nextTipBtn');

  if (nextTipBtn && tipText) {
    nextTipBtn.addEventListener('click', () => {
      tipIndex = (tipIndex + 1) % safetyTips.length;
      tipText.style.opacity = '0';
      setTimeout(() => {
        tipText.textContent = safetyTips[tipIndex];
        tipText.style.opacity = '1';
      }, 200);
    });
  }

  // --- 9. EMERGENCY SOS TRIGGER & MODAL ---
  const sosModal = document.getElementById('sosModal');
  const closeSosModalBtn = document.getElementById('closeSosModalBtn');
  const deactivateSosBtn = document.getElementById('deactivateSosBtn');
  const cancelPinInput = document.getElementById('cancelPinInput');
  const pinErrorMsg = document.getElementById('pinErrorMsg');

  const headerSosBtn = document.getElementById('headerSosBtn');
  const bigSosTriggerBtn = document.getElementById('bigSosTriggerBtn');
  const mobileSosActionBtn = document.getElementById('mobileSosActionBtn');
  const floatingSosBtn = document.getElementById('floatingSosBtn');

  let audioCtx = null;
  let sirenOsc = null;
  let sirenInterval = null;

  function startSirenSound() {
    try {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      sirenOsc = audioCtx.createOscillator();
      const gainNode = audioCtx.createGain();
      sirenOsc.type = 'sawtooth';
      gainNode.gain.setValueAtTime(0.18, audioCtx.currentTime);
      sirenOsc.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      sirenOsc.start();

      sirenInterval = setInterval(() => {
        if (!audioCtx) return;
        const now = audioCtx.currentTime;
        sirenOsc.frequency.setValueAtTime(450, now);
        sirenOsc.frequency.linearRampToValueAtTime(950, now + 0.35);
        sirenOsc.frequency.linearRampToValueAtTime(450, now + 0.7);
      }, 700);
    } catch (e) {
      console.log('Audio autoplay blocked or unsupported:', e);
    }
  }

  function stopSirenSound() {
    if (sirenInterval) clearInterval(sirenInterval);
    if (sirenOsc) {
      try { sirenOsc.stop(); } catch(e){}
      sirenOsc = null;
    }
  }

  function openSosModal() {
    if (sosModal) {
      sosModal.classList.add('active');
      startSirenSound();
      if (cancelPinInput) {
        cancelPinInput.value = '';
        cancelPinInput.focus();
      }
      if (pinErrorMsg) pinErrorMsg.textContent = '';
    }
  }

  function closeSosModal() {
    if (sosModal) {
      sosModal.classList.remove('active');
      stopSirenSound();
    }
  }

  [headerSosBtn, bigSosTriggerBtn, mobileSosActionBtn, floatingSosBtn].forEach(btn => {
    btn?.addEventListener('click', (e) => {
      e.preventDefault();
      openSosModal();
    });
  });

  closeSosModalBtn?.addEventListener('click', closeSosModal);
  sosModal?.addEventListener('click', (e) => {
    if (e.target === sosModal) closeSosModal();
  });

  deactivateSosBtn?.addEventListener('click', () => {
    const pin = cancelPinInput?.value.trim();
    if (pin === '1234') {
      closeSosModal();
      alert('✅ SOS Emergency Beacon deactivated successfully.');
    } else {
      if (pinErrorMsg) pinErrorMsg.textContent = '❌ Incorrect PIN. Enter 1234 to deactivate.';
    }
  });

  // --- 10. DIRECTIONS SIMULATOR ---
  window.getDirections = function(stationName) {
    alert(`📍 Routing to ${stationName}...\nOpening safest direct route in Suraksha Navigation.`);
    document.getElementById('safe-routes')?.scrollIntoView({ behavior: 'smooth' });
  };

  // --- 11. CHECK AREA SCORE BUTTON ---
  const checkAreaScoreBtn = document.getElementById('checkAreaScoreBtn');
  const gaugeScoreText = document.getElementById('gaugeScoreText');
  const gaugeProgressCircle = document.getElementById('gaugeProgressCircle');

  checkAreaScoreBtn?.addEventListener('click', () => {
    if (gaugeScoreText) {
      gaugeScoreText.textContent = '--';
      setTimeout(() => {
        gaugeScoreText.textContent = '94';
        if (gaugeProgressCircle) {
          gaugeProgressCircle.style.strokeDashoffset = '30.9'; // 94%
        }
      }, 400);
    }
  });

  // --- 12. START ROUTE BUTTON ---
  const startRouteBtn = document.getElementById('startRouteBtn');
  startRouteBtn?.addEventListener('click', () => {
    document.getElementById('safe-routes')?.scrollIntoView({ behavior: 'smooth' });
  });

  // --- 13. LOGIN PROMPT SIMULATOR ---
  const loginBtn = document.getElementById('loginBtn');
  const mobileLoginBtn = document.getElementById('mobileLoginBtn');
  const footerLoginLink = document.getElementById('footerLoginLink');

  [loginBtn, mobileLoginBtn, footerLoginLink].forEach(btn => {
    btn?.addEventListener('click', (e) => {
      e.preventDefault();
      alert('🔐 Suraksha AI Secure Portal\nDefault testing accounts:\n• Citizen: citizen / citizen123\n• Police: police / police123');
    });
  });
});
