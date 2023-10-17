import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, Input, Output, State

import warnings
warnings.filterwarnings('ignore')
import joblib

app = dash.Dash(__name__, use_pages=False, external_stylesheets=[dbc.themes.DARKLY]) # Регистрируем веб приложение
model = joblib.load('titanic_dash.pkl')

app.layout = html.Div([
    dbc.Col([
    html.H4('Привет, меня зовут Гайк. Давай попробуем узнать, какие у тебя были бы шансы выжить на Титанике. Выбери свои параметры, а обученная модель предскажет вероятность. Примечание: 1й класс - самый дорогой.'),
], width={'size': 8}),
    dbc.Col([
    html.H4('Класс'),
    dcc.RadioItems([1, 2, 3], id='class', value=3, className='me-2'),
    html.H4('Возраст'),
    dcc.Input( id='age', className='me-2'),
    html.H4('Пол'),
    dcc.RadioItems(['мужской', 'женский'], id='sex', value='мужской'),
    dbc.Button('рассчитать вероятность', className='me-2', id='proba'),
    html.Div(id='output')], width={'size': 12, 'offset': 1})
    ])


@app.callback(Output('output', 'children'),
              [State('class', 'value'),
              State('age', 'value'),
              State('sex', 'value'),
              Input('proba', 'n_clicks')],
              prevent_initial_call=True) 
def update_output(cls, age, sex, trigger):
    print(cls, age, sex)
    if sex=='мужской':
        sex = 1
        h = 'выжил'
    else:
        sex = 0
        h = 'выжила'
    
    for_predict = [[age, sex, cls]]
    pred = model.predict_proba(for_predict)
    ans = f'Ты бы {h} на титанике с вероятностью {(pred[0][1] * 100).round(2)}%'
    return html.H3(ans)


if __name__ == '__main__':
    app.run_server()
