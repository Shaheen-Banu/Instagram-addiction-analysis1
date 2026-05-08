import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Instagram Addiction Analysis",
    page_icon="📱",
    layout="wide"
)

# App Title
st.title("📱 Instagram Addiction & Mental Wellness Analysis")

st.markdown(
    """
    Analyze how Instagram usage affects:
    - Sleep
    - Productivity
    - Anxiety
    - Mental Wellness
    """
)

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\PROJECT\instagram-addiction-analysis\data\instagram_addiction_dataset.csv")
    return df

df = load_data()

# Sidebar
st.sidebar.header("🔍 Filters")

selected_addiction = st.sidebar.multiselect(
    "Select Addiction Level",
    options=df['addiction_level'].unique(),
    default=df['addiction_level'].unique()
)

filtered_df = df[
    df['addiction_level'].isin(selected_addiction)
]

# KPI Section
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Screen Time",
        f"{filtered_df['daily_screen_time_hours'].mean():.1f} hrs"
    )

with col2:
    st.metric(
        "Average Sleep Hours",
        f"{filtered_df['sleep_hours'].mean():.1f} hrs"
    )

with col3:
    st.metric(
        "Average Anxiety Level",
        f"{filtered_df['anxiety_level'].mean():.1f}/10"
    )

with col4:
    st.metric(
        "Average Productivity Loss",
        f"{filtered_df['productivity_loss_hours'].mean():.1f} hrs"
    )

st.divider()

# Chart 1 — Screen Time Distribution
st.subheader("📈 Screen Time Distribution")

fig1, ax1 = plt.subplots(figsize=(8,5))

sns.histplot(
    filtered_df['daily_screen_time_hours'],
    kde=True,
    ax=ax1
)

ax1.set_xlabel("Daily Screen Time (Hours)")
ax1.set_ylabel("Users")

st.pyplot(fig1)

# Chart 2 — Sleep vs Screen Time
st.subheader("😴 Sleep vs Screen Time")

fig2, ax2 = plt.subplots(figsize=(8,5))

sns.scatterplot(
    x='daily_screen_time_hours',
    y='sleep_hours',
    hue='addiction_level',
    data=filtered_df,
    ax=ax2
)

ax2.set_xlabel("Screen Time")
ax2.set_ylabel("Sleep Hours")

st.pyplot(fig2)

# Chart 3 — Productivity Loss
st.subheader("📉 Productivity Loss by Addiction Level")

fig3, ax3 = plt.subplots(figsize=(8,5))

sns.boxplot(
    x='addiction_level',
    y='productivity_loss_hours',
    data=filtered_df,
    ax=ax3
)

st.pyplot(fig3)

# Chart 4 — Correlation Heatmap
st.subheader("🔥 Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include='number')

fig4, ax4 = plt.subplots(figsize=(12,8))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap='coolwarm',
    ax=ax4
)

st.pyplot(fig4)

# Mood Analysis
st.subheader("😊 Mood After Instagram Usage")

mood_counts = filtered_df['mood_after_use'].value_counts()

fig5, ax5 = plt.subplots(figsize=(7,5))

ax5.pie(
    mood_counts,
    labels=mood_counts.index,
    autopct='%1.1f%%'
)

st.pyplot(fig5)

# Raw Data Preview
st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df)

# Insights Section
st.subheader("🧠 Key Insights")

st.markdown(
    """
    ### Observations

    - Users with higher screen time tend to sleep fewer hours.
    - Productivity loss increases among highly addicted users.
    - Anxiety and self-comparison levels rise with screen time.
    - Heavy Instagram users report lower focus levels.
    """
)

# Footer
st.divider()

st.caption(
    "Built using Streamlit, Pandas, Matplotlib, and Seaborn"
)