import datetime
import random
import streamlit as st

var = st.session_state
hl = st.divider

# Initialize session state variables
if "name" not in var:
    var.name = None
if "age_group" not in var:
    var.age_group = None
if "gender" not in var:
    var.gender = None
if "application" not in var:
    var.application = 0
if "mode" not in var:
    var.mode = "DND"
if "timelist" not in var:
    var.timelist = []
if "sleeptime" not in var:
    var.sleeptime = None
if "wi_final" not in var:
    var.wi_final = None
if "rl2" not in var:
    var.rl2 = []
if "reminder_list" not in var:
    var.reminder_list = []
if "completed" not in var:
    var.completed = 0
if "last_reminder_check" not in var:
    var.last_reminder_check = datetime.datetime.now()

# Global Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientFlow 20s ease infinite;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles */
    .particle {
        position: fixed;
        border-radius: 50%;
        pointer-events: none;
        opacity: 0.6;
        z-index: 0;
    }
    
    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.7s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    /* Hero header */
    .hero-header {
        text-align: center;
        color: white;
        text-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        animation: titlePulse 3s ease-in-out infinite;
        margin: 2rem 0;
    }
    
    @keyframes titlePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .hero-header h1 {
        font-size: 3.5em;
        font-weight: 800;
        background: linear-gradient(135deg, #fff, #e0f7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-header p {
        font-size: 1.3em;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Custom input styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: white !important;
        font-size: 1.1em !important;
        padding: 0.8rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Label styling */
    label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 1.1em !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 1rem 3rem !important;
        font-size: 1.2em !important;
        font-weight: 600 !important;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.6) !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.5s, height 0.5s;
    }
    
    .stButton > button:active::before {
        width: 300px;
        height: 300px;
    }
    
    /* Progress bar styling */
    div[data-testid="stProgress"] > div {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px);
        border-radius: 25px !important;
        overflow: hidden;
        height: 35px !important;
        box-shadow: inset 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    div[data-testid="stProgress"] > div > div {
        border-radius: 25px !important;
        height: 35px !important;
        position: relative;
        overflow: hidden;
    }
    
    div[data-testid="stProgress"] > div > div::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: progressFlow 2s linear infinite;
    }
    
    @keyframes progressFlow {
        from { transform: translateX(-100%); }
        to { transform: translateX(100%); }
    }
    
    /* Stats card */
    .stats-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        animation: float 4s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    .stats-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }
    
    .stats-card h2 {
        font-size: 3em;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stats-card p {
        font-size: 1.2em;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    
    /* Reminder card */
    .reminder-card {
        background: rgba(79, 195, 247, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(79, 195, 247, 0.4);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        color: white;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .reminder-card:hover {
        transform: translateX(10px);
        background: rgba(79, 195, 247, 0.35);
        box-shadow: 0 10px 25px rgba(79, 195, 247, 0.3);
    }
    
    .reminder-icon {
        font-size: 2em;
        animation: bell 2s ease-in-out infinite;
    }
    
    @keyframes bell {
        0%, 100% { transform: rotate(0deg); }
        10% { transform: rotate(15deg); }
        20% { transform: rotate(-15deg); }
        30% { transform: rotate(10deg); }
        40% { transform: rotate(-10deg); }
        50% { transform: rotate(0deg); }
    }
    
    /* Time record card */
    .time-record {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: white;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .time-record:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateX(10px);
    }
    
    /* Success celebration */
    .success-container {
        text-align: center;
        animation: celebrate 2s ease-in-out infinite;
    }
    
    @keyframes celebrate {
        0%, 100% {
            transform: scale(1) rotate(0deg);
        }
        25% {
            transform: scale(1.05) rotate(2deg);
        }
        75% {
            transform: scale(1.05) rotate(-2deg);
        }
    }
    
    .success-emoji {
        font-size: 8em;
        animation: bounce 1s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    /* Divider styling */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
        margin: 2rem 0;
    }
    
    /* Info box styling */
    .stAlert {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: white !important;
    }
    
    /* Water droplet animation */
    .droplet {
        position: fixed;
        width: 10px;
        height: 10px;
        background: rgba(79, 195, 247, 0.6);
        border-radius: 50%;
        pointer-events: none;
        animation: fall 3s linear infinite;
        z-index: 0;
    }
    
    @keyframes fall {
        0% {
            transform: translateY(-100px);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh);
            opacity: 0;
        }
    }
    
    /* Wave effect */
    .wave-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 150px;
        pointer-events: none;
        z-index: 0;
    }
    
    .wave {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 200%;
        height: 100%;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120"><path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" fill="rgba(255,255,255,0.1)"></path></svg>');
        background-size: 50% 100%;
        animation: wave 15s linear infinite;
    }
    
    @keyframes wave {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    
    /* Glow effect for important elements */
    .glow {
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% {
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.5),
                         0 0 30px rgba(79, 195, 247, 0.5);
        }
        50% {
            text-shadow: 0 0 30px rgba(255, 255, 255, 0.8),
                         0 0 50px rgba(79, 195, 247, 0.8);
        }
    }
</style>

<script>
// Create floating particles
function createParticles() {
    const container = document.querySelector('.stApp');
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        particle.style.width = Math.random() * 8 + 3 + 'px';
        particle.style.height = particle.style.width;
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.background = `rgba(79, 195, 247, ${Math.random() * 0.5 + 0.2})`;
        particle.style.animation = `float ${Math.random() * 10 + 5}s ease-in-out infinite`;
        particle.style.animationDelay = Math.random() * 5 + 's';
        if (container) container.appendChild(particle);
    }
}

// Create water droplets
function createDroplets() {
    setInterval(() => {
        const droplet = document.createElement('div');
        droplet.classList.add('droplet');
        droplet.style.left = Math.random() * 100 + '%';
        droplet.style.animationDuration = Math.random() * 2 + 2 + 's';
        document.body.appendChild(droplet);
        
        setTimeout(() => droplet.remove(), 3000);
    }, 500);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        createParticles();
        createDroplets();
    });
} else {
    createParticles();
    createDroplets();
}
</script>

<!-- Wave effect -->
<div class="wave-container">
    <div class="wave"></div>
</div>
""", unsafe_allow_html=True)

# Page 1: Initial Setup
if var.application == 0:
    st.markdown("""
    <div class="hero-header">
        <h1>💧 WaterBuddy</h1>
        <p>Your Personal Water Intake Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:white; text-align:center; margin-bottom:2rem;'>✨ Let's Get to Know You</h3>", unsafe_allow_html=True)
    
    age_groups = ["6-12", "13-18", "19-30", "30-50", "50+"]
    
    var.name = st.text_input("👤 What's Your Name?", placeholder="Enter your name here...")
    hl()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p style="color:white; font-weight:500;">🎂 Age Group</p>', unsafe_allow_html=True)
        var.age_group = st.selectbox("Age Group", age_groups, label_visibility="collapsed")
    
    with col2:
        st.markdown('<p style="color:white; font-weight:500;">⚧ Gender</p>', unsafe_allow_html=True)
        var.gender = st.selectbox("Gender", ["male", "female"], label_visibility="collapsed")
    
    hl()
    
    st.markdown("<h4 style='color:white; text-align:center; margin-top:2rem;'>🌙 When Do You Usually Sleep?</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<p style="color:white; font-weight:500;">Hour</p>', unsafe_allow_html=True)
        var.sleephour = st.selectbox("Sleep Hour", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], label_visibility="collapsed")
    
    with col2:
        st.markdown('<p style="color:white; font-weight:500;">Minute</p>', unsafe_allow_html=True)
        var.sleepminute = st.selectbox("Sleep Minute", ["00", "15", "30", "45"], label_visibility="collapsed")
    
    with col3:
        st.markdown('<p style="color:white; font-weight:500;">AM/PM</p>', unsafe_allow_html=True)
        var.sleepmeridien = st.selectbox("AM/PM", ["AM", "PM"], label_visibility="collapsed")
    
    hl()
    
    # Water intake recommendations
    var.male_water_intake = [1.75, 2.50, 2.75, 2.75, 2.75]
    var.female_water_intake = [1.50, 1.75, 2.00, 2.00, 2.00]
    
    if var.gender == "male":
        var.wi = var.male_water_intake[age_groups.index(var.age_group)] * 1000
    if var.gender == "female":
        var.wi = var.female_water_intake[age_groups.index(var.age_group)] * 1000
    
    var.whole = []
    for i in range(250, 5250, 250):
        var.whole.append(str(i))
    
    st.markdown(f"""
    <div style='text-align:center; margin:2rem 0;'>
        <p style='color:white; font-size:1.1em;'>🎯 Your Daily Water Target</p>
        <p style='color:#4fc3f7; font-size:1.3em; font-weight:600;'>Recommended: {int(var.wi)} ml</p>
    </div>
    """, unsafe_allow_html=True)
    
    var.wi_final = st.selectbox("Water Target", var.whole, var.whole.index(str(int(var.wi))), label_visibility="collapsed")
    var.wi_final = int(var.wi_final)
    var.completed = 0
    var.final_name = var.name
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Your Journey", use_container_width=True):
            if var.name.replace(" ", "") == "":
                st.error("🙋 Please enter your name to continue!")
            else:
                var.application = 1
                st.rerun()

# Page 2: Main Water Tracking
if var.application == 1:
    var.init_time = datetime.datetime.now()
    
    if var.sleepmeridien == "PM":
        var.meridien_adjustment = 12
    else:
        var.meridien_adjustment = 0
    
    var.hour_meridien = int(var.sleephour) + var.meridien_adjustment
    var.timeleft = int((var.hour_meridien - var.init_time.hour) * 60) + (int(var.sleepminute) - 30 - var.init_time.minute)
    
    if var.timeleft <= 0:
        var.application = 3
        st.rerun()
    else:
        var.d = 250
        var.n = var.wi_final / var.d
        var.per = int(var.timeleft / var.n)
        
        if round(var.per, 0) < 30:
            var.application = 3
            st.rerun()
        
        # Calculate reminder times
        if not var.reminder_list:
            var.reminder_list = []
            for item in range(1, int(var.n + 1)):
                hour = int(((var.init_time.hour * 60) + var.init_time.minute + (item * var.per)) // 60)
                minute = int(((var.init_time.hour * 60) + var.init_time.minute + (item * var.per)) % 60)
                var.reminder_list.append([hour, minute])
    
    # Header
    st.markdown(f"""
    <div class="hero-header">
        <h1 class="glow">Hi {var.name}! 👋</h1>
        <p>Let's crush your hydration goals today!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    percentage = (var.completed / var.wi_final) * 100 if var.wi_final > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <h2>{int(var.wi_final)}</h2>
            <p>🎯 Target (ml)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <h2>{int(var.completed)}</h2>
            <p>💧 Consumed (ml)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <h2>{round(percentage, 1)}%</h2>
            <p>📊 Progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Progress bar
    st.markdown("""
    <style>
    div[data-testid="stProgress"] > div > div > div {
        height: 20px;  /* Change this value as needed */
    }
    </style>
    """, unsafe_allow_html=True)

    var.bar = st.progress(percentage/100)
    
    # Progress bar color gradient
    if percentage <= 60:
        gradient = "90deg, #4facfe, #00f2fe"
    else:
        gradient = "90deg, #fa709a, #fee140"
    
    st.markdown(f"""
    <style>
    div[data-testid="stProgress"] > div > div > div > div {{
        background: linear-gradient({gradient}) !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Check for reminders
    current_time = datetime.datetime.now()
    for reminder_time in var.reminder_list[:]:
        if (current_time.hour == reminder_time[0] and 
            current_time.minute == reminder_time[1] and
            abs((current_time - var.last_reminder_check).total_seconds()) < 120):
            motivating_words = ["Come on", "You can do it", "Keep pushing", "Nail it"]
            st.success(f"🚰 {random.choice(motivating_words)}! Time for your glass of water!")
            st.balloons()
            var.reminder_list.remove(reminder_time)
            var.last_reminder_check = current_time
    
    # Quick action
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:white; text-align:center; margin-bottom:1.5rem;'>⚡ Quick Action</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💧 Add 250ml", use_container_width=True):
            var.completed += 250
            var.bar.progress(var.completed / var.wi_final)
            
            now = datetime.datetime.now()
            hour = now.hour
            ampm = "A.M."
            if now.hour >= 12:
                if now.hour > 12:
                    hour = now.hour - 12
                ampm = "P.M."
            
            var.timelist.append(f"{now.day}/{now.month}/{now.year} - {hour}:{now.minute:02d} {ampm}")
            
            if var.wi_final - var.completed <= 0:
                var.application = 2
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Upcoming reminders
    if var.reminder_list:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; margin-bottom:1.5rem;'>⏰ Upcoming Reminders</h3>", unsafe_allow_html=True)
        
        for idx, m in enumerate(var.reminder_list):
            show_hour = m[0]
            show_minute = m[1]
            show_ampm = "A.M."
            if show_hour >= 12:
                if show_hour > 12:
                    show_hour = show_hour - 12
                show_ampm = "P.M."
            elif show_hour == 0:
                show_hour = 12
            
            st.markdown(f"""
            <div class="reminder-card">
                <span class="reminder-icon">🔔</span>
                <div>
                    <strong style="font-size:1.2em;">{show_hour}:{show_minute:02d} {show_ampm}</strong>
                    <p style="margin:0; opacity:0.8;">Reminder #{idx + 1}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Time record
    if var.timelist:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; margin-bottom:1.5rem;'>📈 Today's Timeline</h3>", unsafe_allow_html=True)
        
        for x in var.timelist[::-1]:
            st.markdown(f"""
            <div class="time-record">
                <strong>💧 {x}</strong> - Added 250ml
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Auto-refresh button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Check for Reminders", use_container_width=True):
            st.rerun()

# Page 3: Success Page
if var.application == 2:
    st.markdown("""
    <div class="success-container">
        <div class="success-emoji">🎉</div>
        <div class="hero-header">
            <h1 class="glow">Congratulations, {name}!</h1>
            <p>You've crushed your daily hydration goal!</p>
        </div>
    </div>
    """.format(name=var.name), unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <h2>✅</h2>
            <p>Target Achieved</p>
            <h3>{int(var.wi_final)} ml</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <h2>💧</h2>
            <p>Total Consumed</p>
            <h3>{int(var.completed)} ml</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align:center; margin:2rem 0;'>
        <h3 style='color:white;'>🌅 See You Tomorrow!</h3>
        <p style='color:white; font-size:1.2em; opacity:0.9;'>Keep up the amazing work and stay hydrated!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Time record
    if var.timelist:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; text-align:center; margin-bottom:1.5rem;'>📊 Today's Complete Timeline</h3>", unsafe_allow_html=True)
        
        for x in var.timelist[::-1]:
            st.markdown(f"""
            <div class="time-record">
                <strong>💧 {x}</strong> - Added 250ml
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.balloons()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Start Fresh Tomorrow", use_container_width=True):
            for key in list(var.keys()):
                del var[key]
            st.rerun()

# Page 4: Too Late Page
if var.application == 3:
    st.markdown(f"""
    <div class="hero-header">
        <h1>🌙 Good Night, {var.name}!</h1>
        <p>Time to rest and recharge</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align:center;'>
        <div class="success-emoji">😴</div>
        <h3 style='color:white; margin:2rem 0;'>It's Getting Late!</h3>
        <p style='color:white; font-size:1.2em; line-height:1.8; opacity:0.9;'>
            Sorry, but we've run out of time for today.<br>
            Our day ends at midnight (12:00 AM).<br><br>
            Don't worry - tomorrow is a fresh start! 💪<br><br>
            <strong>Sweet dreams and see you in the morning! 🌅</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="display:flex; justify-content:center; align-items:center; margin:3rem 0;">
        <div style="font-size: 120px; animation: bounce 2s ease-in-out infinite;">🌙💤</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌅 Start New Day", use_container_width=True):
            for key in list(var.keys()):
                del var[key]
            st.rerun()

# Auto-refresh script for reminder checking (only on main page)
if var.application == 1:
    st.markdown("""
    <script>
    setTimeout(function(){
        window.location.reload(1);
    }, 6000);
    </script>
    """, unsafe_allow_html=True)
