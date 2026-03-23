import numpy as np
import plotly.graph_objects as go

from functions import rastrigin


class Contour:
    def __init__(self,
                 low_bound: float,
                 up_bound: float,
                 a_param: int,
                 density: int,
                 history_pop: list[list[list[float]]]):
        self.x = np.linspace(low_bound, up_bound, density)
        self.y = np.linspace(low_bound, up_bound, density)
        self.xx, self.yy = np.meshgrid(self.x, self.y)
        self.z = rastrigin(self.xx, self.yy, a=a_param)
        self.fig = go.Figure()
        self.fig.add_trace(
            go.Contour(z=self.z, x=self.x, y=self.y, colorscale='Spectral_r')
        )
        for gen in range(len(history_pop)):
            visible = True
            if gen > 0:
                visible = False
            self.fig.add_trace(
                go.Scatter(
                    x=[ind[0] for ind in history_pop[gen]],
                    y=[ind[1] for ind in history_pop[gen]],
                    mode='markers',
                    marker=dict(color='red', size=13, symbol='circle', opacity=0.7, line=dict(color='white', width=1)),
                    visible=visible
                )
            )
        steps = []
        for gen in range(len(history_pop)):
            # Индекс trace для данного поколения: gen+1 (0 - контур)
            visible_traces = [False] * len(self.fig.data)
            visible_traces[0] = True          # контур всегда видим
            visible_traces[gen + 1] = True    # текущее поколение видимо

            step = dict(
                method="update",
                args=[
                    {"visible": visible_traces},
                    {"title": f"Поколение {gen})"}
                ],
                label=str(gen)  # метка на слайдере
            )
            steps.append(step)
        sliders = [dict(
            active=0,
            currentvalue={"prefix": "Поколение: "},
            pad={"t": 50},
            steps=steps
        )]
        self.fig.update_layout(
            title='Оптимизация функции Растригина (Популяция)', 
            xaxis_title='X', 
            yaxis_title='Y',
            xaxis=dict(range=[low_bound, up_bound]),   # фиксируем диапазон X
            yaxis=dict(range=[low_bound, up_bound]),   # фиксируем диапазон Y
            sliders=sliders if len(history_pop) > 0 else None
        )


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
