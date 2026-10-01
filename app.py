import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(page_title="High School Data Lab", page_icon="📊", layout="wide")

st.title("📊 High School General Science: Computational Lab")
st.caption("Advanced Variable Analytics, Statistical Modeling & Export Engine")

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("🔬 Experimental Controls")
st.sidebar.write("Configure your environmental variables to simulate a full field study.")

# High School: Multiple active variables that interact
water_slider = st.sidebar.slider("Water Input (mL/day)", 10, 100, 50, step=10)
sunlight_slider = st.sidebar.slider("Sunlight Exposure (Hours/day)", 2, 12, 6, step=2)
experimental_noise = st.sidebar.slider("Simulated Experimental Error (Noise)", 1, 10, 4)

# --- EXPANDED DATA SYSTEM (The Engine) ---
@st.cache_data
def generate_master_data(noise_level, sunlight_hours):
    """Generates a complete synthetic matrix for high school trend analysis"""
    np.random.seed(42)
    data_rows = []
    
    # Generate data across a full spectrum of water levels to see the macro trend
    for water in range(10, 110, 10):
        # Math model: interaction between water and light creates a non-linear curve
        optimal_water = 50 + (sunlight_hours * 2) 
        base_growth = -0.012 * (water - optimal_water)**2 + (sunlight_hours * 4) + 15
        
        # 5 distinct trials per setting to teach statistical variance
        for trial in range(1, 6):
            noise = np.random.uniform(-noise_level, noise_level)
            final_yield = round(max(2.0, base_growth + noise), 2)
            data_rows.append({"Water_mL": water, "Trial": f"Trial {trial}", "Biomass_g": final_yield})
            
    return pd.DataFrame(data_rows)

# Generate dataset based on user controls
df_master = generate_master_data(experimental_noise, sunlight_slider)

# Filter for the current specific run selected on the slider
df_current = df_master[df_master["Water_mL"] == water_slider]

# --- DOWNLOAD BUTTON IN SIDEBAR ---
st.sidebar.divider()
st.sidebar.subheader("💾 Export Lab Data")
csv_data = df_master.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="⬇️ Download Complete CSV",
    data=csv_data,
    file_name="high_school_plant_lab_data.csv",
    mime="text/csv",
    help="Click here to download the full master dataset for Excel or Google Sheets!"
)

# --- MAIN LAYOUT ---
col_graph, col_stats = st.columns(2)

with col_graph:
    st.header("📈 Macro Data Distribution & Trend Lines")
    st.write("This plot shows *every* data point collected across all cohorts. Observe the mathematical curvature.")
    
    # High School: Scatter plot with a quadratic trend line (LOWESS regression baseline)
    fig = px.scatter(
        df_master, 
        x="Water_mL", 
        y="Biomass_g",
        title="Plant Biomass vs. Water Input Across All Experimental Groups",
        labels={"Water_mL": "Independent Variable: Water (mL)", "Biomass_g": "Dependent Variable: Biomass Yield (grams)"},
        color="Biomass_g",
        color_continuous_scale="Viridis",
        trendline="lowess" # Plots a smooth trend line through the noisy data points
    )
    
    # Highlight the student's currently selected setting on the graph
    fig.add_scatter(
        x=df_current["Water_mL"], 
        y=df_current["Biomass_g"], 
        mode="markers", 
        name="Your Active Setting",
        marker=dict(
            color="red", 
            size=12, 
            symbol="circle-open", 
            line=dict(width=3)
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_stats:
    st.header("📋 Statistical Summary")
    st.write(f"Metrics for the **{water_slider} mL** cohort:")
    
    # Calculate advanced metrics safely
    avg_yield = round(df_current["Biomass_g"].mean(), 2)
    std_dev = round(df_current["Biomass_g"].std(), 2)
    max_val = df_current["Biomass_g"].max()
    min_val = df_current["Biomass_g"].min()
    data_range = round(max_val - min_val, 2)
    
    # Display professional metrics
    st.metric(label="Sample Mean (μ)", value=f"{avg_yield} g")
    st.metric(label="Standard Deviation (σ)", value=f"± {std_dev} g")
    st.metric(label="Data Spread (Range)", value=f"{data_range} g")
    
    st.subheader("Data Sub-set")
    st.dataframe(df_current, hide_index=True, use_container_width=True)

# --- SCIENTIFIC ANALYSIS PANEL ---
st.divider()
st.header("📝 Post-Lab Data Synthesis")
st.write("Use the data visualization above to answer the following empirical questions:")

q1 = st.text_area("1. Based on the trend line curve, estimate the absolute mathematical optimum for water input. Explain your reasoning using coordinate peaks.")
q2 = st.text_area("2. Adjust the 'Simulated Experimental Error' slider in the sidebar to 10. How does increasing standard deviation impact your confidence in the trend line?")
