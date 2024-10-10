import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_changping = pd.read_csv("changping_data.csv")
df_changping['date_time'] = pd.to_datetime(df_changping[['year', 'month', 'day', 'hour']])

st.title('Air Quality Analysis Dashboard: Changping City')
st.image("polusi.jpeg")
st.write('This dashboard is used to visualize pre-determined answers regarding the air quality conditions in Changping city.')

st.markdown("""
### About Me
- **Name**: Ali Purnomo Shidiq
- **Email Address**: ali.purns122@gmail.com


### Question
- **Based on the available data, does the temperature in Changping city increase as the amount of pollutants (PM2.5, PM10) increases?**
- **What is the trend of annual rainfall?**
- **How is the temperature classification in Changping city divided?**
- **How frequent is the occurrence of each temperature classification each year?**
""")
# Sidebar filters
st.sidebar.header("Select Data")
selected_years = st.sidebar.multiselect("Select Year", options=df_changping["year"].unique(), default=df_changping["year"].unique())
selected_months = st.sidebar.multiselect("Select Month", options=df_changping["month"].unique(), default=df_changping["month"].unique())
if not selected_years or not selected_months:
    st.warning("Maaf, data tidak boleh kosong. Silakan pilih setidaknya satu tahun dan satu bulan.")
else:
    # Filter data based on selected years and months
    filtered_df = df_changping[
        (df_changping["year"].isin(selected_years)) &
        (df_changping["month"].isin(selected_months))
    ]
st.subheader("Daily Pollution PM2.5")
rain_by_year_filtered = filtered_df.groupby('day')['PM2.5'].sum().reset_index()
    
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='day', y='PM2.5', data=rain_by_year_filtered, ax=ax, color='red', linewidth=2)
ax.set_xlabel('Day')
ax.set_ylabel('Total Pollution')
ax.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

st.subheader("Daily Pollution PM10")
rain_by_year_filtered = filtered_df.groupby('day')['PM10'].sum().reset_index()
    
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='day', y='PM10', data=rain_by_year_filtered, ax=ax, color='red', linewidth=2)
ax.set_xlabel('Day')
ax.set_ylabel('Total Pollution')
ax.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

st.subheader('Correlation Temperature With Polluting Substance')
corr = filtered_df[['PM2.5', 'PM10', 'TEMP']].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)
plt.title('Correlation Heatmap')
st.pyplot(fig)

st.markdown("""
## Conclusion
- The increase in temperature in Changping city is not caused by the increase in PM2.5 and PM10 particles, as indicated by the negative correlation in the data.
"""
)

st.subheader("Rainfall Trend")
rain_by_year_filtered = filtered_df.groupby('day')['RAIN'].sum().reset_index()
    
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='day', y='RAIN', data=rain_by_year_filtered, ax=ax, color='red', linewidth=2)
ax.set_xlabel('day')
ax.set_ylabel('Total Rainfall')
ax.set_title('Rainfall Trend Over Time', fontsize=16, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
## Conclusion
- The rainfall trend in Changping city experienced a significant increase in 2015, nearly doubling compared to the previous year. However, the rainfall trend in other years tends to be stable.
"""
)

Q1 = df_changping['TEMP'].quantile(0.25)
Q2 = df_changping['TEMP'].quantile(0.5)
Q3 = df_changping['TEMP'].quantile(0.75)
df_changping['temp_cluster'] = pd.cut(df_changping['TEMP'], bins=[-float('inf'), Q1, Q3, float('inf')], labels=['rendah', 'sedang', 'tinggi'])

# Temperature Distribution
st.subheader("Temperature Distribution")
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(x='temp_cluster', y='TEMP', data=df_changping, ax=ax)
ax.set_title('Distribusi Temperatur per Cluster')
ax.set_xlabel('Cluster')
ax.set_ylabel('Temperatur (°C)')
st.pyplot(fig)

st.markdown("""
## Conclusion
- Temperature classification can be divided into three categories: low, medium, and high. This classification is based on the values of Q1, Q2, and Q3, making it easy to assess the temperature in Changping city"""
)

st.subheader("Temperature Cluster Frequency")
temp_cluster_freq_filtered = filtered_df.groupby(['day', 'temp_cluster'])['temp_cluster'].count().reset_index(name='frequency')
    
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='day', y='frequency', hue='temp_cluster', data=temp_cluster_freq_filtered, ax=ax)
ax.set_xlabel('Day')
ax.set_ylabel('Frequency')
ax.set_title('Temperature Cluster Frequency Over Time', fontsize=16, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
## Conclusion
- The medium temperature category occurs most frequently, with over 4000 occurrences. Other temperature categories tend to have a stable frequency in Changping city. """)