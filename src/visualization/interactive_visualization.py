
import plotly.graph_objs as go

def plot_interactive(data):
    fig = go.Figure(data=[go.Scatter(y=data)])
    fig.show()
