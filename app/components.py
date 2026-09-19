"""
Reusable UI and Chart Components for the Streamlit Dashboard
Provides styled KPI metric cards, section headers, notice callouts, and chart wrappers.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def render_header(title, subtitle=None):
    """Render consistent page top banner."""
    st.markdown(f"<h1 style='margin-bottom: 0px;'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p style='font-size: 1.15rem; color: #555; margin-top: 4px; margin-bottom: 24px;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("---")


def render_section_header(title, description=None):
    """Render structured section header with optional description."""
    st.markdown(f"<h3 style='margin-top: 15px; margin-bottom: 6px;'>{title}</h3>", unsafe_allow_html=True)
    if description:
        st.markdown(f"<p style='color: #666; font-size: 0.95rem; margin-bottom: 12px;'>{description}</p>", unsafe_allow_html=True)


def render_kpi_card(label, value, delta=None, help_text=None):
    """Render styled KPI card."""
    st.metric(label=label, value=value, delta=delta, help=help_text)


def render_info_box(title, content, box_type="info"):
    """
    Render styled informational callout card.
    box_type: 'info', 'warning', 'success', 'error'
    """
    if box_type == "info":
        st.info(f"**{title}**\n\n{content}")
    elif box_type == "warning":
        st.warning(f"**{title}**\n\n{content}")
    elif box_type == "success":
        st.success(f"**{title}**\n\n{content}")
    elif box_type == "error":
        st.error(f"**{title}**\n\n{content}")


def render_footer():
    """Render professional footer across dashboard views."""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888; font-size: 0.85rem; padding: 10px 0;'>
            <strong>Mental Health in Tech Survey – Exploratory Data Analysis & Analytics Dashboard</strong><br>
            Built with Streamlit, Plotly, Pandas, and SciPy &bull; OSMI Mental Health in Tech Dataset &bull; Local VS Code Execution
        </div>
        """,
        unsafe_allow_html=True
    )


def create_bar_chart(df, x_col, y_col, title, orientation='v', color=None, color_discrete_sequence=None):
    """Create a standardized Plotly bar chart."""
    fig = px.bar(
        df, x=x_col, y=y_col, orientation=orientation,
        title=title, color=color,
        color_discrete_sequence=color_discrete_sequence or px.colors.qualitative.Prism,
        text_auto='.1f' if y_col == 'Percentage' else True
    )
    fig.update_layout(
        title_font=dict(size=14, family="Arial", color="#1f2d3d"),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def create_grouped_bar(df_crosstab, title, x_label, y_label='Percentage (%)', barmode='group'):
    """Create standardized grouped/stacked bar chart from contingency table."""
    reset_ct = df_crosstab.reset_index()
    melted = reset_ct.melt(id_vars=reset_ct.columns[0], var_name='Treatment', value_name='Percentage')
    
    fig = px.bar(
        melted, x=reset_ct.columns[0], y='Percentage', color='Treatment',
        barmode=barmode, title=title,
        color_discrete_map={'Yes': '#e6550d', 'No': '#3182bd'},
        text_auto='.1f'
    )
    fig.update_layout(
        title_font=dict(size=14, family="Arial", color="#1f2d3d"),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title="Sought Treatment",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig
