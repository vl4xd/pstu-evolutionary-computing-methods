import numpy as np
import plotly.graph_objects as go

from functions import rastrigin


class Contour:
    def __init__(self,
                 low_bound: float,
                 up_bound: float,
                 a_param: int,
                 density: int):
        self.x = np.linspace(low_bound, up_bound, density)
        self.y = np.linspace(low_bound, up_bound, density)
        self.xx, self.yy = np.meshgrid(self.x, self.y)
        self.z = rastrigin(self.xx, self.yy, a=a_param)
        self.fig = go.Figure()
        self.fig.add_trace(
            go.Contour(z=self.z, x=self.x, y=self.y, colorscale='Spectral_r')
        )
        self.fig.add_trace(
            go.Scatter(x=[], y=[], mode='markers', marker=dict(color='black', size=5, symbol='circle'))
        )
        title = 'Оптимизация функции Растригина (Популяция)'
        self.fig.update_layout(title=title, xaxis_title='X', yaxis_title='Y')

    def update_points(self, x_points: list[float], y_points: list[float]):
        self.fig.data[1].x = x_points
        self.fig.data[1].y = y_points


class Metrics:
    def __init__(self, all_min: list[float], all_avg: list[float], all_max: list[float]):
        list_gen = [i for i in range(len(all_min))]
        self.fig = go.Figure()
        self.fig.add_trace(
            go.Scatter(x=list_gen, y=all_min, mode='lines', name='Минимум')
        )
        self.fig.add_trace(
            go.Scatter(x=list_gen, y=all_avg, mode='lines', name='Среднее')
        )
        self.fig.add_trace(
            go.Scatter(x=list_gen, y=all_max, mode='lines', name='Максимум')
        )
        self.fig.update_layout(
            title=dict(
                text='Оптимизация функции Растригина (Метрики)'
            ),
            xaxis=dict(
                title=dict(
                    text='Поколение'
                )
            ),
            yaxis=dict(
                title=dict(
                    text='Значение'
                )
            ),
        )

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
