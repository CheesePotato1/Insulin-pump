import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime
import time
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Insulin Pump Education Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .pump-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .patient-card {
        background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .alert-info {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = {}
if 'current_simulation' not in st.session_state:
    st.session_state.current_simulation = None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Insulin Pump Education Platform</h1>
        <h3>Interactive Learning for Medical Students</h3>
        <p>Master insulin pump therapy through comprehensive modules and real-world case studies</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress tracking
    progress_col1, progress_col2 = st.columns([3, 1])
    with progress_col1:
        st.progress(st.session_state.progress / 100)
    with progress_col2:
        st.metric("Progress", f"{st.session_state.progress}%")

    # Main navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🏠 Overview", 
        "🧬 Physiology", 
        "📱 Devices", 
        "⚙️ Settings & Calculations", 
        "🎮 CGM Simulation", 
        "👥 Patient Cases", 
        "📝 Assessment"
    ])
    
    with tab1:
        overview_tab()
    
    with tab2:
        physiology_tab()
    
    with tab3:
        devices_tab()
    
    with tab4:
        settings_tab()
    
    with tab5:
        simulation_tab()
    
    with tab6:
        patient_cases_tab()
    
    with tab7:
        assessment_tab()

def overview_tab():
    """Overview and learning objectives"""
    st.header("🎯 Learning Objectives")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### By completing this module, you will:
        - ✅ Understand insulin pump physiology and advantages over MDI
        - ✅ Compare major insulin pump systems (Omnipod, Tandem, Medtronic)
        - ✅ Master basal rate programming and bolus calculations
        - ✅ Interpret CGM data and automated insulin delivery systems
        - ✅ Manage complex patient scenarios using evidence-based protocols
        - ✅ Troubleshoot common pump problems and emergency situations
        """)
        
    with col2:
        st.markdown("""
        ### 📊 Course Structure
        1. **Foundations**: Basic pump physiology and benefits
        2. **Technology**: Device comparison and features
        3. **Programming**: Settings, calculations, and adjustments  
        4. **Integration**: CGM data and closed-loop systems
        5. **Clinical Practice**: Real patient cases and scenarios
        6. **Assessment**: Knowledge validation and competency testing
        """)
    
    # Evidence-based learning info
    st.markdown("""
    <div class="alert-info">
        <strong>💡 Evidence-Based Learning:</strong> This platform incorporates the latest 2024-2025 ADA Standards of Care, 
        clinical research findings, and real-world patient outcomes to provide you with current, practical knowledge.
    </div>
    """, unsafe_allow_html=True)
    
    # Key statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Time in Range Improvement", "8-15%", "vs MDI")
    with col2:
        st.metric("HbA1c Reduction", "0.2-0.3%", "average")
    with col3:
        st.metric("Severe Hypoglycemia", "↓70%", "reduction")
    with col4:
        st.metric("Patient Satisfaction", "90%+", "high ratings")

def physiology_tab():
    """Insulin pump physiology and mechanisms"""
    st.header("🧬 Insulin Pump Physiology")
    
    # Normal physiology explanation
    st.subheader("Normal Pancreatic Function")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Basal Insulin Secretion
        - **Continuous release**: 0.5-1.0 units/hour
        - **Circadian variation**: Higher during dawn hours
        - **Fasting maintenance**: Suppresses hepatic glucose output
        - **Represents 40-50%** of total daily insulin needs
        """)
        
    with col2:
        st.markdown("""
        #### Prandial Insulin Response  
        - **Rapid meal response**: 1-2 units per 10-15g carbs
        - **First phase**: Immediate release (0-10 minutes)
        - **Second phase**: Sustained release (10-120 minutes)  
        - **Represents 50-60%** of total daily insulin needs
        """)
    
    # Pump mechanism
    st.subheader("🔬 How Insulin Pumps Work")
    
    # Create physiologic insulin profile
    time_points = np.arange(0, 24, 0.5)
    basal_profile = []
    
    for hour in time_points:
        if 0 <= hour < 3:
            basal_profile.append(0.8)  # Midnight
        elif 3 <= hour < 6:
            basal_profile.append(1.2)  # Dawn phenomenon
        elif 6 <= hour < 11:
            basal_profile.append(0.9)  # Morning
        elif 11 <= hour < 18:
            basal_profile.append(0.7)  # Afternoon
        else:
            basal_profile.append(0.8)  # Evening
    
    # Add meal boluses
    bolus_times = [7, 12, 18]  # Breakfast, lunch, dinner
    bolus_amounts = [8, 6, 10]
    
    fig = go.Figure()
    
    # Basal rate
    fig.add_trace(go.Scatter(
        x=time_points,
        y=basal_profile,
        mode='lines',
        name='Basal Rate (U/hr)',
        line=dict(color='blue', width=3)
    ))
    
    # Add bolus markers
    for i, (time, amount) in enumerate(zip(bolus_times, bolus_amounts)):
        fig.add_trace(go.Scatter(
            x=[time],
            y=[amount],
            mode='markers',
            name=f'Bolus {amount}U',
            marker=dict(size=amount*2, color='red', symbol='triangle-up')
        ))
    
    fig.update_layout(
        title="24-Hour Insulin Delivery Profile",
        xaxis_title="Time (hours)",
        yaxis_title="Insulin Rate (units/hour or total units for bolus)",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Advantages over MDI
    st.subheader("🎯 Advantages Over Multiple Daily Injections")
    
    advantage_data = {
        'Outcome': ['HbA1c Reduction', 'Time in Range', 'Severe Hypoglycemia', 'Flexibility', 'Quality of Life'],
        'MDI': [8.1, '60%', '12 events/year', 'Limited', 'Good'],
        'Insulin Pump': [7.8, '75%', '4 events/year', 'Excellent', 'Excellent'],
        'Improvement': ['↓0.3%', '↑15%', '↓66%', '+++', '+++']
    }
    
    df = pd.DataFrame(advantage_data)
    st.table(df)
    
    # Interactive quiz
    st.subheader("🧠 Quick Knowledge Check")
    
    quiz_q1 = st.radio(
        "What percentage of total daily insulin is typically delivered as basal insulin?",
        ["20-30%", "40-50%", "60-70%", "80-90%"],
        key="phys_quiz_1"
    )
    
    if st.button("Check Answer", key="phys_check"):
        if quiz_q1 == "40-50%":
            st.success("✅ Correct! Basal insulin represents 40-50% of total daily needs.")
            st.session_state.progress = max(st.session_state.progress, 15)
        else:
            st.error("❌ Incorrect. Basal insulin typically represents 40-50% of total daily insulin needs.")

def devices_tab():
    """Insulin pump device comparison"""
    st.header("📱 Major Insulin Pump Systems")
    
    # Device comparison cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pump-card">
            <h3>🔵 Omnipod 5</h3>
            <p><strong>Tubeless Patch Pump</strong></p>
            <ul>
                <li>Waterproof design (IP28)</li>
                <li>3-day wear time</li>
                <li>SmartAdjust technology</li>
                <li>Dexcom G6/G7 integration</li>
                <li>No tubing disconnections</li>
                <li>Smartphone bolusing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Omnipod Details", key="omnipod_btn"):
            st.session_state.selected_pump = "omnipod"
    
    with col2:
        st.markdown("""
        <div class="pump-card">
            <h3>📱 Tandem t:slim X2</h3>
            <p><strong>Tubed with Touchscreen</strong></p>
            <ul>
                <li>Color touchscreen interface</li>
                <li>Control-IQ automated delivery</li>
                <li>Dexcom G6/G7 integration</li>
                <li>Micro-delivery (0.01U increments)</li>
                <li>Rechargeable battery</li>
                <li>Sleep/exercise modes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Tandem Details", key="tandem_btn"):
            st.session_state.selected_pump = "tandem"
    
    with col3:
        st.markdown("""
        <div class="pump-card">
            <h3>⚕️ Medtronic MiniMed 780G</h3>
            <p><strong>Advanced Auto Mode</strong></p>
            <ul>
                <li>SmartGuard auto-mode</li>
                <li>Guardian 4 CGM sensor</li>
                <li>Meal detection technology</li>
                <li>Customizable targets (100-120mg/dL)</li>
                <li>7-day extended sets</li>
                <li>CareLink data platform</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Medtronic Details", key="medtronic_btn"):
            st.session_state.selected_pump = "medtronic"
    
    # Detailed comparison table
    st.subheader("🔍 Detailed Feature Comparison")
    
    comparison_data = {
        'Feature': ['Design', 'CGM Integration', 'Automated Delivery', 'Basal Rates', 'Bolus Types', 'Battery', 'Waterproof', 'Data Platform'],
        'Omnipod 5': ['Tubeless patch', 'Dexcom G6/G7', 'SmartAdjust', '72 rates/day', 'Standard, Extended', 'Built-in', 'IP28 rating', 'Omnipod VIEW'],
        'Tandem t:slim X2': ['Tubed', 'Dexcom G6/G7', 'Control-IQ', '288 rates/day', 'Standard, Extended', 'Rechargeable', 'IPX8', 't:connect'],
        'Medtronic 780G': ['Tubed', 'Guardian 4', 'SmartGuard', '288 rates/day', 'Standard, Square, Dual', 'AA battery', 'IPX8', 'CareLink']
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True)
    
    # Clinical outcomes comparison
    st.subheader("📊 Real-World Clinical Outcomes")
    
    outcomes_data = {
        'System': ['Omnipod 5', 'Tandem Control-IQ', 'Medtronic 780G'],
        'Time in Range (%)': [73.9, 71.0, 75.8],
        'Time Below Range (%)': [1.6, 2.1, 1.8],
        'HbA1c (%)': [7.16, 7.1, 7.3],
        'User Satisfaction': [4.6, 4.5, 4.2]
    }
    
    df_outcomes = pd.DataFrame(outcomes_data)
    
    # Create comparison chart
    fig = px.bar(df_outcomes, x='System', y='Time in Range (%)', 
                 title='Time in Range Comparison (70-180 mg/dL)',
                 color='System')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Patient matching guide
    st.subheader("🎯 Patient-Device Matching Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Choose Omnipod for:
        - Active patients (sports, swimming)
        - Children and teens
        - Patients who dislike tubing
        - Those wanting discrete delivery
        - Frequent travelers
        """)
        
    with col2:
        st.markdown("""
        #### Choose Tandem for:
        - Tech-savvy users
        - Patients wanting precise control
        - Those comfortable with touchscreens
        - Users prioritizing customization
        """)
    
    with col1:
        st.markdown("""
        #### Choose Medtronic for:
        - Patients with variable carb intake
        - Those frequently missing meal boluses
        - Users wanting integrated CGM system
        - Patients preferring traditional interface
        """)

def settings_tab():
    """Pump settings and calculations"""
    st.header("⚙️ Insulin Pump Settings & Calculations")
    
    # Basal rate programming
    st.subheader("🕐 Basal Rate Programming")
    
    st.markdown("""
    **Key Principles:**
    - Start with 40-50% of total daily insulin dose
    - Program based on physiologic patterns
    - Adjust in 0.1 U/hr increments
    - Test during fasting periods
    """)
    
    # Interactive basal rate calculator
    st.subheader("🧮 Basal Rate Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_daily_dose = st.number_input("Total Daily Insulin Dose (units)", min_value=10, max_value=100, value=40)
        patient_weight = st.number_input("Patient Weight (kg)", min_value=20, max_value=120, value=70)
        age_group = st.selectbox("Age Group", ["Child (5-12)", "Adolescent (13-18)", "Adult (19-65)", "Elderly (65+)"])
    
    with col2:
        basal_percentage = st.slider("Basal Percentage of TDD", min_value=35, max_value=55, value=45)
        st.write(f"**Basal insulin needed:** {total_daily_dose * basal_percentage / 100:.1f} units/day")
        st.write(f"**Average basal rate:** {total_daily_dose * basal_percentage / 100 / 24:.2f} units/hour")
    
    # Generate basal profile based on age
    basal_times = ["Midnight", "3:00 AM", "6:00 AM", "9:00 AM", "Noon", "3:00 PM", "6:00 PM", "9:00 PM"]
    
    if age_group == "Adult (19-65)":
        basal_multipliers = [0.8, 1.2, 1.0, 0.9, 0.8, 0.7, 0.8, 0.9]  # Dawn phenomenon
    elif age_group == "Adolescent (13-18)":
        basal_multipliers = [0.9, 1.3, 1.1, 1.0, 0.8, 0.7, 0.8, 1.0]  # Strong dawn effect
    elif age_group == "Child (5-12)":
        basal_multipliers = [0.7, 0.6, 0.8, 1.0, 1.1, 1.2, 1.1, 0.9]  # Reverse pattern
    else:  # Elderly
        basal_multipliers = [0.9, 1.0, 1.0, 0.9, 0.8, 0.7, 0.8, 0.9]  # Flatter profile
    
    base_rate = total_daily_dose * basal_percentage / 100 / 24
    basal_rates = [base_rate * mult for mult in basal_multipliers]
    
    basal_df = pd.DataFrame({
        'Time': basal_times,
        'Rate (U/hr)': [f"{rate:.2f}" for rate in basal_rates],
        'Rationale': [
            'Overnight maintenance',
            'Dawn phenomenon peak',
            'Post-dawn adjustment', 
            'Morning activity',
            'Midday lowest',
            'Afternoon activity',
            'Evening meals',
            'Pre-sleep'
        ]
    })
    
    st.dataframe(basal_df, use_container_width=True)
    
    # Bolus calculations
    st.subheader("🍽️ Bolus Calculation Tools")
    
    tab1, tab2, tab3 = st.tabs(["Insulin:Carb Ratios", "Correction Factors", "Bolus Calculator"])
    
    with tab1:
        st.markdown("### Insulin-to-Carbohydrate Ratios")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Starting Formula (Weight-based):**
            - I:C Ratio = (5.7 × weight in kg) ÷ TDD
            - More accurate than traditional 500 rule
            - Adjust based on meals and timing
            """)
            
        with col2:
            ic_weight_based = (5.7 * patient_weight) / total_daily_dose
            st.metric("Calculated I:C Ratio", f"1:{ic_weight_based:.0f}")
            
            breakfast_ic = st.number_input("Breakfast I:C", value=int(ic_weight_based * 0.8), key="b_ic")
            lunch_ic = st.number_input("Lunch I:C", value=int(ic_weight_based), key="l_ic")  
            dinner_ic = st.number_input("Dinner I:C", value=int(ic_weight_based * 1.2), key="d_ic")
    
    with tab2:
        st.markdown("### Correction Factor Calculation")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **1800 Rule (Standard):**
            - CF = 1800 ÷ Total Daily Dose
            - Use for most patients
            
            **1960 Rule (Well-controlled):**
            - CF = 1960 ÷ Total Daily Dose  
            - Use for HbA1c < 7%
            """)
            
        with col2:
            cf_standard = 1800 / total_daily_dose
            cf_controlled = 1960 / total_daily_dose
            
            st.metric("Standard CF", f"{cf_standard:.0f} mg/dL per unit")
            st.metric("Well-controlled CF", f"{cf_controlled:.0f} mg/dL per unit")
            
            target_bg = st.number_input("Target Blood Glucose", value=120, min_value=80, max_value=150)
    
    with tab3:
        st.markdown("### Interactive Bolus Calculator")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            current_bg = st.number_input("Current BG (mg/dL)", value=180, min_value=50, max_value=400)
            carbs = st.number_input("Carbohydrates (g)", value=45, min_value=0, max_value=150)
            meal_time = st.selectbox("Meal", ["Breakfast", "Lunch", "Dinner"])
        
        with col2:
            # Select appropriate I:C ratio
            if meal_time == "Breakfast":
                ic_ratio = breakfast_ic
            elif meal_time == "Lunch":
                ic_ratio = lunch_ic
            else:
                ic_ratio = dinner_ic
                
            correction_factor = cf_standard
            
            # Calculate boluses
            food_bolus = carbs / ic_ratio
            correction_bolus = max(0, (current_bg - target_bg) / correction_factor)
            total_bolus = food_bolus + correction_bolus
            
            st.metric("Food Bolus", f"{food_bolus:.1f} units")
            st.metric("Correction Bolus", f"{correction_bolus:.1f} units") 
            st.metric("**Total Bolus**", f"{total_bolus:.1f} units")
            
        with col3:
            st.markdown("#### Calculation Details:")
            st.write(f"• Food: {carbs}g ÷ {ic_ratio} = {food_bolus:.1f}U")
            st.write(f"• Correction: ({current_bg} - {target_bg}) ÷ {correction_factor:.0f} = {correction_bolus:.1f}U")
            
            if current_bg < 70:
                st.error("⚠️ Hypoglycemia - Treat with glucose first!")
            elif current_bg > 250:
                st.warning("⚠️ Consider checking ketones")
    
    # Advanced bolus features
    st.subheader("🎯 Advanced Bolus Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Extended/Square Wave Bolus
        - **Use for:** High-fat meals, gastroparesis
        - **Duration:** 2-8 hours
        - **Example:** Pizza - 50% now, 50% over 3 hours
        """)
        
        duration = st.slider("Extended Duration (hours)", 1, 8, 3)
        immediate_percent = st.slider("Immediate %", 0, 100, 50)
        
        st.write(f"Immediate: {total_bolus * immediate_percent / 100:.1f}U")
        st.write(f"Extended: {total_bolus * (100 - immediate_percent) / 100:.1f}U over {duration}h")
        
    with col2:
        st.markdown("""
        #### Dual Wave Bolus  
        - **Use for:** Mixed meals (protein + carbs)
        - **Combines:** Standard + Extended
        - **Example:** Pasta dinner - Normal + extended for protein
        """)
        
        if st.checkbox("Enable Dual Wave"):
            wave1_percent = st.slider("Wave 1 %", 30, 70, 60)
            wave2_duration = st.slider("Wave 2 Duration", 2, 6, 4)
            
            st.write(f"Wave 1: {total_bolus * wave1_percent / 100:.1f}U (immediate)")
            st.write(f"Wave 2: {total_bolus * (100 - wave1_percent) / 100:.1f}U over {wave2_duration}h")

def simulation_tab():
    """CGM and pump simulation"""
    st.header("🎮 Continuous Glucose Monitoring Simulation")
    
    st.markdown("""
    This interactive simulation demonstrates how insulin pump therapy responds to various scenarios.
    You can observe glucose patterns, make pump adjustments, and see real-time outcomes.
    """)
    
    # Simulation controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sim_speed = st.selectbox("Simulation Speed", ["Real-time", "1 hour/minute", "4 hours/minute"], index=1)
        patient_type = st.selectbox("Patient Profile", ["Normal", "Dawn Phenomenon", "Gastroparesis", "Athletic"])
        
    with col2:
        basal_rate = st.number_input("Current Basal (U/hr)", value=1.0, min_value=0.1, max_value=3.0, step=0.1)
        ic_ratio = st.number_input("I:C Ratio", value=12, min_value=5, max_value=25)
        
    with col3:
        target_range = st.slider("Target Range", 70, 180, (80, 150))
        st.write(f"Target: {target_range[0]}-{target_range[1]} mg/dL")
    
    # Generate simulation data
    if 'sim_data' not in st.session_state:
        st.session_state.sim_data = generate_glucose_data(patient_type)
    
    if st.button("🔄 Reset Simulation"):
        st.session_state.sim_data = generate_glucose_data(patient_type)
    
    # Real-time glucose chart
    fig = create_glucose_chart(st.session_state.sim_data, target_range)
    st.plotly_chart(fig, use_container_width=True)
    
    # Current status
    current_glucose = st.session_state.sim_data['glucose'].iloc[-1]
    current_trend = calculate_trend(st.session_state.sim_data['glucose'].tail(3).tolist())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if current_glucose < 70:
            st.error(f"🔴 {current_glucose:.0f} mg/dL")
        elif current_glucose > 180:
            st.warning(f"🟡 {current_glucose:.0f} mg/dL")
        else:
            st.success(f"🟢 {current_glucose:.0f} mg/dL")
    
    with col2:
        trend_arrow = get_trend_arrow(current_trend)
        st.metric("Trend", trend_arrow)
        
    with col3:
        time_in_range = calculate_time_in_range(st.session_state.sim_data['glucose'], target_range)
        st.metric("Time in Range", f"{time_in_range:.1f}%")
        
    with col4:
        active_insulin = calculate_active_insulin(st.session_state.sim_data)
        st.metric("Active Insulin", f"{active_insulin:.1f}U")
    
    # Intervention buttons
    st.subheader("🎛️ Interventions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💉 Give Correction Bolus"):
            correction = max(0, (current_glucose - 120) / 40)
            st.info(f"Calculated correction: {correction:.1f} units")
            add_intervention("bolus", correction)
            
    with col2:
        if st.button("🍽️ Meal + Bolus"):
            carbs = st.number_input("Carbs (g)", value=45, key="meal_carbs")
            meal_bolus = carbs / ic_ratio
            st.info(f"Meal bolus: {meal_bolus:.1f} units")
            add_intervention("meal", carbs)
            
    with col3:
        if st.button("🏃 Exercise"):
            exercise_intensity = st.selectbox("Intensity", ["Light", "Moderate", "Vigorous"], key="exercise_intensity")
            st.info(f"Starting {exercise_intensity.lower()} exercise")
            add_intervention("exercise", exercise_intensity)
            
    with col4:
        if st.button("⚙️ Adjust Basal"):
            temp_basal = st.number_input("Temp Basal (%)", value=50, min_value=0, max_value=200, key="temp_basal")
            st.info(f"Temp basal: {temp_basal}% for 2 hours")
            add_intervention("temp_basal", temp_basal)
    
    # CGM alerts simulation
    if current_glucose < 70:
        st.error("🚨 LOW GLUCOSE ALERT - Treat immediately with 15g fast-acting carbs!")
    elif current_glucose > 250:
        st.error("🚨 HIGH GLUCOSE ALERT - Check ketones and consider correction!")
    elif current_trend < -2:
        st.warning("⚠️ FALLING RAPIDLY - Monitor closely")
    elif current_trend > 2:
        st.warning("⚠️ RISING RAPIDLY - Consider intervention")

def patient_cases_tab():
    """Longitudinal patient case studies"""
    st.header("👥 Longitudinal Patient Cases")
    
    st.markdown("""
    Follow 10 diverse patients over one year of insulin pump therapy. Each case demonstrates 
    real-world challenges and evidence-based management strategies.
    """)
    
    # Patient selection
    patient_cases = {
        "Emma (8y/o)": {
            "description": "Newly diagnosed T1DM, started Omnipod 3 months ago",
            "current_a1c": 7.8,
            "target_a1c": 7.0,
            "challenges": ["School management", "Growth spurts", "Family dynamics"],
            "pump": "Omnipod 5",
            "timeline": "Month 3 of 12"
        },
        "Marcus (16y/o)": {
            "description": "Poor control on MDI, resistant to pump therapy initially",
            "current_a1c": 9.2,
            "target_a1c": 7.5,
            "challenges": ["Peer pressure", "Body image", "Independence vs safety"],
            "pump": "Tandem t:slim X2",
            "timeline": "Month 6 of 12"
        },
        "Sarah (28y/o)": {
            "description": "Professional athlete transitioning from MDI",
            "current_a1c": 7.1,
            "target_a1c": 6.8,
            "challenges": ["Exercise management", "Travel", "Competition stress"],
            "pump": "Omnipod 5",
            "timeline": "Month 8 of 12"
        },
        "Robert (72y/o)": {
            "description": "Elderly patient needing simplified management",
            "current_a1c": 8.0,
            "target_a1c": 7.5,
            "challenges": ["Cognitive decline", "Dexterity issues", "Safety focus"],
            "pump": "Medtronic 780G",
            "timeline": "Month 4 of 12"
        },
        "Lisa (45y/o)": {
            "description": "T1DM with gastroparesis and hypoglycemia unawareness",
            "current_a1c": 8.5,
            "target_a1c": 7.8,
            "challenges": ["Gastroparesis", "Hypoglycemia unawareness", "Complications"],
            "pump": "Tandem t:slim X2",
            "timeline": "Month 10 of 12"
        }
    }
    
    selected_patient = st.selectbox("Select Patient Case", list(patient_cases.keys()))
    
    if selected_patient:
        case = patient_cases[selected_patient]
        
        # Patient overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="patient-card">
                <h3>{selected_patient}</h3>
                <p>{case['description']}</p>
                <p><strong>Pump:</strong> {case['pump']}</p>
                <p><strong>Timeline:</strong> {case['timeline']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.metric("Current A1C", f"{case['current_a1c']}%")
            st.metric("Target A1C", f"{case['target_a1c']}%")
            
        with col3:
            st.markdown("**Key Challenges:**")
            for challenge in case['challenges']:
                st.write(f"• {challenge}")
        
        # Detailed case study
        if selected_patient == "Emma (8y/o)":
            show_emma_case()
        elif selected_patient == "Marcus (16y/o)":
            show_marcus_case()
        elif selected_patient == "Sarah (28y/o)":
            show_sarah_case()
        elif selected_patient == "Robert (72y/o)":
            show_robert_case()
        elif selected_patient == "Lisa (45y/o)":
            show_lisa_case()

def show_emma_case():
    """Detailed view of Emma's case - pediatric newly diagnosed"""
    st.subheader("👧 Emma's Journey: Pediatric T1DM Management")
    
    # Timeline visualization
    timeline_data = {
        'Month': ['Diagnosis', 'Month 1', 'Month 2', 'Month 3', 'Month 6', 'Month 9', 'Month 12'],
        'A1C (%)': [12.5, 9.2, 8.1, 7.8, 7.2, 7.0, 6.9],
        'Key Events': [
            'DKA presentation',
            'Omnipod start',
            'School training',
            'First growth spurt',
            'Sleepover success',
            'Sports participation',
            'Family independence'
        ]
    }
    
    timeline_df = pd.DataFrame(timeline_data)
    
    fig = px.line(timeline_df, x='Month', y='A1C (%)', 
                  title="Emma's A1C Progression Over Time",
                  markers=True)
    fig.add_hline(y=7.0, line_dash="dash", line_color="green", 
                  annotation_text="Target A1C")
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Current status and challenges
    st.subheader("Current Status (Month 3)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Achievements:**
        - Successfully transitioned to Omnipod
        - Parents confident with pump management
        - School nurse trained and supportive
        - A1C improved from 12.5% to 7.8%
        """)
        
    with col2:
        st.markdown("""
        **Ongoing Challenges:**
        - Occasional missed boluses at school
        - Dawn phenomenon requiring basal adjustments
        - Upcoming growth spurt considerations
        - Peer questions about device
        """)
    
    # Clinical decision points
    st.subheader("🎯 Clinical Decision Points")
    
    decision_scenario = st.radio(
        "Emma's teacher reports her glucose was 250 mg/dL before lunch. What's your priority?",
        [
            "Give correction bolus immediately",
            "Check for ketones first", 
            "Investigate missed breakfast bolus",
            "Call parents immediately"
        ]
    )
    
    if st.button("Submit Decision", key="emma_decision"):
        if decision_scenario == "Check for ketones first":
            st.success("""
            ✅ Correct! In pediatric patients with BG >250 mg/dL:
            1. Check ketones (blood preferred)
            2. If ketones >0.6 mmol/L, treat as DKA
            3. Investigate cause (missed bolus, illness, pump failure)
            4. Notify parents regardless of ketone level
            """)
        else:
            st.info("""
            Consider the comprehensive approach:
            - Always check ketones when BG >250 mg/dL in children
            - Ketone levels guide treatment intensity
            - School personnel need clear protocols
            """)

def show_marcus_case():
    """Detailed view of Marcus's case - adolescent with poor control"""
    st.subheader("👨‍🎓 Marcus's Journey: Adolescent Engagement Challenges")
    
    # Behavioral assessment
    st.markdown("""
    **Background:** Marcus was diagnosed at age 12. Initially compliant, but control deteriorated during adolescence.
    Parents report frequent arguments about diabetes management. Recent A1C 9.2% prompted pump evaluation.
    """)
    
    # Progress tracking with behavioral markers
    progress_data = {
        'Month': ['Baseline', 'Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6'],
        'A1C (%)': [9.2, 8.8, 8.9, 8.5, 8.1, 7.9, 7.6],
        'Pump Usage (%)': [60, 75, 70, 85, 88, 92, 94],
        'Self-Care Score': [3, 4, 4, 6, 7, 8, 8]
    }
    
    progress_df = pd.DataFrame(progress_data)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=progress_df['Month'], y=progress_df['A1C (%)'], name="A1C", line=dict(color='red')),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=progress_df['Month'], y=progress_df['Pump Usage (%)'], name="Pump Usage", line=dict(color='blue')),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="A1C (%)", secondary_y=False)
    fig.update_yaxes(title_text="Pump Usage (%)", secondary_y=True)
    fig.update_layout(title="Marcus's Progress: A1C vs Pump Engagement")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Motivational interviewing scenario
    st.subheader("💬 Motivational Interviewing Practice")
    
    st.markdown("""
    **Scenario:** Marcus says, "I hate this pump. My friends think it's weird, and I feel like a robot."
    """)
    
    response_choice = st.radio(
        "Choose your therapeutic response:",
        [
            "The pump will help prevent complications later in life",
            "Tell me more about how the pump makes you feel different",
            "Your friends will get used to it - diabetes is nothing to be ashamed of",
            "What would need to change for the pump to feel more acceptable?"
        ]
    )
    
    if st.button("Analyze Response", key="marcus_response"):
        if response_choice == "Tell me more about how the pump makes you feel different":
            st.success("""
            ✅ Excellent! This response:
            - Uses open-ended questions
            - Shows empathy and curiosity
            - Avoids defensiveness about the pump
            - Allows Marcus to express his concerns fully
            """)
        elif response_choice == "What would need to change for the pump to feel more acceptable?":
            st.success("""
            ✅ Great choice! This response:
            - Assumes pump continuation while addressing concerns
            - Empowers Marcus in problem-solving
            - Focuses on modifiable factors
            - Builds collaborative relationship
            """)
        else:
            st.warning("""
            ⚠️ Consider these approaches:
            - Avoid lecturing about future complications
            - Don't minimize his social concerns
            - Focus on understanding his perspective first
            - Use motivational interviewing techniques
            """)

def show_sarah_case():
    """Detailed view of Sarah's case - athletic adult"""
    st.subheader("🏃‍♀️ Sarah's Journey: Athletic Performance Optimization")
    
    st.markdown("""
    **Background:** Professional triathlete with T1DM since age 16. Excellent control on MDI but seeking 
    better flexibility for training and competition. Recently started Omnipod 5 with Dexcom G7.
    """)
    
    # Exercise management protocols
    st.subheader("🏋️ Exercise Management Protocols")
    
    exercise_protocols = {
        'Exercise Type': ['Aerobic (>30 min)', 'High Intensity (<10 min)', 'Mixed Training', 'Competition'],
        'Pre-Exercise BG': ['150-180 mg/dL', '120-150 mg/dL', '140-180 mg/dL', '140-160 mg/dL'],
        'Basal Adjustment': ['50% reduction 1hr prior', 'No change', '70% reduction 30min prior', 'Individual plan'],
        'CHO Strategy': ['15-30g/hr if needed', 'Pre-load 15-30g', '15-45g/hr depending', 'Competition-specific']
    }
    
    exercise_df = pd.DataFrame(exercise_protocols)
    st.table(exercise_df)
    
    # Competition scenario
    st.subheader("🏆 Competition Day Challenge")
    
    st.markdown("""
    **Scenario:** Sarah has a triathlon starting at 7:00 AM. Current BG is 95 mg/dL at 5:00 AM.
    She typically eats 60g carbs pre-race and swims for 45 minutes first.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Pre-race decisions needed:**")
        pre_race_carbs = st.number_input("Pre-race carbs (g)", value=30, min_value=0, max_value=80)
        basal_reduction = st.slider("Basal reduction (%)", 0, 100, 50)
        
    with col2:
        st.markdown("**Calculated recommendations:**")
        target_bg = 140  # Ideal pre-exercise
        current_bg = 95
        
        # Carbs needed to reach target
        carbs_needed = (target_bg - current_bg) / 4  # Approximate 4 mg/dL per gram
        
        st.write(f"Carbs to reach 140 mg/dL: ~{carbs_needed:.0f}g")
        st.write(f"Total pre-race carbs: {pre_race_carbs}g")
        st.write(f"Basal reduction: {basal_reduction}%")
        
        if pre_race_carbs >= 25 and basal_reduction >= 30:
            st.success("✅ Good strategy for endurance exercise")
        else:
            st.warning("⚠️ Consider more aggressive preparation")

def show_robert_case():
    """Detailed view of Robert's case - elderly patient"""
    st.subheader("👴 Robert's Journey: Geriatric Diabetes Management")
    
    st.markdown("""
    **Background:** 72-year-old with T1DM for 35 years. Recent mild cognitive impairment and dexterity issues.
    Wife provides significant support. Chose Medtronic 780G for simplicity and automated features.
    """)
    
    # Geriatric considerations
    st.subheader("🎯 Geriatric-Specific Modifications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Safety Modifications:**
        - Higher glucose targets (100-200 mg/dL)
        - Simplified basal patterns (fewer rate changes)
        - Longer duration of insulin action (5-6 hours)
        - Maximum bolus limits (15 units)
        - Simplified menu options
        """)
        
    with col2:
        st.markdown("""
        **Support Systems:**
        - Caregiver training (wife)
        - Large-button remote
        - Audible alarms increased
        - Weekly nurse visits
        - Emergency contact protocols
        """)
    
    # Hypoglycemia risk assessment
    st.subheader("⚠️ Hypoglycemia Risk Assessment")
    
    risk_factors = st.multiselect(
        "Select applicable risk factors:",
        [
            "Age >70 years",
            "Cognitive impairment", 
            "Living alone",
            "Multiple medications",
            "Renal insufficiency",
            "Hypoglycemia unawareness",
            "Previous severe hypoglycemia"
        ],
        default=["Age >70 years", "Cognitive impairment"]
    )
    
    risk_score = len(risk_factors)
    
    if risk_score >= 3:
        st.error(f"🔴 HIGH RISK ({risk_score} factors) - Consider glucose targets 120-200 mg/dL")
    elif risk_score >= 2:
        st.warning(f"🟡 MODERATE RISK ({risk_score} factors) - Targets 100-180 mg/dL acceptable")
    else:
        st.success(f"🟢 LOWER RISK ({risk_score} factors) - Standard targets possible")

def show_lisa_case():
    """Detailed view of Lisa's case - complications management"""
    st.subheader("👩 Lisa's Journey: Managing Diabetes Complications")
    
    st.markdown("""
    **Background:** 45-year-old with T1DM for 28 years. Developed gastroparesis 5 years ago and 
    hypoglycemia unawareness. Recently started Tandem t:slim X2 with Control-IQ for better hypoglycemia protection.
    """)
    
    # Gastroparesis management
    st.subheader("🍽️ Gastroparesis Management Strategies")
    
    tab1, tab2, tab3 = st.tabs(["Bolus Strategies", "Meal Planning", "Monitoring"])
    
    with tab1:
        st.markdown("""
        **Extended Bolus Protocols:**
        - Liquid meals: 70% immediate, 30% over 2 hours
        - Solid meals: 40% immediate, 60% over 4 hours  
        - High-fat meals: 30% immediate, 70% over 6 hours
        - Gastroparesis flare: Consider post-meal bolusing
        """)
        
        meal_type = st.selectbox("Select meal type", ["Liquid (smoothie)", "Regular solid", "High-fat (pizza)", "Gastroparesis flare"])
        total_bolus = st.number_input("Total bolus needed (units)", value=8.0)
        
        if meal_type == "Liquid (smoothie)":
            immediate = total_bolus * 0.7
            extended = total_bolus * 0.3
            duration = 2
        elif meal_type == "Regular solid":
            immediate = total_bolus * 0.4
            extended = total_bolus * 0.6
            duration = 4
        elif meal_type == "High-fat (pizza)":
            immediate = total_bolus * 0.3
            extended = total_bolus * 0.7
            duration = 6
        else:  # Gastroparesis flare
            immediate = 0
            extended = total_bolus
            duration = 8
            
        st.write(f"**Recommended split:**")
        st.write(f"• Immediate: {immediate:.1f} units")
        st.write(f"• Extended: {extended:.1f} units over {duration} hours")
        
    with tab2:
        st.markdown("""
        **Meal Composition Guidelines:**
        - Prefer liquid calories during flares
        - Avoid high-fiber foods
        - Small, frequent meals (6 per day)
        - Avoid carbonated beverages
        - Consider prokinetic medications timing
        """)
        
    with tab3:
        st.markdown("""
        **Enhanced Monitoring:**
        - CGM critical for delayed glucose rises
        - Post-meal monitoring up to 6 hours
        - Trend arrows more important than current value
        - Consider professional CGM during med changes
        """)

def assessment_tab():
    """Knowledge assessment and competency validation"""
    st.header("📝 Knowledge Assessment & Competency Validation")
    
    st.markdown("""
    Test your understanding of insulin pump therapy through clinical scenarios and knowledge questions.
    This assessment covers all major learning objectives.
    """)
    
    # Assessment sections
    assessment_type = st.selectbox(
        "Choose assessment type:",
        ["Quick Knowledge Check", "Clinical Scenario Assessment", "Calculation Competency", "Final Comprehensive Exam"]
    )
    
    if assessment_type == "Quick Knowledge Check":
        quick_knowledge_assessment()
    elif assessment_type == "Clinical Scenario Assessment":
        clinical_scenario_assessment()
    elif assessment_type == "Calculation Competency":
        calculation_competency()
    else:
        comprehensive_exam()

def quick_knowledge_assessment():
    """Quick multiple choice questions"""
    st.subheader("⚡ Quick Knowledge Check")
    
    questions = [
        {
            "question": "What percentage of total daily insulin is typically delivered as basal insulin in pump therapy?",
            "options": ["20-30%", "40-50%", "60-70%", "80-90%"],
            "correct": 1,
            "explanation": "Basal insulin represents 40-50% of total daily insulin needs, mimicking normal pancreatic function."
        },
        {
            "question": "Which insulin pump feature is most important for managing gastroparesis?",
            "options": ["Waterproof design", "Extended/dual-wave bolus", "Smartphone connectivity", "Small size"],
            "correct": 1,
            "explanation": "Extended and dual-wave boluses allow insulin delivery to match delayed gastric emptying."
        },
        {
            "question": "What is the primary advantage of tubeless pump systems?",
            "options": ["Better glucose control", "Reduced disconnection risk", "Longer battery life", "Lower cost"],
            "correct": 1,
            "explanation": "Tubeless systems eliminate tubing disconnections, a common cause of missed insulin delivery."
        },
        {
            "question": "For exercise >30 minutes, basal rates should typically be reduced by:",
            "options": ["10-25%", "25-50%", "50-75%", "75-100%"],
            "correct": 1,
            "explanation": "Most patients need 25-50% basal reduction for prolonged aerobic exercise to prevent hypoglycemia."
        }
    ]
    
    score = 0
    total_questions = len(questions)
    
    for i, q in enumerate(questions):
        st.markdown(f"**Question {i+1}:** {q['question']}")
        
        user_answer = st.radio(
            "Select your answer:",
            q['options'],
            key=f"q_{i}"
        )
        
        if st.button(f"Check Answer {i+1}", key=f"check_{i}"):
            user_index = q['options'].index(user_answer)
            if user_index == q['correct']:
                st.success(f"✅ Correct! {q['explanation']}")
                score += 1
            else:
                st.error(f"❌ Incorrect. {q['explanation']}")
        
        st.markdown("---")
    
    if st.button("Calculate Final Score"):
        percentage = (score / total_questions) * 100
        st.metric("Final Score", f"{percentage:.0f}%")
        
        if percentage >= 80:
            st.success("🎉 Excellent work! You have strong foundational knowledge.")
            st.session_state.progress = max(st.session_state.progress, 85)
        elif percentage >= 60:
            st.warning("👍 Good job! Review the areas you missed.")
            st.session_state.progress = max(st.session_state.progress, 70)
        else:
            st.error("📚 Keep studying! Review the course material and try again.")

def clinical_scenario_assessment():
    """Complex clinical scenarios"""
    st.subheader("🏥 Clinical Scenario Assessment")
    
    scenario = st.selectbox(
        "Choose a clinical scenario:",
        [
            "Dawn Phenomenon Management",
            "Exercise-Induced Hypoglycemia", 
            "Sick Day Management",
            "Pump Malfunction Emergency"
        ]
    )
    
    if scenario == "Dawn Phenomenon Management":
        st.markdown("""
        **Case:** 16-year-old Marcus shows consistent glucose elevation from 4:00-8:00 AM despite 
        good overnight control. Current basal rates are flat at 0.9 U/hr throughout the night.
        
        **Current pattern:**
        - Bedtime (10 PM): 120 mg/dL
        - 2:00 AM: 115 mg/dL  
        - 6:00 AM: 180 mg/dL
        - Pre-breakfast: 220 mg/dL
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**What is your management plan?**")
            
            management_choice = st.radio(
                "Primary intervention:",
                [
                    "Increase dinner rapid-acting insulin",
                    "Add bedtime NPH insulin",
                    "Increase basal rates 3:00-8:00 AM",
                    "Change to different rapid-acting analog"
                ]
            )
            
        with col2:
            st.markdown("**Proposed basal adjustments:**")
            
            midnight_rate = st.number_input("Midnight-3 AM (U/hr)", value=0.9, step=0.1)
            dawn_rate = st.number_input("3-8 AM (U/hr)", value=1.2, step=0.1)
            morning_rate = st.number_input("8-11 AM (U/hr)", value=0.9, step=0.1)
            
        if st.button("Submit Management Plan"):
            if management_choice == "Increase basal rates 3:00-8:00 AM" and dawn_rate > 1.0:
                st.success("""
                ✅ Excellent management! Dawn phenomenon requires:
                - Increased basal rates during 3:00-8:00 AM
                - Gradual adjustments (0.1-0.2 U/hr increases)
                - Monitor for hypoglycemia risk
                - May need different rates for weekdays vs weekends
                """)
            else:
                st.warning("""
                Consider the pump-specific approach:
                - Dawn phenomenon is best managed with basal rate adjustments
                - Increase rates 2-3 hours before glucose rise
                - Avoid adding other insulin types when using pump therapy
                """)

def calculation_competency():
    """Insulin calculation assessments"""
    st.subheader("🧮 Calculation Competency Assessment")
    
    st.markdown("Demonstrate your ability to perform essential insulin pump calculations.")
    
    # Generate random patient parameters
    if 'calc_patient' not in st.session_state:
        np.random.seed(42)  # For reproducible results
        st.session_state.calc_patient = {
            'weight': np.random.randint(60, 90),
            'tdd': np.random.randint(35, 65),
            'current_bg': np.random.randint(150, 280),
            'carbs': np.random.randint(30, 80)
        }
    
    patient = st.session_state.calc_patient
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Patient Parameters:**
        - Weight: {patient['weight']} kg
        - Total Daily Dose: {patient['tdd']} units
        - Current BG: {patient['current_bg']} mg/dL
        - Planned carbs: {patient['carbs']} g
        - Target BG: 120 mg/dL
        """)
        
    with col2:
        st.markdown("**Your Calculations:**")
        
        # Basal calculation
        basal_calc = st.number_input("Total daily basal insulin (units)", value=0.0, step=0.1)
        
        # I:C ratio calculation  
        ic_calc = st.number_input("I:C ratio (1:X)", value=0, step=1)
        
        # Correction factor
        cf_calc = st.number_input("Correction factor (mg/dL per unit)", value=0, step=5)
        
        # Total bolus
        total_bolus_calc = st.number_input("Total bolus needed (units)", value=0.0, step=0.1)
    
    if st.button("Check All Calculations"):
        # Correct answers
        correct_basal = patient['tdd'] * 0.45  # 45% for basal
        correct_ic = round((5.7 * patient['weight']) / patient['tdd'])
        correct_cf = round(1800 / patient['tdd'])
        
        food_bolus = patient['carbs'] / correct_ic
        correction_bolus = max(0, (patient['current_bg'] - 120) / correct_cf)
        correct_total = food_bolus + correction_bolus
        
        results = []
        
        # Check basal
        if abs(basal_calc - correct_basal) <= 1.0:
            results.append("✅ Basal calculation correct")
        else:
            results.append(f"❌ Basal: Expected {correct_basal:.1f} units, got {basal_calc:.1f}")
            
        # Check I:C
        if abs(ic_calc - correct_ic) <= 2:
            results.append("✅ I:C ratio correct")
        else:
            results.append(f"❌ I:C ratio: Expected 1:{correct_ic}, got 1:{ic_calc}")
            
        # Check CF
        if abs(cf_calc - correct_cf) <= 10:
            results.append("✅ Correction factor correct") 
        else:
            results.append(f"❌ Correction factor: Expected {correct_cf}, got {cf_calc}")
            
        # Check total bolus
        if abs(total_bolus_calc - correct_total) <= 0.5:
            results.append("✅ Total bolus correct")
        else:
            results.append(f"❌ Total bolus: Expected {correct_total:.1f} units, got {total_bolus_calc:.1f}")
        
        for result in results:
            if "✅" in result:
                st.success(result)
            else:
                st.error(result)
        
        # Show detailed breakdown
        st.markdown("**Detailed Solution:**")
        st.write(f"1. Basal insulin: {patient['tdd']} × 0.45 = {correct_basal:.1f} units/day")
        st.write(f"2. I:C ratio: (5.7 × {patient['weight']}) ÷ {patient['tdd']} = 1:{correct_ic}")
        st.write(f"3. Correction factor: 1800 ÷ {patient['tdd']} = {correct_cf} mg/dL per unit")
        st.write(f"4. Food bolus: {patient['carbs']} ÷ {correct_ic} = {food_bolus:.1f} units")
        st.write(f"5. Correction bolus: ({patient['current_bg']} - 120) ÷ {correct_cf} = {correction_bolus:.1f} units")
        st.write(f"6. Total bolus: {food_bolus:.1f} + {correction_bolus:.1f} = {correct_total:.1f} units")

def comprehensive_exam():
    """Final comprehensive examination"""
    st.subheader("🎓 Final Comprehensive Examination")
    
    st.markdown("""
    This comprehensive exam tests all learning objectives. You must score ≥80% to demonstrate competency.
    """)
    
    if st.button("Start Comprehensive Exam"):
        st.session_state.exam_started = True
        st.session_state.exam_answers = {}
    
    if st.session_state.get('exam_started', False):
        
        # Comprehensive questions covering all modules
        exam_questions = [
            {
                "id": "comp_1",
                "question": "A 25-year-old patient on insulin pump therapy has consistent pre-breakfast hyperglycemia (200-250 mg/dL) despite good bedtime control (110-130 mg/dL). What is the most likely cause and appropriate intervention?",
                "type": "multiple_choice",
                "options": [
                    "Insufficient dinner insulin - increase dinner I:C ratio",
                    "Dawn phenomenon - increase basal rates 3:00-7:00 AM", 
                    "Somogyi effect - decrease bedtime basal rates",
                    "Pump malfunction - change infusion set"
                ],
                "correct": 1,
                "points": 5
            },
            {
                "id": "comp_2", 
                "question": "Calculate the appropriate bolus for: 60g carbohydrate meal, current BG 180 mg/dL, I:C ratio 1:12, correction factor 40 mg/dL per unit, target BG 120 mg/dL",
                "type": "calculation",
                "answer": 6.5,  # (60/12) + ((180-120)/40) = 5.0 + 1.5 = 6.5
                "tolerance": 0.5,
                "points": 10
            },
            {
                "id": "comp_3",
                "question": "A patient with gastroparesis is eating pizza (high fat, 45g carbs). How should the 4.5-unit bolus be delivered?",
                "type": "multiple_choice", 
                "options": [
                    "All 4.5 units immediately",
                    "1.4 units now, 3.1 units over 4-6 hours",
                    "2.3 units now, 2.2 units over 2 hours", 
                    "No bolus until after the meal"
                ],
                "correct": 1,
                "points": 5
            },
            {
                "id": "comp_4",
                "question": "Which CGM alert requires the most immediate intervention?",
                "type": "multiple_choice",
                "options": [
                    "Glucose 250 mg/dL, trending up slowly",
                    "Glucose 85 mg/dL, trending down rapidly", 
                    "Glucose 160 mg/dL, trending up rapidly",
                    "Glucose 200 mg/dL, stable trend"
                ],
                "correct": 1,
                "points": 5
            },
            {
                "id": "comp_5",
                "question": "For a 70-year-old patient with mild cognitive impairment, what should be the primary consideration when setting glucose targets?",
                "type": "multiple_choice",
                "options": [
                    "Tight control to prevent complications (70-140 mg/dL)",
                    "Standard targets with slight relaxation (80-160 mg/dL)", 
                    "Relaxed targets prioritizing safety (100-200 mg/dL)",
                    "Very tight control due to reduced life expectancy"
                ],
                "correct": 2,
                "points": 5
            }
        ]
        
        total_points = 0
        earned_points = 0
        
        for question in exam_questions:
            total_points += question['points']
            
            st.markdown(f"**Question ({question['points']} points):** {question['question']}")
            
            if question['type'] == 'multiple_choice':
                answer = st.radio(
                    "Select your answer:",
                    question['options'],
                    key=question['id']
                )
                
                if question['id'] in st.session_state.get('exam_answers', {}):
                    user_index = question['options'].index(answer)
                    if user_index == question['correct']:
                        earned_points += question['points']
                        
            elif question['type'] == 'calculation':
                answer = st.number_input(
                    "Enter your calculated answer:",
                    value=0.0,
                    step=0.1,
                    key=question['id']
                )
                
                if abs(answer - question['answer']) <= question['tolerance']:
                    earned_points += question['points']
            
            st.markdown("---")
        
        if st.button("Submit Final Exam"):
            st.session_state.exam_answers = {q['id']: True for q in exam_questions}  # Mark as answered
            
            percentage = (earned_points / total_points) * 100
            
            st.markdown("## 📊 Exam Results")
            st.metric("Final Score", f"{earned_points}/{total_points} ({percentage:.1f}%)")
            
            if percentage >= 80:
                st.success("🎉 Congratulations! You have demonstrated competency in insulin pump therapy!")
                st.balloons()
                st.session_state.progress = 100
                
                # Generate certificate
                st.markdown("""
                ## 🏆 Certificate of Completion
                
                **This certifies that you have successfully completed the**
                **Insulin Pump Education Platform for Medical Students**
                
                **Competencies Demonstrated:**
                - ✅ Insulin pump physiology and mechanisms
                - ✅ Device comparison and patient matching  
                - ✅ Programming and calculation proficiency
                - ✅ CGM integration and interpretation
                - ✅ Complex patient case management
                - ✅ Clinical decision-making skills
                
                **Score:** {:.1f}% (≥80% required for certification)
                **Date:** {}
                """.format(percentage, datetime.datetime.now().strftime("%B %d, %Y")))
                
            elif percentage >= 60:
                st.warning("📚 Good effort! You need ≥80% to demonstrate competency. Review missed topics and retake.")
                st.session_state.progress = max(st.session_state.progress, 75)
            else:
                st.error("📖 Additional study needed. Please review the course materials thoroughly before retaking.")
                st.session_state.progress = max(st.session_state.progress, 50)

# Helper functions for simulation and data generation
def generate_glucose_data(patient_type):
    """Generate realistic glucose data based on patient type"""
    np.random.seed(42)  # For reproducible results
    
    # Base glucose pattern (24 hours in 5-minute intervals)
    time_points = np.arange(0, 24*60, 5) / 60  # Convert to hours
    base_glucose = np.ones(len(time_points)) * 120
    
    # Add circadian variation
    for i, hour in enumerate(time_points):
        if 3 <= hour < 8:  # Dawn phenomenon
            base_glucose[i] += 20 * np.sin((hour - 3) * np.pi / 5)
        elif 18 <= hour < 22:  # Evening rise
            base_glucose[i] += 10 * np.sin((hour - 18) * np.pi / 4)
    
    # Add meals
    meal_times = [7, 12, 18]  # 7 AM, 12 PM, 6 PM
    meal_effects = [60, 50, 70]  # Peak glucose rise
    
    for meal_time, effect in zip(meal_times, meal_effects):
        for i, hour in enumerate(time_points):
            if meal_time <= hour < meal_time + 4:
                # Gaussian curve for meal effect
                time_from_meal = hour - meal_time
                meal_impact = effect * np.exp(-(time_from_meal - 1)**2 / 0.5)
                base_glucose[i] += meal_impact
    
    # Add patient-specific patterns
    if patient_type == "Dawn Phenomenon":
        for i, hour in enumerate(time_points):
            if 4 <= hour < 9:
                base_glucose[i] += 40
    elif patient_type == "Gastroparesis":
        # Delayed and prolonged meal responses
        for meal_time, effect in zip(meal_times, meal_effects):
            for i, hour in enumerate(time_points):
                if meal_time + 1 <= hour < meal_time + 6:
                    time_from_meal = hour - meal_time - 1
                    delayed_impact = effect * 0.8 * np.exp(-time_from_meal**2 / 2)
                    base_glucose[i] += delayed_impact
    
    # Add random noise
    noise = np.random.normal(0, 10, len(base_glucose))
    glucose_values = base_glucose + noise
    
    # Ensure realistic bounds
    glucose_values = np.clip(glucose_values, 50, 400)
    
    return pd.DataFrame({
        'time': time_points,
        'glucose': glucose_values,
        'timestamp': [datetime.datetime.now() + datetime.timedelta(hours=h) for h in time_points]
    })

def create_glucose_chart(data, target_range):
    """Create interactive glucose chart"""
    fig = go.Figure()
    
    # Main glucose line
    fig.add_trace(go.Scatter(
        x=data['time'],
        y=data['glucose'],
        mode='lines',
        name='Glucose',
        line=dict(color='blue', width=3),
        hovertemplate='Time: %{x:.1f}h<br>Glucose: %{y:.0f} mg/dL<extra></extra>'
    ))
    
    # Target range
    fig.add_hline(y=target_range[0], line_dash="dash", line_color="green", 
                  annotation_text=f"Target Low: {target_range[0]}")
    fig.add_hline(y=target_range[1], line_dash="dash", line_color="green",
                  annotation_text=f"Target High: {target_range[1]}")
    
    # Critical thresholds
    fig.add_hline(y=70, line_dash="dot", line_color="red", 
                  annotation_text="Hypoglycemia: 70")
    fig.add_hline(y=250, line_dash="dot", line_color="orange",
                  annotation_text="Severe Hyperglycemia: 250")
    
    fig.update_layout(
        title="Continuous Glucose Monitoring - 24 Hour View",
        xaxis_title="Time (hours)",
        yaxis_title="Glucose (mg/dL)",
        height=400,
        showlegend=True,
        yaxis=dict(range=[50, 350])
    )
    
    return fig

def calculate_trend(glucose_values):
    """Calculate glucose trend from recent values"""
    if len(glucose_values) < 2:
        return 0
    return (glucose_values[-1] - glucose_values[0]) / len(glucose_values)

def get_trend_arrow(trend):
    """Get trend arrow based on rate of change"""
    if trend > 3:
        return "⇈"  # Rising rapidly
    elif trend > 1:
        return "↗"  # Rising
    elif trend > -1:
        return "→"  # Stable
    elif trend > -3:
        return "↘"  # Falling
    else:
        return "⇊"  # Falling rapidly

def calculate_time_in_range(glucose_values, target_range):
    """Calculate percentage of time in target range"""
    in_range = ((glucose_values >= target_range[0]) & 
                (glucose_values <= target_range[1]))
    return (in_range.sum() / len(glucose_values)) * 100

def calculate_active_insulin(data):
    """Estimate active insulin on board (simplified)"""
    # Simplified calculation - in reality this would track actual boluses
    recent_glucose = data['glucose'].tail(6).mean()  # Last 30 minutes
    baseline = 120
    
    if recent_glucose < baseline:
        return max(0, (baseline - recent_glucose) / 40)  # Rough estimate
    return 0

def add_intervention(intervention_type, value):
    """Add intervention to simulation"""
    # In a real app, this would modify the glucose simulation
    st.info(f"Intervention added: {intervention_type} = {value}")

# Run the main application
if __name__ == "__main__":
    main()
