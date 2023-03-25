import panel as pn
import holoviews as hv
from vyper_example.sim.open_auction import View as OpenAuctionView
from vyper_example.sim.account import View as AccountView
from vyper_example.sim.sim import View as SimView


pn.extension()
hv.extension("bokeh")

ACCENT_COLOR = "#00286e"
SITE = "Vyper Example"
TITLE = "Simulations"

models_row = pn.Row(
    AccountView().display(),
    OpenAuctionView().display(),
)

models_pane = pn.Column(
    '# Models',
    models_row,
)

sim_pane = pn.Column(
    '# Simulation',
    SimView().display(),
)

apps = [
    sim_pane,
    models_pane,
]



def app():
    return pn.template.FastListTemplate(
        site=SITE,
        title=TITLE,
        header_background=ACCENT_COLOR,
        main=apps,
    ).servable()


app()
