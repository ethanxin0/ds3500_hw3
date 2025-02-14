import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Function to plot the strike zone
def plot_strike_zone(pitch_data):
    fig, ax = plt.subplots(figsize=(6, 7))
    
    # Scatter plot of pitch locations
    ax.scatter(pitch_data["plate_x"], pitch_data["plate_z"], c=pitch_data["pitch_type"].astype("category").cat.codes,alpha=0.7, label =pitch_data["pitch_type"])
    
    # Draw the strike zone (standard MLB dimensions)
    strike_zone = plt.Rectangle((-0.83, 1.5), 1.66, 2.0, fill=False, color="black", linewidth=2)
    ax.add_patch(strike_zone)
    
    # Labels and limits
    ax.set_xlabel("Horizontal Location (plate_x)")
    ax.set_ylabel("Vertical Location (plate_z)")
    ax.set_title("2024 Strike Zone Plot")
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, 5)
    plt.legend()
    plt.show()


