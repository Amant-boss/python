# idk.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="Advanced Fitness Dashboard", layout="wide")

# -----------------------
# SESSION STATE INIT
# -----------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Steps", "Calories", "Workout"])

# -----------------------
# SIDEBAR INPUT
# -----------------------
st.sidebar.title("⚙️ Controls")

name = st.sidebar.text_input("Name", "User")

st.sidebar.subheader("Add Daily Entry")

entry_date = st.sidebar.date_input("Date", date.today())
steps = st.sidebar.number_input("Steps", 0, 50000, 5000)
calories = st.sidebar.number_input("Calories Burned", 0, 5000, 300)
workout = st.sidebar.number_input("Workout Minutes", 0, 300, 30)

if st.sidebar.button("➕ Add Entry"):
    new_row = pd.DataFrame([[entry_date, steps, calories, workout]],
                           columns=["Date", "Steps", "Calories", "Workout"])
    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

if st.sidebar.button("🗑 Clear Data"):
    st.session_state.data = pd.DataFrame(columns=["Date", "Steps", "Calories", "Workout"])

# -----------------------
# MAIN TITLE
# -----------------------
st.title(f"📊 Advanced Fitness Dashboard — {name}")

df = st.session_state.data.copy()

if df.empty:
    st.warning("No data yet. Add entries from the sidebar.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# -----------------------
# FILTERS
# -----------------------
st.subheader("🔍 Filters")

colf1, colf2 = st.columns(2)

with colf1:
    date_range = st.date_input("Select Date Range",
                               [df["Date"].min(), df["Date"].max()])

with colf2:
    metric = st.selectbox("Select Metric to Analyze",
                          ["Steps", "Calories", "Workout"])

filtered_df = df[(df["Date"] >= pd.to_datetime(date_range[0])) &
                 (df["Date"] <= pd.to_datetime(date_range[1]))]

# -----------------------
# METRICS
# -----------------------
st.subheader("📈 Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Steps", int(filtered_df["Steps"].sum()))
col2.metric("Total Calories", int(filtered_df["Calories"].sum()))
col3.metric("Total Workout (min)", int(filtered_df["Workout"].sum()))

# -----------------------
# CHARTS
# -----------------------
st.subheader("📊 Visualizations")

# Line Chart
fig_line = px.line(filtered_df, x="Date", y=metric, markers=True,
                   title=f"{metric} Over Time")
st.plotly_chart(fig_line, use_container_width=True)

# Multi-metric comparison
fig_multi = go.Figure()
fig_multi.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Steps"],
                              mode='lines+markers', name='Steps'))
fig_multi.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Calories"],
                              mode='lines+markers', name='Calories'))
fig_multi.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Workout"],
                              mode='lines+markers', name='Workout'))
fig_multi.update_layout(title="All Metrics Comparison")
st.plotly_chart(fig_multi, use_container_width=True)

# Pie Chart
fig_pie = px.pie(values=[
    filtered_df["Steps"].sum(),
    filtered_df["Calories"].sum(),
    filtered_df["Workout"].sum()
],
names=["Steps", "Calories", "Workout"],
title="Distribution of Activity")
st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------
# GOAL TRACKER
# -----------------------
st.subheader("🎯 Goal Tracker")

goal_steps = st.number_input("Set Daily Step Goal", 1000, 20000, 8000)

avg_steps = filtered_df["Steps"].mean()

progress = min(avg_steps / goal_steps, 1.0)

st.progress(progress)

if avg_steps >= goal_steps:
    st.success("Goal achieved ✅")
else:
    st.warning("Goal not reached ❌")

# -----------------------
# DATA TABLE + DOWNLOAD
# -----------------------
st.subheader("📋 Data Table")

st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button("⬇ Download Data as CSV", csv, "fitness_data.csv", "text/csv")

# -----------------------
# ADVANCED INSIGHTS
# -----------------------
st.subheader("🧠 Insights")

st.write(f"Average Steps: {int(filtered_df['Steps'].mean())}")
st.write(f"Average Calories: {int(filtered_df['Calories'].mean())}")
st.write(f"Average Workout: {int(filtered_df['Workout'].mean())} min")

best_day = filtered_df.loc[filtered_df[metric].idxmax()]

st.info(f"Best day for {metric}: {best_day['Date'].date()}")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.caption("Interactive dashboard with Streamlit + Pandas + Plotly")