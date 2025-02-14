import panel as pn
from base_api import BASEAPI
from zone2 import plot_strike_zone

# Loads javascript dependencies and configures Panel (required)
pn.extension()

api = BASEAPI()
api.load_base("player_data.csv")

# WIDGET DECLARATIONS
pitcher = pn.widgets.Select(name="Pitcher", options=api.get_pitcher(), value='Sale, Chris')
batter_selection = pn.widgets.RadioButtonGroup(name="Batter Type",options=["Righty", "Lefty"], button_type="primary")
date_picker = pn.widgets.DatePicker(name="Select a Date", value=None)
# Search Widgets


# Plotting widgets




# CALLBACK FUNCTIONS
def get_df(pitcher, batter_selection, date_picker):
    global local
    local = api.get_stats(pitcher, date_picker)
    return local



def get_plot(df):
    return plot_strike_zone(local)
# CALLBACK BINDINGS (Connecting widgets to callback functions)
catalog = pn.bind(pitcher, batter_selection, date_picker)
plot = pn.bind(get_plot, pitcher, batter_selection, date_picker)
# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 320

search_card = pn.Card(
    pn.Column(
        # Widget 1
        pitcher,
        batter_selection,
        date_picker
    ),
    title="Search", width=card_width, collapsed=False
)


plot_card = pn.Card(
    pn.Column(
        # Widget 1
        # Widget 2
        # Widget 3
    ),

    title="Plot", width=card_width, collapsed=True
)


# LAYOUT

layout = pn.template.FastListTemplate(
    title="Dashboard Title Goes Here",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Tab1", catalog),  # Replace None with callback binding
            ("Tab2", plot),  # Replace None with callback binding
            active=1  # Which tab is active by default?
        )

    ],
    header_background='#a93226'

).servable()

layout.show()
