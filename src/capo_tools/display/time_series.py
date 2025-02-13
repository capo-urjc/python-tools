import pandas as pd
import plotly.graph_objects as go
import numpy as np
from matplotlib.figure import Figure


def plot_time_series(y: np.ndarray, y_hat: np.ndarray, x_values=None, title: str = None, xlabel: str = None,
                     ylabel: str = None, path_to_save: str = None, colors: list = ["blue", "red"],
                     markers: list = ["circle", "square"], styles: list = ["solid", "dash"], x_dtick=None, y_dtick=None,
                     y_range: tuple = None, legend: bool = True, show_grid: bool = True, show: bool = False,
                     height: int = 500, aspect_ratio: float = 1.5) -> Figure:
    """
        Visualizes and compares real and predicted time series using Plotly.

        Args:
            y (np.ndarray): Array with the actual values of the time series.
            y_hat (np.ndarray): Array with the predicted values of the time series.
            x_values (list, optional): List of values for the X-axis (default is a numeric range).
            title (str, optional): Title of the plot.
            xlabel (str, optional): Label for the X-axis.
            ylabel (str, optional): Label for the Y-axis.
            path_to_save (str, optional): Path to save the plot as an HTML file. If None, the plot won't be saved.
            colors (list, optional): List of colors for the series (default `["blue", "red"]`).
            markers (list, optional): List of markers for the series (default `["circle", "square"]`).
            styles (list, optional): List of line styles for the series (default `["solid", "dash"]`).
            x_dtick (str, optional): Granularity for the X-axis ticks (e.g., `"D1"` for days, `"M1"` for months).
            y_dtick (int, optional): Granularity for the Y-axis ticks.
            y_range (tuple, optional): Tuple `(min, max)` defining the Y-axis range. If None, it is set automatically.
            legend (bool, optional): Whether to show the legend (default is `True`).
            show_grid (bool, optional): Whether to show the grid (default is `True`).
            show (bool, optional): Whether to display the plot (default is `False`).
            height (int, optional): Height of the plot in pixels (default is `500`).
            aspect_ratio (float, optional): Width-to-height ratio of the plot (default is `1.5`, meaning width = `1.5 * height`).

        Returns:
            matplotlib.Figure
        """

    fig = go.Figure()

    # If no specific X values are provided, generate a default numeric range
    if x_values is None:
        x_values = np.arange(np.maximum(len(y), len(y_hat)))

    # Convert string-based x_values (e.g., dates) to datetime format
    if isinstance(x_values[0], str):
        x_values = pd.to_datetime(x_values)

    # Compute the width dynamically based on the aspect ratio
    width = int(height * aspect_ratio)

    # Add the ground truth (actual values) trace
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y,
        mode="lines+markers",
        name="Ground Truth",
        line=dict(color=colors[0], dash=styles[0]),
        marker=dict(symbol=markers[0])
    ))

    # Add the prediction trace
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_hat,
        mode="lines+markers",
        name="Prediction",
        line=dict(color=colors[1], dash=styles[1]),
        marker=dict(symbol=markers[1])
    ))

    # Update layout with title, axis labels, grid, and styling options
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_white",
        showlegend=legend,
        width=width,
        height=height,
        xaxis=dict(
            showgrid=show_grid,
            gridcolor='lightgray',
            dtick=x_dtick  # Granularity for the X-axis ticks
        ),
        yaxis=dict(
            showgrid=show_grid,
            gridcolor='lightgray',
            dtick=y_dtick,  # Granularity for the Y-axis ticks
            range=y_range  # <-- Manually set Y-axis range if provided
        )
    )

    # Display the plot if specified
    if show:
        fig.show()

    # Save the plot as an HTML file if a path is provided
    if path_to_save is not None:
        fig.write_html(path_to_save)

    return fig


if __name__ == "__main__":
    # # Example data
    # y = np.array([10, 12, 15, 13, 17, 20, 22, 24, 23, 25])
    # y_hat = np.array([9, 11, 14, 12, 16, 19, 21, 23, 22])
    #
    # # Create a list of dates for the X-axis
    # dates = pd.date_range(start="2025-01-01", periods=len(y), freq='D')
    #
    # # Plot the time series with dates on the X-axis and granular tick control
    # f = plot_time_series(y, y_hat, x_values=None, x_dtick="D1", path_to_save="dlt.html", show=False, height=700)

    y = np.array([2, 3, 4, 5])
    y_hat = np.array([1.5, 2.5, 3.5, 4.5])
    y_range = (0, 10)

    fig = plot_time_series(y, y_hat, y_range=y_range)

    # Extract y-axis range from the figure
    y_axis_range = fig.layout.yaxis.range

    assert y_axis_range == list(y_range)
