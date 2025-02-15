import panel as pn
from base_api import BASEAPI
from zone2 import plot_strike_zone
import datetime


pn.extension('plotly')

api = BASEAPI()
api.load_base("player_data.csv")


def get_pitcher_dates(pitcher_name):
    if pitcher_name == "Select a pitcher":
        return []
    dates = api.df[api.df['player_name'] == pitcher_name]['game_date'].unique()
    return [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]


def get_pitch_types(pitcher_name):
    if pitcher_name == "Select a pitcher":
        return []
    return sorted(api.df[api.df['player_name'] == pitcher_name]['pitch_type'].unique())


# WIDGET DECLARATIONS
pitcher_options = ["Select a Pitcher"] + api.get_pitcher()
pitcher = pn.widgets.Select(
    name="Pitcher",
    options=pitcher_options,
    value="Select a Pitcher"
)

initial_dates = []
date_picker = pn.widgets.DatePicker(
    name="Select a Date",
    value=None,
    enabled_dates=initial_dates
)

batter_selection = pn.widgets.RadioButtonGroup(
    name="Batter Type",
    options=["Right", "Left", "All"],
    button_type="primary",
    value="All"
)

pitch_types = pn.widgets.MultiChoice(
    name='Pitch Types',
    value=[],
    options=[],
    placeholder='Select Pitch Types'
)


def update_pitcher_data(event):
    # Update dates
    new_dates = get_pitcher_dates(event.new)
    date_picker.enabled_dates = new_dates
    date_picker.value = None

    # Update pitch types
    new_pitch_types = get_pitch_types(event.new)
    pitch_types.options = new_pitch_types
    pitch_types.value = []


pitcher.param.watch(update_pitcher_data, 'value')


# CALLBACK FUNCTIONS
def get_df(pitcher_val, batter_val, date_val, selected_pitches):
    if pitcher_val == "Select a pitcher":
        return None

    print(f"Getting data for {pitcher_val} on {date_val} with batter type: {batter_val}")
    print(f"Selected pitch types: {selected_pitches}")

    if date_val is None:
        return None

    # Get initial data
    df = api.get_stats(pitcher_val, str(date_val))

    if df.empty:
        return df

    # Filter by pitch types if any are selected
    if selected_pitches:
        df = df[df['pitch_type'].isin(selected_pitches)]

    # Filter by batter stance only if not "All"
    if batter_val != "All":
        df = api.seperate_batter_stand(df, batter_val)
        print(f"Found {len(df)} rows after filtering for {batter_val}-handed batters")
    else:
        print(f"Found {len(df)} total rows for all batters")
    return df


def get_plot(df):
    if df is None:
        return pn.pane.Markdown("Please select a pitcher and date")
    if df.empty:
        return pn.pane.Markdown("No data available for selected criteria")
    return plot_strike_zone(df)


# CALLBACK BINDINGS (Connecting widgets to callback functions)
df = pn.bind(get_df, pitcher, batter_selection, date_picker, pitch_types)
plot = pn.bind(get_plot, df)

# DASHBOARD WIDGET CONTAINERS ("CARDS")
card_width = 320

search_card = pn.Card(
    pn.Column(
        pitcher,
        batter_selection,
        date_picker,
        pitch_types
    ),
    title="Search", width=card_width, collapsed=False
)

# Create info display
info_display = pn.pane.DataFrame(width=800)


def update_info(df):
    if df is not None and not df.empty:
        return df
    return None


info = pn.bind(update_info, df)

# LAYOUT
layout = pn.template.FastListTemplate(
    title="MLB Pitcher Strike Zone Analysis",
    sidebar=[
        search_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Strike Zone", plot),
            ("Raw Data", info),
            active=0
        )
    ],
    header_background='#a93226'
).servable()

# Keep the server running
if __name__ == "__main__":
    layout.show(port=5006)