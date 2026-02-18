import plotly.graph_objects as go


def get_contour(x: list[float],
                y: list[float],
                z: list[list[float]],
                title: str) -> go.Figure:
    fig = go.Figure(data=go.Contour(z=z, x=x, y=y, colorscale='Spectral_r'))
    fig.update_layout(title=title, xaxis_title='X', yaxis_title='Y')
    return fig


def get_surface_3d(xx: list[list[float]],
                   yy: list[list[float]],
                   z: list[list[float]],
                   title: str) -> go.Figure:
    fig = go.Figure(data=[go.Surface(z=z, x=xx, y=yy, colorscale='Spectral_r')])
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
    )
    return fig
