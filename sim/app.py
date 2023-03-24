import panel as pn
import holoviews as hv


pn.extension()
hv.extension("bokeh")

ACCENT_COLOR = "#00286e"
SITE = "Vyper Example"
TITLE = "Simulations"

from open_auction import View

apps = [View().display()]


def app():
    return pn.template.FastListTemplate(
        site=SITE,
        title=TITLE,
        header_background=ACCENT_COLOR,
        main=apps,
    ).servable()


app()
