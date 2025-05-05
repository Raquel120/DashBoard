import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = dash.Dash(__name__)

# =======================================
# Dados principais
# =======================================

regioes = ['Trás-os-Montes', 'Baixo Vouga', 'Lezíria do Tejo', 'Minho-Lima', 'Beira Interior Norte']

# Dados para gráfico de linha
valores_trás_os_montes = [17, 20, 7, 3, 8, 13, 12, 17, 28, 17, 7, 7, 21, 17, 11, 13, 14, 14, 17, 60, 24, 8, 8, 5, 16, 15, 6, 1, 3, 14, 8, 17, 22, 11, 2, 1, 9, 5, 5, 5, 2, 1, 7, 28, 10, 14, 6, 2, 7, 9, 10, 8, 1, 11, 8, 17, 14, 11, 12, 3, 7, 11, 7, 3]
valores_baixo_vouga = [13, 11, 5, 6, 8, 21, 27, 39, 31, 3, 12, 8, 14, 21, 3, 15, 15, 11, 15, 32, 21, 14, 6, 9, 16, 14, 8, 5, 7, 13, 13, 8, 33, 12, 13, 6, 9, 12, 4, 9, 10, 6, 21, 24, 13, 16, 9, 10, 9, 10, 7, 5, 12, 15, 24, 25, 24, 14, 2, 4, 13, 16, 18, 1]
valores_leziria_do_tejo = [24, 25, 14, 8, 12, 15, 19, 30, 21, 21, 10, 11, 11, 25, 9, 9, 7, 9, 11, 26, 21, 12, 11, 1, 13, 12, 15, 13, 9, 6, 8, 16, 21, 10, 16, 10, 13, 21, 16, 12, 4, 11, 20, 25, 10, 7, 6, 3, 9, 17, 12, 5, 5, 10, 15, 18, 43, 17, 5, 4, 14, 9, 15, 0]
valores_minho_lima = [5, 10, 3, 7, 2, 6, 13, 28, 8, 3, 9, 6, 5, 12, 4, 7, 7, 10, 6, 21, 14, 11, 2, 8, 6, 4, 5, 1, 6, 4, 3, 14, 3, 11, 1, 4, 7, 5, 3, 10, 10, 3, 5, 8, 5, 5, 5, 4, 7, 7, 2, 3, 3, 5, 5, 10, 14, 3, 7, 3, 8, 3, 4, 0]
valores_beira_interior_norte = [9, 13, 2, 3, 4, 4, 12, 23, 9, 11, 3, 4, 16, 9, 4, 4, 4, 2, 11, 31, 9, 3, 3, 1, 4, 6, 4, 2, 3, 7, 11, 5, 6, 4, 0, 1, 2, 6, 7, 1, 9, 4, 12, 9, 1, 2, 2, 1, 1, 10, 6, 4, 5, 6, 6, 12, 12, 4, 7, 1, 11, 7, 6, 1]

anos = [2020, 2021, 2022, 2023, 2024, 2025]
meses = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
anos_mes = [f'{ano}-{mes}' for ano in anos for mes in meses][:64]
anos_mes_full = anos_mes * len(regioes)
regioes_full = sum([[r] * 64 for r in regioes], [])

valores = (
    valores_trás_os_montes +
    valores_baixo_vouga +
    valores_leziria_do_tejo +
    valores_minho_lima +
    valores_beira_interior_norte
)

df_linha = pd.DataFrame({
    'Região': regioes_full,
    'Ano-Mes': anos_mes_full,
    'Valor': valores
})

df_barras = pd.DataFrame({
    'Região': regioes,
    'População Jovem': [3412, 8591, 6472, 8405, 3969],
    'Likes': [0, 3585, 2036, 1710, 1698],
    'Candidatos': [221, 144, 165, 68, 33]
})

df_barras_long = df_barras.melt(id_vars='Região', var_name='Tipo', value_name='Valor')

fig_barras = px.bar(
    df_barras_long, x='Região', y='Valor',
    color='Tipo', barmode='group',
    text='Valor',
    color_discrete_map={
        'População Jovem': '#A2C8E3',
        'Likes': '#FFCD80',
        'Candidatos': '#A8E6A3'
    }
)
fig_barras.update_traces(textposition='outside')
fig_barras.update_layout(yaxis_title='Valor', xaxis_title='Região')

# Mapa
df_mapa = pd.DataFrame({
    'Ano': [2020, 2021, 2022, 2023, 2024],
    'Trás-os-Montes': [156, 212, 116, 94, 111],
    'Baixo Vouga': [184, 176, 148, 143, 151],
    'Lezíria do Tejo': [210, 152, 149, 148, 160],
    'Minho-Lima': [100, 107, 62, 70, 69],
    'Beira Interior Norte': [97, 97, 53, 56, 74]
})
df_mapa_long = df_mapa.melt(id_vars='Ano', var_name='Região', value_name='Candidatos')
coords = {
    'Trás-os-Montes': [41.5, -7.0],
    'Baixo Vouga': [40.6, -8.6],
    'Lezíria do Tejo': [39.2, -8.6],
    'Minho-Lima': [41.7, -8.8],
    'Beira Interior Norte': [40.5, -7.2]
}
df_mapa_long['lat'] = df_mapa_long['Região'].map(lambda x: coords[x][0])
df_mapa_long['lon'] = df_mapa_long['Região'].map(lambda x: coords[x][1])
# Mapa - utilizando scatter_map
colorscale = [
    [0, '#00FF00'],  # Verde
    [0.33, '#FFFF00'],  # Amarelo
    [0.66, '#FFA500'],  # Laranja
    [1, '#FF0000']   # Vermelho
]
fig_mapa = px.scatter_map(
    df_mapa_long, lat='lat', lon='lon', size='Candidatos',
    color='Candidatos', animation_frame='Ano',
    size_max=100, zoom=5.7, height=500,
    title='Número de Candidatos por Região e Ano',
    color_continuous_scale=colorscale
)

fig_mapa.update_layout(map_style="open-street-map")
fig_mapa.update_traces(marker=dict(
    colorscale=[[0, '#00FF00'], [0.33, '#FFFF00'], [0.66, '#FFA500'], [1, '#FF0000']],
    colorbar=dict(title='Candidatos'),
    showscale=True
))

# === Depois de montar df_mapa, antes do app.layout ===

# Dados para gráfico de dispersão
df_disp = pd.DataFrame({
    'Região': regioes,
    'Candidatos': [221, 144, 165, 68, 33],
    'Duração': [7, 5, 5, 6, 6],
    'Orquestra': ['Não', 'Sim', 'Sim', 'Sim', 'Sim'],
    'Banda Sinfónica': ['Não', 'Sim', 'Sim', 'Sim', 'Sim'],
    'Seminário': ['Sim', 'Não', 'Não', 'Sim', 'Não'],
    'Encontro Gímnico': ['Não', 'Sim', 'Sim', 'Sim', 'Sim'],
    'Apresentação de Livro': ['Não', 'Sim', 'Sim', 'Sim', 'Não'],
    'Expo Exército': ['Não', 'Sim', 'Sim', 'Sim', 'Sim'],
    'Música de Câmara': ['Não', 'Não', 'Não', 'Sim', 'Não'],
    'Demonstração Cinotécnica': ['Não', 'Não', 'Não', 'Sim', 'Não'],
    'Salto de Paraquedistas Noturno': ['Não', 'Não', 'Não', 'Sim', 'Sim'],
    'Fogo de Artifício': ['Não', 'Não', 'Não', 'Sim', 'Não'],
    'Corrida Solidário': ['Não', 'Não', 'Não', 'Sim', 'Não'],
    'Radical Adventure': ['Não', 'Não', 'Não', 'Não', 'Sim'],
    'Concerto Jovem': ['Não', 'Não', 'Não', 'Sim', 'Sim']
})

anos = [2020, 2021, 2022, 2023, 2024]
atividades_por_ano = {
    2020: ["Seminário"],
    2021: ["OLE", "BFE", "Encontro Gímnico", "Apresentação de Livro", "EXPO"],
    2022: ["OLE", "BFE", "Encontro Gímnico", "Apresentação de Livro", "EXPO"],
    2023: ["OLE", "BFE", "Seminário", "Encontro Gímnico", "Apresentação de Livro", "EXPO", "Música de Câmara",
           "Demonstração Cinotécnica", "Salto de Paraquedistas Noturno", "Fogo de Artifício", "Corrida Solidária", "Concerto Jovem"],
    2024: ["BFE", "EXPO", "Salto de Paraquedistas Noturno", "Radical Adventure", "Concerto Jovem"]
}

# 1) Define o mapeamento ano → nº de candidatos aqui, fora de qualquer loop
candidatos_por_ano = {
    '2020': 747,
    '2021': 744,
    '2022': 528,
    '2023': 511,
    '2024': 565
}

# ──────────────── definir antes do loop ────────────────
# ──────────────── antes do app.layout ────────────────
import plotly.express as px

# … lá em cima, antes do app.layout …

figs_pizza = {}
for ano, atividades in atividades_por_ano.items():
    df_pizza = pd.DataFrame({
        'Atividade': atividades,
        'Percentagem': [100.0 / len(atividades)] * len(atividades)
    })
    fig_p = px.pie(
        df_pizza,
        names='Atividade',
        values='Percentagem',
        height=350,
        width=350,
        color_discrete_sequence=px.colors.qualitative.Pastel  # <— aqui
    )
    fig_p.update_traces(textinfo='percent')
    fig_p.update_layout(
        title={
            'text': f"Distribuição das Atividades – {ano}",
            'x': 0.5, 'xanchor': 'center',
            'font': {'size': 20, 'color': 'black'}
        },
        margin={'t': 40, 'b': 20, 'l': 20, 'r': 20},
        paper_bgcolor='white',
        showlegend=True
    )
    figs_pizza[str(ano)] = fig_p

# ─────────────────────────────────────────
    
app.layout = html.Div(style={
    'backgroundColor': '#556B2F', 'padding': '20px', 'fontFamily': 'Arial, sans-serif'
}, children=[
    html.H1(
        "CELEBRAÇÕES DO DIA DO EXÉRCITO: IMPACTO NO RECRUTAMENTO",
        style={
            'textAlign': 'center',
            'color': 'white',
            'fontSize': '36px',
            'marginBottom': '30px'
        }
    ),

    html.Div([
        html.Label("Selecionar Região:", style={'fontWeight': 'bold', 'fontSize': '18px', 'color': 'white'}),
        dcc.Dropdown(
    id='grafico-dropdown',
    options=[{'label': r, 'value': r} for r in regioes] + [{'label': 'Todas as regiões', 'value': 'Todas as regiões'}],
    value='Trás-os-Montes',  # Valor inicial
    style={'width': '50%', 'marginBottom': '30px'}
),

        dcc.Graph(id='grafico-linha')
    ], style={'marginBottom': '50px'}),

dcc.Graph(id='grafico-mapa', figure=fig_mapa),


    dcc.Graph(id='grafico-barras', figure=fig_barras, style={'marginBottom': '50px'}),

    html.Div([
        html.Label("Comparar Nº de Candidatos com:", style={'fontWeight': 'bold', 'fontSize': '18px', 'color': 'white'}),
        dcc.Dropdown(
            id='disp-xaxis-dropdown',
            options=[{'label': col, 'value': col} for col in df_disp.columns if col != 'Região' and col != 'Candidatos'],
            value='Duração',
            style={'width': '60%', 'marginBottom': '30px'}
        ),
        dcc.Graph(id='grafico-disp')
    ], style={'marginBottom': '50px'}),


       # Dropdown para escolher o ano da cerimónia (aciona pizza & gauge)
    html.Div([
        html.Label("Selecionar Ano da Cerimónia:", style={
            'fontWeight': 'bold', 'fontSize': '18px', 'color': 'white',
            'marginBottom': '10px'
        }),
        dcc.Dropdown(
            id='dropdown-pizza',
            options=[{'label': str(ano), 'value': str(ano)} for ano in anos],
            value='2020',
            style={'width': '200px', 'marginBottom': '20px'}
        )
    ], style={'marginBottom': '20px'}),
   
    # … logo após o Dropdown de ano …

# … dentro do app.layout, no lugar do seu Div de pizza+gauge …

# … logo após o Div do dropdown de ano …

html.Div(
    [
        # coluna da pizza + legenda em baixo
         html.Div([
                dcc.Graph(
                    id='grafico-pizza',
                    config={'displayModeBar': False},
                    style={'width': '350px', 'height': '350px'}
                ),
                html.Div(
                    id='pizza-legend',
                    style={
                        'width': '350px',
                        'height': '120px',
                        'overflowY': 'auto',
                        'marginTop': '10px'
                    }
                )
            ], style={
                'flex': '0 0 350px',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center'
            }),

        # coluna do gauge
        html.Div(
            dcc.Graph(
                id='grafico-gauge',
                style={'width': '350px', 'height': '350px'}
            ),
            style={
                'flex': '0 0 350px',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center'
            }
        )
    ],
    style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 0 10px rgba(0,0,0,0.2)',
        'marginBottom': '50px'
    }
),

])  # <--- fecha o app.layout aqui, SEM MAIS html.Div nem style

# Callbacks
@app.callback(
    Output('grafico-linha', 'figure'),
    Input('grafico-dropdown', 'value')  # Entrada do dropdown
)
def update_line_graph(regiao):
    if regiao == 'Todas as regiões':
        # Para "Todas as regiões", combinamos os dados de todas as regiões
        df_regiao = df_linha
    else:
        # Caso contrário, filtra apenas pela região selecionada
        df_regiao = df_linha[df_linha['Região'] == regiao]
    
    # Cria o gráfico de linha com os dados da região ou todas as regiões
    fig = px.line(df_regiao, x='Ano-Mes', y='Valor', color='Região' if regiao == 'Todas as regiões' else None,
                  title=f'Evolução dos Candidatos em {regiao}' if regiao != 'Todas as regiões' else 'Evolução dos Candidatos em Todas as Regiões')
    
    # Atualiza os títulos dos eixos
    fig.update_layout(xaxis_title='Ano-Mês', yaxis_title='Valor')
    
    return fig

@app.callback(
    Output('grafico-disp', 'figure'),
    Input('disp-xaxis-dropdown', 'value')
)
def update_disp_graph(_):
    df_plot = df_disp[['Região', 'Candidatos', 'Duração']]

    fig = px.scatter(
        df_plot,
        x='Duração',
        y='Candidatos',
        color='Região',
        size='Candidatos',
        hover_name='Região',
        title='Número de Candidatos por Duração das Celebrações',
        labels={'Duração': 'Duração (dias)', 'Candidatos': 'Nº de Candidatos'}
    )

    # só markers, sem texto
    fig.update_traces(mode='markers')

    fig.update_layout(
        xaxis=dict(dtick=1),
        legend_title_text='Região'
    )

    return fig

from dash.dependencies import Input, Output

@app.callback(
    [ Output('grafico-pizza', 'figure'),
      Output('pizza-legend', 'children') ],
    Input('dropdown-pizza', 'value')
)
def update_pizza(ano):
    fig = figs_pizza[ano]
    fig.update_layout(showlegend=False)

    trace = fig.data[0]
    # fallback para a mesma paleta que usaste lá em cima
    palette = px.colors.qualitative.Pastel
    colors = list(trace.marker.colors) if trace.marker.colors is not None else palette

    legend_items = []
    for lbl, val, col in zip(trace.labels, trace.values, colors):
        legend_items.append(
            html.Div([
                html.Span(style={
                    'display': 'inline-block',
                    'width': '12px', 'height': '12px',
                    'backgroundColor': col,
                    'marginRight': '6px'
                }),
                html.Span(f"{lbl}: {val:.0f}%")
            ], style={'marginBottom': '4px'})
        )

    return fig, legend_items

@app.callback(
    Output('grafico-gauge','figure'),
    Input('dropdown-pizza','value')
)
def update_gauge(ano):
    val = candidatos_por_ano[ano]
    fig = go.Figure(go.Indicator(
        mode="gauge", value=val,
        gauge={
            'axis':{'range':[500,800],'tickfont':{'color':'black'}},
            'bar':{'color':'black','thickness':0.1},
            'steps':[
                {'range':[500,600],'color':'#FF6666'},
                {'range':[600,700],'color':'#FFE066'},
                {'range':[700,800],'color':'#A8E6A3'}
            ],
            'borderwidth':2,'bordercolor':'black'
        }
    ))
    fig.update_layout(
        height=350, width=350,
        title={'text':f"Número de Candidatos",'x':0.5,'xanchor':'center',
               'font':{'size':20,'color':'black'}},
        paper_bgcolor='white',
        margin={'t':40,'b':20,'l':20,'r':20}
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
