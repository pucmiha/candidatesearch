import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Candidate Search",
    page_icon="👥",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .card:hover {
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    .header {
        color: #1E88E5;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .subheader {
        color: #424242;
        font-size: 1.5em;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv('blue_collar_candidates.csv')

# Load data
df = load_data()

# Header
st.markdown('<div class="header">👥 Candidate Search</div>', unsafe_allow_html=True)

# Create two columns for filters
col1, col2 = st.columns(2)

with col1:
    # Job position filter
    job_positions = ['All'] + sorted(df['job_position'].unique().tolist())
    selected_job = st.selectbox('Select Job Position', job_positions)

with col2:
    # Location filter
    locations = ['All'] + sorted(df['location'].unique().tolist())
    selected_location = st.selectbox('Select Location', locations)

# Filter the data
filtered_df = df.copy()
if selected_job != 'All':
    filtered_df = filtered_df[filtered_df['job_position'] == selected_job]
if selected_location != 'All':
    filtered_df = filtered_df[filtered_df['location'] == selected_location]

# Display statistics
st.markdown('<div class="subheader">📊 Statistics</div>', unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)
with col3:
    st.metric("Total Candidates", len(filtered_df))
with col4:
    st.metric("Unique Job Positions", filtered_df['job_position'].nunique())
with col5:
    st.metric("Unique Locations", filtered_df['location'].nunique())

# Display candidates in cards
st.markdown('<div class="subheader">👤 Candidates</div>', unsafe_allow_html=True)

# Create a grid of cards
cols = st.columns(3)
for idx, (_, row) in enumerate(filtered_df.iterrows()):
    with cols[idx % 3]:
        st.markdown(f"""
            <div class="card">
                <h3>{row['firstname']} {row['lastname']}</h3>
                <p><strong>Position:</strong> {row['job_position']}</p>
                <p><strong>Location:</strong> {row['location']}</p>
            </div>
        """, unsafe_allow_html=True)

# Add a visualization
st.markdown('<div class="subheader">📈 Job Distribution</div>', unsafe_allow_html=True)
job_counts = filtered_df['job_position'].value_counts()
fig = px.bar(
    x=job_counts.index,
    y=job_counts.values,
    title='Distribution of Job Positions',
    labels={'x': 'Job Position', 'y': 'Number of Candidates'}
)
fig.update_layout(
    xaxis_tickangle=-45,
    height=400,
    margin=dict(b=100)
)
st.plotly_chart(fig, use_container_width=True)
