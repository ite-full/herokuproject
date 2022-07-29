# Lab 20
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import date
from dash.dependencies import Output, Input

# Import App data from csv sheets **************************************
# Data preparation
df_orders = pd.read_csv("OrdersSmaller.csv")
df_orders["Order Date"] = pd.to_datetime(df_orders["Order Date"], format='%d/%m/%Y')
df_orders["Ship Date"] = pd.to_datetime(df_orders["Ship Date"], format='%d/%m/%Y')
# taking out the $ and , and converting the profit to numeric field.
df_orders["Profit"] = df_orders["Profit"].str.replace('$', '', regex=False).str.replace(',', '', regex=False)
df_orders["Profit"] = pd.to_numeric(df_orders["Profit"])
# taking out the $ and , and converting the Sales to numeric field.
df_orders["Sales"] = df_orders["Sales"].str.replace('$', '', regex=False).str.replace(',', '', regex=False)
df_orders["Sales"] = pd.to_numeric(df_orders["Sales"])

# Use a boostrap theme SKETCHY
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

# Prepare the two charts using the dataframe prepared earlier
fig1 = px.histogram(df_orders, x="Order Date", y='Sales', title='Sales by Order Date')
fig2 = px.histogram(df_orders, x="Category", y="Quantity", title="Category Quantity",
                    color='Category', barmode='group')

# layout has 3 rows, first row contains image & Title, 2nd row are cards and 3rd rows are charts
app.layout = dbc.Container([
    dbc.Row([  # Row 1, logo image needs to be stored in the assets subfolder
        dbc.Col([
            html.Img(src=app.get_asset_url('logo.png'), alt='MyLogo')
        ], width=2),
        # added date slider
        dbc.Col([
            dcc.DatePickerSingle(
                id='my-date-picker-start',
                display_format='YYYY-MM-DD',
                date=date(2015, 12, 1)
            ),
            dcc.DatePickerSingle(
                id='my-date-picker-end',
                display_format='YYYY-MM-DD',
                date=date(2015, 12, 31)
            ),
        ], width=4),
        # end of date slider
        dbc.Col([
            html.H1('Sales & Profit Dashboard'),
        ], width=6)
    ], className='mb-2 mt-2'),
    dbc.Row([  # Row 2 consists of 4 cards
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Total Sales'),
                    html.H2(id='card_TotalSales', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Total Profit'),
                    html.H2(id='card_TotalProfit', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Total Quantity'),
                    html.H2(id='card_TotalQuantity', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Customer Count'),
                    html.H2(id='card_TotalCustomer', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=3),
    ], className='mb-2 mt-2'),
    dbc.Row([  # Row 3 consists of two charts fig 1 & fig 2
        dbc.Col([
            dcc.Graph(
                id='chart1',
                figure=fig1
            )
        ], width=6),
        dbc.Col([
            dcc.Graph(
                id='chart2',
                figure=fig2
            )
        ], width=6),
    ], className='mb-2'),
], fluid=True)


# Updating the 4 number cards ******************************************
@app.callback(
    Output('card_TotalSales', 'children'),
    Output('card_TotalProfit', 'children'),
    Output('card_TotalQuantity', 'children'),
    Output('card_TotalCustomer', 'children'),
    Input('my-date-picker-start', 'date'),
    Input('my-date-picker-end', 'date'),
)
def update_small_cards(start_date, end_date):
    # filter the records to mask & allocate to new dataframe
    mask = (df_orders['Order Date'] >= start_date) & (df_orders['Order Date'] <= end_date)
    df2 = df_orders.loc[mask]
    totalSales = round(df2['Sales'].sum(), 0)
    totalProfit = round(df2['Profit'].sum(), 0)
    total_Qty = df2['Quantity'].sum()
    total_Customer = len(df2['Customer ID'].unique())

    return totalSales, totalProfit, total_Qty, total_Customer


# Bar Chart1 ************************************************************
@app.callback(
    Output('chart1', 'figure'),
    Input('my-date-picker-start', 'date'),
    Input('my-date-picker-end', 'date'),
)
def update_chart1(start_date, end_date):
    # filter the records to mask & allocate to new dataframe
    mask = (df_orders['Order Date'] >= start_date) & (df_orders['Order Date'] <= end_date)
    df2 = df_orders.loc[mask]
    fig_1 = px.histogram(df2, x="Order Date", y='Sales', title='Sales by Order Date')
    return fig_1


# Bar Chart2 ************************************************************
@app.callback(
    Output('chart2', 'figure'),
    Input('my-date-picker-start', 'date'),
    Input('my-date-picker-end', 'date'),
)
def update_chart2(start_date, end_date):
    # filter the records to mask & allocate to new dataframe
    mask = (df_orders['Order Date'] >= start_date) & (df_orders['Order Date'] <= end_date)
    df2 = df_orders.loc[mask]
    fig_2 = px.histogram(df2, x="Category", y="Quantity", title="Category Quantity",
                         color='Category', barmode='group')
    return fig_2


# execute the program
if __name__ == '__main__':
    app.run_server(host='localhost', port=8050)
