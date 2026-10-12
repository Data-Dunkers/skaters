// Data Skaters – Archetype Backgrounds
// Provides 6 distinct themed backgrounds for each archetype:
// 1. Playmaker: Arena floodlights & crystalline ice facets
// 2. Power Forward: Bold geometric athletic wedges & speed chevrons
// 3. Two-Way Forward: Deep arctic frozen lake with intricate cracked ice fissures
// 4. Speed Winger: Flowing aerodynamic wind-tunnel ribbons & electric neon accents
// 5. Sniper: Technical blueprint coordinate grid & precision targeting reticles
// 6. Defenseman: Glacial fortress ice wall & heavy defensive armor bastion plates

const ARCHETYPE_BACKGROUNDS = {
  'playmaker': `<svg class="ice-bg arch-bg-playmaker" width="1000" height="700" viewBox="0 0 1000 700" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="pm_iceBase" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#e8f2fb"/>
      <stop offset="50%" stop-color="#d2e5f4"/>
      <stop offset="100%" stop-color="#b7d4ec"/>
    </linearGradient>
    <radialGradient id="pm_spotGlow" cx="20%" cy="0%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.85"/>
      <stop offset="35%" stop-color="#d4ecfd" stop-opacity="0.45"/>
      <stop offset="70%" stop-color="#b2dbfc" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#b2dbfc" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="pm_beam1" x1="0" y1="0" x2="0.8" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.40"/>
      <stop offset="50%" stop-color="#d9eefa" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#b8defa" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="pm_beam2" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.32"/>
      <stop offset="60%" stop-color="#d9eefa" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#b8defa" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="pm_beam3" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.25"/>
      <stop offset="50%" stop-color="#cde7f8" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#cde7f8" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="pm_mountainGrad1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8bbbe2" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="#5591c8" stop-opacity="0.85"/>
    </linearGradient>
    <linearGradient id="pm_mountainGrad2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6ba6d8" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#2a6ca8" stop-opacity="0.95"/>
    </linearGradient>
  </defs>
  <rect width="1000" height="700" fill="url(#pm_iceBase)"/>
  <ellipse cx="140" cy="0" rx="340" ry="180" fill="url(#pm_spotGlow)"/>
  <ellipse cx="280" cy="-20" rx="260" ry="140" fill="url(#pm_spotGlow)" opacity="0.6"/>
  <polygon points="40,-20 180,-20 440,520 180,520" fill="url(#pm_beam1)"/>
  <polygon points="120,-20 280,-20 560,460 300,460" fill="url(#pm_beam2)"/>
  <polygon points="220,-20 360,-20 680,380 460,380" fill="url(#pm_beam3)"/>
  <g fill="#ffffff" opacity="0.85">
    <circle cx="80" cy="6" r="3.5"/>
    <circle cx="110" cy="5" r="3.5"/>
    <circle cx="140" cy="4" r="4"/>
    <circle cx="170" cy="4" r="4"/>
    <circle cx="200" cy="5" r="3.5"/>
    <circle cx="230" cy="6" r="3.5"/>
  </g>
  <polygon points="0,0 420,0 260,230 0,330" fill="#ffffff" opacity="0.38"/>
  <polygon points="420,0 640,0 520,170 330,150" fill="#ffffff" opacity="0.22"/>
  <polygon points="0,330 260,230 330,470 0,520" fill="#9fc6e6" opacity="0.30"/>
  <polygon points="700,0 1000,0 1000,260 820,150" fill="#ffffff" opacity="0.30"/>
  <polygon points="0,520 330,470 460,700 0,700" fill="#ffffff" opacity="0.28"/>
  <polygon points="520,170 820,150 760,420 560,380" fill="#8dbbe2" opacity="0.16"/>
  <polygon points="1000,260 1000,520 800,600 760,420" fill="#ffffff" opacity="0.24"/>
  <polygon points="480,700 580,630 640,650 710,580 770,610 840,540 910,570 960,520 1000,540 1000,700" fill="url(#pm_mountainGrad1)"/>
  <polygon points="540,700 630,640 700,660 760,610 830,635 890,575 950,615 1000,565 1000,700" fill="url(#pm_mountainGrad2)"/>
  <polygon points="620,700 710,650 780,670 850,620 920,650 970,610 1000,630 1000,700" fill="#205c96" opacity="0.75"/>
  <polygon points="840,540 855,565 825,565" fill="#ffffff" opacity="0.6"/>
  <polygon points="960,520 975,545 948,545" fill="#ffffff" opacity="0.6"/>
  <polygon points="710,580 722,600 700,600" fill="#ffffff" opacity="0.5"/>
  <polygon points="890,575 905,595 878,595" fill="#ffffff" opacity="0.55"/>
  <polygon points="0,640 330,700 0,700" fill="#1565b0"/>
  <polygon points="0,672 180,700 0,700" fill="#0a3d8f"/>
  <polygon points="470,700 640,650 1000,700" fill="#2a85d6" opacity="0.9"/>
  <polygon points="610,700 860,664 1000,684 1000,700" fill="#0a3d8f"/>
  <polygon points="800,700 930,640 1000,650 1000,700" fill="#1670c4" opacity="0.85"/>
</svg>`,

  'power-forward': `<svg class="ice-bg arch-bg-power-forward" width="1000" height="700" viewBox="0 0 1000 700" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="pf_base" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="45%" stop-color="#f2f7fc"/>
      <stop offset="100%" stop-color="#dceaf6"/>
    </linearGradient>
    <linearGradient id="pf_cyanGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#008ecc"/>
    </linearGradient>
    <linearGradient id="pf_blueGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1e78cc"/>
      <stop offset="100%" stop-color="#0e4f96"/>
    </linearGradient>
    <linearGradient id="pf_navyGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0e3d82"/>
      <stop offset="100%" stop-color="#071e47"/>
    </linearGradient>
  </defs>
  <rect width="1000" height="700" fill="url(#pf_base)"/>
  <polygon points="-50,180 320,-40 390,-40 -20,220" fill="#cfe2f5" opacity="0.4"/>
  <polygon points="120,720 720,240 780,240 180,720" fill="#d8e8f7" opacity="0.35"/>
  <polygon points="560,720 1020,360 1050,360 590,720" fill="#c2ddf4" opacity="0.25"/>
  <polygon points="0,0 270,0 240,14 0,14" fill="url(#pf_navyGrad)"/>
  <polygon points="0,14 240,14 220,19 0,19" fill="url(#pf_cyanGrad)"/>
  <polygon points="250,0 430,0 380,24 220,14" fill="url(#pf_blueGrad)" opacity="0.9"/>
  <polygon points="340,0 510,0 465,18 310,12" fill="url(#pf_cyanGrad)" opacity="0.75"/>
  <polygon points="0,116 260,116 285,126 0,126" fill="#d2e7f7" opacity="0.7"/>
  <polygon points="60,120 220,120 235,124 80,124" fill="url(#pf_cyanGrad)" opacity="0.6"/>
  <polygon points="305,48 350,25 365,30 325,53" fill="#00a4e4" opacity="0.65"/>
  <polygon points="345,62 380,44 395,49 360,67" fill="#1670c4" opacity="0.5"/>
  <polygon points="0,310 64,350 64,420 0,460" fill="url(#pf_blueGrad)"/>
  <polygon points="0,355 45,380 45,435 0,470" fill="url(#pf_navyGrad)"/>
  <polygon points="0,480 30,495 30,530 0,550" fill="#00a4e4" opacity="0.75"/>
  <polygon points="0,540 120,470 210,540 0,680" fill="url(#pf_blueGrad)"/>
  <polygon points="0,640 160,540 280,630 180,700 0,700" fill="url(#pf_navyGrad)"/>
  <polygon points="0,685 340,510 400,545 70,700 0,700" fill="url(#pf_cyanGrad)"/>
  <polygon points="50,700 280,580 320,600 120,700" fill="#ffffff" opacity="0.5"/>
  <polygon points="30,700 240,600 480,700" fill="url(#pf_blueGrad)" opacity="0.5"/>
  <polygon points="160,690 190,690 140,700 110,700" fill="#ffffff"/>
  <polygon points="210,690 240,690 190,700 160,700" fill="#ffffff"/>
  <polygon points="260,690 290,690 240,700 210,700" fill="#ffffff"/>
  <polygon points="800,0 1000,0 1000,90 910,35" fill="url(#pf_blueGrad)"/>
  <polygon points="890,0 1000,0 1000,55" fill="url(#pf_navyGrad)"/>
  <polygon points="930,30 1000,65 1000,140 860,65" fill="url(#pf_cyanGrad)"/>
  <polygon points="730,0 840,0 790,32 700,32" fill="url(#pf_cyanGrad)" opacity="0.7"/>
  <polygon points="680,0 750,0 710,22 650,22" fill="#0e4f96" opacity="0.5"/>
  <polygon points="820,55 880,30 900,38 840,63" fill="#ffffff" opacity="0.65"/>
  <polygon points="870,95 930,68 950,76 890,103" fill="#1670c4" opacity="0.6"/>
  <polygon points="740,700 1000,530 1000,600 840,700" fill="url(#pf_cyanGrad)"/>
  <polygon points="820,700 1000,575 1000,665 910,700" fill="url(#pf_blueGrad)"/>
  <polygon points="890,700 1000,635 1000,700" fill="url(#pf_navyGrad)"/>
  <polygon points="960,670 1000,670 1000,700 930,700" fill="#00a4e4"/>
</svg>`,

  'two-way-forward': `<svg class="ice-bg arch-bg-two-way-forward" width="1000" height="700" viewBox="0 0 1000 700" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="tw_base" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#edf6fd"/>
      <stop offset="40%" stop-color="#d6e8f8"/>
      <stop offset="80%" stop-color="#b6d7f2"/>
      <stop offset="100%" stop-color="#9fc7ea"/>
    </linearGradient>
    <linearGradient id="tw_shelfGrad1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#145da0"/>
      <stop offset="100%" stop-color="#072b5c"/>
    </linearGradient>
    <linearGradient id="tw_shelfGrad2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#217ec7"/>
      <stop offset="100%" stop-color="#0b407d"/>
    </linearGradient>
  </defs>
  <rect width="1000" height="700" fill="url(#tw_base)"/>
  <polygon points="0,0 380,0 210,180 0,260" fill="#ffffff" opacity="0.45"/>
  <polygon points="380,0 720,0 600,160 210,180" fill="#cfe5f7" opacity="0.35"/>
  <polygon points="720,0 1000,0 1000,220 780,140" fill="#ffffff" opacity="0.38"/>
  <polygon points="0,260 210,180 290,420 0,480" fill="#8cbde5" opacity="0.25"/>
  <polygon points="210,180 600,160 520,380 290,420" fill="#ffffff" opacity="0.28"/>
  <polygon points="600,160 780,140 850,380 520,380" fill="#7faedb" opacity="0.20"/>
  <polygon points="780,140 1000,220 1000,480 850,380" fill="#ffffff" opacity="0.32"/>
  <polygon points="0,480 290,420 410,650 0,650" fill="#9fc7ea" opacity="0.28"/>
  <polygon points="290,420 520,380 580,620 410,650" fill="#ffffff" opacity="0.25"/>
  <polygon points="520,380 850,380 790,620 580,620" fill="#6b9ecc" opacity="0.18"/>
  <polygon points="850,380 1000,480 1000,640 790,620" fill="#ffffff" opacity="0.30"/>
  <g fill="#ffffff" opacity="0.6">
    <polygon points="50,0 65,35 50,75 35,35"/>
    <polygon points="12,40 50,55 85,40 50,28"/>
    <polygon points="22,18 78,72 70,78 18,22"/>
    <polygon points="75,20 20,74 25,80 80,25"/>
    <polygon points="180,0 190,28 180,55 170,28"/>
    <polygon points="155,28 180,38 205,28 180,18"/>
    <polygon points="880,0 892,30 880,60 868,30"/>
    <polygon points="850,30 880,40 910,30 880,20"/>
    <polygon points="950,0 960,35 950,70 940,35"/>
    <polygon points="915,35 950,45 985,35 950,25"/>
    <polygon points="0,150 30,160 60,150 30,140"/>
    <polygon points="30,120 40,150 30,180 20,150"/>
  </g>
  <g fill="none" stroke="#0e3d7a" opacity="0.35" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -10,210 L 60,225 L 115,195 L 175,235 L 240,210 L 310,260 L 390,230 L 460,280 L 540,245 L 630,310 L 710,280 L 790,340 L 870,315 L 945,365 L 1010,340" stroke-width="3"/>
    <path d="M 460,-10 L 485,75 L 455,140 L 510,205 L 475,260 L 530,340 L 495,420 L 550,510 L 515,590" stroke-width="2.5"/>
    <path d="M -10,480 L 75,460 L 130,500 L 210,465 L 285,520 L 360,490 L 440,545" stroke-width="2.5"/>
    <path d="M 720,-10 L 750,80 L 715,145 L 780,220 L 850,250 L 920,225 L 1010,270" stroke-width="2.5"/>
  </g>
  <g fill="none" stroke="#ffffff" opacity="0.9" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -10,210 L 60,225 L 115,195 L 175,235 L 240,210 L 310,260 L 390,230 L 460,280 L 540,245 L 630,310 L 710,280 L 790,340 L 870,315 L 945,365 L 1010,340" stroke-width="1.8"/>
    <path d="M 460,-10 L 485,75 L 455,140 L 510,205 L 475,260 L 530,340 L 495,420 L 550,510 L 515,590" stroke-width="1.6"/>
    <path d="M -10,480 L 75,460 L 130,500 L 210,465 L 285,520 L 360,490 L 440,545" stroke-width="1.6"/>
    <path d="M 720,-10 L 750,80 L 715,145 L 780,220 L 850,250 L 920,225 L 1010,270" stroke-width="1.6"/>
  </g>
  <g fill="none" stroke="#e0f2fe" opacity="0.75" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.1">
    <path d="M 115,195 L 145,150 L 180,165"/>
    <path d="M 175,235 L 160,280 L 195,310"/>
    <path d="M 310,260 L 335,315 L 310,350"/>
    <path d="M 390,230 L 420,180 L 460,195"/>
    <path d="M 630,310 L 660,265 L 700,280"/>
    <path d="M 710,280 L 690,335 L 730,370"/>
    <path d="M 790,340 L 830,385 L 815,430"/>
    <path d="M 870,315 L 890,270 L 935,285"/>
    <path d="M 485,75 L 530,55 L 565,80"/>
    <path d="M 455,140 L 410,120 L 380,145"/>
    <path d="M 510,205 L 555,190 L 590,220"/>
    <path d="M 530,340 L 580,360 L 610,335"/>
    <path d="M 495,420 L 450,445 L 425,420"/>
    <path d="M 0,90 L 45,110 L 80,85 L 115,120"/>
    <path d="M 0,340 L 55,320 L 90,355 L 140,330"/>
    <path d="M 210,465 L 190,420 L 230,390"/>
    <path d="M 1000,120 L 950,140 L 920,110 L 870,135"/>
    <path d="M 1000,450 L 945,430 L 910,470 L 855,445"/>
  </g>
  <polygon points="0,600 90,625 180,595 290,640 410,605 520,645 640,610 760,650 880,615 1000,645 1000,700 0,700" fill="url(#tw_shelfGrad1)"/>
  <polygon points="0,640 120,660 230,635 340,670 470,640 590,675 720,645 840,680 950,650 1000,670 1000,700 0,700" fill="url(#tw_shelfGrad2)"/>
  <polygon points="0,670 140,685 280,665 430,690 570,670 710,695 860,675 1000,690 1000,700 0,700" fill="#041a38"/>
  <polyline points="0,600 90,625 180,595 290,640 410,605 520,645 640,610 760,650 880,615 1000,645" fill="none" stroke="#ffffff" stroke-width="2.2" opacity="0.85"/>
  <polyline points="0,640 120,660 230,635 340,670 470,640 590,675 720,645 840,680 950,650 1000,670" fill="none" stroke="#8ec5f5" stroke-width="1.5" opacity="0.7"/>
</svg>`,

  'speed-winger': `<svg class="ice-bg arch-bg-speed-winger" width="1000" height="700" viewBox="0 0 1000 700" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sw_base" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="40%" stop-color="#f8fafc"/>
      <stop offset="75%" stop-color="#edf4fc"/>
      <stop offset="100%" stop-color="#e0eefb"/>
    </linearGradient>
    <linearGradient id="sw_ribbon1" x1="0" y1="0" x2="1" y2="0.8">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.35"/>
      <stop offset="45%" stop-color="#818cf8" stop-opacity="0.25"/>
      <stop offset="85%" stop-color="#c084fc" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#f472b6" stop-opacity="0.18"/>
    </linearGradient>
    <linearGradient id="sw_ribbon2" x1="0.2" y1="1" x2="0.9" y2="0">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.30"/>
      <stop offset="50%" stop-color="#6366f1" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0.15"/>
    </linearGradient>
    <linearGradient id="sw_ribbon3" x1="0" y1="0.5" x2="1" y2="0.5">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0"/>
      <stop offset="30%" stop-color="#38bdf8" stop-opacity="0.25"/>
      <stop offset="70%" stop-color="#a855f7" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#f43f5e" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sw_accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#06b6d4"/>
      <stop offset="50%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
    <radialGradient id="sw_vaporGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#c4b5fd" stop-opacity="0.40"/>
      <stop offset="50%" stop-color="#bae6fd" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#bae6fd" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1000" height="700" fill="url(#sw_base)"/>
  <circle cx="20" cy="320" r="180" fill="url(#sw_vaporGlow)"/>
  <circle cx="240" cy="80" r="160" fill="url(#sw_vaporGlow)" opacity="0.6"/>
  <circle cx="950" cy="620" r="220" fill="url(#sw_vaporGlow)" opacity="0.5"/>
  <path d="M -60,180 C 140,80 260,260 440,160 C 580,80 720,130 860,60 C 940,20 1020,40 1060,-10 L 1060,50 C 980,100 880,80 780,140 C 620,230 500,160 380,240 C 220,340 100,180 -60,250 Z" fill="url(#sw_ribbon1)"/>
  <path d="M -50,560 C 120,480 220,620 400,520 C 560,430 700,480 840,380 C 940,310 1010,340 1060,280 L 1060,340 C 980,410 900,380 800,450 C 640,560 520,500 360,600 C 200,700 80,540 -50,630 Z" fill="url(#sw_ribbon2)"/>
  <path d="M 0,380 C 200,300 350,440 550,360 C 720,290 850,330 1000,260 L 1000,310 C 820,390 700,350 520,430 C 320,510 180,370 0,440 Z" fill="url(#sw_ribbon3)"/>
  <g fill="none" stroke-linecap="round">
    <path d="M -20,130 C 180,50 320,210 500,120 C 660,40 820,90 980,30" stroke="#38bdf8" stroke-width="2" opacity="0.65" stroke-dasharray="80 15 30 15"/>
    <path d="M 20,155 C 200,85 340,230 520,145 C 680,70 840,115 1000,55" stroke="#818cf8" stroke-width="1.5" opacity="0.55" stroke-dasharray="120 20 50 20"/>
    <path d="M -10,180 C 160,110 300,255 480,170 C 640,95 800,140 960,80" stroke="#c084fc" stroke-width="1.2" opacity="0.5" stroke-dasharray="60 25 100 25"/>
    <path d="M -30,500 C 150,420 280,560 480,460 C 660,370 820,420 1020,330" stroke="#00b4d8" stroke-width="2.2" opacity="0.6" stroke-dasharray="140 30 40 20"/>
    <path d="M 0,530 C 170,455 300,585 500,490 C 680,405 840,450 1040,365" stroke="#a78bfa" stroke-width="1.6" opacity="0.55" stroke-dasharray="90 20 60 20"/>
    <path d="M -20,560 C 140,490 270,615 470,520 C 650,435 810,480 1010,400" stroke="#f472b6" stroke-width="1.3" opacity="0.45" stroke-dasharray="160 30 50 30"/>
    <line x1="80" y1="28" x2="340" y2="28" stroke="#38bdf8" stroke-width="1" opacity="0.45" stroke-dasharray="40 10 20 10"/>
    <line x1="140" y1="42" x2="480" y2="42" stroke="#818cf8" stroke-width="0.8" opacity="0.4" stroke-dasharray="70 15 35 15"/>
    <line x1="600" y1="18" x2="880" y2="18" stroke="#a855f7" stroke-width="1" opacity="0.4" stroke-dasharray="50 12 25 12"/>
  </g>
  <polyline points="30,70 10,70 10,120" fill="none" stroke="#38bdf8" stroke-width="1.5" opacity="0.6"/>
</svg>`,

  'sniper': `<svg class="ice-bg arch-bg-sniper" width="1000" height="700" viewBox="0 0 1000 700" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="sn_minorGrid" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#1670c4" stroke-width="0.75" opacity="0.22"/>
    </pattern>
    <pattern id="sn_majorGrid" width="100" height="100" patternUnits="userSpaceOnUse">
      <rect width="100" height="100" fill="url(#sn_minorGrid)"/>
      <path d="M 100 0 L 0 0 0 100" fill="none" stroke="#1670c4" stroke-width="1.3" opacity="0.45"/>
    </pattern>
    <linearGradient id="sn_base" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f8fbff"/>
      <stop offset="50%" stop-color="#eff6fc"/>
      <stop offset="100%" stop-color="#e2eef9"/>
    </linearGradient>
  </defs>
  <rect width="1000" height="700" fill="url(#sn_base)"/>
  <rect width="1000" height="700" fill="url(#sn_majorGrid)"/>
  <g stroke="#0a3d8f" stroke-width="1.2" opacity="0.7">
    <path d="M 96,100 L 104,100 M 100,96 L 100,104"/>
    <path d="M 196,100 L 204,100 M 200,96 L 200,104"/>
    <path d="M 296,100 L 304,100 M 300,96 L 300,104"/>
    <path d="M 396,100 L 404,100 M 400,96 L 400,104"/>
    <path d="M 696,100 L 704,100 M 700,96 L 700,104"/>
    <path d="M 796,100 L 804,100 M 800,96 L 800,104"/>
    <path d="M 896,100 L 904,100 M 900,96 L 900,104"/>
    <path d="M 96,300 L 104,300 M 100,296 L 100,304"/>
    <path d="M 896,300 L 904,300 M 900,296 L 900,304"/>
    <path d="M 96,500 L 104,500 M 100,496 L 100,504"/>
    <path d="M 696,500 L 704,500 M 700,496 L 700,504"/>
    <path d="M 796,500 L 804,500 M 800,496 L 800,504"/>
    <path d="M 896,500 L 904,500 M 900,496 L 900,504"/>
  </g>
  <g transform="translate(800, 180)" stroke="#1670c4" fill="none">
    <circle cx="0" cy="0" r="28" stroke-width="1.2" opacity="0.6"/>
    <circle cx="0" cy="0" r="58" stroke-width="1" stroke-dasharray="4 4" opacity="0.5"/>
    <circle cx="0" cy="0" r="88" stroke-width="1.4" opacity="0.65"/>
    <circle cx="0" cy="0" r="118" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.4"/>
    <line x1="-130" y1="0" x2="-35" y2="0" stroke-width="1.5" stroke="#0a3d8f"/>
    <line x1="35" y1="0" x2="130" y2="0" stroke-width="1.5" stroke="#0a3d8f"/>
    <line x1="0" y1="-130" x2="0" y2="-35" stroke-width="1.5" stroke="#0a3d8f"/>
    <line x1="0" y1="35" x2="0" y2="130" stroke-width="1.5" stroke="#0a3d8f"/>
    <line x1="-70" y1="-4" x2="-70" y2="4" stroke-width="1"/>
    <line x1="-100" y1="-4" x2="-100" y2="4" stroke-width="1"/>
    <line x1="70" y1="-4" x2="70" y2="4" stroke-width="1"/>
    <line x1="100" y1="-4" x2="100" y2="4" stroke-width="1"/>
    <line x1="-4" y1="-70" x2="4" y2="-70" stroke-width="1"/>
    <line x1="-4" y1="-100" x2="4" y2="-100" stroke-width="1"/>
    <line x1="-4" y1="70" x2="4" y2="70" stroke-width="1"/>
    <line x1="-4" y1="100" x2="4" y2="100" stroke-width="1"/>
    <line x1="-62" y1="-62" x2="-52" y2="-52" stroke-width="1.2"/>
    <line x1="52" y1="-52" x2="62" y2="-62" stroke-width="1.2"/>
    <line x1="-62" y1="62" x2="-52" y2="52" stroke-width="1.2"/>
    <line x1="52" y1="52" x2="62" y2="62" stroke-width="1.2"/>
  </g>
  <g transform="translate(180, 580)" stroke="#1670c4" fill="none" opacity="0.5">
    <circle cx="0" cy="0" r="35" stroke-width="1"/>
    <circle cx="0" cy="0" r="65" stroke-width="0.8" stroke-dasharray="3 3"/>
    <line x1="-75" y1="0" x2="75" y2="0" stroke-width="1"/>
    <line x1="0" y1="-75" x2="0" y2="75" stroke-width="1"/>
  </g>
</svg>`,

  'defenseman': `<svg class="ice-bg arch-bg-defenseman" width="1000" height="700" viewBox="0 0 1000 700" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="df_base" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#eaf3fa"/>
      <stop offset="45%" stop-color="#cfe4f5"/>
      <stop offset="100%" stop-color="#a6cdec"/>
    </linearGradient>
    <linearGradient id="df_plateNavy" x1="0" y1="0" x2="0.8" y2="1">
      <stop offset="0%" stop-color="#0a2a5c"/>
      <stop offset="100%" stop-color="#04142b"/>
    </linearGradient>
    <linearGradient id="df_plateBlue" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0%" stop-color="#1e78cc"/>
      <stop offset="100%" stop-color="#0e4380"/>
    </linearGradient>
    <linearGradient id="df_plateCyan" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00a4e4"/>
      <stop offset="100%" stop-color="#38bdf8"/>
    </linearGradient>
  </defs>
  <rect width="1000" height="700" fill="url(#df_base)"/>
  <polygon points="0,0 360,0 240,240 0,310" fill="#ffffff" opacity="0.40"/>
  <polygon points="360,0 680,0 560,200 240,240" fill="#c3e0f7" opacity="0.32"/>
  <polygon points="680,0 1000,0 1000,280 820,180" fill="#ffffff" opacity="0.38"/>
  <polygon points="0,310 240,240 310,480 0,550" fill="#8cbde5" opacity="0.28"/>
  <polygon points="240,240 560,200 480,440 310,480" fill="#ffffff" opacity="0.22"/>
  <polygon points="560,200 820,180 780,440 480,440" fill="#7faedb" opacity="0.24"/>
  <polygon points="820,180 1000,280 1000,520 780,440" fill="#ffffff" opacity="0.30"/>
  <g fill="#ffffff" opacity="0.65">
    <polygon points="0,0 180,0 130,45 70,25 35,60 0,45"/>
    <polygon points="170,0 340,0 290,40 210,55 160,30"/>
    <polygon points="640,0 840,0 800,45 720,25 670,50"/>
    <polygon points="830,0 1000,0 1000,70 940,45 880,60"/>
    <polygon points="0,180 40,210 20,245 0,230"/>
    <polygon points="0,390 35,415 15,445 0,435"/>
  </g>
  <g fill="none" stroke="#ffffff" opacity="0.75" stroke-linecap="round" stroke-linejoin="round">
    <path d="M 0,280 L 50,295 L 90,270 L 140,305 L 200,280 L 250,320" stroke-width="1.8"/>
    <path d="M 780,140 L 820,180 L 870,165 L 930,210 L 1000,190" stroke-width="1.8"/>
    <path d="M 520,0 L 540,65 L 515,120 L 550,170" stroke-width="1.6"/>
  </g>
  <polygon points="0,670 190,670 290,570 510,570 570,630 790,630 840,575 1000,575 1000,700 0,700" fill="url(#df_plateNavy)"/>
  <polygon points="0,685 170,685 260,590 490,590 550,650 770,650 820,595 1000,595 1000,700 0,700" fill="url(#df_plateBlue)"/>
  <polygon points="260,590 490,590 500,596 268,596" fill="url(#df_plateCyan)"/>
  <polygon points="820,595 1000,595 1000,601 828,601" fill="url(#df_plateCyan)"/>
  <polygon points="550,650 770,650 778,655 558,655" fill="url(#df_plateCyan)"/>
  <polygon points="410,700 580,575 640,575 470,700" fill="url(#df_plateCyan)" opacity="0.9"/>
  <polygon points="470,700 640,575 730,575 560,700" fill="url(#df_plateNavy)"/>
  <polygon points="560,700 730,575 800,575 630,700" fill="url(#df_plateBlue)"/>
  <polygon points="880,700 1000,590 1000,650 940,700" fill="url(#df_plateCyan)"/>
  <polygon points="930,700 1000,630 1000,700 870,700" fill="url(#df_plateNavy)"/>
  <polygon points="0,640 100,560 160,560 0,700" fill="url(#df_plateBlue)" opacity="0.65"/>
  <polygon points="0,690 180,690 130,700 0,700" fill="#ffffff" opacity="0.4"/>
  <line x1="290" y1="570" x2="510" y2="570" stroke="#ffffff" stroke-width="1.5" opacity="0.75"/>
  <line x1="840" y1="575" x2="1000" y2="575" stroke="#ffffff" stroke-width="1.5" opacity="0.75"/>
  <line x1="570" y1="630" x2="790" y2="630" stroke="#ffffff" stroke-width="1.5" opacity="0.75"/>
</svg>`
};

function normalizeArchetype(arch) {
  if (!arch) return 'playmaker';
  const s = String(arch).toLowerCase().replace(/[^a-z0-9]/g, '');
  if (s.includes('sniper')) return 'sniper';
  if (s.includes('speed') || s.includes('winger')) return 'speed-winger';
  if (s.includes('playmaker')) return 'playmaker';
  if (s.includes('defense') || s.includes('defence')) return 'defenseman';
  if (s.includes('power')) return 'power-forward';
  if (s.includes('two') || s.includes('twoway')) return 'two-way-forward';
  return 'playmaker';
}

function getArchetypeBackgroundSvg(archetype) {
  const key = normalizeArchetype(archetype);
  return ARCHETYPE_BACKGROUNDS[key] || ARCHETYPE_BACKGROUNDS['playmaker'];
}
