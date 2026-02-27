import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & OTB Styling
st.set_page_config(page_title="OTB | Housing Oversight Dashboard", layout="wide")

# Custom CSS to make it look like an official OTB tool
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #C21B33; }
    </style>
    """, unsafe_content_set=True)

@st.cache_data
def load_data():
    return pd.read_csv('final_oversight_dashboard_data.csv')

df = load_data()

# 2. Sidebar with OTB Colors
st.sidebar.markdown("<h1 style='color: #C21B33;'>OPEN THE BOOKS</h1>", unsafe_allow_html=True)
st.sidebar.markdown("### Housing Oversight Intelligence")
page = st.sidebar.radio("Navigation", ["National Analysis", "State Audit", "FOIA Builder"])

# 3. View: National Heatmap (Using Red/Blue Scale)
if page == "National Analysis":
    st.title("🗺️ National Affordability Crisis Heatmap")
    
    # Using a Red-Blue color scale to match the logo
    fig = px.choropleth(df, 
                        locations='State_Abbr', 
                        locationmode="USA-states", 
                        color='Affordability_Gap',
                        hover_name='State',
                        scope="usa",
                        color_continuous_scale=["#1F2B3E", "#C21B33"], # Blue to Red
                        labels={'Affordability_Gap':'Gap %'})
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, width='stretch')
    
    st.subheader("Priority Audit List (Highest Gaps)")
    st.dataframe(df.sort_values('Affordability_Gap', ascending=False)[['State', 'Gap_Bucket', 'Affordability_Gap']].head(10), width='stretch')

# 4. View: State Audit (With OTB Branding)
elif page == "State Audit":
    state = st.selectbox("Select State for Audit", df['State'].sort_values())
    row = df[df['State'] == state].iloc[0]
    
    st.header(f"Forensic Profile: {state}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Housing Growth", f"{row['HPI_Growth']:.1%}")
    c2.metric("Income Growth", f"{row['Income_Growth']:.1%}")
    c3.metric("Affordability Gap", f"{row['Affordability_Gap']:.1%}")
    
    # Comparison Bar Chart with OTB Colors
    bar_data = pd.DataFrame({
        "Metric": ["Price Increase", "Income Increase"],
        "Value": [row['HPI_Growth'], row['Income_Growth']]
    })
    fig_bar = px.bar(bar_data, x="Metric", y="Value", 
                     color="Metric", 
                     color_discrete_map={"Price Increase": "#C21B33", "Income Increase": "#1F2B3E"})
    st.plotly_chart(fig_bar)

    # NEW: Automated Summary for Chris
    st.subheader("📝 Executive Summary for Oversight")
    summary = f"""In {state}, housing prices have surged by {row['HPI_Growth']:.1%} over the last decade, 
    vastly outstripping the {row['Income_Growth']:.1%} growth in median household income. 
    This has created a structural affordability gap of {row['Affordability_Gap']:.1%}. 
    Our investigation suggests current state agency spending is failing to mitigate this divergence."""
    st.text_area("Copy for Substack/Articles:", summary, height=150)

# 5. View: FOIA Builder
elif page == "FOIA Builder":
    st.title("📝 FOIA Request Generator")
    target_state = st.selectbox("Select Target State", df['State'].sort_values())
    
    st.info("Use this tool to request spending transparency from states with high affordability gaps.")
    
    foia_template = f"Subject: Records Request - Housing Spending Trends ({target_state})\n\nDear Records Officer..."
    st.text_area("Draft:", foia_template, height=250)