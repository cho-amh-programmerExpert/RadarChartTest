import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_radar_chart(categories, values_list, labels, title='Radar Chart'):
    """
    Creates a radar chart with multiple layers.

    :param categories: List of categories (labels for the axes)
    :param values_list: List of lists containing values for each category for multiple datasets
    :param labels: List of labels for each dataset
    :param title: Title of the chart
    """
    # Number of variables we're plotting
    num_vars = len(categories)
    
    # Compute angle of each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    
    # Initialize the radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)
    
    # Draw one axe per variable and add labels
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw the frame
    plt.xticks(angles[:-1], categories, size=12)
    
    # Draw ylabels
    ax.set_rlabel_position(180 / num_vars)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=10)
    plt.ylim(0, 5)
    
    # Colors
    colors = sns.color_palette("Set2", len(values_list))
    
    # Plot each dataset
    for values, label, color in zip(values_list, labels, colors):
        # Ensure the values close the circle
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=label, color=color)
        ax.fill(angles, values, color=color, alpha=0.25)
    
    # Title
    plt.title(title, size=20, color='blue', y=1.1)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    # Add spacing between the labels and the chart
    for label, angle in zip(ax.get_xticklabels(), angles):
        x, y = label.get_position()
        label.set_position((x, y - 0.15))  # Increase the offset by 0.15
    
    st.pyplot(fig)

# Example usage with multiple datasets
categories = ['Speed', 'Reliability', 'Comfort', 'Safety', 'Efficiency']
values_list = [
    [4, 3, 2, 5, 4],  # Car 1
    [5, 4, 3, 2, 5],  # Car 2
    [3, 5, 4, 3, 4]   # Car 3
]
labels = ['Car 1', 'Car 2', 'Car 3']

create_radar_chart(categories, values_list, labels, title='Car Performance Comparison')


st.divider()


