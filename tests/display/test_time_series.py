import datetime
import numpy as np
from capo_tools.display.time_series import plot_time_series  # Replace 'your_module' with the actual filename

def test_default_x_values():
    """
    Test that when x_values is None, it defaults to a numeric range with the maximum length of y and y_hat.
    """
    y = np.array([1, 2, 3, 4])
    y_hat = np.array([1, 2, 3])  # Shorter than y

    # Capture the generated figure
    fig = plot_time_series(y, y_hat)

    # Extract x values from the first trace (ground truth)
    x_values = fig.data[0].x

    # Expected range should match the longer array (y) = np.arange(len(y))
    assert np.array_equal(x_values, np.arange(len(y))), "Default x_values should match np.arange(max(len(y), len(y_hat)))"

def test_x_values_with_dates():
    """
    Test that x_values are correctly converted to datetime when given as a list of strings.
    """
    y = np.array([1, 2, 3, 4])
    y_hat = np.array([1, 2, 3, 3.5])
    dates = ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"]

    fig = plot_time_series(y, y_hat, x_values=dates)

    # Extract x values from the first trace (ground truth)
    x_values = fig.data[0].x

    # Ensure they are converted to pandas datetime format
    assert isinstance(x_values[0], np.datetime64), "x_values should be converted to datetime"

def test_y_axis_range():
    """
    Test that setting y_range correctly enforces the y-axis limits.
    """
    y = np.array([2, 3, 4, 5])
    y_hat = np.array([1.5, 2.5, 3.5, 4.5])
    y_range = (0, 10)

    fig = plot_time_series(y, y_hat, y_range=y_range)

    # Extract y-axis range from the figure
    y_axis_range = fig.layout.yaxis.range

    assert y_axis_range == tuple(y_range), "Y-axis range should match the provided y_range argument"

def test_plot_dimensions():
    """
    Test that the aspect ratio correctly sets the width based on height.
    """
    y = np.array([1, 2, 3])
    y_hat = np.array([1, 2, 2.8])

    height = 600
    aspect_ratio = 2.0  # Width should be height * aspect_ratio = 600 * 2 = 1200

    fig = plot_time_series(y, y_hat, height=height, aspect_ratio=aspect_ratio)

    assert fig.layout.width == int(height * aspect_ratio), "Plot width should be height * aspect_ratio"

def test_legend_visibility():
    """
    Test that legend visibility is controlled by the 'legend' argument.
    """
    y = np.array([1, 2, 3])
    y_hat = np.array([1, 2, 2.8])

    fig = plot_time_series(y, y_hat, legend=False)

    assert fig.layout.showlegend is False, "Legend should be hidden when legend=False"

def test_grid_visibility():
    """
    Test that grid visibility is controlled by the 'show_grid' argument.
    """
    y = np.array([1, 2, 3])
    y_hat = np.array([1, 2, 2.8])

    fig = plot_time_series(y, y_hat, show_grid=False)

    assert fig.layout.xaxis.showgrid is False, "X-axis grid should be hidden when show_grid=False"
    assert fig.layout.yaxis.showgrid is False, "Y-axis grid should be hidden when show_grid=False"
