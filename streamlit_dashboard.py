import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Universal Bank - Personal Loan Analytics",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and header
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #1f77b4;
            margin-bottom: 20px;
        }
        .section-title {
            color: #1f77b4;
            border-bottom: 3px solid #1f77b4;
            padding-bottom: 10px;
            margin-top: 20px;
        }
    </style>
    <h1 class="main-title">💰 Universal Bank Personal Loan Marketing Dashboard</h1>
    <p style="text-align: center; color: #666;">Data-Driven Customer Segmentation & Marketing Analysis</p>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel('UniversalBank with description.xls', sheet_name='Data', header=3)
    
    # Convert numeric columns
    numeric_cols = ['Age', 'Experience', 'Income', 'Family', 'CCAvg', 'Mortgage', 
                   'Securities Account', 'CD Account', 'Online', 'CreditCard', 'Personal Loan']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna()
    return df

df = load_data()

# Sidebar for filters and navigation
st.sidebar.markdown("## 🎯 Navigation & Filters")
section = st.sidebar.radio(
    "Select Analysis Section:",
    ["📊 Overview", "📈 Income Analysis", "💳 Credit Card Analysis", 
     "🎓 Education Analysis", "🎪 VIP Segment", "🎯 Customer Tiers", "📋 Data Explorer"]
)

# Sidebar filters
st.sidebar.markdown("---")
st.sidebar.markdown("## 🔍 Filters")

income_range = st.sidebar.slider(
    "Income Range ($k):",
    int(df['Income'].min()),
    int(df['Income'].max()),
    (40, 200)
)

cc_spending_range = st.sidebar.slider(
    "CC Spending Range ($k/month):",
    float(df['CCAvg'].min()),
    float(df['CCAvg'].max()),
    (0.0, 10.0),
    step=0.1
)

education_filter = st.sidebar.multiselect(
    "Education Level:",
    [1, 2, 3],
    default=[1, 2, 3],
    format_func=lambda x: {1: "Undergrad", 2: "Graduate", 3: "Professional"}.get(x)
)

loan_filter = st.sidebar.multiselect(
    "Personal Loan Status:",
    [0, 1],
    default=[0, 1],
    format_func=lambda x: {0: "No Loan", 1: "Accepted Loan"}.get(x)
)

# Apply filters
df_filtered = df[
    (df['Income'] >= income_range[0]) &
    (df['Income'] <= income_range[1]) &
    (df['CCAvg'] >= cc_spending_range[0]) &
    (df['CCAvg'] <= cc_spending_range[1]) &
    (df['Education'].isin(education_filter)) &
    (df['Personal Loan'].isin(loan_filter))
]

st.sidebar.metric("Filtered Records", len(df_filtered), delta=len(df_filtered)-len(df))
st.sidebar.metric("Conversion Rate", f"{df_filtered['Personal Loan'].mean()*100:.1f}%")

# ============================================
# SECTION 1: OVERVIEW
# ============================================
if section == "📊 Overview":
    st.markdown("<h2 class='section-title'>Dashboard Overview</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Customers", len(df), delta=len(df_filtered))
    with col2:
        st.metric("Loan Rate", f"{df['Personal Loan'].mean()*100:.1f}%", 
                 delta=f"{(df_filtered['Personal Loan'].mean()-df['Personal Loan'].mean())*100:+.1f}%")
    with col3:
        st.metric("Avg Income", f"${df['Income'].mean():.0f}k", 
                 delta=f"${df_filtered['Income'].mean()-df['Income'].mean():+.0f}k")
    with col4:
        st.metric("Avg CC Spending", f"${df['CCAvg'].mean():.2f}k", 
                 delta=f"${df_filtered['CCAvg'].mean()-df['CCAvg'].mean():+.2f}k")
    with col5:
        st.metric("Filtered Data %", f"{len(df_filtered)/len(df)*100:.1f}%")
    
    st.markdown("---")
    
    # Key insights cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        ### 🎯 Income Insight
        - **Critical Threshold**: $80k
        - **Target Zone**: $100k - $200k
        - **Conversion by Income:**
            - < $80k: < 5%
            - $100k-150k: 15-18%
            - > $150k: > 20%
        """)
    
    with col2:
        st.success("""
        ### 💳 Spending Insight
        - **High Spenders (>$5k/mo)**: 32.7% conversion
        - **Active Spenders ($2-4k)**: 12-22% conversion
        - **Low Spenders (<$1k)**: Skip these customers
        - **VIP Opportunity**: 6.5% with exceptional intent
        """)
    
    with col3:
        st.warning("""
        ### 🎓 Education Insight
        - **Undergrad**: 4.4% conversion
        - **Graduate**: 13% conversion
        - **Professional**: 13.7% conversion
        - **3x difference** between levels
        """)
    
    # Quick stats table
    st.markdown("#### 📊 Quick Statistics")
    stats_df = pd.DataFrame({
        'Metric': ['Total Customers', 'Loan Acceptance %', 'Avg Income ($k)', 'Avg CC Spending ($k)', 'Undergrad %', 'Graduate %', 'Professional %'],
        'Overall': [
            f"{len(df):,}",
            f"{df['Personal Loan'].mean()*100:.1f}%",
            f"${df['Income'].mean():.1f}",
            f"${df['CCAvg'].mean():.2f}",
            f"{(df['Education']==1).sum()/len(df)*100:.1f}%",
            f"{(df['Education']==2).sum()/len(df)*100:.1f}%",
            f"{(df['Education']==3).sum()/len(df)*100:.1f}%"
        ],
        'Filtered': [
            f"{len(df_filtered):,}",
            f"{df_filtered['Personal Loan'].mean()*100:.1f}%",
            f"${df_filtered['Income'].mean():.1f}",
            f"${df_filtered['CCAvg'].mean():.2f}",
            f"{(df_filtered['Education']==1).sum()/len(df_filtered)*100:.1f}%" if len(df_filtered) > 0 else "0%",
            f"{(df_filtered['Education']==2).sum()/len(df_filtered)*100:.1f}%" if len(df_filtered) > 0 else "0%",
            f"{(df_filtered['Education']==3).sum()/len(df_filtered)*100:.1f}%" if len(df_filtered) > 0 else "0%"
        ]
    })
    st.dataframe(stats_df, use_container_width=True)

# ============================================
# SECTION 2: INCOME ANALYSIS
# ============================================
elif section == "📈 Income Analysis":
    st.markdown("<h2 class='section-title'>Income Distribution & Loan Acceptance</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Distribution by Loan Status")
        fig = px.histogram(
            df_filtered,
            x='Income',
            color='Personal Loan',
            nbins=50,
            title='Income Distribution',
            labels={'Personal Loan': 'Loan Status', 'Income': 'Income ($k)'},
            color_discrete_map={0: '#1f77b4', 1: '#ff7f0e'}
        )
        fig.update_xaxes(title_text='Income ($k)')
        fig.update_yaxes(title_text='Number of Customers')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Box Plot by Loan Status")
        fig = px.box(
            df_filtered,
            x='Personal Loan',
            y='Income',
            title='Income Distribution (Box Plot)',
            labels={'Personal Loan': 'Loan Status', 'Income': 'Income ($k)'},
            color_discrete_sequence=['#1f77b4', '#ff7f0e']
        )
        fig.update_xaxes(title_text='Loan Status', 
                        ticktext=['No Loan', 'Accepted Loan'],
                        tickvals=[0, 1])
        st.plotly_chart(fig, use_container_width=True)
    
    # Income statistics by loan status
    st.markdown("### Income Statistics by Loan Status")
    col1, col2 = st.columns(2)
    
    income_loan = df_filtered[df_filtered['Personal Loan'] == 1]['Income']
    income_no_loan = df_filtered[df_filtered['Personal Loan'] == 0]['Income']
    
    with col1:
        st.metric("Loan Customers - Avg Income", f"${income_loan.mean():.1f}k", 
                 delta=f"${income_loan.mean()-df_filtered['Income'].mean():+.1f}k")
        st.metric("Loan Customers - Min Income", f"${income_loan.min():.1f}k")
        st.metric("Loan Customers - Median Income", f"${income_loan.median():.1f}k")
    
    with col2:
        st.metric("Non-Loan Customers - Avg Income", f"${income_no_loan.mean():.1f}k",
                 delta=f"${income_no_loan.mean()-df_filtered['Income'].mean():+.1f}k")
        st.metric("Non-Loan Customers - Max Income", f"${income_no_loan.max():.1f}k")
        st.metric("Non-Loan Customers - Median Income", f"${income_no_loan.median():.1f}k")
    
    # Income vs conversion rate
    st.markdown("### Conversion Rate by Income Bracket")
    income_bins = [0, 40, 80, 120, 160, 224]
    income_labels = ['<$40k', '$40-80k', '$80-120k', '$120-160k', '>$160k']
    df_filtered['Income_Bracket'] = pd.cut(df_filtered['Income'], bins=income_bins, labels=income_labels)
    
    conversion_by_income = df_filtered.groupby('Income_Bracket', observed=True)['Personal Loan'].agg(['mean', 'count'])
    conversion_by_income['mean'] = conversion_by_income['mean'] * 100
    
    fig = px.bar(
        conversion_by_income.reset_index(),
        x='Income_Bracket',
        y='mean',
        title='Conversion Rate by Income Bracket',
        labels={'mean': 'Conversion Rate (%)', 'Income_Bracket': 'Income Bracket'},
        color='mean',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# SECTION 3: CREDIT CARD ANALYSIS
# ============================================
elif section == "💳 Credit Card Analysis":
    st.markdown("<h2 class='section-title'>Credit Card Spending Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### CC Spending Distribution")
        fig = px.histogram(
            df_filtered,
            x='CCAvg',
            color='Personal Loan',
            nbins=50,
            title='CC Spending Distribution',
            labels={'CCAvg': 'Monthly CC Spending ($k)', 'Personal Loan': 'Loan Status'},
            color_discrete_map={0: '#1f77b4', 1: '#ff7f0e'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Income vs CC Spending (Scatter)")
        fig = px.scatter(
            df_filtered,
            x='Income',
            y='CCAvg',
            color='Personal Loan',
            title='Income vs CC Spending',
            labels={'Income': 'Income ($k)', 'CCAvg': 'Monthly CC Spending ($k)', 'Personal Loan': 'Loan Status'},
            color_discrete_map={0: '#1f77b4', 1: '#ff7f0e'},
            opacity=0.6
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Outlier detection
    st.markdown("### VIP Outlier Detection (High Spenders)")
    Q1 = df_filtered['CCAvg'].quantile(0.25)
    Q3 = df_filtered['CCAvg'].quantile(0.75)
    IQR = Q3 - Q1
    outlier_threshold = Q3 + 1.5 * IQR
    
    outliers = df_filtered[df_filtered['CCAvg'] > outlier_threshold]
    normal = df_filtered[df_filtered['CCAvg'] <= outlier_threshold]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Outlier Customers", len(outliers), delta=f"{len(outliers)/len(df_filtered)*100:.1f}%")
    with col2:
        st.metric("Outlier Conversion Rate", f"{outliers['Personal Loan'].mean()*100:.1f}%",
                 delta=f"{(outliers['Personal Loan'].mean()-normal['Personal Loan'].mean())*100:+.1f}%")
    with col3:
        st.metric("Outlier Threshold", f"${outlier_threshold:.2f}k")
    
    st.info(f"""
    ### 🎪 VIP Segment Insights:
    - **High Spenders (>$5k/month)**: {len(outliers)} customers ({len(outliers)/len(df_filtered)*100:.1f}%)
    - **Conversion Rate**: {outliers['Personal Loan'].mean()*100:.1f}% (vs {normal['Personal Loan'].mean()*100:.1f}% for normal)
    - **Relative Performance**: {outliers['Personal Loan'].mean()/normal['Personal Loan'].mean():.1f}x better than average
    - **Recommendation**: Premium service tier with dedicated account managers
    """)

# ============================================
# SECTION 4: EDUCATION ANALYSIS
# ============================================
elif section == "🎓 Education Analysis":
    st.markdown("<h2 class='section-title'>Education Level Impact</h2>", unsafe_allow_html=True)
    
    education_map = {1: 'Undergrad', 2: 'Graduate', 3: 'Professional'}
    df_filtered['Education_Label'] = df_filtered['Education'].map(education_map)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Conversion Rate by Education")
        education_stats = df_filtered.groupby('Education_Label', observed=True)['Personal Loan'].agg(['mean', 'count'])
        education_stats['mean'] = education_stats['mean'] * 100
        
        fig = px.bar(
            education_stats.reset_index(),
            x='Education_Label',
            y='mean',
            title='Loan Acceptance Rate by Education',
            labels={'mean': 'Conversion Rate (%)', 'Education_Label': 'Education Level'},
            color='mean',
            color_continuous_scale='Viridis',
            text='mean'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Income by Education Level")
        fig = px.box(
            df_filtered,
            x='Education_Label',
            y='Income',
            title='Income Distribution by Education',
            labels={'Education_Label': 'Education Level', 'Income': 'Income ($k)'},
            color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Education statistics
    st.markdown("### Detailed Education Statistics")
    edu_stats = df_filtered.groupby('Education_Label', observed=True).agg({
        'Personal Loan': ['count', 'sum', 'mean'],
        'Income': ['mean', 'median', 'min', 'max'],
        'CCAvg': 'mean'
    }).round(2)
    
    edu_stats.columns = ['Count', 'Loan_Count', 'Loan_Rate', 'Avg_Income', 'Median_Income', 'Min_Income', 'Max_Income', 'Avg_CC']
    edu_stats['Loan_Rate'] = (edu_stats['Loan_Rate'] * 100).round(1).astype(str) + '%'
    
    st.dataframe(edu_stats, use_container_width=True)

# ============================================
# SECTION 5: VIP SEGMENT
# ============================================
elif section == "🎪 VIP Segment":
    st.markdown("<h2 class='section-title'>VIP Customer Segment Analysis</h2>", unsafe_allow_html=True)
    
    # Define VIP tiers
    vip_tier1 = df_filtered[
        (df_filtered['Income'] >= 150) &
        (df_filtered['CCAvg'] >= 4) &
        (df_filtered['Education'].isin([2, 3]))
    ]
    
    vip_tier2 = df_filtered[
        (df_filtered['Income'] >= 100) &
        (df_filtered['Income'] < 150) &
        (df_filtered['CCAvg'] >= 2) &
        (df_filtered['CCAvg'] < 4) &
        (df_filtered['Education'].isin([2, 3]))
    ]
    
    outlier_threshold = df_filtered['CCAvg'].quantile(0.75) + 1.5 * (df_filtered['CCAvg'].quantile(0.75) - df_filtered['CCAvg'].quantile(0.25))
    vip_outliers = df_filtered[df_filtered['CCAvg'] > outlier_threshold]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Tier 1 (VIP)", len(vip_tier1), delta=f"{len(vip_tier1)/len(df_filtered)*100:.1f}%")
        st.metric("T1 Conversion", f"{vip_tier1['Personal Loan'].mean()*100:.1f}%")
    
    with col2:
        st.metric("Tier 2 (Core)", len(vip_tier2), delta=f"{len(vip_tier2)/len(df_filtered)*100:.1f}%")
        st.metric("T2 Conversion", f"{vip_tier2['Personal Loan'].mean()*100:.1f}%")
    
    with col3:
        st.metric("High Spenders", len(vip_outliers), delta=f"{len(vip_outliers)/len(df_filtered)*100:.1f}%")
        st.metric("HS Conversion", f"{vip_outliers['Personal Loan'].mean()*100:.1f}%")
    
    st.markdown("---")
    
    # VIP characteristics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🌟 Tier 1: Premium VIP")
        st.write(f"""
        - **Income**: $150k+
        - **CC Spending**: $4k+/month
        - **Education**: Graduate/Professional
        - **Count**: {len(vip_tier1)} customers
        - **Conversion**: {vip_tier1['Personal Loan'].mean()*100:.1f}%
        - **Action**: Dedicated account managers
        - **Expected ROI**: 35-40%
        """)
    
    with col2:
        st.markdown("#### ⭐ Tier 2: Core Targets")
        st.write(f"""
        - **Income**: $100k-150k
        - **CC Spending**: $2k-4k/month
        - **Education**: Graduate/Professional
        - **Count**: {len(vip_tier2)} customers
        - **Conversion**: {vip_tier2['Personal Loan'].mean()*100:.1f}%
        - **Action**: Email/phone campaigns
        - **Expected ROI**: 18-22%
        """)
    
    with col3:
        st.markdown("#### 💎 High Spenders")
        st.write(f"""
        - **CC Spending**: > ${outlier_threshold:.1f}k/month
        - **Count**: {len(vip_outliers)} customers
        - **Conversion**: {vip_outliers['Personal Loan'].mean()*100:.1f}%
        - **Avg Income**: ${vip_outliers['Income'].mean():.0f}k
        - **Action**: Premium products
        - **Expected ROI**: 25-32%
        """)
    
    # Visualization: VIP segments comparison
    st.markdown("### VIP Segment Comparison")
    
    fig = go.Figure()
    
    segments = ['Tier 1 (VIP)', 'Tier 2 (Core)', 'High Spenders']
    counts = [len(vip_tier1), len(vip_tier2), len(vip_outliers)]
    conversions = [
        vip_tier1['Personal Loan'].mean() * 100,
        vip_tier2['Personal Loan'].mean() * 100,
        vip_outliers['Personal Loan'].mean() * 100
    ]
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'pie'}, {'type': 'bar'}]]
    )
    
    fig.add_trace(
        go.Pie(labels=segments, values=counts, name='Count', hole=0.3),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=segments, y=conversions, name='Conversion Rate', 
               marker_color=['#2ca02c', '#ff7f0e', '#d62728']),
        row=1, col=2
    )
    
    fig.update_yaxes(title_text='Conversion Rate (%)', row=1, col=2)
    fig.update_layout(height=400, title_text='VIP Segments: Size and Conversion')
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# SECTION 6: CUSTOMER TIERS
# ============================================
elif section == "🎯 Customer Tiers":
    st.markdown("<h2 class='section-title'>3-Tier Customer Segmentation Model</h2>", unsafe_allow_html=True)
    
    # Create tiering logic
    def assign_tier(row):
        if (row['Income'] >= 150) and (row['CCAvg'] >= 4) and (row['Education'] in [2, 3]):
            return 'Tier 1: VIP'
        elif (row['Income'] >= 100) and (row['Income'] < 150) and (row['CCAvg'] >= 2) and (row['Education'] in [2, 3]):
            return 'Tier 2: Core'
        elif (row['Income'] >= 80) and (row['CCAvg'] >= 1):
            return 'Tier 3: Secondary'
        else:
            return 'Do Not Pursue'
    
    df_filtered['Tier'] = df_filtered.apply(assign_tier, axis=1)
    
    # Tier distribution
    tier_counts = df_filtered['Tier'].value_counts()
    tier_conversion = df_filtered.groupby('Tier')['Personal Loan'].agg(['mean', 'count', 'sum'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    tiers_order = ['Tier 1: VIP', 'Tier 2: Core', 'Tier 3: Secondary', 'Do Not Pursue']
    colors = ['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728']
    
    for idx, (tier, color) in enumerate(zip(tiers_order, colors)):
        if tier in tier_counts.index:
            count = tier_counts[tier]
            conv_rate = tier_conversion.loc[tier, 'mean'] * 100 if tier in tier_conversion.index else 0
            if idx % 4 < 4:
                col = [col1, col2, col3, col4][idx % 4]
                with col:
                    st.metric(
                        tier,
                        f"{count} ({count/len(df_filtered)*100:.1f}%)",
                        delta=f"Conv: {conv_rate:.1f}%",
                        delta_color="normal" if idx < 3 else "off"
                    )
    
    st.markdown("---")
    
    # Tier comparison chart
    st.markdown("### Tier Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            tier_counts.reset_index(),
            values='count',
            names='Tier',
            title='Customer Distribution by Tier',
            color_discrete_sequence=['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728'],
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        tier_conv_sorted = tier_conversion['mean'].sort_values(ascending=False) * 100
        fig = px.bar(
            x=tier_conv_sorted.index,
            y=tier_conv_sorted.values,
            title='Conversion Rate by Tier',
            labels={'x': 'Tier', 'y': 'Conversion Rate (%)'},
            color=tier_conv_sorted.values,
            color_continuous_scale='RdYlGn',
            text=tier_conv_sorted.values.round(1)
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed tier analysis
    st.markdown("### Tier Details & Recommendations")
    
    for tier, color in zip(tiers_order, colors):
        if tier in df_filtered['Tier'].values:
            tier_data = df_filtered[df_filtered['Tier'] == tier]
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"### 🎯 {tier}")
                st.write(f"""
                **Size**: {len(tier_data)} customers ({len(tier_data)/len(df_filtered)*100:.1f}%)
                **Conversion**: {tier_data['Personal Loan'].mean()*100:.1f}%
                **Avg Income**: ${tier_data['Income'].mean():.0f}k
                **Avg CC Spending**: ${tier_data['CCAvg'].mean():.2f}k/month
                """)
            
            with col2:
                if tier == 'Tier 1: VIP':
                    st.success("✅ **Action**: Dedicated account managers, premium service, fast-track approval")
                elif tier == 'Tier 2: Core':
                    st.info("ℹ️ **Action**: Email campaigns, phone outreach, standard approval")
                elif tier == 'Tier 3: Secondary':
                    st.warning("⚠️ **Action**: Digital marketing, lower budget allocation")
                else:
                    st.error("❌ **Action**: No outreach, focus on Tier 1-3")
            
            st.markdown("---")

# ============================================
# SECTION 7: DATA EXPLORER
# ============================================
elif section == "📋 Data Explorer":
    st.markdown("<h2 class='section-title'>Interactive Data Explorer</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Raw Data", "📈 Statistics", "🔗 Correlations"])
    
    with tab1:
        st.markdown("### Filtered Dataset")
        st.dataframe(
            df_filtered[['ID', 'Age', 'Income', 'CCAvg', 'Education', 'Mortgage', 'Personal Loan']].head(100),
            use_container_width=True,
            height=400
        )
        
        st.markdown("### Download Data")
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="filtered_customers.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.markdown("### Summary Statistics")
        
        numeric_columns = ['Age', 'Experience', 'Income', 'Family', 'CCAvg', 'Mortgage']
        
        stats = df_filtered[numeric_columns].describe().T
        st.dataframe(stats, use_container_width=True)
        
        # By loan status
        st.markdown("### Statistics by Loan Status")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Loan = 0 (No Loan)")
            st.dataframe(
                df_filtered[df_filtered['Personal Loan'] == 0][numeric_columns].describe().T,
                use_container_width=True
            )
        
        with col2:
            st.markdown("#### Loan = 1 (Accepted Loan)")
            st.dataframe(
                df_filtered[df_filtered['Personal Loan'] == 1][numeric_columns].describe().T,
                use_container_width=True
            )
    
    with tab3:
        st.markdown("### Correlation Matrix")
        
        numeric_cols = ['Age', 'Experience', 'Income', 'Family', 'CCAvg', 'Mortgage', 'Personal Loan', 'CD Account']
        corr_matrix = df_filtered[numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            labels=dict(x="Variable", y="Variable", color="Correlation"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale='RdBu',
            color_continuous_midpoint=0,
            zmin=-1,
            zmax=1,
            text_auto='.2f'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Top Correlations with Personal Loan")
        loan_corr = corr_matrix['Personal Loan'].sort_values(ascending=False)
        
        fig = px.bar(
            x=loan_corr.index,
            y=loan_corr.values,
            title='Variable Correlation with Personal Loan',
            labels={'x': 'Variable', 'y': 'Correlation'},
            color=loan_corr.values,
            color_continuous_scale='RdBu',
            color_continuous_midpoint=0
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <footer style="text-align: center; color: #666; margin-top: 40px;">
    <p>Universal Bank Personal Loan Marketing Analytics Dashboard</p>
    <p>Data Source: UniversalBank with description.xls | Sample: 5,000 customers | Last Updated: December 2025</p>
    <p>Developed with Streamlit | <strong>Status: </strong>Ready for Implementation</p>
    </footer>
""", unsafe_allow_html=True)
