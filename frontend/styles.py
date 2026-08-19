# -*- coding: utf-8 -*-
# ===============================================================================
# Suraksha Safety Platform -- Master Style System
# Expert UI/UX Design: Glassmorphism + Neon + Particle Canvas + Animations
# ===============================================================================

DARK_THEME_CSS = """
<style>
/* -- GOOGLE FONTS ----------------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* -- CSS CUSTOM PROPERTIES -------------------------------------------------- */
:root {
  --clr-bg:       #05010f;
  --clr-bg2:      #0a0520;
  --clr-surface:  rgba(255,255,255,0.035);
  --clr-border:   rgba(255,255,255,0.08);
  --clr-purple:   #8b5cf6;
  --clr-pink:     #ec4899;
  --clr-cyan:     #06b6d4;
  --clr-blue:     #3b82f6;
  --clr-green:    #10b981;
  --clr-amber:    #f59e0b;
  --clr-red:      #ef4444;
  --clr-text:     #f1f5f9;
  --clr-muted:    #94a3b8;
  --glow-purple:  0 0 30px rgba(139,92,246,0.4);
  --glow-pink:    0 0 30px rgba(236,72,153,0.4);
  --glow-cyan:    0 0 30px rgba(6,182,212,0.4);
  --radius-lg:    20px;
  --radius-xl:    28px;
  --blur:         backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
}

/* -- GLOBAL RESET & BASE ---------------------------------------------------- */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
  background: var(--clr-bg) !important;
  font-family: 'Inter', sans-serif !important;
  color: var(--clr-text) !important;
  overflow-x: hidden !important;
}

/* Animated gradient background mesh */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%,  rgba(139,92,246,0.18) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%,  rgba(6,182,212,0.14) 0%,  transparent 55%),
    radial-gradient(ellipse 70% 60% at 50% 50%,  rgba(236,72,153,0.08) 0%, transparent 65%),
    radial-gradient(ellipse 90% 80% at 10% 90%,  rgba(59,130,246,0.10) 0%, transparent 60%);
  animation: meshDrift 18s ease-in-out infinite alternate;
  pointer-events: none;
  z-index: 0;
}

@keyframes meshDrift {
  0%   { transform: scale(1)   rotate(0deg); }
  50%  { transform: scale(1.08) rotate(1.5deg); }
  100% { transform: scale(1.04) rotate(-1deg); }
}

/* Floating orbs */
[data-testid="stAppViewContainer"]::after {
  content: '';
  position: fixed;
  width: 600px; height: 600px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%);
  top: -200px; right: -200px;
  animation: orbFloat 12s ease-in-out infinite;
  pointer-events: none;
  z-index: 0;
}

@keyframes orbFloat {
  0%, 100% { transform: translateY(0px)  translateX(0px); }
  33%       { transform: translateY(40px) translateX(-30px); }
  66%       { transform: translateY(-25px) translateX(20px); }
}

/* -- STREAMLIT HEADER ------------------------------------------------------- */
[data-testid="stHeader"] {
  background: rgba(5,1,15,0.7) !important;
  backdrop-filter: blur(24px) !important;
  -webkit-backdrop-filter: blur(24px) !important;
  border-bottom: 1px solid rgba(139,92,246,0.15) !important;
  box-shadow: 0 1px 0 rgba(139,92,246,0.1) !important;
}

/* -- SIDEBAR ---------------------------------------------------------------- */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(10,5,32,0.98) 0%, rgba(5,1,15,0.98) 100%) !important;
  border-right: 1px solid rgba(139,92,246,0.15) !important;
  backdrop-filter: blur(20px) !important;
}

/* -- GLASS CARD ------------------------------------------------------------- */
.glass-card {
  background: rgba(255,255,255,0.04);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255,255,255,0.09);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow:
    0 8px 32px rgba(0,0,0,0.4),
    inset 0 1px 0 rgba(255,255,255,0.07);
  padding: 24px;
  margin-bottom: 20px;
  transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 60%);
  pointer-events: none;
}

.glass-card:hover {
  border-color: rgba(139,92,246,0.35);
  box-shadow:
    0 16px 48px rgba(0,0,0,0.5),
    0 0 0 1px rgba(139,92,246,0.2),
    var(--glow-purple),
    inset 0 1px 0 rgba(255,255,255,0.1);
  transform: translateY(-4px) scale(1.005);
}

/* -- GLOW TITLE ------------------------------------------------------------- */
.glow-title {
  font-family: 'Outfit', sans-serif !important;
  font-weight: 800 !important;
  background: linear-gradient(135deg, #a78bfa 0%, #ec4899 45%, #06b6d4 100%);
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  filter: drop-shadow(0 0 20px rgba(139,92,246,0.5));
  animation: titleShimmer 4s ease-in-out infinite;
  background-size: 200% 200%;
}

@keyframes titleShimmer {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* -- NAVBAR BRAND ----------------------------------------------------------- */
.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav-logo-ring {
  width: 48px; height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6, #ec4899, #06b6d4);
  padding: 2px;
  animation: logoSpin 8s linear infinite;
  box-shadow: 0 0 20px rgba(139,92,246,0.5), 0 0 40px rgba(236,72,153,0.3);
}

@keyframes logoSpin {
  0%   { box-shadow: 0 0 20px rgba(139,92,246,0.5), 0 0 40px rgba(236,72,153,0.2); }
  33%  { box-shadow: 0 0 25px rgba(236,72,153,0.6), 0 0 50px rgba(6,182,212,0.3); }
  66%  { box-shadow: 0 0 20px rgba(6,182,212,0.5), 0 0 40px rgba(139,92,246,0.3); }
  100% { box-shadow: 0 0 20px rgba(139,92,246,0.5), 0 0 40px rgba(236,72,153,0.2); }
}

.nav-title {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.5rem;
  background: linear-gradient(90deg, #a78bfa, #ec4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
}

/* -- HERO SECTION ----------------------------------------------------------- */
.hero-section {
  text-align: center;
  padding: 60px 20px 40px;
  position: relative;
  z-index: 1;
}

.hero-logo-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
}

.hero-logo-container {
  position: relative;
  width: 140px; height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Outer rotating ring */
.hero-logo-container::before {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  background: conic-gradient(
    from 0deg,
    #8b5cf6, #ec4899, #06b6d4, #3b82f6, #8b5cf6
  );
  animation: ringRotate 3s linear infinite;
  z-index: -1;
}

/* Inner blur mask */
.hero-logo-container::after {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 50%;
  background: var(--clr-bg);
  z-index: -1;
}

@keyframes ringRotate {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

.hero-logo-img {
  width: 120px; height: 120px;
  border-radius: 50%;
  object-fit: cover;
  background: rgba(255,255,255,0.06);
  animation: logoBreathe 3s ease-in-out infinite;
  box-shadow:
    0 0 30px rgba(139,92,246,0.4),
    0 0 60px rgba(236,72,153,0.2),
    inset 0 0 20px rgba(139,92,246,0.1);
}

@keyframes logoBreathe {
  0%, 100% { transform: scale(1);    filter: brightness(1); }
  50%       { transform: scale(1.06); filter: brightness(1.15); }
}

/* Pulse rings around logo */
.pulse-ring {
  position: absolute;
  border-radius: 50%;
  border: 2px solid rgba(139,92,246,0.4);
  animation: pulseExpand 2.5s ease-out infinite;
}

.pulse-ring:nth-child(1) { width: 160px; height: 160px; animation-delay: 0s; }
.pulse-ring:nth-child(2) { width: 200px; height: 200px; animation-delay: 0.8s; }
.pulse-ring:nth-child(3) { width: 240px; height: 240px; animation-delay: 1.6s; }

@keyframes pulseExpand {
  0%   { transform: scale(0.8); opacity: 0.8; }
  100% { transform: scale(1.4); opacity: 0; }
}

/* -- HERO TITLE ------------------------------------------------------------- */
.hero-title {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #ffffff 0%, #a78bfa 35%, #ec4899 65%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 300% 300%;
  animation: heroTitleFlow 6s ease-in-out infinite;
}

@keyframes heroTitleFlow {
  0%   { background-position: 0%   50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0%   50%; }
}

.hero-subtitle {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.15rem;
  color: var(--clr-muted);
  max-width: 640px;
  margin: 0 auto 36px;
  line-height: 1.7;
  animation: fadeSlideUp 1s ease 0.3s both;
}

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* -- STAT TICKER ------------------------------------------------------------ */
.stat-ticker {
  display: flex;
  justify-content: center;
  gap: 0;
  flex-wrap: wrap;
  margin-bottom: 40px;
}

.stat-item {
  padding: 14px 28px;
  border: 1px solid rgba(255,255,255,0.06);
  border-right: none;
  background: rgba(255,255,255,0.025);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.stat-item:first-child { border-radius: 12px 0 0 12px; }
.stat-item:last-child  { border-radius: 0 12px 12px 0; border-right: 1px solid rgba(255,255,255,0.06); }

.stat-item::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(139,92,246,0.1), transparent);
  transform: translateX(-100%);
  animation: shimmerSlide 3s ease infinite;
}

@keyframes shimmerSlide {
  0%   { transform: translateX(-100%); }
  40%  { transform: translateX(100%); }
  100% { transform: translateX(100%); }
}

.stat-number {
  font-family: 'Outfit', sans-serif;
  font-size: 1.8rem;
  font-weight: 800;
  display: block;
}
.stat-label {
  font-size: 11px;
  color: var(--clr-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 500;
}

/* -- FEATURE CARDS GRID ----------------------------------------------------- */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  padding: 8px 0;
}

.feature-card {
  background: rgba(255,255,255,0.03);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255,255,255,0.07);
  backdrop-filter: blur(16px);
  padding: 28px;
  transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  border-radius: 3px 3px 0 0;
  background: linear-gradient(90deg, var(--card-c1), var(--card-c2));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(circle at var(--mx, 50%) var(--my, 50%), rgba(139,92,246,0.08) 0%, transparent 60%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.feature-card:hover {
  border-color: rgba(139,92,246,0.3);
  transform: translateY(-8px);
  box-shadow:
    0 20px 60px rgba(0,0,0,0.5),
    0 0 0 1px rgba(139,92,246,0.15),
    0 0 40px rgba(139,92,246,0.1);
}

.feature-card:hover::before { opacity: 1; }
.feature-card:hover::after  { opacity: 1; }

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 16px;
  display: block;
  animation: iconFloat 3s ease-in-out infinite;
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-6px); }
}

.feature-card:nth-child(1) { --card-c1: #8b5cf6; --card-c2: #ec4899; }
.feature-card:nth-child(1) .feature-icon { animation-delay: 0s; }
.feature-card:nth-child(2) { --card-c1: #06b6d4; --card-c2: #3b82f6; }
.feature-card:nth-child(2) .feature-icon { animation-delay: 0.4s; }
.feature-card:nth-child(3) { --card-c1: #10b981; --card-c2: #06b6d4; }
.feature-card:nth-child(3) .feature-icon { animation-delay: 0.8s; }
.feature-card:nth-child(4) { --card-c1: #f59e0b; --card-c2: #ef4444; }
.feature-card:nth-child(4) .feature-icon { animation-delay: 1.2s; }
.feature-card:nth-child(5) { --card-c1: #ec4899; --card-c2: #8b5cf6; }
.feature-card:nth-child(5) .feature-icon { animation-delay: 1.6s; }
.feature-card:nth-child(6) { --card-c1: #3b82f6; --card-c2: #10b981; }
.feature-card:nth-child(6) .feature-icon { animation-delay: 2.0s; }

.feature-title {
  font-family: 'Outfit', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 8px;
}

.feature-desc {
  font-size: 13px;
  color: var(--clr-muted);
  line-height: 1.6;
}

/* -- BUTTONS ---------------------------------------------------------------- */
.stButton > button {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 50%, #5b21b6 100%) !important;
  color: #fff !important;
  border: 1px solid rgba(139,92,246,0.4) !important;
  border-radius: 12px !important;
  padding: 12px 28px !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  letter-spacing: 0.02em !important;
  transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
  box-shadow:
    0 4px 15px rgba(124,58,237,0.35),
    inset 0 1px 0 rgba(255,255,255,0.1) !important;
  position: relative !important;
  overflow: hidden !important;
}

.stButton > button::after {
  content: '' !important;
  position: absolute !important;
  inset: 0 !important;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent) !important;
  transform: translateX(-100%) !important;
  transition: transform 0.5s ease !important;
}

.stButton > button:hover {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 50%, #6d28d9 100%) !important;
  box-shadow:
    0 8px 30px rgba(139,92,246,0.5),
    0 0 0 1px rgba(139,92,246,0.4),
    inset 0 1px 0 rgba(255,255,255,0.15) !important;
  transform: translateY(-2px) !important;
}

.stButton > button:hover::after {
  transform: translateX(100%) !important;
}

/* Primary CTA button */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 50%, #06b6d4 100%) !important;
  background-size: 200% 200% !important;
  animation: btnGradientFlow 4s ease infinite !important;
  box-shadow:
    0 4px 20px rgba(236,72,153,0.4),
    0 0 40px rgba(139,92,246,0.2) !important;
}

@keyframes btnGradientFlow {
  0%   { background-position: 0%   50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0%   50%; }
}

/* -- FORM INPUTS ------------------------------------------------------------ */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stTextArea textarea {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(139,92,246,0.25) !important;
  border-radius: 12px !important;
  color: var(--clr-text) !important;
  font-family: 'Inter', sans-serif !important;
  transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
  border-color: rgba(139,92,246,0.6) !important;
  box-shadow: 0 0 0 3px rgba(139,92,246,0.15), 0 0 20px rgba(139,92,246,0.2) !important;
  background: rgba(139,92,246,0.06) !important;
}

.stTextInput > label,
.stSelectbox > label,
.stTextArea > label {
  color: var(--clr-muted) !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
}

/* -- TABS ------------------------------------------------------------------- */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(255,255,255,0.03) !important;
  border-radius: 14px !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  padding: 4px !important;
  gap: 2px !important;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 10px !important;
  color: var(--clr-muted) !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 500 !important;
  font-size: 0.85rem !important;
  transition: all 0.25s ease !important;
  padding: 8px 18px !important;
}

.stTabs [data-baseweb="tab"]:hover {
  color: #f1f5f9 !important;
  background: rgba(139,92,246,0.1) !important;
}

.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(139,92,246,0.3), rgba(236,72,153,0.2)) !important;
  color: #fff !important;
  box-shadow: 0 2px 12px rgba(139,92,246,0.3) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
  background: transparent !important;
}

/* -- METRICS ---------------------------------------------------------------- */
[data-testid="stMetric"] {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.07) !important;
  border-radius: 16px !important;
  padding: 20px !important;
  transition: all 0.3s ease !important;
}

[data-testid="stMetric"]:hover {
  border-color: rgba(139,92,246,0.3) !important;
  box-shadow: 0 8px 30px rgba(0,0,0,0.3), var(--glow-purple) !important;
  transform: translateY(-2px) !important;
}

[data-testid="stMetricValue"] {
  font-family: 'Outfit', sans-serif !important;
  font-weight: 800 !important;
  background: linear-gradient(135deg, #a78bfa, #ec4899) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
}

[data-testid="stMetricLabel"] {
  color: var(--clr-muted) !important;
  font-size: 0.75rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
  font-weight: 500 !important;
}

[data-testid="stMetricDelta"] {
  font-weight: 600 !important;
  font-size: 0.8rem !important;
}

/* -- DATAFRAMES / TABLES ---------------------------------------------------- */
[data-testid="stDataFrame"], .stDataFrame {
  border-radius: 16px !important;
  overflow: hidden !important;
  border: 1px solid rgba(139,92,246,0.15) !important;
}

.stDataFrame thead th {
  background: rgba(139,92,246,0.2) !important;
  color: #c4b5fd !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.05em !important;
  border-bottom: 1px solid rgba(139,92,246,0.3) !important;
}

.stDataFrame tbody tr:hover td {
  background: rgba(139,92,246,0.06) !important;
}

table {
  border-collapse: collapse !important;
  width: 100% !important;
}
th {
  background: rgba(139,92,246,0.18) !important;
  color: #c4b5fd !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important;
  padding: 12px 16px !important;
  font-size: 0.78rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}
td {
  padding: 11px 16px !important;
  border-bottom: 1px solid rgba(255,255,255,0.04) !important;
  font-size: 0.875rem !important;
  color: #cbd5e1 !important;
}
tr:hover td {
  background: rgba(139,92,246,0.05) !important;
}

/* -- SAFETY ALERT CARDS ----------------------------------------------------- */
.safety-alert {
  padding: 16px 20px;
  border-radius: 14px;
  margin-bottom: 14px;
  border-left: 4px solid;
  backdrop-filter: blur(12px);
  animation: alertSlideIn 0.4s ease;
}

@keyframes alertSlideIn {
  from { opacity: 0; transform: translateX(-16px); }
  to   { opacity: 1; transform: translateX(0); }
}

.safety-alert-safe {
  background: rgba(16,185,129,0.08);
  border-left-color: #10b981;
  box-shadow: 0 4px 20px rgba(16,185,129,0.1), inset 0 0 20px rgba(16,185,129,0.05);
}

.safety-alert-moderate {
  background: rgba(245,158,11,0.08);
  border-left-color: #f59e0b;
  box-shadow: 0 4px 20px rgba(245,158,11,0.1), inset 0 0 20px rgba(245,158,11,0.05);
}

.safety-alert-unsafe {
  background: rgba(239,68,68,0.08);
  border-left-color: #ef4444;
  box-shadow: 0 4px 20px rgba(239,68,68,0.15), inset 0 0 20px rgba(239,68,68,0.05);
}

/* -- SOS BUTTON ------------------------------------------------------------- */
.sos-container {
  display: flex;
  justify-content: center;
  padding: 30px 0;
}

.sos-btn {
  width: 160px; height: 160px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #ff6b6b, #ef4444 40%, #b91c1c 100%);
  border: none;
  cursor: pointer;
  font-family: 'Outfit', sans-serif;
  font-size: 1.6rem;
  font-weight: 900;
  color: #fff;
  letter-spacing: 0.08em;
  box-shadow:
    0 0 0 0 rgba(239,68,68,0.7),
    0 0 40px rgba(239,68,68,0.5),
    inset 0 2px 0 rgba(255,255,255,0.2),
    inset 0 -2px 8px rgba(0,0,0,0.3);
  animation: sosPulse 1.6s ease-out infinite;
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sos-btn:hover {
  transform: scale(1.05);
}

@keyframes sosPulse {
  0%   { box-shadow: 0 0 0 0   rgba(239,68,68,0.8), 0 0 40px rgba(239,68,68,0.4); }
  50%  { box-shadow: 0 0 0 28px rgba(239,68,68,0), 0 0 60px rgba(239,68,68,0.6); }
  100% { box-shadow: 0 0 0 0   rgba(239,68,68,0), 0 0 40px rgba(239,68,68,0.4); }
}

/* -- DIVIDER ---------------------------------------------------------------- */
hr, [data-testid="stDivider"] > div {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg,
    transparent 0%, rgba(139,92,246,0.4) 30%,
    rgba(236,72,153,0.3) 50%, rgba(6,182,212,0.3) 70%,
    transparent 100%) !important;
  margin: 24px 0 !important;
}

/* -- SPINNER ---------------------------------------------------------------- */
[data-testid="stSpinner"] > div {
  border-color: rgba(139,92,246,0.2) !important;
  border-top-color: #8b5cf6 !important;
}

/* -- SUCCESS / ERROR / INFO ------------------------------------------------- */
[data-testid="stSuccess"] {
  background: rgba(16,185,129,0.08) !important;
  border: 1px solid rgba(16,185,129,0.25) !important;
  border-radius: 12px !important;
  color: #6ee7b7 !important;
}

[data-testid="stError"] {
  background: rgba(239,68,68,0.08) !important;
  border: 1px solid rgba(239,68,68,0.25) !important;
  border-radius: 12px !important;
  color: #fca5a5 !important;
}

[data-testid="stInfo"] {
  background: rgba(59,130,246,0.08) !important;
  border: 1px solid rgba(59,130,246,0.25) !important;
  border-radius: 12px !important;
  color: #93c5fd !important;
}

[data-testid="stWarning"] {
  background: rgba(245,158,11,0.08) !important;
  border: 1px solid rgba(245,158,11,0.25) !important;
  border-radius: 12px !important;
  color: #fcd34d !important;
}

/* -- SELECTBOX DROPDOWN ----------------------------------------------------- */
[data-baseweb="popover"] {
  background: rgba(10,5,32,0.97) !important;
  border: 1px solid rgba(139,92,246,0.3) !important;
  border-radius: 14px !important;
  backdrop-filter: blur(24px) !important;
  box-shadow: 0 20px 60px rgba(0,0,0,0.6), 0 0 0 1px rgba(139,92,246,0.15) !important;
}

/* -- SCROLLBAR -------------------------------------------------------------- */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #8b5cf6, #ec4899);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #a78bfa, #f472b6);
}

/* -- COLOURED GLOW TEXT ----------------------------------------------------- */
.glow-text-green  { color: #4ade80 !important; text-shadow: 0 0 15px rgba(74,222,128,0.5); font-weight: 700; }
.glow-text-yellow { color: #fbbf24 !important; text-shadow: 0 0 15px rgba(251,191,36,0.5); font-weight: 700; }
.glow-text-red    { color: #f87171 !important; text-shadow: 0 0 15px rgba(248,113,113,0.5); font-weight: 700; }
.glow-text-cyan   { color: #22d3ee !important; text-shadow: 0 0 15px rgba(34,211,238,0.5); font-weight: 700; }
.glow-text-purple { color: #c084fc !important; text-shadow: 0 0 15px rgba(192,132,252,0.5); font-weight: 700; }

/* -- KPI / FORECAST CARDS --------------------------------------------------- */
.kpi-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 16px;
  padding: 20px 22px;
  text-align: center;
  transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
  position: relative;
  overflow: hidden;
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0; left: -60%; right: -60%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139,92,246,0.6), rgba(236,72,153,0.4), transparent);
  animation: kpiTopShimmer 3s ease infinite;
}

@keyframes kpiTopShimmer {
  0%   { transform: translateX(-50%); opacity: 0; }
  50%  { opacity: 1; }
  100% { transform: translateX(50%);  opacity: 0; }
}

.kpi-card:hover {
  border-color: rgba(139,92,246,0.35);
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.4), var(--glow-purple);
}

.kpi-value {
  font-family: 'Outfit', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 4px;
}

.kpi-label {
  font-size: 11px;
  color: var(--clr-muted);
  text-transform: uppercase;
  letter-spacing: 0.07em;
  font-weight: 500;
}

/* -- RISK BADGES ------------------------------------------------------------ */
.risk-critical { background: rgba(239,68,68,0.15);  color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); border-radius: 99px; display:inline-block; padding:3px 12px; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; }
.risk-high     { background: rgba(249,115,22,0.15); color: #fdba74; border: 1px solid rgba(249,115,22,0.3); border-radius: 99px; display:inline-block; padding:3px 12px; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; }
.risk-moderate { background: rgba(245,158,11,0.15); color: #fde68a; border: 1px solid rgba(245,158,11,0.3); border-radius: 99px; display:inline-block; padding:3px 12px; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; }
.risk-low      { background: rgba(16,185,129,0.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.3); border-radius: 99px; display:inline-block; padding:3px 12px; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; }

/* -- TREND TEXT ------------------------------------------------------------- */
.trend-rising    { color: #f87171; font-weight: 700; }
.trend-declining { color: #4ade80; font-weight: 700; }
.trend-stable    { color: #fbbf24; font-weight: 700; }

/* -- DATA SOURCE NOTE ------------------------------------------------------- */
.data-source-note {
  background: rgba(59,130,246,0.05);
  border: 1px solid rgba(59,130,246,0.15);
  border-radius: 10px;
  padding: 11px 16px;
  font-size: 11.5px;
  color: #93c5fd;
  margin-top: 14px;
  line-height: 1.5;
}

/* -- FORECAST CHART CONTAINER ----------------------------------------------- */
.forecast-hero {
  background: linear-gradient(135deg, rgba(139,92,246,0.1) 0%, rgba(236,72,153,0.07) 50%, rgba(6,182,212,0.06) 100%);
  border: 1px solid rgba(139,92,246,0.2);
  border-radius: 24px;
  padding: 32px;
  margin-bottom: 28px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.forecast-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 60% 50% at 50% 0%, rgba(139,92,246,0.15) 0%, transparent 70%);
  pointer-events: none;
}

/* -- PARTICLE CANVAS CONTAINER ---------------------------------------------- */
.particle-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

/* -- NAV SELECT OVERRIDE ---------------------------------------------------- */
[data-testid="stSelectbox"] > div > div {
  background: rgba(139,92,246,0.08) !important;
  border: 1px solid rgba(139,92,246,0.25) !important;
  border-radius: 12px !important;
}

/* -- MAP CONTAINER ---------------------------------------------------------- */
.stFolium, [data-testid="stIFrame"] {
  border-radius: 20px !important;
  overflow: hidden !important;
  border: 1px solid rgba(139,92,246,0.2) !important;
  box-shadow: 0 8px 40px rgba(0,0,0,0.4) !important;
}

/* -- SECTION HEADERS -------------------------------------------------------- */
.section-label {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--clr-muted);
  margin-bottom: 4px;
}

.section-title {
  font-family: 'Outfit', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 8px;
}

/* -- ANIMATED BADGE --------------------------------------------------------- */
.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(16,185,129,0.12);
  border: 1px solid rgba(16,185,129,0.3);
  border-radius: 99px;
  padding: 4px 12px;
  font-size: 11px;
  font-weight: 600;
  color: #6ee7b7;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.live-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #10b981;
  animation: livePulse 1.5s ease-in-out infinite;
}

@keyframes livePulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.4; transform: scale(0.7); }
}

/* -- PAGE ENTRY ANIMATION --------------------------------------------------- */
.page-enter {
  animation: pageEnter 0.5s cubic-bezier(0.4,0,0.2,1) both;
}

@keyframes pageEnter {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* -- GOOGLE MAPS STYLE ROUTE PLANNER --------------------------------------- */
.gmap-box {
  background: rgba(255, 255, 255, 0.035);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 20px;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  margin-bottom: 18px;
  transition: all 0.3s ease;
}

.gmap-mode-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
  padding: 4px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.gmap-route-card {
  position: relative;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 14px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.gmap-route-card:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.05);
}

.gmap-route-active {
  background: rgba(255, 255, 255, 0.055) !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}

.gmap-eta {
  font-family: 'Outfit', sans-serif;
  font-size: 1.65rem;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.gmap-dist {
  font-size: 0.95rem;
  font-weight: 600;
  color: #94a3b8;
}

.gmap-step-row {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 12px 14px;
  border-radius: 12px;
  margin-bottom: 8px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  transition: all 0.2s ease;
}

.gmap-step-row:hover {
  background: rgba(255, 255, 255, 0.045);
  border-color: rgba(255, 255, 255, 0.08);
}

.gmap-step-icon {
  font-size: 1.25rem;
  min-width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
}

.gmap-btn-live {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
  color: #ffffff !important;
  font-family: 'Outfit', sans-serif;
  font-weight: 700;
  font-size: 0.95rem;
  padding: 12px 24px;
  border-radius: 12px;
  text-decoration: none !important;
  box-shadow: 0 4px 18px rgba(66, 133, 244, 0.4);
  transition: all 0.25s ease;
}

.gmap-btn-live:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(66, 133, 244, 0.6);
  color: #ffffff !important;
}

.checkpoint-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11.5px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

/* -- INPUT TEXT VISIBILITY & CONTRAST (DARK MODE) ------------------------ */
div[data-testid="stTextInput"],
div[data-testid="stTextInput"] > div,
div[data-testid="stTextInput"] > div > div,
div[data-testid="stTextInputRootElement"],
div[data-baseweb="input"],
div[data-baseweb="base-input"],
.stTextInput,
.stTextInput > div,
.stTextInput > div > div {
  background-color: #110829 !important;
  background: #110829 !important;
  border-color: rgba(139, 92, 246, 0.5) !important;
  border-radius: 12px !important;
}

div[data-testid="stTextInput"] input,
div[data-baseweb="input"] input,
div[data-baseweb="base-input"] input,
.stTextInput input,
input[type="text"],
input[type="password"] {
  background-color: #110829 !important;
  background: #110829 !important;
  color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important;
  caret-color: #ec4899 !important;
  border: none !important;
  padding: 10px 14px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="base-input"]:focus-within,
div[data-testid="stTextInput"] > div:focus-within {
  background-color: #190c3b !important;
  background: #190c3b !important;
  border-color: #c084fc !important;
  box-shadow: 0 0 16px rgba(139, 92, 246, 0.5) !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-baseweb="input"] input:focus,
div[data-baseweb="base-input"] input:focus,
.stTextInput input:focus,
input[type="text"]:focus,
input[type="password"]:focus {
  background-color: #190c3b !important;
  background: #190c3b !important;
  color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important;
}

div[data-testid="stTextInput"] input::placeholder,
div[data-baseweb="input"] input::placeholder,
.stTextInput input::placeholder,
input[type="text"]::placeholder {
  color: #a78bfa !important;
  -webkit-text-fill-color: #a78bfa !important;
  opacity: 0.8 !important;
  font-weight: 400 !important;
}

/* -- LIGHT MODE OVERRIDE ---------------------------------------------------- */
.light-mode html, .light-mode body,
.light-mode [data-testid="stAppViewContainer"] {
  background: #f8fafc !important;
  color: #0f172a !important;
}

</style>
"""

# Light mode supplement CSS
LIGHT_THEME_CSS = """
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
  background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 50%, #f0fffa 100%) !important;
  color: #0f172a !important;
}
[data-testid="stAppViewContainer"]::before {
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%, rgba(139,92,246,0.08) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(6,182,212,0.06) 0%, transparent 55%) !important;
}
[data-testid="stHeader"] {
  background: rgba(255,255,255,0.85) !important;
  border-bottom: 1px solid rgba(139,92,246,0.15) !important;
}
.glass-card {
  background: rgba(255,255,255,0.75) !important;
  border-color: rgba(139,92,246,0.15) !important;
  box-shadow: 0 4px 20px rgba(139,92,246,0.08) !important;
  color: #0f172a !important;
}
.glass-card:hover {
  box-shadow: 0 12px 40px rgba(139,92,246,0.15) !important;
}
.feature-card {
  background: rgba(255,255,255,0.8) !important;
  border-color: rgba(139,92,246,0.12) !important;
  color: #0f172a !important;
}
.kpi-card {
  background: rgba(255,255,255,0.8) !important;
  border-color: rgba(139,92,246,0.15) !important;
}
h1, h2, h3, h4, h5, h6, p, li, span, label, div {
  color: #0f172a !important;
}
.kpi-label, .feature-desc, [data-testid="stMetricLabel"] {
  color: #64748b !important;
}
.glow-title {
  filter: none !important;
}

/* Light mode input */
div[data-testid="stTextInput"] input,
div[data-baseweb="input"] input,
div[data-baseweb="base-input"] input,
.stTextInput input,
input[type="text"],
input[type="password"] {
  background-color: #ffffff !important;
  color: #0f172a !important;
  -webkit-text-fill-color: #0f172a !important;
  caret-color: #7c3aed !important;
  border: 1.5px solid #cbd5e1 !important;
  border-radius: 12px !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-baseweb="input"] input:focus,
div[data-baseweb="base-input"] input:focus,
.stTextInput input:focus,
input[type="text"]:focus,
input[type="password"]:focus {
  border-color: #8b5cf6 !important;
  box-shadow: 0 0 14px rgba(139, 92, 246, 0.25) !important;
}

div[data-testid="stTextInput"] input::placeholder,
div[data-baseweb="input"] input::placeholder,
.stTextInput input::placeholder,
input[type="text"]::placeholder {
  color: #64748b !important;
  -webkit-text-fill-color: #64748b !important;
}
</style>
"""
