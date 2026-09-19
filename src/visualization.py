"""
Visualization Module for Mental Health in Tech Survey
Generates publication-quality charts using Matplotlib and Seaborn,
saving high-resolution PNG figures directly to outputs/figures/.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Apply clean publication-ready aesthetic
sns.set_theme(style="whitegrid", font_scale=1.05)
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8


def plot_missing_values(df_raw, output_path=None):
    """
    Plot missing value counts and percentages across raw dataset columns.
    """
    missing = df_raw.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    
    if len(missing) == 0:
        return
        
    pcts = (missing / len(df_raw)) * 100
    
    fig, ax1 = plt.subplots(figsize=(9, 5))
    color_palette = sns.color_palette("mako", len(missing))
    
    bars = ax1.bar(missing.index, missing.values, color=color_palette, edgecolor='black', alpha=0.85)
    ax1.set_ylabel('Missing Count', fontsize=12, fontweight='bold', color='#1f2d3d')
    ax1.set_title('Missing Values in Survey Dataset by Column', fontsize=14, fontweight='bold', pad=15)
    
    for bar, pct in zip(bars, pcts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 15,
                 f'{int(height):,}\n({pct:.1f}%)',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
                 
    ax1.set_ylim(0, len(df_raw) * 1.15)
    plt.xticks(rotation=15, ha='right', fontsize=11)
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Saved: {output_path}")


def plot_age_distribution(df, output_path=None):
    """
    Plot histogram with KDE and accompanying boxplot for respondent age.
    """
    fig, (ax_box, ax_hist) = plt.subplots(2, 1, figsize=(9, 6), sharex=True,
                                          gridspec_kw={'height_ratios': [0.25, 0.75]})
                                          
    sns.boxplot(x=df['Age_Cleaned'], ax=ax_box, color='#6baed6', fliersize=4)
    ax_box.set(xlabel='')
    ax_box.set_title('Respondent Age Distribution (Cleaned 18–75 Yrs)', fontsize=14, fontweight='bold', pad=10)
    
    sns.histplot(df['Age_Cleaned'], kde=True, ax=ax_hist, color='#2b5c8f', bins=25, edgecolor='black', alpha=0.7)
    ax_hist.axvline(df['Age_Cleaned'].median(), color='#e6550d', linestyle='--', linewidth=2,
                    label=f"Median: {df['Age_Cleaned'].median():.0f} yrs")
    ax_hist.axvline(df['Age_Cleaned'].mean(), color='#31a354', linestyle=':', linewidth=2,
                    label=f"Mean: {df['Age_Cleaned'].mean():.1f} yrs")
                    
    ax_hist.set_xlabel('Age (Years)', fontsize=12, fontweight='bold')
    ax_hist.set_ylabel('Respondent Frequency', fontsize=12, fontweight='bold')
    ax_hist.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Saved: {output_path}")


def plot_gender_distribution(df, output_path=None):
    """
    Plot distribution of cleaned gender identities.
    """
    counts = df['Gender_Cleaned'].value_counts()
    pcts = (counts / len(df)) * 100
    
    plt.figure(figsize=(8, 5))
    palette = ['#3182bd', '#fd8d3c', '#74c476']
    bars = plt.bar(counts.index, counts.values, color=palette[:len(counts)], edgecolor='black', alpha=0.85)
    
    for bar, pct in zip(bars, pcts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 15,
                 f'{int(height):,}\n({pct:.1f}%)',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
                 
    plt.title('Demographic Breakdown: Cleaned Gender Representation', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Gender Identity', fontsize=12, fontweight='bold')
    plt.ylabel('Respondent Count', fontsize=12, fontweight='bold')
    plt.ylim(0, max(counts.values) * 1.18)
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Saved: {output_path}")


def plot_country_distribution(df, top_n=10, output_path=None):
    """
    Plot horizontal bar chart of top respondent countries.
    """
    counts = df['Country'].value_counts().head(top_n)
    pcts = (counts / len(df)) * 100
    
    plt.figure(figsize=(9, 6))
    colors = sns.color_palette('viridis', len(counts))[::-1]
    y_pos = range(len(counts))
    
    plt.barh(y_pos, counts.values, color=colors, edgecolor='black', alpha=0.85)
    plt.yticks(y_pos, counts.index, fontsize=11)
    plt.gca().invert_yaxis()
    
    for i, (cnt, pct) in enumerate(zip(counts.values, pcts.values)):
        plt.text(cnt + 10, i, f'{cnt:,} ({pct:.1f}%)', va='center', fontsize=10, fontweight='bold')
        
    plt.title(f'Geographic Distribution: Top {top_n} Surveyed Countries', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Respondents', fontsize=12, fontweight='bold')
    plt.xlim(0, max(counts.values) * 1.22)
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Saved: {output_path}")


def plot_treatment_distribution(df, output_path=None):
    """
    Plot primary target variable: Mental Health Treatment Rate.
    """
    counts = df['treatment'].value_counts()
    pcts = (counts / len(df)) * 100
    
    plt.figure(figsize=(7, 5))
    colors = ['#e6550d', '#3182bd']
    bars = plt.bar(counts.index, counts.values, color=colors, edgecolor='black', alpha=0.85, width=0.55)
    
    for bar, pct in zip(bars, pcts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 15,
                 f'{int(height):,} Respondents\n({pct:.1f}%)',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
                 
    plt.title('Overall Mental Health Treatment Uptake in Tech', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Has Sought Treatment for Mental Health Condition?', fontsize=12, fontweight='bold')
    plt.ylabel('Count', fontsize=12, fontweight='bold')
    plt.ylim(0, max(counts.values) * 1.2)
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Saved: {output_path}")


def plot_treatment_bivariate(df, feature, title, xlabel, output_path=None, order=None):
    """
    Generate grouped and normalized percentage bar chart comparing a feature against treatment.
    """
    sub = df.dropna(subset=[feature, 'treatment'])
    ct = pd.crosstab(sub[feature], sub['treatment'], normalize='index') * 100
    
    if order:
        ct = ct.reindex([o for o in order if o in ct.index])
        
    ax = ct.plot(kind='bar', stacked=False, figsize=(8, 5),
                 color=['#9ecae1', '#fc9272'], edgecolor='black', alpha=0.9, width=0.65)
                 
    plt.title(title, fontsize=13, fontweight='bold', pad=15)
    plt.xlabel(xlabel, fontsize=11, fontweight='bold')
    plt.ylabel('Percentage within Group (%)', fontsize=11, fontweight='bold')
    plt.legend(title='Treatment', labels=['No', 'Yes'], frameon=True, facecolor='white')
    plt.xticks(rotation=15 if len(ct.index) > 3 else 0, ha='right' if len(ct.index) > 3 else 'center')
    plt.ylim(0, 100)
    
    for p in ax.patches:
        height = p.get_height()
        if height > 4:
            ax.annotate(f"{height:.1f}%",
                        (p.get_x() + p.get_width() / 2., height / 2),
                        ha='center', va='center', fontsize=9, fontweight='bold', color='black')
                        
    plt.tight_layout()
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Saved: {output_path}")


def plot_workplace_support_multi(df, output_path=None):
    """
    Multi-panel bar chart comparing employer mental health provisions.
    """
    support_vars = ['benefits', 'care_options', 'wellness_program', 'seek_help', 'anonymity']
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()
    
    for idx, var in enumerate(support_vars):
        counts = df[var].value_counts(normalize=True) * 100
        sns.barplot(x=counts.index, y=counts.values, ax=axes[idx], palette='Blues_r', edgecolor='black', alpha=0.85)
        axes[idx].set_title(f"Employer: '{var}'", fontsize=11, fontweight='bold')
        axes[idx].set_ylabel('Percentage (%)', fontsize=10)
        axes[idx].set_ylim(0, 75)
        for p in axes[idx].patches:
            h = p.get_height()
            axes[idx].annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h + 1.5),
                               ha='center', va='bottom', fontsize=9, fontweight='bold')
                               
    axes[5].axis('off')  # Hide 6th empty subplot
    plt.suptitle("Workplace Mental Health Support Provisions Overview", fontsize=15, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Saved: {output_path}")


def plot_correlation_heatmap(df, output_path=None):
    """
    Plot correlation matrix heatmap of encoded categorical and numerical survey variables.
    """
    encoding_map = {
        'treatment': {'No': 0, 'Yes': 1},
        'family_history': {'No': 0, 'Yes': 1},
        'remote_work': {'No': 0, 'Yes': 1},
        'tech_company': {'No': 0, 'Yes': 1},
        'obs_consequence': {'No': 0, 'Yes': 1},
        'self_employed': {'No': 0, 'Yes': 1},
        'benefits': {'No': 0, "Don't know": 1, 'Yes': 2},
        'care_options': {'No': 0, 'Not sure': 1, 'Yes': 2},
        'wellness_program': {'No': 0, "Don't know": 1, 'Yes': 2},
        'seek_help': {'No': 0, "Don't know": 1, 'Yes': 2},
        'anonymity': {'No': 0, "Don't know": 1, 'Yes': 2},
        'work_interfere': {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Not Applicable / Unreported': 0}
    }
    
    encoded_df = pd.DataFrame()
    encoded_df['Age'] = df['Age_Cleaned']
    for col, mapping in encoding_map.items():
        if col in df.columns:
            encoded_df[col] = df[col].map(mapping).fillna(0)
            
    corr = encoded_df.corr(method='spearman')
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", vmin=-0.5, vmax=0.5,
                linewidths=0.5, cbar_kws={'label': "Spearman Rank Correlation"})
    plt.title("Correlation Heatmap: Survey Features & Treatment Seeking", fontsize=13, fontweight='bold', pad=15)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Saved: {output_path}")


def plot_pairplot_mental_health(df, output_path=None):
    """
    Generate pairplot/relational plot of key numerical and ordinal factors stratified by treatment.
    """
    sub = df.copy()
    sub['Work_Interfere_Rank'] = sub['work_interfere'].map({
        'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Not Applicable / Unreported': 0
    })
    sub['Benefits_Score'] = sub['benefits'].map({'No': 0, "Don't know": 1, 'Yes': 2})
    
    plot_df = sub[['Age_Cleaned', 'Work_Interfere_Rank', 'Benefits_Score', 'treatment']].dropna()
    plot_df.columns = ['Age', 'Work Interference', 'Benefits Score', 'Treatment']
    
    g = sns.pairplot(plot_df, hue='Treatment', palette={'Yes': '#e6550d', 'No': '#3182bd'},
                     diag_kind='kde', plot_kws={'alpha': 0.6, 's': 40})
    g.fig.subplots_adjust(top=0.92)
    g.fig.suptitle("Multivariate Pair Plot: Age, Work Interference & Benefits by Treatment",
                   fontsize=14, fontweight='bold')
                   
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        g.savefig(output_path, dpi=300)
        plt.close()
        print(f"Saved: {output_path}")


def generate_all_figures(df_raw, df_cleaned, figures_dir):
    """
    Generate and save all 15 required figures for project EDA and reports.
    """
    os.makedirs(figures_dir, exist_ok=True)
    
    # 1. Missing values
    plot_missing_values(df_raw, os.path.join(figures_dir, "missing_values.png"))
    
    # 2. Age distribution
    plot_age_distribution(df_cleaned, os.path.join(figures_dir, "age_distribution.png"))
    
    # 3. Gender breakdown
    plot_gender_distribution(df_cleaned, os.path.join(figures_dir, "gender_distribution.png"))
    
    # 4. Country distribution
    plot_country_distribution(df_cleaned, 10, os.path.join(figures_dir, "country_distribution.png"))
    
    # 5. Treatment overall
    plot_treatment_distribution(df_cleaned, os.path.join(figures_dir, "treatment_distribution.png"))
    
    # 6. Treatment vs Family history
    plot_treatment_bivariate(df_cleaned, 'family_history',
                             'Mental Health Treatment by Family History of Mental Illness',
                             'Family History',
                             os.path.join(figures_dir, "treatment_vs_family_history.png"),
                             order=['No', 'Yes'])
                             
    # 7. Treatment vs Work interference
    plot_treatment_bivariate(df_cleaned, 'work_interfere',
                             'Treatment Uptake by Work Interference Severity',
                             'Work Interference Frequency',
                             os.path.join(figures_dir, "treatment_vs_work_interfere.png"),
                             order=['Often', 'Sometimes', 'Rarely', 'Never', 'Not Applicable / Unreported'])
                             
    # 8. Treatment vs Benefits
    plot_treatment_bivariate(df_cleaned, 'benefits',
                             'Treatment Rate by Employer Mental Health Benefits Coverage',
                             'Employer Provides Benefits',
                             os.path.join(figures_dir, "treatment_vs_benefits.png"),
                             order=['Yes', "Don't know", 'No'])
                             
    # 9. Treatment vs Care Options
    plot_treatment_bivariate(df_cleaned, 'care_options',
                             'Treatment Rate by Knowledge of Care Options',
                             'Awareness of Care Options',
                             os.path.join(figures_dir, "treatment_vs_care_options.png"),
                             order=['Yes', 'Not sure', 'No'])
                             
    # 10. Treatment vs Gender
    plot_treatment_bivariate(df_cleaned, 'Gender_Cleaned',
                             'Treatment Rate by Gender Identity',
                             'Gender Identity',
                             os.path.join(figures_dir, "treatment_vs_gender.png"),
                             order=['Female', 'Non-Binary/Other', 'Male'])
                             
    # 11. Treatment vs Age Group
    plot_treatment_bivariate(df_cleaned, 'Age_Group',
                             'Treatment Rate by Age Demographic Cohort',
                             'Age Cohort',
                             os.path.join(figures_dir, "treatment_vs_age_group.png"),
                             order=['18-24', '25-34', '35-44', '45-54', '55+'])
                             
    # 12. Treatment vs Company Size
    plot_treatment_bivariate(df_cleaned, 'no_employees',
                             'Treatment Rate Across Organization Headcount Brackets',
                             'Company Size (# Employees)',
                             os.path.join(figures_dir, "treatment_vs_company_size.png"),
                             order=['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000'])
                             
    # 13. Workplace Support Provisions Multi-Panel
    plot_workplace_support_multi(df_cleaned, os.path.join(figures_dir, "workplace_support_comparison.png"))
    
    # 14. Correlation Heatmap
    plot_correlation_heatmap(df_cleaned, os.path.join(figures_dir, "correlation_heatmap.png"))
    
    # 15. Pairplot / Multivariate plot
    plot_pairplot_mental_health(df_cleaned, os.path.join(figures_dir, "pairplot_mental_health.png"))
    
    print("All 15 publication-grade figures successfully generated.")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    raw_csv = os.path.join(project_root, "data", "raw", "survey.csv")
    cleaned_csv = os.path.join(project_root, "data", "processed", "survey_cleaned.csv")
    fig_dir = os.path.join(project_root, "outputs", "figures")
    
    df_raw = pd.read_csv(raw_csv)
    df_clean = pd.read_csv(cleaned_csv)
    generate_all_figures(df_raw, df_clean, fig_dir)
