import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns

def sns_patch_bartchart_set_width(ax: matplotlib.axes.Axes, w:float) -> None:
    for patch in ax.patches :
        current_width = patch.get_width()
        diff = current_width - w

        # update the bar width
        patch.set_width(w)
        
        # recenter the bar
        patch.set_x(patch.get_x() + diff * .5)
        
def pstr(df:pd.DataFrame) -> None:
    """Python equivalent of the str(df) function in R.
    """
    display(df.shape, df.apply(lambda col: [col.unique()], axis=0))

def display_df(df:pd.DataFrame, show_index:bool=True, left_align=True) -> None:
    """Print the DataFrame object with rendering options.
    """
    s = df.style
    if left_align:
        s = s.set_properties(**{'text-align': 'left'}).set_table_styles([ dict(selector='th', props=[('text-align', 'left')] ) ])
    if show_index:
        s = s.hide_index()
        
    display(s)
    
def csv_flatten(series:pd.Series) -> list:
    """
    Flatten CSV strings in a series. For example, say you have a series:
    
    [0] "tim, tom, tammy"
    [1] "cindy, peter, mary"
    [2] "apple, juice, grapes"
    
    Return is a flattern list: [tim, tom, tammy, cindy, peter, mary, apple, juice, grapes]
    
    Args:
        series (pd.Series): A series of CSV strings (e.g. "tim, tom, tammy").
    Returns:
        (set): CSV strings will be seperated and flatten.
    """
    return series[series.notnull()].str.cat(sep=', ').split(", ")