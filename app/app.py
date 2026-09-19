"""
Streamlit Analytics Dashboard: Mental Health in Tech Survey
Interactive analytics, exploratory visualization, relationship exploration,
statistical hypothesis inspection, and data explorer.
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# Ensure local imports resolve cleanly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from components import (
    render_header, render_section_header, render_kpi_card,
    render_info_box, render_footer, create_bar_chart, create_grouped_bar
)

# Page configuration
st.set_page_config(
    page_title="Mental Health in Tech Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for polished appearance
st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
        .stMetric { background-color: #f8fafc; padding: 12px 18px; border-radius: 8px; border: 1px solid #e2e8f0; }
        [data-testid="stSidebar"] { background-color: #f1f5f9; }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_survey_data():
    """
    Load cleaned survey dataset using relative path resolution.
    Gracefully handles missing data with actionable instructions.
    """
    cleaned_path = os.path.join(project_root, "data", "processed", "survey_cleaned.csv")
    if not os.path.exists(cleaned_path):
        st.error(
            "Cleaned dataset (`data/processed/survey_cleaned.csv`) was not found!\n\n"
            "Please run the data cleaning pipeline first by executing:\n"
            "```bash\npython src/data_cleaning.py\n```"
        )
        st.stop()
        
    df = pd.read_csv(cleaned_path)
    
    # Expected core columns validation
    required_cols = ['Age_Cleaned', 'Age_Group', 'Gender_Cleaned', 'Country', 'treatment', 'family_history', 'work_interfere']
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        st.error(f"Missing expected columns in cleaned dataset: {missing_cols}")
        st.stop()
        
    return df


@st.cache_data
def load_data_dictionary():
    """Load data dictionary if present."""
    dict_path = os.path.join(project_root, "data", "processed", "data_dictionary.csv")
    if os.path.exists(dict_path):
        return pd.read_csv(dict_path)
    return None


# Load cached data
df = load_survey_data()
data_dict = load_data_dictionary()

# Sidebar navigation
st.sidebar.image("https://img.icons8.com/color/96/000000/mental-health.png", width=64)
st.sidebar.title("Navigation")
menu_selection = st.sidebar.radio(
    "Go to page:",
    [
        "1. Overview",
        "2. Demographics",
        "3. Mental Health",
        "4. Workplace & Support",
        "5. Relationship Analysis",
        "6. Statistical Analysis",
        "7. Data Explorer"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Mental Health in Tech EDA Project\nOpen Sourcing Mental Illness (OSMI)")


# ==============================================================================
# PAGE 1: OVERVIEW
# ==============================================================================
if menu_selection == "1. Overview":
    render_header("Mental Health in Tech Survey", "Exploratory Data Analysis & Interactive Insights Dashboard")
    
    # Dynamic KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    total_n = len(df)
    treatment_n = (df['treatment'] == 'Yes').sum()
    treatment_rate = (treatment_n / total_n) * 100
    missing_n = int(df.isnull().sum().sum())
    countries_n = df['Country'].nunique()
    
    with col1:
        render_kpi_card("Total Respondents", f"{total_n:,}", help_text="Total verified survey submissions")
    with col2:
        render_kpi_card("Treatment Sought", f"{treatment_n:,}", help_text="Respondents who sought mental health care")
    with col3:
        render_kpi_card("Treatment Rate", f"{treatment_rate:.1f}%", help_text="Proportion seeking professional mental care")
    with col4:
        render_kpi_card("Missing Values (Cleaned)", f"{missing_n}", help_text="Null values remaining after imputation")
    with col5:
        render_kpi_card("Countries Represented", f"{countries_n}", help_text="Geographic coverage of respondents")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([3, 2])
    with c1:
        render_section_header("Project Overview & Analytical Scope")
        st.write(
            """
            This dashboard synthesizes the findings from an in-depth Exploratory Data Analysis (EDA)
            of the **Mental Health in Tech Survey** (OSMI dataset).
            
            Mental health conditions in technology environments are often under-discussed due to workplace stigma,
            career repercussions, or lack of institutional support. This study measures:
            - Demographic patterns and baseline treatment uptake across the tech sector.
            - Impact of personal and familial history on treatment-seeking behavior.
            - How employer provisions (benefits, care options, wellness programs, and anonymity) associate with employee health decisions.
            - Statistical validation through Chi-Square tests of independence and Cramér's V effect sizes.
            """
        )
        render_info_box(
            "Primary Takeaway",
            "Treatment uptake is strongly associated with personal severity (Work Interference: Cramér's V = 0.542) "
            "and Family History (Cramér's V = 0.375). Employer care options and explicit benefits significantly improve "
            "treatment seeking, while structural variables like company size and remote work show no significant effect.",
            box_type="info"
        )
    with c2:
        render_section_header("Dataset Metadata & Health")
        meta_df = pd.DataFrame({
            "Metric": ["Dataset Name", "Original Shape", "Cleaned Shape", "Age Range (Cleaned)", "Tech Sector Share", "Remote Workers"],
            "Value": ["OSMI Mental Health in Tech", "1,259 rows × 27 cols", f"{df.shape[0]} rows × {df.shape[1]} cols",
                      f"{df['Age_Cleaned'].min()} - {df['Age_Cleaned'].max()} yrs (Median: {int(df['Age_Cleaned'].median())})",
                      f"{(df['tech_company']=='Yes').mean()*100:.1f}%",
                      f"{(df['remote_work']=='Yes').mean()*100:.1f}%"]
        })
        st.dataframe(meta_df, hide_index=True, use_container_width=True)

    render_footer()


# ==============================================================================
# PAGE 2: DEMOGRAPHICS
# ==============================================================================
elif menu_selection == "2. Demographics":
    render_header("Demographic Profile", "Analysis of Age, Gender, Geography, and Employment Structure")
    
    col_filter1, col_filter2 = st.columns([1, 2])
    with col_filter1:
        selected_genders = st.multiselect(
            "Filter by Gender Identity:",
            options=df['Gender_Cleaned'].unique().tolist(),
            default=df['Gender_Cleaned'].unique().tolist()
        )
    with col_filter2:
        top_n_countries = st.slider("Select Top N Countries to Display:", min_value=5, max_value=25, value=10)
        
    filtered_df = df[df['Gender_Cleaned'].isin(selected_genders)]
    
    st.markdown("---")
    
    # Age Distribution
    r1_c1, r1_c2 = st.columns(2)
    with r1_c1:
        fig_age = px.histogram(
            filtered_df, x="Age_Cleaned", nbins=25,
            title="Respondent Age Distribution (Cleaned 18–75 Yrs)",
            color_discrete_sequence=['#2b5c8f'], marginal="box"
        )
        fig_age.update_layout(xaxis_title="Age (Years)", yaxis_title="Frequency", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_age, use_container_width=True)
    
    with r1_c2:
        age_counts = filtered_df['Age_Group'].value_counts().sort_index().reset_index()
        age_counts.columns = ['Age_Group', 'Count']
        age_counts['Percentage'] = (age_counts['Count'] / len(filtered_df)) * 100
        fig_cohort = create_bar_chart(age_counts, 'Age_Group', 'Percentage', "Age Cohort Breakdown (%)", color_discrete_sequence=['#41b6c4'])
        st.plotly_chart(fig_cohort, use_container_width=True)
        
    r2_c1, r2_c2 = st.columns(2)
    with r2_c1:
        gender_counts = filtered_df['Gender_Cleaned'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        gender_counts['Percentage'] = (gender_counts['Count'] / len(filtered_df)) * 100
        fig_gen = px.pie(
            gender_counts, names='Gender', values='Count', hole=0.45,
            title="Harmonized Gender Representation",
            color_discrete_sequence=['#3182bd', '#fd8d3c', '#74c476']
        )
        fig_gen.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_gen, use_container_width=True)
        
    with r2_c2:
        country_counts = filtered_df['Country'].value_counts().head(top_n_countries).reset_index()
        country_counts.columns = ['Country', 'Count']
        fig_country = px.bar(
            country_counts, x='Count', y='Country', orientation='h',
            title=f"Top {top_n_countries} Countries Represented",
            color='Count', color_continuous_scale='Viridis'
        )
        fig_country.update_layout(yaxis=dict(autorange="reversed"), plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_country, use_container_width=True)

    render_info_box(
        "Demographic Insights",
        f"The sample is predominantly composed of young tech professionals (median age {int(df['Age_Cleaned'].median())} years), "
        f"with {df['Age_Group'].value_counts(normalize=True).get('25-34', 0)*100:.1f}% falling into the 25-34 cohort. "
        f"Male respondents account for {df['Gender_Cleaned'].value_counts(normalize=True).get('Male', 0)*100:.1f}%, while the United States "
        f"represents {df['Country'].value_counts(normalize=True).get('United States', 0)*100:.1f}% of total submissions.",
        box_type="info"
    )
    render_footer()


# ==============================================================================
# PAGE 3: MENTAL HEALTH
# ==============================================================================
elif menu_selection == "3. Mental Health":
    render_header("Mental Health & Treatment Uptake", "Examining Treatment Patterns, Family History, and Work Interference")
    
    m1, m2 = st.columns(2)
    with m1:
        # Treatment vs Family History
        ct_fam = pd.crosstab(df['family_history'], df['treatment'], normalize='index') * 100
        fig_fam = create_grouped_bar(ct_fam, "Treatment Seeking by Family History of Mental Illness", "Family History")
        st.plotly_chart(fig_fam, use_container_width=True)
        
    with m2:
        # Treatment vs Work Interference
        order_wi = ['Often', 'Sometimes', 'Rarely', 'Never', 'Not Applicable / Unreported']
        ct_wi = pd.crosstab(df['work_interfere'], df['treatment'], normalize='index') * 100
        ct_wi = ct_wi.reindex([o for o in order_wi if o in ct_wi.index])
        fig_wi = create_grouped_bar(ct_wi, "Treatment Uptake by Work Interference Frequency", "Work Interference Severity")
        st.plotly_chart(fig_wi, use_container_width=True)
        
    m3, m4 = st.columns(2)
    with m3:
        # Treatment by Gender
        ct_gen = pd.crosstab(df['Gender_Cleaned'], df['treatment'], normalize='index') * 100
        fig_gen = create_grouped_bar(ct_gen, "Treatment Seeking by Gender Identity", "Gender Identity")
        st.plotly_chart(fig_gen, use_container_width=True)
        
    with m4:
        # Treatment by Age Group
        ct_age = pd.crosstab(df['Age_Group'], df['treatment'], normalize='index') * 100
        fig_age = create_grouped_bar(ct_age, "Treatment Seeking Across Age Cohorts", "Age Group")
        st.plotly_chart(fig_age, use_container_width=True)

    render_info_box(
        "Analytical Observations",
        "- **Family History Impact**: Individuals with a positive family history seek treatment at more than double the rate of those without (75.5% vs 34.0%).\n"
        "- **Work Interference**: 84.0% of respondents reporting that mental health interferes 'Often' with their work have sought professional care, versus only 14.6% for 'Never'.\n"
        "- **Gender Disparity**: Female (68.8%) and Non-Binary/Other (76.2%) respondents access mental health care significantly more frequently than Male peers (45.1%).",
        box_type="success"
    )
    render_footer()


# ==============================================================================
# PAGE 4: WORKPLACE & SUPPORT
# ==============================================================================
elif menu_selection == "4. Workplace & Support":
    render_header("Workplace Support & Employer Provisions", "Analysis of Mental Health Benefits, Anonymity, and Corporate Policies")
    
    w1, w2 = st.columns(2)
    with w1:
        ct_ben = pd.crosstab(df['benefits'], df['treatment'], normalize='index') * 100
        fig_ben = create_grouped_bar(ct_ben, "Treatment Uptake by Mental Health Benefits Coverage", "Employer Provides Benefits")
        st.plotly_chart(fig_ben, use_container_width=True)
        
    with w2:
        ct_care = pd.crosstab(df['care_options'], df['treatment'], normalize='index') * 100
        fig_care = create_grouped_bar(ct_care, "Treatment Rate by Knowledge of Care Options", "Awareness of Care Options")
        st.plotly_chart(fig_care, use_container_width=True)
        
    w3, w4 = st.columns(2)
    with w3:
        # Anonymity
        ct_anon = pd.crosstab(df['anonymity'], df['treatment'], normalize='index') * 100
        fig_anon = create_grouped_bar(ct_anon, "Treatment Rate by Anonymity Protection", "Anonymity Protected")
        st.plotly_chart(fig_anon, use_container_width=True)
        
    with w4:
        # Company Size
        order_size = ['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000']
        ct_size = pd.crosstab(df['no_employees'], df['treatment'], normalize='index') * 100
        ct_size = ct_size.reindex([s for s in order_size if s in ct_size.index])
        fig_size = create_grouped_bar(ct_size, "Treatment Rate Across Company Size Brackets", "Number of Employees")
        st.plotly_chart(fig_size, use_container_width=True)

    render_info_box(
        "Workplace Insights (Non-Causal Grounding)",
        "- **Awareness Drives Utilization**: Employees who know their care options exhibit a 63.8% treatment rate compared to 36.9% among those whose employers offer no options.\n"
        "- **Uncertainty Gap**: Over 32% of respondents answer 'Don\'t know' regarding whether their employer provides mental health benefits, highlighting an internal communication gap.\n"
        "- **Company Size Neutrality**: Differences across company size tiers are modest (varying between 44% and 55%) and fail to reach statistical significance.",
        box_type="info"
    )
    render_footer()


# ==============================================================================
# PAGE 5: RELATIONSHIP ANALYSIS
# ==============================================================================
elif menu_selection == "5. Relationship Analysis":
    render_header("Interactive Relationship Analysis", "Explore Bivariate Associations Across Any Two Survey Features")
    
    selectable_cols = [
        'family_history', 'work_interfere', 'benefits', 'care_options',
        'wellness_program', 'seek_help', 'anonymity', 'remote_work',
        'no_employees', 'tech_company', 'self_employed', 'Age_Group',
        'Gender_Cleaned', 'mental_health_consequence', 'phys_health_consequence',
        'coworkers', 'supervisor', 'mental_health_interview', 'mental_vs_physical',
        'obs_consequence', 'treatment'
    ]
    
    c_sel1, c_sel2, c_sel3 = st.columns(3)
    with c_sel1:
        var_x = st.selectbox("Select Variable A (X-Axis / Group):", selectable_cols, index=selectable_cols.index('benefits'))
    with c_sel2:
        var_y = st.selectbox("Select Variable B (Comparison / Color):", selectable_cols, index=selectable_cols.index('treatment'))
    with c_sel3:
        chart_mode = st.radio("Display Mode:", ["Normalized Percentage (%)", "Absolute Counts", "Contingency Heatmap"])
        
    if var_x == var_y:
        st.warning("Please select two distinct variables to explore bivariate relationships.")
    else:
        st.markdown("---")
        sub_df = df.dropna(subset=[var_x, var_y])
        
        if chart_mode == "Normalized Percentage (%)":
            ct = pd.crosstab(sub_df[var_x], sub_df[var_y], normalize='index') * 100
            ct_reset = ct.reset_index().melt(id_vars=var_x, var_name=var_y, value_name='Percentage')
            fig_rel = px.bar(
                ct_reset, x=var_x, y='Percentage', color=var_y, barmode='group',
                title=f"Normalized Percentage Breakdown: {var_x} vs {var_y}",
                text_auto='.1f'
            )
            fig_rel.update_layout(yaxis_title="Percentage within Group (%)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_rel, use_container_width=True)
            
        elif chart_mode == "Absolute Counts":
            ct = pd.crosstab(sub_df[var_x], sub_df[var_y])
            ct_reset = ct.reset_index().melt(id_vars=var_x, var_name=var_y, value_name='Count')
            fig_rel = px.bar(
                ct_reset, x=var_x, y='Count', color=var_y, barmode='group',
                title=f"Respondent Counts: {var_x} vs {var_y}",
                text_auto=True
            )
            fig_rel.update_layout(yaxis_title="Respondent Count", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_rel, use_container_width=True)
            
        else:
            ct = pd.crosstab(sub_df[var_x], sub_df[var_y])
            fig_rel = px.imshow(
                ct, text_auto=True, color_continuous_scale="Blues",
                title=f"Contingency Matrix Heatmap: {var_x} vs {var_y}"
            )
            st.plotly_chart(fig_rel, use_container_width=True)
            
        # Display cross-tab data table
        st.markdown("#### Contingency Table")
        st.dataframe(pd.crosstab(sub_df[var_x], sub_df[var_y], margins=True), use_container_width=True)

    render_footer()


# ==============================================================================
# PAGE 6: STATISTICAL ANALYSIS
# ==============================================================================
elif menu_selection == "6. Statistical Analysis":
    render_header("Statistical Hypothesis Testing Battery", "Rigorous Verification via Chi-Square Test of Independence & Cramér's V")
    
    render_info_box(
        "Methodology & Interpretation Standard",
        "Hypothesis testing was conducted at significance threshold α = 0.05. "
        "Associations do not indicate causal mechanisms. Cramér's V indicates degree of association (bias-corrected).\n"
        "- H₀ (Null): There is no association between the surveyed attribute and treatment seeking.\n"
        "- H₁ (Alternative): There is a statistically significant association within this sample.",
        box_type="info"
    )
    
    # Run full battery dynamically
    from src.eda_analysis import run_full_statistical_battery, run_chi2_test
    stats_df = run_full_statistical_battery(df, target='treatment', alpha=0.05)
    
    st.markdown("### Hypothesis Test Outcomes Summary")
    
    # Styled dataframe
    def highlight_sig(val):
        color = '#d4edda' if val == 'Yes' else '#f8d7da'
        return f'background-color: {color}; font-weight: bold;'
        
    styled_df = stats_df.style.applymap(highlight_sig, subset=['Significant (p < 0.05)'])
    st.dataframe(styled_df, use_container_width=True)
    
    st.markdown("---")
    render_section_header("Detailed Feature Hypothesis Inspector")
    
    selected_feature = st.selectbox("Select a Feature to Inspect Statistical Details:", stats_df['Feature'].tolist())
    detail = run_chi2_test(df, selected_feature, 'treatment', alpha=0.05)
    
    d_col1, d_col2 = st.columns([3, 2])
    with d_col1:
        st.markdown(f"**Tested Variable:** `{detail['variable']}` against `treatment`")
        st.markdown(f"**Null Hypothesis ($H_0$):** {detail['null_hypothesis']}")
        st.markdown(f"**Alternative Hypothesis ($H_1$):** {detail['alt_hypothesis']}")
        st.markdown(f"**Decision:** `{detail['decision']}`")
    with d_col2:
        render_kpi_card("Chi-Square Statistic", f"{detail['chi2_statistic']:.3f}")
        render_kpi_card("p-value", f"{detail['p_value']:.4e}" if detail['p_value'] < 0.0001 else f"{detail['p_value']:.4f}")
        render_kpi_card("Cramér's V", f"{detail['cramers_v']:.3f}", delta=detail['association_strength'])

    render_footer()


# ==============================================================================
# PAGE 7: DATA EXPLORER
# ==============================================================================
elif menu_selection == "7. Data Explorer":
    render_header("Interactive Data Explorer", "Filter, Inspect, and Export Analysis-Ready Survey Records")
    
    # Data privacy alert
    render_info_box(
        "Privacy & Confidentiality Notice",
        "In accordance with ethical data privacy guidelines, free-text qualitative comments are hidden by default "
        "to prevent accidental exposure of identifiable experiences.",
        box_type="warning"
    )
    
    # Controls
    f_c1, f_c2, f_c3, f_c4 = st.columns(4)
    with f_c1:
        f_gender = st.multiselect("Gender:", df['Gender_Cleaned'].unique(), default=df['Gender_Cleaned'].unique())
    with f_c2:
        f_treat = st.multiselect("Treatment:", df['treatment'].unique(), default=df['treatment'].unique())
    with f_c3:
        f_age = st.multiselect("Age Cohort:", df['Age_Group'].dropna().unique().tolist(), default=df['Age_Group'].dropna().unique().tolist())
    with f_c4:
        f_tech = st.multiselect("Tech Company:", df['tech_company'].unique(), default=df['tech_company'].unique())
        
    filtered = df[
        (df['Gender_Cleaned'].isin(f_gender)) &
        (df['treatment'].isin(f_treat)) &
        (df['Age_Group'].isin(f_age)) &
        (df['tech_company'].isin(f_tech))
    ]
    
    # Column selection
    all_cols = [c for c in df.columns if c != 'comments']
    selected_cols = st.multiselect("Select Columns to Display:", options=all_cols, default=[
        'Age_Cleaned', 'Age_Group', 'Gender_Cleaned', 'Country', 'treatment',
        'family_history', 'work_interfere', 'benefits', 'care_options', 'no_employees', 'remote_work'
    ])
    
    show_comments = st.checkbox("Show free-text comments column (Acknowledging potential sensitive text)")
    display_cols = list(selected_cols)
    if show_comments and 'comments' in df.columns:
        display_cols.append('comments')
        
    st.markdown(f"**Showing {len(filtered):,} matching records (out of {len(df):,} total)**")
    st.dataframe(filtered[display_cols], use_container_width=True, height=450)
    
    # CSV Download Button
    csv_data = filtered[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Records as CSV",
        data=csv_data,
        file_name="mental_health_filtered_records.csv",
        mime="text/csv"
    )
    
    # Show Data Dictionary tab
    if data_dict is not None:
        with st.expander("📚 View Field Data Dictionary"):
            st.dataframe(data_dict, use_container_width=True)

    render_footer()
