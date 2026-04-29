import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import os

# ── Load processed data ───────────────────────────────────────────────────────
data_path = os.path.join(os.path.dirname(__file__), "data", "processed_sales.csv")
df = pd.read_csv(data_path)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Aggregate total sales per day (across all regions)
daily_sales = df.groupby("date")["sales"].sum().reset_index()

# Price increase date
PRICE_INCREASE_DATE = "2021-01-15"

# ── Build chart ───────────────────────────────────────────────────────────────
fig = go.Figure()

# Before price increase
before = daily_sales[daily_sales["date"] < PRICE_INCREASE_DATE]
after  = daily_sales[daily_sales["date"] >= PRICE_INCREASE_DATE]

fig.add_trace(go.Scatter(
    x=before["date"],
    y=before["sales"],
    mode="lines",
    name="Before Price Increase",
    line=dict(color="#F4845F", width=2.5),
    hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales: $%{y:,.2f}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=after["date"],
    y=after["sales"],
    mode="lines",
    name="After Price Increase",
    line=dict(color="#2EC4B6", width=2.5),
    hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales: $%{y:,.2f}<extra></extra>"
))

# Vertical line for price increase
fig.add_vline(
    x=PRICE_INCREASE_DATE,
    line_dash="dash",
    line_color="#FFFFFF",
    line_width=1.5,
    annotation_text="  Price Increase (15 Jan 2021)",
    annotation_position="top right",
    annotation_font=dict(color="#FFFFFF", size=12)
)

fig.update_layout(
    paper_bgcolor="#0F1117",
    plot_bgcolor="#0F1117",
    font=dict(family="Georgia, serif", color="#E8E8E8"),
    xaxis=dict(
        title="Date",
        title_font=dict(size=14, color="#AAAAAA"),
        tickfont=dict(size=11, color="#AAAAAA"),
        gridcolor="#1E2130",
        showline=True,
        linecolor="#2A2D3E",
        zeroline=False,
    ),
    yaxis=dict(
        title="Total Sales ($)",
        title_font=dict(size=14, color="#AAAAAA"),
        tickfont=dict(size=11, color="#AAAAAA"),
        gridcolor="#1E2130",
        showline=True,
        linecolor="#2A2D3E",
        zeroline=False,
        tickprefix="$",
    ),
    legend=dict(
        bgcolor="#1A1D2E",
        bordercolor="#2A2D3E",
        borderwidth=1,
        font=dict(size=12),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=60, r=40, t=60, b=60),
    hovermode="x unified",
)

# ── App layout ────────────────────────────────────────────────────────────────
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#0F1117",
        "minHeight": "100vh",
        "fontFamily": "Georgia, serif",
        "padding": "0",
    },
    children=[

        # Header
        html.Div(
            style={
                "backgroundColor": "#0F1117",
                "borderBottom": "1px solid #2A2D3E",
                "padding": "32px 48px 24px",
            },
            children=[
                html.H1(
                    "Pink Morsel Sales Visualiser",
                    style={
                        "color": "#F4845F",
                        "fontSize": "2.2rem",
                        "fontWeight": "bold",
                        "margin": "0 0 8px 0",
                        "letterSpacing": "0.5px",
                    }
                ),
                html.P(
                    "Analysing Soul Foods sales revenue before and after the Pink Morsel price increase — 15 January 2021",
                    style={
                        "color": "#888888",
                        "fontSize": "1rem",
                        "margin": "0",
                    }
                ),
            ]
        ),

        # Chart
        html.Div(
            style={"padding": "32px 48px"},
            children=[
                dcc.Graph(
                    id="sales-chart",
                    figure=fig,
                    config={"displayModeBar": False},
                    style={"height": "520px"},
                )
            ]
        ),

        # Footer insight
        html.Div(
            style={
                "padding": "0 48px 40px",
                "display": "flex",
                "gap": "24px",
            },
            children=[
                html.Div(
                    style={
                        "backgroundColor": "#1A1D2E",
                        "border": "1px solid #F4845F33",
                        "borderLeft": "4px solid #F4845F",
                        "borderRadius": "8px",
                        "padding": "20px 24px",
                        "flex": "1",
                    },
                    children=[
                        html.H3("Before Price Increase", style={"color": "#F4845F", "margin": "0 0 6px", "fontSize": "1rem"}),
                        html.P("Lower daily sales revenue recorded prior to 15 Jan 2021.",
                               style={"color": "#AAAAAA", "margin": "0", "fontSize": "0.9rem"})
                    ]
                ),
                html.Div(
                    style={
                        "backgroundColor": "#1A1D2E",
                        "border": "1px solid #2EC4B633",
                        "borderLeft": "4px solid #2EC4B6",
                        "borderRadius": "8px",
                        "padding": "20px 24px",
                        "flex": "1",
                    },
                    children=[
                        html.H3("After Price Increase", style={"color": "#2EC4B6", "margin": "0 0 6px", "fontSize": "1rem"}),
                        html.P("Higher daily sales revenue observed following the price increase on 15 Jan 2021.",
                               style={"color": "#AAAAAA", "margin": "0", "fontSize": "0.9rem"})
                    ]
                ),
            ]
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
