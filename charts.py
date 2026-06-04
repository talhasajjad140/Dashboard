import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

sns.set_theme(style="white")
sns.set_style("ticks")
PALETTE = ["#1B2A4A", "#2E86AB", "#C0392B", "#E67E22", "#27AE60", "#8E44AD"]
PRIMARY = "#1B2A4A"
ACCENT = "#C0392B"
TEXT_PRIMARY = "#1A1A1A"
TEXT_SECONDARY = "#666666"
BORDER = "#DCDCDC"


def _prep_ax(ax, title, xlabel=None, ylabel=None):
    ax.set_facecolor("white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(BORDER)
    ax.spines["bottom"].set_color(BORDER)
    ax.set_title(title, fontsize=13, fontweight="bold", color=PRIMARY, pad=12, loc="left")
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=10, color=TEXT_PRIMARY)
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=10, color=TEXT_PRIMARY)
    ax.tick_params(axis="both", colors=TEXT_SECONDARY, labelsize=9)
    ax.yaxis.grid(True, color=BORDER, linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    return ax


def pie_chart(df):
    """Top 10 storm types by count"""
    if len(df) == 0:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
        return fig

    top_events = df['event_type'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = PALETTE[:len(top_events)]
    ax.pie(
        top_events.values,
        labels=top_events.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'color': TEXT_PRIMARY, 'fontsize': 10},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    )
    ax.set_title('Storm Type Distribution', fontsize=13, fontweight='bold', color=PRIMARY, pad=12, loc='left')
    ax.set_aspect('equal')
    plt.tight_layout()
    return fig


def histogram(df):
    """Distribution of property damage with log scale"""
    if len(df) == 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
        return fig

    damage_data = df[df['damage_property'] > 0]['damage_property']

    if len(damage_data) == 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No damage data available', ha='center', va='center', fontsize=12)
        return fig

    fig, ax = plt.subplots(figsize=(10, 6))
    _prep_ax(ax, 'Property Damage Distribution', 'Property Damage ($)', 'Frequency')
    ax.hist(damage_data, bins=50, color=PRIMARY, edgecolor='white', alpha=0.92)
    ax.set_xscale('log')
    sns.despine(ax=ax)
    plt.tight_layout()
    return fig


def line_chart(df):
    """Number of storm events per year"""
    if len(df) == 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
        return fig

    events_per_year = df.groupby('year').size()

    fig, ax = plt.subplots(figsize=(12, 6))
    _prep_ax(ax, 'Storm Events Over the Years', 'Year', 'Number of Events')
    ax.plot(events_per_year.index, events_per_year.values, marker='o', linewidth=2.5, markersize=6, color=PRIMARY)
    sns.despine(ax=ax)
    plt.tight_layout()
    return fig


def bar_chart(df):
    """Top 10 states by total direct deaths"""
    if len(df) == 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
        return fig

    if 'deaths_direct' not in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Deaths data not available', ha='center', va='center', fontsize=12)
        return fig

    deaths_by_state = df.groupby('state')['deaths_direct'].sum().nlargest(10)

    if len(deaths_by_state) == 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No deaths data', ha='center', va='center', fontsize=12)
        return fig

    fig, ax = plt.subplots(figsize=(10, 6))
    _prep_ax(ax, 'Top 10 States by Deaths', 'Total Deaths', '')
    ax.barh(deaths_by_state.index, deaths_by_state.values, color=ACCENT, edgecolor='white', alpha=0.95)
    sns.despine(ax=ax)
    plt.tight_layout()
    return fig


def scatter_plot(df):
    """Property damage vs injuries, colored by top 6 event types"""
    if len(df) == 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
        return fig

    if 'injuries_direct' not in df.columns or 'damage_property' not in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Required data not available', ha='center', va='center', fontsize=12)
        return fig

    top_events = df['event_type'].value_counts().head(6).index
    plot_df = df[df['event_type'].isin(top_events)].copy()

    if len(plot_df) == 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No data for top event types', ha='center', va='center', fontsize=12)
        return fig

    fig, ax = plt.subplots(figsize=(10, 6))
    _prep_ax(ax, 'Damage vs Injuries', 'Property Damage ($)', 'Injuries (Direct)')
    for i, event in enumerate(top_events):
        event_data = plot_df[plot_df['event_type'] == event]
        ax.scatter(
            event_data['damage_property'],
            event_data['injuries_direct'],
            label=event,
            alpha=0.65,
            s=46,
            color=PALETTE[i % len(PALETTE)]
        )
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9, frameon=False)
    ax.set_xscale('log')
    sns.despine(ax=ax)
    plt.tight_layout()
    return fig


def box_plot(df):
    """Damage distribution across top 6 storm types"""
    if len(df) == 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
        return fig

    if 'damage_property' not in df.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'Damage data not available', ha='center', va='center', fontsize=12)
        return fig

    top_events = df['event_type'].value_counts().head(6).index
    plot_df = df[df['event_type'].isin(top_events)].copy()

    if len(plot_df) == 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'No data for top event types', ha='center', va='center', fontsize=12)
        return fig

    fig, ax = plt.subplots(figsize=(12, 6))
    _prep_ax(ax, 'Damage Spread by Storm Type', 'Event Type', 'Property Damage ($)')
    sns.boxplot(data=plot_df, x='event_type', y='damage_property', palette=PALETTE, ax=ax)
    ax.tick_params(axis='x', rotation=45)
    sns.despine(ax=ax)
    plt.tight_layout()
    return fig


def heatmap(df):
    """Correlation matrix of numeric damage and injury columns"""
    if len(df) == 0:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
        return fig

    cols_to_check = ['deaths_direct', 'injuries_direct', 'damage_property', 'damage_crops', 'magnitude']
    cols_exist = [col for col in cols_to_check if col in df.columns]

    if len(cols_exist) < 2:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, 'Not enough data for correlation', ha='center', va='center', fontsize=12)
        return fig

    corr_data = df[cols_exist].fillna(0)
    corr_matrix = corr_data.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_facecolor("white")
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.2f',
        cmap='Blues',
        linewidths=0.5,
        linecolor=BORDER,
        center=0,
        ax=ax,
        cbar_kws={'label': 'Correlation'}
    )
    ax.set_title('Feature Correlation Heatmap', fontsize=13, fontweight='bold', color=PRIMARY, pad=12, loc='left')
    ax.tick_params(axis='both', colors=TEXT_SECONDARY, labelsize=9)
    plt.tight_layout()
    return fig


def area_chart(df):
    """Cumulative storm count over years"""
    if len(df) == 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
        return fig

    events_per_year = df.groupby('year').size()
    cumulative = events_per_year.cumsum()

    fig, ax = plt.subplots(figsize=(12, 6))
    _prep_ax(ax, 'Cumulative Storm Events Over Time', 'Year', 'Cumulative Count')
    ax.fill_between(cumulative.index, cumulative.values, alpha=0.25, color=PRIMARY)
    ax.plot(cumulative.index, cumulative.values, color=PRIMARY, linewidth=2.5)
    sns.despine(ax=ax)
    plt.tight_layout()
    return fig


def count_plot(df):
    """Top 10 most frequent event types"""
    if len(df) == 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
        return fig

    top_events = df['event_type'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    _prep_ax(ax, 'Most Frequent Storm Types', 'Count', '')
    ax.barh(range(len(top_events)), top_events.values, color=PRIMARY, edgecolor='white', alpha=0.95)
    ax.set_yticks(range(len(top_events)))
    ax.set_yticklabels(top_events.index)
    sns.despine(ax=ax)
    plt.tight_layout()
    return fig


def violin_plot(df):
    """Magnitude distribution across top 5 storm types"""
    if len(df) == 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12)
        return fig

    if 'magnitude' not in df.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'Magnitude data not available', ha='center', va='center', fontsize=12)
        return fig

    top_events = df['event_type'].value_counts().head(5).index
    plot_df = df[df['event_type'].isin(top_events)].copy()
    plot_df = plot_df.dropna(subset=['magnitude'])

    if len(plot_df) == 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'No magnitude data available', ha='center', va='center', fontsize=12)
        return fig

    fig, ax = plt.subplots(figsize=(12, 6))
    _prep_ax(ax, 'Magnitude Distribution by Storm Type', 'Event Type', 'Magnitude')
    sns.violinplot(data=plot_df, x='event_type', y='magnitude', palette=PALETTE, ax=ax)
    ax.tick_params(axis='x', rotation=45)
    sns.despine(ax=ax)
    plt.tight_layout()
    return fig
