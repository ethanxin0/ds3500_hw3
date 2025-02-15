import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def plot_strike_zone(pitch_data):
    print(pitch_data.head())
    print(f"Plotting data with shape: {pitch_data.shape}")
    print(f"Columns available: {pitch_data.columns.tolist()}")

    # Create scatter plot with hover info
    fig = px.scatter(
        pitch_data,
        x="plate_x",
        y="plate_z",
        color="pitch_type",
        hover_data=["game_date", "player_name", "pitch_type", "description"],
        title="2024 Strike Zone Plot",
        labels={"plate_x": "Horizontal Location (plate_x)", "plate_z": "Vertical Location (plate_z)"},
    )



    # Add a rectangle for the strike zone (MLB dimensions)
    fig.add_shape(
        type="rect",
        x0=-0.83, x1=0.83,  # Horizontal strike zone limits
        y0=1.5, y1=3.5,  # Vertical strike zone limits
        line=dict(color="black", width=2)
    )

    # Customize layout
    fig.update_layout(
        xaxis=dict(range=[-2, 2], title="Horizontal Location"),
        yaxis=dict(range=[0, 5], title="Vertical Location"),
        legend_title="Pitch Type",
        width=700,
        height=800
    )



    return fig