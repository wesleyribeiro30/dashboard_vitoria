import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import datetime

app = dash.Dash(__name__, external_stylesheets=['styles.css'])
app.config['suppress_callback_exceptions'] = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# Função para formatar moeda
def format_currency(value):
    return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

# Função para atualizar os dados
def update_data():
    aba_desejada = "junho2023"  # Especifique a aba desejada
    df_data = pd.read_excel(r"C:\ASIMOV\Projeto Vitoria\Vendedores 2023.xlsx", sheet_name=aba_desejada)
    

    colunas_numericas = ['OBJ. DIA', 'REALIZADO', 'PEDIDO', 'TICKET M', 'META PEDIDO', 'MEDIA TICK', 'META']
    for col in colunas_numericas:
        df_data[col] = df_data[col].apply(lambda x: '{:.2f}'.format(x) if isinstance(x, (float, int)) else x)
    
    df_data[colunas_numericas] = df_data[colunas_numericas].apply(pd.to_numeric, errors="coerce")
    df_numeric = df_data.dropna(subset=colunas_numericas, how="all")
    df_data['D'] = df_data['D'].dt.date
    df_data['D'] = pd.to_datetime(df_data['D'])
    df_data['D'] = df_data['D'].dt.strftime('%d/%m/%Y')

    total_realizado = df_data["REALIZADO"].sum()
    pedido_realizado = df_data["PEDIDO"].sum()
    media_tick = df_data.at[0, "MEDIA TICK"]
    meta = df_data["META"].sum()
    dias_t = df_data["DiasTrab"].sum()
    dias_m = df_data["DiasM"].sum()
    diferenca_meta = meta - total_realizado
    projecao_mes = (total_realizado / dias_t) * dias_m
    
    return df_data, total_realizado, pedido_realizado, media_tick, meta, dias_t, dias_m, diferenca_meta, projecao_mes

# Layout do gráfico
def update_bar_chart(df):
    fig2 = go.Figure(data=[
        go.Bar(name='OBJ. DIA', x=df['D'], y=df['OBJ. DIA']),
        go.Bar(name='REALIZADO', x=df['D'], y=df['REALIZADO'])
    ])

    # Layout do gráfico
    fig2.update_layout(
        barmode='group',  # Modo de agrupamento das barras
        bargap=0.2,  # Espaço entre as barras do mesmo grupo
        bargroupgap=0.1,  # Espaço entre os grupos de barras
        plot_bgcolor='rgba(0,0,0,0)',  # Fundo do gráfico
        paper_bgcolor='rgba(0,0,0,0)',  # Fundo da área do gráfico
        legend=dict(font=dict(color="white")),  # Cor da legenda
        title=dict(text='Objetivo Diário vs Realizado', font=dict(color="white")),  # Título
        xaxis=dict(title='Data', color='white'),  # Título do eixo x
        yaxis=dict(title='Valores', color='white'),  # Título do eixo y
        font_color="white",  # Cor da fonte
        #autosize=True  # Ajustar automaticamente ao tamanho da tela
        width=800,  # Largura do gráfico
        height=300  # Altura do gráfico
    )

    # Remover botões de modo e de tirar foto
    fig2.update_layout(
        modebar={'bgcolor': 'rgba(0, 0, 0, 0)'},
        showlegend=True
    )

    # Estilo das barras
    fig2.update_traces(
        marker_color=['#1f77b4', '#ff7f0e'],  # Cores das barras
        marker_line_color='rgb(8,48,107)',  # Cor da borda das barras
        marker_line_width=1.5,  # Largura da borda das barras
        opacity=0.7  # Opacidade das barras
    )
    return fig2

# Função para atualizar o gráfico de pizza
def update_pie_chart(meta, total_realizado):
    falta_para_meta = meta - total_realizado
    percentages = [(falta_para_meta / meta) * 100, (total_realizado / meta) * 100]

    fig3 = px.pie(values=percentages, title='', names=['Falta para Meta', 'Total Realizado'])

    fig3.update_layout(
        template="plotly_dark",  # Usar um template de estilo escuro
        paper_bgcolor='rgba(0,0,0,0)',  # Fundo da área do gráfico transparente
        plot_bgcolor='rgba(0,0,0,0)',  # Fundo do gráfico transparente
        font_color="white",  # Cor da fonte
        legend=dict(font=dict(color="white")),  # Cor da legenda
        title=dict(text='', font=dict(color="white")),  # Remover título
        margin=dict(l=0, r=0, t=0, b=0),  # Remover margens
        autosize=True,  # Ajustar o tamanho do gráfico automaticamente
        showlegend=False,  # Remover a legenda
        #config={'modeBarButtonsToRemove': ['toImage'], 'displayModeBar': False}  # Remover botão "Tirar Foto" e ocultar a barra de ferramentas
    )

    return fig3 

# Chamada da função update_pie_chart para definir a variável fig3
df_data, total_realizado, pedido_realizado, media_tick, meta, dias_t, dias_m, diferenca_meta, projecao_mes = update_data()
fig3 = update_pie_chart(meta, total_realizado)
fig2 = update_bar_chart(df_data)

#load_figure_template("minty")

interval = dcc.Interval(
    id='interval-component',
    interval=5*1000,  # 5 segundos em milissegundos
    n_intervals=0
)

@app.callback(
    [Output('grafico2', 'figure'),
     Output('grafico3', 'figure'),
     Output('table', 'data')],
    [Input('interval-component', 'n_intervals'),
     Input('update-button', 'n_clicks')]
)
def update_charts_and_table(n_intervals, n_clicks):
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'interval-component':
        df_data, _, _, _, _, _, _, _, _ = update_data()  # Atualize apenas df_data
    else:
        df_data, total_realizado, pedido_realizado, media_tick, meta, _, _, _, _ = update_data()
    
    fig2_updated = update_bar_chart(df_data)
    fig3_updated = update_pie_chart(meta, total_realizado)  # Use as variáveis já definidas para atualizar fig3
    table_data = df_data.to_dict('records')
    return fig2_updated, fig3_updated, table_data

    # Renderize novamente todo o layout
   # ========= Layout ===========
   
layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                    html.H2("Vitoria Perfilados", style={'font-family': 'Voltaire', 'font-size': '50px'}),
                    html.Hr(),
                    html.P("Dashboard para análise de vendas."),

                      # Botão de Atualização de Dados
                    html.Button('Atualizar Dados', id='update-button', n_clicks=0),
      
                    # Grafico de Pizza      
                    dcc.Graph(id='grafico3', figure=fig3, style={'margin-top': '20px', 'width': '100%', 'background-color': 'transparent', 'position': 'relative', 'z-index': 1}),
                    # Calendario
                    html.H5("Calendario:", style={"margin-top": "20px"}),
                    html.Div([
                        dcc.DatePickerSingle(
                            id='my-date-picker',
                            date=datetime.datetime.today().date(),
                            display_format='DD-MM-YYYY',
                            clearable=True
                        ),
                        
                    ], style={'position': 'relative', 'z-index': 3}),
                ], style={"margin": "20px", "padding": "20px", "height": "max"})
        ], md=3),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Alert([
                        html.Span("Meta: ", style={'color': 'black'}),
                        html.Span(format_currency(abs(meta)), style={'color': 'orange'})
                    ],
                    className="transparent-card",
                    style={'font-weight': 'family', 'border-left': '1px solid', 'border-color': 'orange'}),
                ]),
                dbc.Col([
                    dbc.Alert([
                        html.Span("Valor Total Realizado: ", style={'color': 'black'}),
                        html.Span(format_currency(abs(total_realizado)), style={'color': 'orange'})
                    ],
                    className="transparent-card",
                    style={'font-weight': 'family', 'border-left': '1px solid', 'border-color': 'orange'}),
                ]),
                dbc.Col([
                    dbc.Alert([
                        html.Span("Pedido Realizado: ", style={'color': 'black'}),
                        html.Span(f"{abs(pedido_realizado):.2f}", style={'color': 'orange'})
                    ],
                    className="transparent-card",
                    style={'font-weight': 'family', 'border-left': '1px solid', 'border-color': 'orange'}),
                ]),
                dbc.Col([
                    dbc.Alert([
                        html.Span("Valor Média TICK: ", style={'color': 'black'}),
                        html.Span(format_currency(abs(media_tick)), style={'color': 'orange'})
                    ],
                    className="transparent-card",
                    style={'font-weight': 'family', 'border-left': '1px solid', 'border-color': 'orange'}),
                ]),
                dbc.Col([
                    dbc.Alert([
                        html.Span("Diferença entre Meta e Realizado: ", style={'color': 'black'}),
                        html.Span(f"{'-' if total_realizado < meta else ''}{format_currency(abs(diferenca_meta))}", style={'color': 'orange'})
                    ],
                    className="transparent-card",
                    style={'font-weight': 'family', 'border-left': '1px solid', 'border-color': 'orange'}),
                ]),
                dbc.Col([
                    dbc.Alert([
                        html.Span("Projetado Mês: ", style={'color': 'black'}),
                        html.Span(format_currency(abs(projecao_mes)), style={'color': 'orange'})
                    ],
                    className="transparent-card",
                    style={'font-weight': 'family', 'border-left': '1px solid', 'border-color': 'orange'}),           
                ]),
            ], style={'display': 'flex', 'flex-direction': 'row'}),
            
            html.Div(
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in ['D', 'S', 'OBJ. DIA', 'REALIZADO', 'PEDIDO', 'TICKET M', 'META PEDIDO']],
                    data=df_data.to_dict('records'),
                    style_table={
                        'overflowX': 'auto',
                        'height': '400px',  # Defina a altura desejada
                        'border': '1px solid #ddd',  # Borda da tabela
                        'border-collapse': 'collapse',
                        'position': 'sticky',  # Torna a primeira coluna fixa
                        'left': 0,  # Posição fixa à esquerda
                        'zIndex': 1,  # Para ficar acima das outras colunas
                    },
                    fixed_columns={'headers': True},  # Congela a primeira coluna do cabeçalho
                    style_header={
                        'backgroundColor': '#f8f9fa',
                        'fontWeight': 'bold',
                        'font-size': '14px',
                        'border': '1px solid #ddd',  # Borda do cabeçalho
                        'text-align': 'center',
                        'whiteSpace': 'normal',
                    },
                    style_cell={
                        'textAlign': 'center',
                        'font-size': '12px',
                        'border': '1px solid #ddd',  # Borda das células
                        'padding': '5px',
                        'whiteSpace': 'normal',
                    },
                    style_data={'border': '1px solid #ddd'},  # Borda dos dados
                    style_as_list_view=True,
                    sort_action='native',
                ),
                className="table-responsive"
            ),
            dcc.Graph(id='grafico2', figure=fig2, style={'margin-top': '20px', 'width': '100%', 'background-color': 'transparent'}),
              # Adicione o componente dcc.Interval

        ], md=9),
    ], style={'margin-top': '10px'})
], fluid=True)

if __name__ == '__main__':
    app.layout = layout  # Defina o layout da aplicação
    app.run_server(debug=False, host="0.0.0.0", port="8080")
