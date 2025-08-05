import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Job Hunt Analytics", layout="wide")
st.title("📈 Job Hunt Analytics Dashboard")

TRACKER_FILE = "data/application_tracker.csv"

if os.path.exists(TRACKER_FILE):
    df = pd.read_csv(TRACKER_FILE)
    
    if not df.empty:
        # Convert Date once
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        df = df.dropna(subset=["Date"])

        # 1. Applications by Status (Pie)
        st.subheader("📊 Applications by Status")
        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_status = px.pie(
            status_counts,
            names="Status",
            values="Count",
            hole=0.4,
            title="Applications by Status"
        )
        fig_status.update_traces(textinfo='label+value')
        total_apps = status_counts["Count"].sum()
        fig_status.add_annotation(
            dict(
                text=f"<b>{total_apps}</b><br>Total",
                x=0.5,
                y=0.5,
                font_size=20,
                showarrow=False,
                font=dict(color="black"),
                bgcolor="white"
            )
        )
        st.plotly_chart(fig_status, use_container_width=True)

        # 2. Applications Over Time (Monthly) - Line + Markers
        st.subheader("📅 Applications Over Time (Monthly)")
        monthly_counts = df.groupby(df["Date"].dt.to_period("M")).size().reset_index(name="Applications")
        monthly_counts["Date"] = monthly_counts["Date"].dt.to_timestamp()

        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Scatter(
            x=monthly_counts["Date"],
            y=monthly_counts["Applications"],
            mode='lines+markers',
            line=dict(color='royalblue', width=2),
            marker=dict(size=6)
        ))
        fig_monthly.update_layout(
            xaxis=dict(
                tickformat="%b %Y",
                tickangle=-45,
                dtick="M1"
            ),
            yaxis_title="Number of Applications",
            template="plotly_white",
            hovermode="x unified"
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

        # 3. Applications by Company (Bar chart)
        st.subheader("🏢 Applications by Company")
        company_counts = df["Company"].value_counts().reset_index()
        company_counts.columns = ["Company", "Count"]
        fig_company = px.bar(
            company_counts.head(20),
            x="Count",
            y="Company",
            orientation='h',
            title="Top 20 Companies Applied To",
            labels={"Count": "Applications", "Company": "Company"},
            text="Count"
        )
        fig_company.update_traces(textposition='outside')
        fig_company.update_layout(yaxis={'categoryorder':'total ascending'}, template="plotly_white")
        st.plotly_chart(fig_company, use_container_width=True)

        # 4. Applications by Position (Bar chart)
        st.subheader("💼 Applications by Position")
        position_counts = df["Position"].value_counts().reset_index()
        position_counts.columns = ["Position", "Count"]
        fig_position = px.bar(
            position_counts.head(20),
            x="Count",
            y="Position",
            orientation='h',
            title="Top 20 Positions Applied For",
            labels={"Count": "Applications", "Position": "Position"},
            text="Count"
        )
        fig_position.update_traces(textposition='outside')
        fig_position.update_layout(yaxis={'categoryorder':'total ascending'}, template="plotly_white")
        st.plotly_chart(fig_position, use_container_width=True)

        # 5. Applications by Weekday (Histogram)
        st.subheader("📅 Applications by Day of the Week")
        df['Weekday'] = df["Date"].dt.day_name()
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday_counts = df["Weekday"].value_counts().reindex(weekday_order).reset_index()
        weekday_counts.columns = ["Weekday", "Count"]
        fig_weekday = px.bar(
            weekday_counts,
            x="Weekday",
            y="Count",
            title="Applications by Weekday",
            labels={"Count": "Applications"},
            text="Count"
        )
        fig_weekday.update_traces(textposition='outside')
        fig_weekday.update_layout(template="plotly_white")
        st.plotly_chart(fig_weekday, use_container_width=True)

        # 6. Status Trend Over Time (Stacked Area Chart)
        st.subheader("📈 Application Status Trend Over Time")
        # Pivot data by month and status
        df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()
        status_trend = df.groupby(["Month", "Status"]).size().reset_index(name="Count")
        status_pivot = status_trend.pivot(index="Month", columns="Status", values="Count").fillna(0)

        fig_status_trend = go.Figure()
        for status in status_pivot.columns:
            fig_status_trend.add_trace(go.Scatter(
                x=status_pivot.index,
                y=status_pivot[status],
                stackgroup='one',
                mode='none',
                name=status
            ))
        fig_status_trend.update_layout(
            title="Application Status Over Time (Monthly)",
            xaxis_title="Month",
            yaxis_title="Number of Applications",
            template="plotly_white",
            hovermode="x unified"
        )
        st.plotly_chart(fig_status_trend, use_container_width=True)

    else:
        st.info("No applications tracked yet. Add some applications to see analytics.")
else:
    st.info("No tracker file found. It will be created when you add your first application.")
