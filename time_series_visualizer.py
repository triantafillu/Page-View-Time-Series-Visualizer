import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data
df = pd.read_csv('fcc-forum-pageviews.csv')
df.set_index('date', drop=True, inplace=True)
df.index = [pd.Timestamp(dt) for dt in df.index]

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, axis = plt.subplots(1, 1, figsize=(30, 10))
    plt.plot(df.index, df['value'], color='r', linewidth=1)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=25)
    plt.xlabel('Date', fontsize=20)
    plt.ylabel('Page Views', fontsize=20)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar=df.copy()
    df_bar['Date'] = df_bar.index
    df_bar['Year'] = df_bar['Date'].map(lambda row: row.strftime('%Y'))
    df_bar['Month'] = df_bar['Date'].map(lambda row: row.strftime('%B'))
    df_bar = pd.DataFrame({
        'Average Page Views':
        df_bar.groupby(['Year', 'Month'])['value'].mean()
    }).reset_index().sort_values(['Year', 'Month'], ascending=[1, 1])

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(20, 20))

    #Order of hue
    months = [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ]

    sns.barplot(
        x='Year',
        y='Average Page Views',
        hue='Month',
        hue_order=months,
        data=df_bar)

    ax.set_ylabel("Average Page Views", fontsize=20)
    ax.set_xlabel("Years", fontsize=20)
    ax.legend(loc=2, fontsize=20)

    ax.tick_params(axis='both', which='major', labelsize=14)
    plt.xticks(rotation=90, horizontalalignment="center")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box['date'] = df_box.index
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box['months'] = [d.strftime('%m') for d in df_box.date]

    df_box = df_box.sort_values(by='months')

    fig, axes = plt.subplots(1, 2)
    fig.set_figwidth(20)
    fig.set_figheight(10)

    axes[0].set_title("Year-wise Box Plot (Trend)", fontsize=20)
    axes[0] = sns.boxplot(x=df_box.year, y=df_box.value, ax=axes[0])
    axes[0].set_xlabel('Year', fontsize=20)
    axes[0].set_ylabel('Page Views', fontsize=20)
    axes[0].tick_params(axis='both', which='major', labelsize=14)

    axes[1].set_title("Month-wise Box Plot (Seasonality)", fontsize=20)
    axes[1] = sns.boxplot(x="month", y="value", data=df_box, ax=axes[1])
    axes[1].set_xlabel('Month', fontsize=20)
    axes[1].set_ylabel('Page Views', fontsize=20)
    axes[1].tick_params(axis='both', which='major', labelsize=14)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

