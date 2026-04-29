import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import os

# ── Load processed data ───────────────────────────────────────────────────────
data_path = os.path.join(os.path.dirname(__file__), "data", "processed_sales.csv")
df = pd.read_csv(data_path)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

PRICE_INCREASE_DATE = "2021-01-15"

# ── Chart builder ─────────────────────────────────────────────────────────────
def build_figure(region="all"):
    filtered = df if region == "all" else df[df["region"] == region]
    daily = filtered.groupby("date")["sales"].sum().reset_index()

    before = daily[daily["date"] <  PRICE_INCREASE_DATE]
    after  = daily[daily["date"] >= PRICE_INCREASE_DATE]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=before["date"], y=before["sales"],
        mode="lines", name="Before Price Increase",
        line=dict(color="#E8A87C", width=2.5),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales: $%{y:,.2f}<extra></extra>",
        fill="tozeroy",
        fillcolor="rgba(232,168,124,0.06)"
    ))

    fig.add_trace(go.Scatter(
        x=after["date"], y=after["sales"],
        mode="lines", name="After Price Increase",
        line=dict(color="#7CC8C8", width=2.5),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales: $%{y:,.2f}<extra></extra>",
        fill="tozeroy",
        fillcolor="rgba(124,200,200,0.06)"
    ))

    fig.add_vline(
        x=PRICE_INCREASE_DATE,
        line_dash="dot",
        line_color="rgba(255,255,255,0.25)",
        line_width=1.5,
        annotation_text="  15 Jan 2021",
        annotation_position="top right",
        annotation_font=dict(color="rgba(255,255,255,0.4)", size=11)
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#888880"),
        xaxis=dict(
            title=dict(text="Date", font=dict(size=12, color="#666660")),
            tickfont=dict(size=11, color="#666660"),
            gridcolor="rgba(255,255,255,0.04)",
            showline=False,
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text="Total Sales (AUD)", font=dict(size=12, color="#666660")),
            tickfont=dict(size=11, color="#666660"),
            gridcolor="rgba(255,255,255,0.04)",
            showline=False,
            zeroline=False,
            tickprefix="$",
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(size=11, color="#888880"),
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right",  x=1
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#1E1E1E",
            bordercolor="#2A2A2A",
            font=dict(family="DM Sans, sans-serif", size=12, color="#F0EDE8")
        )
    )

    return fig

# ── App ───────────────────────────────────────────────────────────────────────
app = dash.Dash(__name__)

app.layout = html.Div([

    # Header
    html.Div(className="header", children=[
        html.P("Soul Foods · Analytics", className="header-eyebrow"),
        html.H1(["Pink Morsel ", html.Em("Sales"), " Visualiser"], className="header-title"),
        html.P(
            "Explore regional sales revenue for Pink Morsels across time. "
            "The dashed line marks the price increase on 15 January 2021.",
            className="header-subtitle"
        ),
    ]),

    # Main grid: sidebar + chart
    html.Div(className="main-content", children=[

        # Sidebar
        html.Div(className="sidebar", children=[
            html.P("Filter by Region", className="sidebar-label"),

            dcc.RadioItems(
                id="region-filter",
                options=[
                    {"label": "All Regions", "value": "all"},
                    {"label": "North",       "value": "north"},
                    {"label": "East",        "value": "east"},
                    {"label": "South",       "value": "south"},
                    {"label": "West",        "value": "west"},
                ],
                value="all",
                className="region-radio",
                inputClassName="region-radio-input",
                labelClassName="region-radio-label",
            ),

            html.Hr(className="sidebar-divider"),

            html.P("Legend", className="sidebar-label"),
            html.Div(className="legend-item", children=[
                html.Div(className="legend-dot before"),
                html.P("Before\nprice increase", className="legend-text"),
            ]),
            html.Div(className="legend-item", children=[
                html.Div(className="legend-dot after"),
                html.P("After\nprice increase", className="legend-text"),
            ]),
        ]),

        # Chart area
        html.Div(className="chart-area", children=[
            html.H2("Daily Sales Revenue", className="chart-title"),
            html.P("Aggregated by day · All values in AUD", className="chart-subtitle"),

            dcc.Graph(
                id="sales-chart",
                figure=build_figure(),
                config={"displayModeBar": False},
                style={"height": "420px"},
            ),

            # Stat cards
            html.Div(className="stat-cards", children=[
                html.Div(className="stat-card before-card", children=[
                    html.P("Before Price Increase", className="stat-card-label"),
                    html.P(
                        "Lower daily revenue recorded prior to 15 Jan 2021, "
                        "reflecting the original Pink Morsel price point.",
                        className="stat-card-desc"
                    ),
                ]),
                html.Div(className="stat-card after-card", children=[
                    html.P("After Price Increase", className="stat-card-label"),
                    html.P(
                        "Higher daily revenue observed post price increase — "
                        "the answer to Soul Foods' key business question.",
                        className="stat-card-desc"
                    ),
                ]),
            ]),
        ]),
    ]),

    # Footer
    html.Div(className="footer", children=[
        html.P("Pink Morsel Sales · Quantium Data Analytics", className="footer-text"),
        html.Span("Soul Foods Confidential", className="footer-badge"),
    ]),

])

# ── Callback ──────────────────────────────────────────────────────────────────
@callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(region):
    return build_figure(region)


if __name__ == "__main__":
    app.run(debug=True)
