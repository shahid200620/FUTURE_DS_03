import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Growth Funnel Dashboard", layout="wide")

# ===== PREMIUM UI =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #312e81, #38bdf8);
}
.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding: 15px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.2);
    margin-bottom: 15px;
}
h1, h2, h3 {
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
df = pd.read_csv("data/funnel_advanced.csv")

# ===== NAVIGATION =====
st.sidebar.title("🚀 Growth Dashboard")
page = st.sidebar.radio("Navigate", [
    "Executive Overview",
    "Conversion Flow",
    "Acquisition Channels",
    "Drop-off Intelligence",
    "Strategic Insights"
])

st.markdown("<h1 style='text-align:center;'>🚀 Growth Funnel Intelligence</h1>", unsafe_allow_html=True)

# ===== FILTERS =====
if page != "Strategic Insights":
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    channel = col1.multiselect("Channel", df["Channel"].unique(), df["Channel"].unique())
    min_visitors = col2.slider("Min Visitors", 0, 5000, 0)

    st.markdown("</div>", unsafe_allow_html=True)

    df = df[(df["Channel"].isin(channel)) & (df["Visitors"] >= min_visitors)]

# ================= OVERVIEW =================
if page == "Executive Overview":

    total_visitors = df["Visitors"].sum()
    total_customers = df["Customers"].sum()
    conversion = (total_customers / total_visitors) * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("Visitors", total_visitors)
    c2.metric("Customers", total_customers)
    c3.metric("Conversion %", f"{conversion:.2f}")

    col1, col2 = st.columns(2)

    funnel = df[["Visitors","Leads","Qualified","Customers"]].sum().reset_index()
    funnel.columns = ["Stage","Count"]

    col1.plotly_chart(px.funnel(funnel, x="Count", y="Stage"), use_container_width=True)

    col2.plotly_chart(px.pie(df, names="Channel", values="Visitors", hole=0.4), use_container_width=True)

    col3, col4 = st.columns(2)

    col3.plotly_chart(px.treemap(df, path=["Channel"], values="Visitors"), use_container_width=True)

    col4.plotly_chart(px.area(funnel, x="Stage", y="Count"), use_container_width=True)

# ================= FLOW =================
elif page == "Conversion Flow":

    funnel = df[["Visitors","Leads","Qualified","Customers"]].sum().reset_index()
    funnel.columns = ["Stage","Count"]

    funnel["Conversion %"] = funnel["Count"].pct_change().fillna(1) * 100

    col1, col2 = st.columns(2)

    col1.plotly_chart(px.line(funnel, x="Stage", y="Conversion %", markers=True), use_container_width=True)

    col2.plotly_chart(px.bar(funnel, x="Stage", y="Count", color="Stage"), use_container_width=True)

    col3, col4 = st.columns(2)

    col3.plotly_chart(px.scatter(funnel, x="Stage", y="Conversion %", size="Count"), use_container_width=True)

    col4.plotly_chart(px.area(funnel, x="Stage", y="Conversion %"), use_container_width=True)

    st.dataframe(funnel)

# ================= CHANNEL =================
elif page == "Acquisition Channels":

    grouped = df.groupby("Channel")[["Visitors","Leads","Customers"]].sum().reset_index()

    col1, col2 = st.columns(2)

    col1.plotly_chart(px.bar(grouped, x="Channel", y="Visitors", color="Channel"), use_container_width=True)

    col2.plotly_chart(px.bar(grouped, x="Channel", y="Customers", color="Channel"), use_container_width=True)

    col3, col4 = st.columns(2)

    col3.plotly_chart(px.pie(grouped, names="Channel", values="Customers"), use_container_width=True)

    col4.plotly_chart(px.scatter(grouped, x="Visitors", y="Customers", color="Channel", size="Customers"), use_container_width=True)

    col5, col6 = st.columns(2)

    col5.plotly_chart(px.treemap(grouped, path=["Channel"], values="Customers"), use_container_width=True)

    col6.plotly_chart(px.area(grouped, x="Channel", y="Visitors"), use_container_width=True)

# ================= DROP OFF =================
elif page == "Drop-off Intelligence":

    funnel = df[["Visitors","Leads","Qualified","Customers"]].sum()

    drop = pd.DataFrame({
        "Stage": ["Visitors→Leads","Leads→Qualified","Qualified→Customers"],
        "Drop %": [
            100 - (funnel["Leads"]/funnel["Visitors"]*100),
            100 - (funnel["Qualified"]/funnel["Leads"]*100),
            100 - (funnel["Customers"]/funnel["Qualified"]*100)
        ]
    })

    col1, col2 = st.columns(2)

    col1.plotly_chart(px.bar(drop, x="Stage", y="Drop %", color="Stage"), use_container_width=True)

    col2.plotly_chart(px.line(drop, x="Stage", y="Drop %", markers=True), use_container_width=True)

    col3, col4 = st.columns(2)

    col3.plotly_chart(px.area(drop, x="Stage", y="Drop %"), use_container_width=True)

    col4.plotly_chart(px.pie(drop, names="Stage", values="Drop %"), use_container_width=True)

    st.dataframe(drop)

# ================= INSIGHTS =================
elif page == "Strategic Insights":

    st.markdown("""
    ## 🚀 Executive Growth Intelligence

    ### 🔍 Funnel Bottlenecks
    Significant friction exists in early funnel stages, causing major user drop-offs before conversion.

    ### 📊 Channel Effectiveness
    High traffic does not always equal high-quality leads. Some channels underperform in conversion.

    ### ⚡ Optimization Opportunities
    Early-stage optimization (landing pages, targeting) offers the highest ROI impact.

    ### 🚀 Strategic Actions
    - Double down on high-converting channels  
    - Optimize landing experience and CTAs  
    - Implement retargeting funnels  
    - Improve lead qualification pipelines  

    ### 💰 Business Impact
    Even a **5% improvement in funnel conversion can exponentially increase revenue and customer acquisition efficiency**.
    """)