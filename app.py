import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title='Nassau Candy Route Efficiency', page_icon='🍫', layout='wide')
BASE = Path(__file__).parent

@st.cache_data
def load_data():
    parts = sorted(BASE.glob('nassau_data_part*.csv'))
    df = pd.concat([pd.read_csv(p) for p in parts], ignore_index=True)
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
    route = pd.read_csv(BASE/'route_summary.csv')
    state = pd.read_csv(BASE/'state_summary.csv')
    region = pd.read_csv(BASE/'region_summary.csv')
    ship = pd.read_csv(BASE/'ship_mode_summary.csv')
    factory = pd.read_csv(BASE/'factory_summary.csv')
    bottleneck = pd.read_csv(BASE/'geographic_bottlenecks.csv')
    return df, route, state, region, ship, factory, bottleneck

df, route_all, state_all, region_all, ship_all, factory_all, bottleneck_all = load_data()

st.markdown('''<style>
.stApp{background:#0e1117;color:#f5f5f5}.block-container{padding-top:1.2rem}
[data-testid="stSidebar"]{background:#151922}
.metric-card{background:#171b24;border:1px solid #2b3240;border-radius:12px;padding:14px;text-align:center}
.metric-title{color:#aab2c0;font-size:.82rem}.metric-value{color:#fff;font-size:1.45rem;font-weight:700}
</style>''', unsafe_allow_html=True)

st.title('🍫 Nassau Candy — Factory-to-Customer Shipping Route Efficiency')
st.caption('Interactive analysis of routes, factories, regions, geographic bottlenecks and shipping modes')

st.sidebar.header('Filters')
min_date, max_date = df['Order Date'].min().date(), df['Order Date'].max().date()
date_range = st.sidebar.date_input('Order Date Range', (min_date, max_date), min_value=min_date, max_value=max_date)
regions = sorted(df['Region'].dropna().unique())
region_filter = st.sidebar.multiselect('Region', regions, default=regions)
states = sorted(df['State/Province'].dropna().unique())
state_filter = st.sidebar.multiselect('State / Province', states, default=[])
modes = sorted(df['Ship Mode'].dropna().unique())
mode_filter = st.sidebar.multiselect('Ship Mode', modes, default=modes)
threshold = st.sidebar.number_input('Lead-Time Threshold (days)', 0.0, float(df['Lead Time Days'].max()), float(df['Lead Time Days'].median()), 1.0)

filtered=df.copy()
if isinstance(date_range,(tuple,list)) and len(date_range)==2:
    s,e=pd.Timestamp(date_range[0]),pd.Timestamp(date_range[1])
    filtered=filtered[(filtered['Order Date']>=s)&(filtered['Order Date']<e+pd.Timedelta(days=1))]
if region_filter: filtered=filtered[filtered['Region'].isin(region_filter)]
if state_filter: filtered=filtered[filtered['State/Province'].isin(state_filter)]
if mode_filter: filtered=filtered[filtered['Ship Mode'].isin(mode_filter)]
if filtered.empty: st.warning('No records match the selected filters.'); st.stop()

delay=(filtered['Lead Time Days']>threshold).mean()*100
routes=filtered[['Factory','State/Province']].drop_duplicates().shape[0]
eff=max(0,min(100,(df['Lead Time Days'].max()-filtered['Lead Time Days'].mean())/(df['Lead Time Days'].max()-df['Lead Time Days'].min())*100))

cols=st.columns(5)
for col,title,value in zip(cols,['Total Orders','Avg Lead Time','Route Volume','Delay Frequency','Route Efficiency'],[f'{len(filtered):,}',f"{filtered['Lead Time Days'].mean():,.2f} days",f'{routes:,}',f'{delay:.2f}%',f'{eff:.2f}/100']):
    col.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value">{value}</div></div>',unsafe_allow_html=True)

keys=filtered[['Factory','State/Province']].drop_duplicates()
route=route_all.merge(keys,on=['Factory','State/Province'],how='inner')
state=state_all[state_all['State/Province'].isin(filtered['State/Province'].unique())]
region=region_all[region_all['Region'].isin(filtered['Region'].unique())]
ship=ship_all[ship_all['Ship Mode'].isin(filtered['Ship Mode'].unique())]
bottleneck=bottleneck_all[bottleneck_all['State/Province'].isin(filtered['State/Province'].unique())]

c1,c2=st.columns(2)
with c1:
    st.subheader('Fastest Routes')
    x=route.sort_values('Average_Lead_Time').head(10).sort_values('Average_Lead_Time')
    fig=px.bar(x,x='Average_Lead_Time',y='Route',orientation='h',text='Average_Lead_Time',template='plotly_dark',labels={'Average_Lead_Time':'Average Lead Time (days)','Route':''})
    fig.update_traces(texttemplate='%{text:.1f}',textposition='outside'); fig.update_layout(height=430); st.plotly_chart(fig,use_container_width=True)
with c2:
    st.subheader('Route Performance Leaderboard')
    x=route.sort_values('Route_Efficiency_Score',ascending=False).head(15).sort_values('Route_Efficiency_Score')
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
    x=bottleneck.sort_values('Average_Lead_Time',ascending=False).head(15)
    fig=px.bar(x,x='Average_Lead_Time',y='State/Province',orientation='h',text='Route_Volume',template='plotly_dark',labels={'Average_Lead_Time':'Average Lead Time (days)','Route_Volume':'Shipments'})
    fig.update_traces(texttemplate='Vol: %{text}',textposition='outside'); fig.update_layout(height=470); st.plotly_chart(fig,use_container_width=True)

st.subheader('State Performance')
mapdf=state[state['State/Province'].str.len()==2]
if not mapdf.empty:
    fig=px.choropleth(mapdf,locations='State/Province',locationmode='USA-states',color='Average_Lead_Time',scope='usa',hover_name='State/Province',hover_data=['Route_Volume','Median_Lead_Time','Sales','Gross_Profit'],template='plotly_dark',labels={'Average_Lead_Time':'Avg Lead Time'})
    fig.update_layout(height=500); st.plotly_chart(fig,use_container_width=True)

st.subheader('Route Drill-Down')
show=[c for c in ['Factory','State/Province','Region','Route_Volume','Average_Lead_Time','Median_Lead_Time','Sales','Gross_Profit','Route_Efficiency_Score'] if c in route.columns]
st.dataframe(route.sort_values('Route_Efficiency_Score',ascending=False)[show],use_container_width=True,hide_index=True)

st.subheader('Filtered Order Timeline')
timeline=filtered.sort_values('Order Date')[['Order Date','Ship Date','Lead Time Days','Factory','State/Province','Ship Mode']]
fig=px.scatter(timeline,x='Order Date',y='Lead Time Days',color='Ship Mode',hover_data=['Ship Date','Factory','State/Province'],template='plotly_dark',labels={'Lead Time Days':'Lead Time (days)'})
fig.add_hline(y=threshold,line_dash='dash',annotation_text=f'Threshold: {threshold:.0f} days'); fig.update_layout(height=430); st.plotly_chart(fig,use_container_width=True)

st.caption('Data validation note: the supplied source dates produce unusually large lead-time values (about 904–1642 days). These values are retained for analysis consistency and should be validated before operational decisions.')
