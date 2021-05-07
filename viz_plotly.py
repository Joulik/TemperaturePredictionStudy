import plotly.graph_objects as go
from plotly.subplots import make_subplots

def viz(x_min,x_max):
    
    fig = make_subplots(rows=1, cols=2)
    
    trace0 = go.Histogram(x=x_min,histnorm='probability',nbinsx=50)
    trace1 = go.Histogram(x=x_max,histnorm='probability',nbinsx=50)
    
    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 2)
    
    fig.update_xaxes(range=[-25, 25])
    fig.update_yaxes(range=[0, 0.125])
    
    fig.show()