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
        title="MLB Strike Zone Analysis",
        labels={"plate_x": "Horizontal Location (plate_x)", "plate_z": "Vertical Location (plate_z)"},
    )

    # Add the main strike zone rectangle (solid border)
    fig.add_shape(
        type="rect",
        x0=-0.83, x1=0.83,  # Horizontal strike zone limits
        y0=1.5, y1=3.5,     # Vertical strike zone limits
        line=dict(color="black", width=2),
        fillcolor="rgba(255,255,255,0)"
    )

    # Add vertical dotted line through middle of zone
    fig.add_shape(
        type="line",
        x0=0, x1=0,
        y0=1.5, y1=3.5,
        line=dict(color="black", width=1, dash="dot")
    )

    # Add horizontal dotted line through middle of zone
    fig.add_shape(
        type="line",
        x0=-0.83, x1=0.83,
        y0=2.5, y1=2.5,  # Middle of vertical zone (1.5 to 3.5)
        line=dict(color="black", width=1, dash="dot")
    )

    # Add home plate shape (centered)
    plate_width = 0.83 * 2
    plate_y = 2.5  # Center of zone
    fig.add_shape(
        type="line",
        x0=-plate_width/2, x1=-plate_width/3,
        y0=plate_y, y1=plate_y,
        line=dict(color="black", width=2)
    )
    fig.add_shape(
        type="line",
        x0=-plate_width/3, x1=0,
        y0=plate_y, y1=plate_y,
        line=dict(color="black", width=2)
    )
    fig.add_shape(
        type="line",
        x0=0, x1=plate_width/3,
        y0=plate_y, y1=plate_y,
        line=dict(color="black", width=2)
    )
    fig.add_shape(
        type="line",
        x0=plate_width/3, x1=plate_width/2,
        y0=plate_y, y1=plate_y,
        line=dict(color="black", width=2)
    )

    # Customize layout
    fig.update_layout(
        xaxis=dict(range=[-2, 2], title="Horizontal Location (plate_x)"),
        yaxis=dict(range=[0, 5], title="Vertical Location (plate_z)"),
        legend_title="Pitch Type",
        width=700,
        height=800,
        showlegend=True,
        plot_bgcolor='white',  # White background
        paper_bgcolor='white'
    )

    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')

    return fig