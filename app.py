import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title='Nassau Candy Route Efficiency', page_icon='🍫', layout='wide')
BASE = Path(__file__).parent

@st.cache_data
def load_data():
    route = pd.read_csv(BASE/'route_summary.csv')
    state = pd.read_csv(BASE/'state_summary.csv')
    region = pd.read_csv(BASE/'region_summary.csv')
    ship = pd.read_csv(BASE/'ship_mode_summary.csv')
    factory = pd.read_csv(BASE/'factory_summary.csv')
    bottleneck = pd.read_csv(BASE/'geographic_bottlenecks.csv')
    return route, state, region, ship, factory, bottleneck

route_all, state_all, region_all, ship_all, factory_all, bottleneck_all = load_data()

st.markdown('''<style>
.stApp{background:#0e1117;color:#f5f5f5}.block-container{padding-top:1.2rem}
[data-testid="stSidebar"]{background:#151922}
.metric-card{background:#171b24;border:1px solid #2b3240;border-radius:12px;padding:14px;text-align:center}
.metric-title{color:#aab2c0;font-size:.82rem}.metric-value{color:#fff;font-size:1.45rem;font-weight:700}
</style>''', unsafe_allow_html=True)

st.title('🍫 Nassau Candy — Factory-to-Customer Shipping Route Efficiency')
st.caption('Interactive analysis of routes, factories, regions, geographic bottlenecks and shipping modes')

st.sidebar.header('Filters')
regions = sorted(region_all['Region'].dropna().unique())
region_filter = st.sidebar.multiselect('Region', regions, default=regions)
states = sorted(state_all['State/Province'].dropna().unique())
state_filter = st.sidebar.multiselect('State / Province', states, default=[])
modes = sorted(ship_all['Ship Mode'].dropna().unique())
mode_filter = st.sidebar.multiselect('Ship Mode', modes, default=modes)
threshold = st.sidebar.number_input('Lead-Time Threshold (days)', 0.0, 2000.0, 1274.0, 1.0)

region = region_all[region_all['Region'].isin(region_filter)] if region_filter else region_all.copy()
state = state_all[state_all['State/Province'].isin(state_filter)] if state_filter else state_all.copy()
ship = ship_all[ship_all['Ship Mode'].isin(mode_filter)] if mode_filter else ship_all.copy()
bottleneck = bottleneck_all[bottleneck_all['State/Province'].isin(state_filter)] if state_filter else bottleneck_all.copy()

total_orders = 10194
weighted_lead = (factory_all['Shipments'] * factory_all['Average_Lead_Time']).sum() / factory_all['Shipments'].sum()
route_volume = int(region['Route_Volume'].sum()) if not region.empty else 0
delay_freq = float(ship['Default_Delay_Frequency_%'].mean()) if not ship.empty else 0

cols=st.columns(5)
for col,title,value in zip(cols,['Total Orders','Avg Lead Time','Route Volume','Delay Frequency','Factories'],[f'{total_orders:,}',f'{weighted_lead:,.2f} days',f'{route_volume:,}',f'{delay_freq:.2f}%',f'{factory_all.shape[0]}']):
    col.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value">{value}</div></div>',unsafe_allow_html=True)

c1,c2=st.columns(2)
with c1:
    st.subheader('Fastest Routes')
    x=route_all.sort_values('Average_Lead_Time').head(10).sort_values('Average_Lead_Time')
    fig=px.bar(x,x='Average_Lead_Time',y='Route',orientation='h',text='Average_Lead_Time',template='plotly_dark',labels={'Average_Lead_Time':'Average Lead Time (days)','Route':''})
    fig.update_traces(texttemplate='%{text:.1f}',textposition='outside'); fig.update_layout(height=430); st.plotly_chart(fig,use_container_width=True)
with c2:
    st.subheader('Route Performance Leaderboard')
    x=route_all.sort_values('Route_Efficiency_Score',ascending=False).head(10).sort_values('Route_Efficiency_Score')
    fig=px.bar(x,x='Route_Efficiency_Score',y='Route',orientation='h',text='Route_Efficiency_Score',template='plotly_dark',labels={'Route_Efficiency_Score':'Efficiency Score','Route':''})
    fig.update_traces(texttemplate='%{text:.1f}',textposition='outside'); fig.update_layout(height=430); st.plotly_chart(fig,use_container_width=True)

c1,c2=st.columns(2)
with c1:
    st.subheader('Average Lead Time by Region')
    fig=px.bar(region.sort_values('Average_Lead_Time'),x='Region',y='Average_Lead_Time',text='Route_Volume',template='plotly_dark',labels={'Average_Lead_Time':'Average Lead Time (days)','Route_Volume':'Route Volume'})
    fig.update_traces(texttemplate='Volume: %{text}',textposition='outside'); fig.update_layout(height=400); st.plotly_chart(fig,use_container_width=True)
with c2:
    st.subheader('Ship Mode Comparison')
    fig=px.bar(ship.sort_values('Average_Lead_Time'),x='Ship Mode',y='Average_Lead_Time',text='Average_Lead_Time',template='plotly_dark',labels={'Average_Lead_Time':'Average Lead Time (days)'})
    fig.update_traces(texttemplate='%{text:.1f}',textposition='outside'); fig.update_layout(height=400); st.plotly_chart(fig,use_container_width=True)

st.subheader('Geographic Bottlenecks')
if not bottleneck.empty:
    x=bottleneck.sort_values('Bottleneck_Score',ascending=False).head(15)
    fig=px.bar(x,x='Bottleneck_Score',y='State/Province',orientation='h',text='Route_Volume',template='plotly_dark',labels={'Bottleneck_Score':'Bottleneck Score','Route_Volume':'Shipments'})
    fig.update_traces(texttemplate='Vol: %{text}',textposition='outside'); fig.update_layout(height=470); st.plotly_chart(fig,use_container_width=True)

st.subheader('State Performance')
mapdf=state[state['State/Province'].str.len()==2]
if not mapdf.empty:
    fig=px.choropleth(mapdf,locations='State/Province',locationmode='USA-states',color='Average_Lead_Time',scope='usa',hover_name='State/Province',hover_data=['Route_Volume','Median_Lead_Time','Sales','Gross_Profit'],template='plotly_dark',labels={'Average_Lead_Time':'Avg Lead Time'})
    fig.update_layout(height=500); st.plotly_chart(fig,use_container_width=True)

st.subheader('Factory Performance')
st.dataframe(factory_all.sort_values('Shipments',ascending=False),use_container_width=True,hide_index=True)

st.subheader('Route Drill-Down')
st.dataframe(route_all.sort_values('Route_Efficiency_Score',ascending=False),use_container_width=True,hide_index=True)

st.caption('Data validation note: the supplied source dates produce unusually large lead-time values (about 904–1642 days). These values are retained for analysis consistency and should be validated before operational decisions.')
