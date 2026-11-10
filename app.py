from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Ocean Waste Management", page_icon="🌊", layout="wide")
DATA = Path(__file__).parent / "data" / "ocean_waste_dashboard_data.csv"
BLUE, ORANGE, TEAL, NAVY = "#1687D9", "#F28C5B", "#10A6A6", "#102A43"

st.markdown("""
<style>
.block-container{padding-top:1.2rem;max-width:1500px}
.hero{background:linear-gradient(110deg,#ef895b,#f5a477);padding:17px;border-radius:12px;margin-bottom:18px}
.hero h1{text-align:center;color:#142b3b;font-family:Georgia,serif;margin:0}
div[data-testid="stMetric"]{background:white;border:1px solid #dbe5ee;padding:13px;border-radius:10px}
</style>
<div class="hero"><h1>Ocean Waste Management</h1></div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    return df.dropna(subset=["Year"]).sort_values("Year")

df = load_data()
with st.sidebar:
    st.header("Dashboard filters")
    years = st.slider("Year range", int(df.Year.min()), int(df.Year.max()),
                      (int(df.Year.min()), int(df.Year.max())))
    era = st.multiselect("Historical period", ["Pre-plastic", "Industrial", "Modern"],
                         default=["Pre-plastic", "Industrial", "Modern"])
    st.caption("Filters apply to all visuals.")

def period(y):
    return "Pre-plastic" if y < 1950 else ("Industrial" if y < 1990 else "Modern")

df["Period"] = df.Year.map(period)
view = df[df.Year.between(*years) & df.Period.isin(era)].copy()
if view.empty:
    st.warning("No records match these filters.")
    st.stop()

latest = view.iloc[-1]
k = st.columns(4)
k[0].metric("Peak ocean waste", f'{view["Ocean Waste (MT)"].max():.2f} MT')
k[1].metric("Peak recycled waste", f'{view["Waste Recycled (MT)"].max():.2f} MT')
k[2].metric("Peak collected waste", f'{view["Waste Collected (MT)"].max():.2f} MT')
k[3].metric(f'Management efficiency ({int(latest.Year)})',
            f'{latest["Management Efficiency (%)"]:.0f}%')

left, right = st.columns(2)
with left:
    st.subheader("Waste composition")
    composition = pd.DataFrame({
        "Category": ["Plastic", "Fishing", "Other"],
        "MT": [view["Plastic Waste (MT)"].sum(),
               view["Fishing Waste (MT)"].sum(),
               view["Other Waste (MT)"].sum()]})
    fig = px.pie(composition, names="Category", values="MT", hole=.58,
                 color="Category", color_discrete_map={"Plastic": BLUE, "Fishing": ORANGE, "Other": TEAL})
    fig.update_traces(textposition="outside", textinfo="label+percent")
    fig.update_layout(height=340, margin=dict(t=10,b=10,l=10,r=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Management efficiency")
    fig = go.Figure(go.Indicator(mode="gauge+number",
        value=float(latest["Management Efficiency (%)"]), number={"suffix":"%"},
        title={"text": f'Latest selected year: {int(latest.Year)}'},
        gauge={"axis":{"range":[0,100]}, "bar":{"color":BLUE},
               "steps":[{"range":[0,40],"color":"#fce4d8"},
                        {"range":[40,70],"color":"#fff0d5"},
                        {"range":[70,100],"color":"#d8f1e9"}]}))
    fig.update_layout(height=340, margin=dict(t=35,b=10,l=20,r=20))
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Waste trends by year")
melt = view.melt("Year", ["Plastic Waste (MT)", "Fishing Waste (MT)",
                          "Other Waste (MT)", "Ocean Waste (MT)"],
                 var_name="Measure", value_name="Metric tons")
fig = px.line(melt, x="Year", y="Metric tons", color="Measure",
              color_discrete_map={"Plastic Waste (MT)":BLUE, "Fishing Waste (MT)":ORANGE,
                                  "Other Waste (MT)":TEAL, "Ocean Waste (MT)":NAVY})
fig.update_layout(height=390, hovermode="x unified", legend_title_text="")
st.plotly_chart(fig, use_container_width=True)

a, b = st.columns(2)
with a:
    st.subheader("Collected vs recycled")
    mgmt = view.melt("Year", ["Waste Collected (MT)", "Waste Recycled (MT)"],
                     var_name="Measure", value_name="Metric tons")
    fig = px.area(mgmt, x="Year", y="Metric tons", color="Measure",
                  color_discrete_map={"Waste Collected (MT)":BLUE, "Waste Recycled (MT)":TEAL})
    fig.update_layout(height=330, legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)
with b:
    st.subheader("Ocean waste by year")
    fig = px.bar(view, x="Year", y="Ocean Waste (MT)", color="Ocean Waste (MT)",
                 color_continuous_scale=["#b8d9f2", BLUE])
    fig.update_layout(height=330, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered annual data")
st.dataframe(view.drop(columns=["Period"]), use_container_width=True, hide_index=True)
st.download_button("Download filtered data (CSV)", view.drop(columns=["Period"]).to_csv(index=False),
                   "ocean_waste_filtered.csv", "text/csv")
st.caption("Source: supplied Ocean Waste Management annual dataset (1900–2026). AQI and geographic fields were not supplied, so no AQI or map values are fabricated.")
