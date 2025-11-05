import streamlit as st
import pandas as pd
import time
from datetime import timedelta
from utils.system_stats import get_system_stats
import plotly.express as px

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="System Health Dashboard", layout="wide")

# ---------------- CUSTOM CSS (minimal aesthetic) ----------------
st.markdown("""
    <style>
        .stApp { background-color: #0e1117; color: white; }
        .stSidebar { background-color: #1c1e24; }
        h1, h2, h3 { color: #f5f5f5; }
        hr { margin: 0.5em 0; }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("💻 System Health Monitoring Dashboard")
st.markdown("Monitor your system’s CPU, Memory, Disk, and Network performance in real time.")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Dashboard Controls")

refresh_rate = st.sidebar.slider("⏱️ Refresh Interval (seconds)", 1, 10, 3)

st.sidebar.subheader("📊 Select Metrics to Display")
show_cpu = st.sidebar.checkbox("CPU Usage", True)
show_mem = st.sidebar.checkbox("Memory Usage", True)
show_disk = st.sidebar.checkbox("Disk Usage", True)
show_sent = st.sidebar.checkbox("Network Sent", False)
show_recv = st.sidebar.checkbox("Network Received", False)

st.sidebar.subheader("📆 Time Range")
time_range = st.sidebar.selectbox(
    "Display last:",
    ["Last 1 minute", "Last 5 minutes", "Last 15 minutes", "All data"]
)

# ---------------- SESSION STATE INITIALIZATION ----------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "timestamp", "cpu_percent", "memory_percent", "disk_usage", "net_sent", "net_recv"
    ])

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

placeholder = st.empty()

# ---------------- MAIN LOOP ----------------
while True:
    # Fetch new system stats
    new_data = get_system_stats()

    # Avoid concat warning by ignoring empty df gracefully
    if st.session_state.data.empty:
        st.session_state.data = new_data
    else:
        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True).tail(500)

    df = st.session_state.data.copy()

    # Save new record to CSV
    new_data.to_csv("data/system_log.csv", mode="a", header=False, index=False)

    # Time-based filter
    if time_range != "All data":
        now = df["timestamp"].max()
        minutes = {"Last 1 minute": 1, "Last 5 minutes": 5, "Last 15 minutes": 15}[time_range]
        df = df[df["timestamp"] > now - pd.Timedelta(minutes=minutes)]

    # ---------------- DASHBOARD RENDERING ----------------
    with placeholder.container():

        st.subheader("📊 Key Metrics Overview")

        cpu_val = df["cpu_percent"].iloc[-1]
        mem_val = df["memory_percent"].iloc[-1]
        disk_val = df["disk_usage"].iloc[-1]

        col1, col2, col3 = st.columns(3)
        col1.metric("🧠 CPU Usage (%)", f"{cpu_val:.1f}")
        col2.metric("💾 Memory Usage (%)", f"{mem_val:.1f}")
        col3.metric("📀 Disk Usage (%)", f"{disk_val:.1f}")

        st.markdown("---")

        # ---------------- GRAPHS ----------------
        # Colors professionally assigned
        if show_cpu:
            fig = px.line(df, x="timestamp", y="cpu_percent",
                          title="CPU Usage (%) Over Time",
                          color_discrete_sequence=["#29B6F6"])
            fig.update_layout(template="plotly_dark", margin=dict(l=30, r=30, t=40, b=30))
            st.plotly_chart(fig, use_container_width=True)

        if show_mem:
            fig = px.line(df, x="timestamp", y="memory_percent",
                          title="Memory Usage (%) Over Time",
                          color_discrete_sequence=["#26C6DA"])
            fig.update_layout(template="plotly_dark", margin=dict(l=30, r=30, t=40, b=30))
            st.plotly_chart(fig, use_container_width=True)

        if show_disk:
            fig = px.line(df, x="timestamp", y="disk_usage",
                          title="Disk Usage (%) Over Time",
                          color_discrete_sequence=["#26A69A"])
            fig.update_layout(template="plotly_dark", margin=dict(l=30, r=30, t=40, b=30))
            st.plotly_chart(fig, use_container_width=True)

        if show_sent:
            fig = px.line(df, x="timestamp", y="net_sent",
                          title="Network Sent (MB)",
                          color_discrete_sequence=["#AB47BC"])
            fig.update_layout(template="plotly_dark", margin=dict(l=30, r=30, t=40, b=30))
            st.plotly_chart(fig, use_container_width=True)

        if show_recv:
            fig = px.line(df, x="timestamp", y="net_recv",
                          title="Network Received (MB)",
                          color_discrete_sequence=["#EC407A"])
            fig.update_layout(template="plotly_dark", margin=dict(l=30, r=30, t=40, b=30))
            st.plotly_chart(fig, use_container_width=True)

        # ---------------- DATA TABLE ----------------
        st.markdown("---")
        st.subheader("📋 Recent System Data")
        st.dataframe(df.tail(20), use_container_width=True)

        # ---------------- EXTRA INFO (MINIMAL SET) ----------------
        last_update = df['timestamp'].max().strftime("%H:%M:%S")
        total_records = len(st.session_state.data)

        uptime_seconds = int(time.time() - st.session_state.start_time)
        uptime_str = str(timedelta(seconds=uptime_seconds))

        st.markdown(f"**📦 Total Records Collected:** {total_records}")
        st.markdown(f"**⏱️ Last Updated:** {last_update}")
        st.markdown(f"**🟢 Dashboard Uptime:** {uptime_str}")

        # ---------------- DOWNLOAD BUTTON ----------------
        st.download_button(
            label="📥 Download System Log as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="system_health_log.csv",
            mime="text/csv",
            key=f"download_btn_{time.time()}"
        )

        st.caption("🔁 Dashboard auto-refreshes every few seconds.")

    time.sleep(refresh_rate)
