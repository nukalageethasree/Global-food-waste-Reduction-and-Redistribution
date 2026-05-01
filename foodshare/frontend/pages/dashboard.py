"""Dashboard page with stats, charts and AI recommendations."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.api import api_get
from utils.hf_ai import hf_impact_summary

def show_dashboard():
    user = st.session_state.user or {}

    st.markdown(f"""
    <div class="hero-banner">
      <h1>🌍 Dashboard</h1>
      <p>Welcome back, <strong>{user.get('full_name','Demo User')}</strong>! Here's your impact overview for the Global Food Waste Reduction Platform.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Fetch stats ──────────────────────────────────────────────────────────
    with st.spinner("Loading dashboard…"):
        stats, s_code = api_get("/dashboard/stats")
        recs,  r_code = api_get("/dashboard/recommendations")

    if s_code != 200:
        st.error(stats.get("error", "Failed to load stats"))
        stats = {}

    # ── KPI Cards ────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 Total Listings",  stats.get("total_listings",  48),   "+12% from last month")
    c2.metric("✅ Active Requests", stats.get("active_requests", 23),   f"{stats.get('pending_approval',8)} pending approval")
    c3.metric("🍽️ Meals Donated",   f"{stats.get('meals_donated',1247):,}", "+18% from last month")
    c4.metric("♻️ Waste Reduced",   f"{stats.get('waste_reduced_kg',342)} kg", f"≈{stats.get('co2_saved',684)} kg CO₂ saved")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 📈 Monthly Impact Trends")
        monthly = stats.get("monthly_trend", [
            {"month":"Jan","meals":95},{"month":"Feb","meals":110},{"month":"Mar","meals":285},
            {"month":"Apr","meals":290},{"month":"May","meals":280},{"month":"Jun","meals":380}
        ])
        df_m = pd.DataFrame(monthly)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_m["month"], y=df_m["meals"], mode="lines+markers",
            fill="tozeroy", fillcolor="rgba(34,197,94,0.15)",
            line=dict(color="#16a34a", width=2.5),
            marker=dict(color="#16a34a", size=7),
            name="Meals Donated"
        ))
        fig.update_layout(
            height=230, margin=dict(l=0,r=0,t=10,b=0),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False, tickfont=dict(size=12)),
            yaxis=dict(gridcolor="#f0f0f0", tickfont=dict(size=12)),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("#### 🗂️ Food Category Distribution")
        cats = stats.get("category_distribution", [
            {"category":"Prepared Food","count":150},{"category":"Vegetables","count":100},
            {"category":"Fruits","count":80},{"category":"Bakery","count":55},{"category":"Dairy","count":45}
        ])
        df_c = pd.DataFrame(cats)
        fig2 = px.bar(df_c, x="count", y="category", orientation="h",
                      color_discrete_sequence=["#16a34a"])
        fig2.update_layout(
            height=230, margin=dict(l=0,r=0,t=10,b=0),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(gridcolor="#f0f0f0", tickfont=dict(size=12)),
            yaxis=dict(showgrid=False, tickfont=dict(size=11), title=""),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── AI Recommendations ────────────────────────────────────────────────────
    st.markdown("#### 🤖 AI-Powered Recommendations")
    if r_code == 200 and recs.get("recommendations"):
        rec_list = recs["recommendations"]
        cols = st.columns(len(rec_list))
        priority_color = {"high": "#ef4444", "medium": "#f97316", "low": "#16a34a"}
        action_page    = {"browse": "browse", "create": "create_listing", "profile": "profile", "impact": "impact"}
        for i, rec in enumerate(rec_list):
            with cols[i]:
                pcolor = priority_color.get(rec.get("priority","low"), "#16a34a")
                st.markdown(f"""
                <div class="fs-card" style="min-height:140px;">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <strong style="font-size:14px;color:#111827;">{rec['title']}</strong>
                    <span style="font-size:10px;font-weight:700;color:{pcolor};text-transform:uppercase;">{rec.get('priority','')}</span>
                  </div>
                  <p style="font-size:13px;color:#6b7280;margin-bottom:0;">{rec['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                target = action_page.get(rec.get("action","browse"), "browse")
                if st.button("Take Action →", key=f"rec_{i}", use_container_width=True):
                    st.session_state.page = target
                    st.rerun()
    else:
        st.info("AI recommendations loading… ensure your HuggingFace token is set.")

    # ── Quick Actions ─────────────────────────────────────────────────────────
    st.markdown("#### ⚡ Quick Actions")
    qa1, qa2, qa3, qa4 = st.columns(4)
    if qa1.button("➕ Create Listing",    use_container_width=True, type="primary"):
        st.session_state.page = "create_listing"; st.rerun()
    if qa2.button("🔍 Browse Food",       use_container_width=True):
        st.session_state.page = "browse"; st.rerun()
    if qa3.button("📦 View Requests",     use_container_width=True):
        st.session_state.page = "requests"; st.rerun()
    if qa4.button("📈 My Impact",         use_container_width=True):
        st.session_state.page = "impact"; st.rerun()
