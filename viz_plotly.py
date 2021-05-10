import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def viz(x_min,x_max):
    
    #kwargs = {'title_font':dict(size= 24)}
    fig = make_subplots(
                        rows=1,
                        cols=2,
                        subplot_titles=("T<sub>min</sub>", "T<sub>max</sub>"),
                        )

    trace0 = go.Histogram(x=x_min,histnorm='probability',nbinsx=50,name="T<sub>min</sub>",showlegend=False)
    trace1 = go.Histogram(x=x_max,histnorm='probability',nbinsx=50,name="T<sub>max</sub>",showlegend=False)

    d = np.arange(-25,25,0.5)
    
    mu = x_min.mean()
    sigma = x_min.std()
    y_min = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (d - mu)**2 / (2 * sigma**2))
    trace2 = go.Scatter(x=d, y=y_min, mode='lines',line = dict(color='rgb(0,0,255)', width=4),name="Gaussian distr.",showlegend=False)
    
    mu = x_max.mean()
    sigma = x_max.std()
    y_max = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (d - mu)**2 / (2 * sigma**2))
    trace3 = go.Scatter(x=d, y=y_max, mode='lines',line = dict(color='rgb(255,0,0)', width=4),name="Gaussian distr.",showlegend=False)

    fig.update_xaxes(title_text="T<sub>observed</sub> - T<sub>predicted</sub>",
                    title_font={"size": 20},
                    tickfont=dict(size=18),
                    showgrid=True, gridwidth=1, gridcolor='LightPink',
                    tick0=-25, dtick=5)
    fig.update_yaxes(title_text="Distribution",
                    title_font={"size": 20},
                    tickfont=dict(size=18),
                    showgrid=True, gridwidth=1, gridcolor='LightPink')

    fig.update_annotations(font_size=24)
    fig.add_annotation(dict(x=0.075, y=0.8, xref="paper", yref="paper", 
                            text='mean = 0.6°C', showarrow=False),font_size=20,font_color='rgb(0,0,255)')
    fig.add_annotation(dict(x=0.075, y=0.75, xref="paper", yref="paper", 
                            text='std dev = 3°C', showarrow=False),font_size=20,font_color='rgb(0,0,255)')
    
    fig.add_annotation(dict(x=0.725, y=0.8, xref="paper", yref="paper", 
                            text='mean = 0.2°C', showarrow=False),font_size=20,font_color='rgb(255,0,0)')
    fig.add_annotation(dict(x=0.725, y=0.75, xref="paper", yref="paper", 
                            text='std dev = 4°C', showarrow=False),font_size=20,font_color='rgb(255,0,0)')


    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 2)

    fig.append_trace(trace2, 1, 1)
    fig.append_trace(trace3, 1, 2)

    fig.update_xaxes(range=[-25, 25])
    fig.update_yaxes(range=[0, 0.125])
    
    fig.write_image("fig_model_1.png")
    fig.show()