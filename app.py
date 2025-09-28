import streamlit as st
import datetime
from datetime import timedelta
import pandas as pd
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="💧 Hydration Reminder",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for futuristic design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .water-glass {
        width: 100px;
        height: 150px;
        border: 3px solid #4a90e2;
        border-radius: 0 0 10px 10px;
        position: relative;
        margin: 0 auto;
        background: linear-gradient(to top, #4fc3f7 0%, #4fc3f7 var(--fill-height), transparent var(--fill-height));
    }
    
    .stats-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .reminder-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .track-record {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .congratulations {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'details'
    
if 'water_consumed' not in st.session_state:
    st.session_state.water_consumed = 0
    
if 'consumption_log' not in st.session_state:
    st.session_state.consumption_log = []

def calculate_water_target(age_group, gender):
    """Calculate recommended water target based on age and gender"""
    male_targets = [1.75, 2.5, 2.75, 2.75, 2.75]  # for age groups 6-12,13-18,19-30,31-50,50+
    female_targets = [1.5, 1.75, 2, 2, 2]
    
    age_groups = ["6-12", "13-18", "19-30", "31-50", "50+"]
    age_index = age_groups.index(age_group)
    
    if gender == "Male":
        return male_targets[age_index] * 1000  # Convert to ml
    else:
        return female_targets[age_index] * 1000

def calculate_reminders(target_ml, consumed_ml, sleep_hour, sleep_minute):
    """Calculate reminder timings based on remaining water and time"""
    now = datetime.datetime.now()
    sleep_time = now.replace(hour=sleep_hour, minute=sleep_minute)
    
    # If sleep time is earlier than current time, assume it's for tomorrow
    if sleep_time <= now:
        sleep_time += timedelta(days=1)
    
    remaining_time = sleep_time - now
    remaining_hours = remaining_time.total_seconds() / 3600
    
    remaining_ml = target_ml - consumed_ml
    servings_needed = max(0, (remaining_ml / 250)+1)
    
    if servings_needed <= 0 or remaining_hours <= 0:
        return []
    
    interval_hours = remaining_hours / servings_needed if servings_needed > 0 else 1
    
    reminders = []
    current_time = now
    
    for i in range(int(servings_needed)):
        current_time += timedelta(hours=interval_hours)
        if current_time < sleep_time:
            reminders.append(current_time.strftime("%H:%M"))
    
    return reminders

def draw_water_glass(percentage):
    """Draw a water glass with fill percentage"""
    fig = go.Figure()
    
    # Glass outline
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=1, y1=1,
        line=dict(color="#4a90e2", width=3),
        fillcolor="rgba(0,0,0,0)"
    )
    
    # Water fill
    fill_height = percentage / 100
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=1, y1=fill_height,
        fillcolor="#4fc3f7",
        line=dict(width=0)
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        width=200,
        height=300,
        margin=dict(l=0, r=0, b=0, t=0)
    )
    
    return fig

# Stage 1: User Details
if st.session_state.stage == 'details':
    st.markdown('<div class="main-header"><h1>💧 Welcome to Hydration Reminder</h1><p>Let\'s personalize your water intake goals!</p></div>', unsafe_allow_html=True)
    
    with st.form("user_details"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Your Name", placeholder="Enter your name")
            age_group = st.selectbox("🎂 Age Group", ["6-12", "13-18", "19-30", "31-50", "50+"])
            gender = st.selectbox("⚧ Gender", ["Male", "Female"])
        
        with col2:
            sleep_hour = st.selectbox("🌙 Sleep Hour", range(18, 24), index=4)  # Default 22:00
            sleep_minute = st.selectbox("🌙 Sleep Minute", [0, 15, 30, 45], index=0)
            
            # Calculate recommended target
            recommended_target = calculate_water_target(age_group, gender)
            
            # Custom water target
            custom_target = st.selectbox(
                f"🎯 Water Target (ml) - Recommended: {int(recommended_target)}ml",
                range(250, 10250, 250),
                index=int((recommended_target - 250) / 250)
            )
        
        submitted = st.form_submit_button("🚀 Start Your Hydration Journey!", use_container_width=True)
        
        if submitted and name:
            st.session_state.user_name = name
            st.session_state.age_group = age_group
            st.session_state.gender = gender
            st.session_state.sleep_hour = sleep_hour
            st.session_state.sleep_minute = sleep_minute
            st.session_state.water_target = custom_target
            st.session_state.stage = 'dashboard'
            st.rerun()
        elif submitted:
            st.error("Please enter your name to continue!")

# Stage 2: Dashboard
elif st.session_state.stage == 'dashboard':
    # Check if target is reached
    if st.session_state.water_consumed >= st.session_state.water_target:
        st.session_state.stage = 'congratulations'
        st.rerun()
    percentage = (st.session_state.water_consumed / st.session_state.water_target) * 100
    
    st.markdown(f'<div class="main-header"><h1>🌟 Hello, {st.session_state.user_name}!</h1><p>Stay hydrated and healthy today!</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💧 Quick Action")
        if st.button("⚡ +250ml", use_container_width=True, type="primary"):
            st.session_state.water_consumed += 250
            st.session_state.consumption_log.append({
                'time': datetime.datetime.now().strftime("%H:%M"),
                'amount': 250
            })
            st.rerun()
        st.markdown(f"""
        <div class="stats-card">
            <h3>{percentage:.1f}% Complete</h3>
            <p>{st.session_state.water_consumed}ml / {st.session_state.water_target}ml</p>
            <p>Remaining: {max(0, st.session_state.water_target - st.session_state.water_consumed)}ml</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Progress")
        
        # Display water glass
        fig = draw_water_glass(min(percentage, 100))
        st.plotly_chart(fig, use_container_width=True)
        
    
    # with col3:
    #     st.markdown("### ⏰ Custom Amount")
    #     custom_amount = st.number_input("Add ml:", min_value=50, max_value=1000, step=50, value=250)
    #     if st.button(f"Add {custom_amount}ml", use_container_width=True):
    #         st.session_state.water_consumed += custom_amount
    #         st.session_state.consumption_log.append({
    #             'time': datetime.datetime.now().strftime("%H:%M"),
    #             'amount': custom_amount
    #         })
    #         st.rerun()
    
    # Reminder Section
    st.markdown("### 🔔 Smart Reminders")
    
    reminders = calculate_reminders(
        st.session_state.water_target,
        st.session_state.water_consumed,
        st.session_state.sleep_hour,
        st.session_state.sleep_minute
    )
    
    if reminders:
        st.markdown("**Calculated reminder times:**")
        for i, reminder_time in enumerate(reminders):
            # col1, col2 = st.columns([3, 1])
            # with col1:
            st.markdown(f'<div class="reminder-card">💧 Reminder {i+1}: {reminder_time}</div>', unsafe_allow_html=True)
            # with col2:
            #     new_time = st.selectbox(f"Edit #{i+1}", 
            #                           [f"{h:02d}:{m:02d}" for h in range(6, 24) for m in [0, 15, 30, 45]], 
            #                           index=0, key=f"reminder_{i}")
    else:
        st.success("🎉 Great job! You're on track or have completed your daily goal!")
    
    # Track Record
    st.markdown("### 📈 Today's Track Record")
    
    if st.session_state.consumption_log:
        df = pd.DataFrame(st.session_state.consumption_log)
        
        for idx, record in enumerate(st.session_state.consumption_log):
            st.markdown(f"""
            <div class="track-record">
                <strong>{record['time']}</strong> - Added {record['amount']}ml 💧
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No water consumed yet today. Start hydrating! 💧")
    
    # Reset button
    if st.button("🔄 Reset Today's Progress", type="secondary"):
        st.session_state.water_consumed = 0
        st.session_state.consumption_log = []
        st.rerun()

# Stage 3: Congratulations
elif st.session_state.stage == 'congratulations':
    st.markdown(f"""
    <div class="congratulations">
        <h1>🎉 Congratulations, {st.session_state.user_name}!</h1>
        <h2>💧 You've reached your daily hydration goal! 💧</h2>
        <p style="font-size: 1.2em;">Target: {st.session_state.water_target}ml ✅</p>
        <p style="font-size: 1.2em;">Consumed: {st.session_state.water_consumed}ml 🌟</p>
        <br>
        <h3>🌅 See you tomorrow morning for another healthy day!</h3>
        <p>Keep up the great work and stay hydrated! 🚀</p>
    </div>
    """, unsafe_allow_html=True)
    for idx, record in enumerate(st.session_state.consumption_log):
            st.markdown(f"""
            <div class="track-record">
                <strong>{record['time']}</strong> - Added {record['amount']}ml 💧
            </div>
            """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🔄 Start New Day", use_container_width=True, type="primary"):
            st.session_state.water_consumed = 0
            st.session_state.consumption_log = []
            st.session_state.stage = 'dashboard'
            st.rerun()
