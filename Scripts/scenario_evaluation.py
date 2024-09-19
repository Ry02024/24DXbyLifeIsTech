import matplotlib.pyplot as plt

def plot_comparison_bar_chart(data, columns, title, xlabel, ylabel, rotation=0, show_values=False):
    """
    Function to create a bar plot with optional value annotations.
    
    Parameters:
    - data: DataFrame containing the data to plot.
    - columns: list of columns to sum and plot (e.g., ['数量', '売上予測']).
    - title: Title of the chart.
    - xlabel: Label for the x-axis.
    - ylabel: Label for the y-axis.
    - rotation: Degree to rotate the x-axis labels (default is 0).
    - show_values: Whether to show values on top of the bars (default is False).
    """
    # Sum the selected columns
    sum_values = data[columns].sum()
    
    # Create the bar plot
    plt.figure(figsize=(5, 5))
    ax = sum_values.plot(kind='bar')

    # Add title and labels
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)

    # Rotate the x-axis labels
    plt.xticks(rotation=rotation)

    # Optionally add value labels to the bars
    if show_values:
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    
    # Display the plot
    plt.show()
