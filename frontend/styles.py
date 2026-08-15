# Premium Dark Glassmorphism Styling for Streamlit App

DARK_THEME_CSS = """
<style>
/* Import Outfit and Inter Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

/* Global overrides */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c20 0%, #15102a 50%, #06040d 100%) !important;
    font-family: 'Inter', sans-serif !important;
    color: #e0def4 !important;
}

[data-testid="stHeader"] {
    background: rgba(15, 12, 32, 0.6) !important;
    backdrop-filter: blur(12px) !important;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #110c24 0%, #080613 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

[data-testid="stSidebarNav"] {
    font-family: 'Outfit', sans-serif !important;
}

/* Glassmorphic Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.07);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 24px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: rgba(138, 92, 246, 0.3);
    box-shadow: 0 8px 32px 0 rgba(138, 92, 246, 0.1);
    transform: translateY(-2px);
}

/* Glowing text and headers */
.glow-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa 0%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(167, 139, 250, 0.2);
}

.glow-text-green {
    color: #4ade80 !important;
    text-shadow: 0 0 10px rgba(74, 222, 128, 0.4);
}

.glow-text-yellow {
    color: #facc15 !important;
    text-shadow: 0 0 10px rgba(250, 204, 21, 0.4);
}

.glow-text-red {
    color: #f87171 !important;
    text-shadow: 0 0 10px rgba(248, 113, 113, 0.4);
}

/* Gauge metrics container */
.gauge-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 15px;
}

.gauge-val {
    font-size: 3rem;
    font-weight: 800;
    font-family: 'Outfit', sans-serif;
    margin-bottom: 0px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #7c3aed 0%, #c084fc 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stButton>button:hover {
    box-shadow: 0 4px 25px rgba(192, 132, 252, 0.5) !important;
    transform: scale(1.02) !important;
}

/* Alert styles */
.safety-alert {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    border-left: 5px solid;
}
.safety-alert-safe {
    background: rgba(74, 222, 128, 0.1);
    border-left-color: #4ade80;
    color: #e2fbe9;
}
.safety-alert-moderate {
    background: rgba(250, 204, 21, 0.1);
    border-left-color: #facc15;
    color: #fffde6;
}
.safety-alert-unsafe {
    background: rgba(248, 113, 113, 0.1);
    border-left-color: #f87171;
    color: #ffebeb;
}

/* SOS Glowing Button */
.sos-btn-container {
    display: flex;
    justify-content: center;
    margin: 20px 0;
}

.sos-btn {
    background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
    color: white;
    font-family: 'Outfit', sans-serif;
    font-size: 24px;
    font-weight: 800;
    width: 140px;
    height: 140px;
    border-radius: 50%;
    border: 4px solid #fca5a5;
    cursor: pointer;
    box-shadow: 0 0 20px #ef4444, inset 0 0 15px rgba(255,255,255,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: pulse 1.8s infinite;
    transition: all 0.2s ease;
}

.sos-btn:active {
    transform: scale(0.95);
    box-shadow: 0 0 10px #ef4444;
}

@keyframes pulse {
    0% {
        transform: scale(1);
        box-shadow: 0 0 20px #ef4444, 0 0 0 0px rgba(239, 68, 68, 0.7);
    }
    70% {
        transform: scale(1.05);
        box-shadow: 0 0 25px #ef4444, 0 0 0 15px rgba(239, 68, 68, 0);
    }
    100% {
        transform: scale(1);
        box-shadow: 0 0 20px #ef4444, 0 0 0 0px rgba(239, 68, 68, 0);
    }
}

/* Table Style */
table {
    background: rgba(255, 255, 255, 0.02) !important;
    border-collapse: collapse !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

th {
    background-color: rgba(124, 58, 237, 0.2) !important;
    color: #c084fc !important;
    font-weight: 600 !important;
}

td, th {
    padding: 12px 15px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
}

</style>
"""
