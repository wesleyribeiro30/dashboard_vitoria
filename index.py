import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import importlib.util
import dash_html_components as html
from  app import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY],
        suppress_callback_exceptions=True)


# Dados simulados de usuários
users = {
    'wesley': '231288',
    'vendedor02': '123456',
    'vendedor03': '789012',
    'vendedor04': '102030',
    'vendedor05': '304050',
    'vendedor06': '708090',
}

# Layout do login
login_layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Login", className="text-center mb-4", style={'color': 'white', 'font-size': '2.5rem'}),
                    dbc.Input(id='username', placeholder="Username", type="text", className="mb-3", style={'font-size': '1.5rem'}),
                    dbc.Input(id='password', placeholder="Password", type="password", className="mb-3", style={'font-size': '1.5rem'}),
                    dbc.Button("Login", id='login-button', color="primary", className="mr-1", style={'font-size': '1.5rem'}),
                ], className="login-box", style={'text-align': 'center', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'gap': '10px'})
            ], width=6, className="mx-auto mt-5")
        ])
    ], className="login-container", style={'height': '100vh', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'background-image': 'url("https://uploaddeimagens.com.br/images/004/570/379/original/301685108_570362328147371_5973469643414345361_n.jpg")', 'background-size': 'cover', 'background-position': 'center'})
], className="login-background")

# Layout do dashboard
def create_dashboard_layout(username):
    return html.Div([
        html.H1(f"Dashboard do Usuário {username}"),
        # ... Conteúdo específico para o usuário ...
    ])

# Layout de acesso não autorizado
unauthorized_layout = html.Div([
    html.H1("Acesso Não Autorizado"),
    dcc.Link("Voltar ao Login", href="/")
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback para validação de login vendedor01
@app.callback(Output('url', 'pathname'),
              [Input('login-button', 'n_clicks')],
              [State('username', 'value'),
               State('password', 'value')])
def login(n_clicks, username, password):
    if n_clicks is None:
        raise PreventUpdate

    if username in users and users[username] == password:
        if username == 'wesley':
            return f"/vendedor01/{username}"  # Redireciona para a página de dashboard do usuário vendedor01
        elif username == 'vendedor02':
            return f"/vendedor02/{username}"  # Redireciona para a página de dashboard do usuário vendedor02
        elif username == 'vendedor03':
            return f"/vendedor03/{username}"  # Redireciona para a página de dashboard do usuário vendedor03
        elif username == 'vendedor04':
            return f"/vendedor04/{username}"  # Redireciona para a página de dashboard do usuário vendedor04
        elif username == 'vendedor05':
            return f"/vendedor05/{username}"  # Redireciona para a página de dashboard do usuário vendedor05
        elif username == 'vendedor06':
            return f"/vendedor06/{username}"  # Redireciona para a página de dashboard do usuário vendedor06
    else:
        return "/invalid"  # Redireciona para uma página de erro
# Callback para exibir o conteúdo da página correta
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname.startswith('/vendedor01/'):
        username = pathname.split('/')[-1]
        if username in users and username == 'wesley':
            from vendedor01 import layout  # Import the layout from vendedor01.py
            return layout  # Return the imported layout
        else:
            return unauthorized_layout
    elif pathname.startswith('/vendedor02/'):
        username = pathname.split('/')[-1]
        if username in users and username == 'vendedor02':
            from vendedor02 import layout  # Import the layout from vendedor02.py
            return layout  # Return the imported layout
        else:
            return unauthorized_layout
    elif pathname.startswith('/vendedor03/'):
        username = pathname.split('/')[-1]
        if username in users and username == 'vendedor03':
            from vendedor03 import layout  # Import the layout from vendedor03.py
            return layout  # Return the imported layout
        else:
            return unauthorized_layout
    elif pathname.startswith('/vendedor04/'):
        username = pathname.split('/')[-1]
        if username in users and username == 'vendedor04':
            from vendedor04 import layout  # Import the layout from vendedor04.py
            return layout  # Return the imported layout
        else:
            return unauthorized_layout
    elif pathname.startswith('/vendedor05/'):
        username = pathname.split('/')[-1]
        if username in users and username == 'vendedor05':
            from vendedor05 import layout  # Import the layout from vendedor05.py
            return layout  # Return the imported layout
        else:
            return unauthorized_layout
    elif pathname.startswith('/vendedor06/'):
        username = pathname.split('/')[-1]
        if username in users and username == 'vendedor06':
            from vendedor06 import layout # Import the layout from vendedor06.py
            return layout  # Return the imported layout
        else:
            return unauthorized_layout
    elif pathname == '/invalid':
        return unauthorized_layout
    else:
        return login_layout
#if __name__ == '__main__':
    #app.run_server(debug=True)
if __name__ == '__main__':
    app.run_server(debug=False)
    app.run_server(host="0.0.0.0", port="8080")
