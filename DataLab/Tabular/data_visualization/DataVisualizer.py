from ..computations import Distribution

import pandas as pd
import missingno as msno
import matplotlib

from ..utils import ProjectHelpers

class DataVisualizer:

    def __init__(self, df: pd.DataFrame, columns:list =None):
        import pandas as pd
        
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f'df must be pandas DataFrame, got {type(df).__name__}')

        if not isinstance(columns, (list, type(None))):
            raise TypeError(f'columns must be a list or type None, got {type(columns).__name__}')

        self.df = df

        if columns is None:
            self.columns = df.columns.to_list()
        # ensuring that the columns passed are in a list
        else:
            self.columns = columns

        print(f'Data Visualizer initialized with columns: {self.columns}')

    def plot_missing(self, viz_type: str|None = None) -> matplotlib.axes.Axes:  # viz : alias for 'visualization'
        '''
        Visualize missing values in each column of the DataFrame

        Parameters:
            df : pd.DataFrame
                A pandas DataFrame

            viz_type : str or type(None) (default is None)

                How you want to visualize missing values:
                    - 'bar'        : Displays a bar chart of missing vs non-missing values for each column
                    - 'heatmap'    : Creates a correlation heatmap showing how missing values present in one column relate with missing values in another.
                    - 'matrix'     : Displays a matrix plot where each row is a record in the DataFrame, and the column represents a column of the DataFrame
                    - 'dendrogram' : Displays a hierarchical clustering plot that groups columns in the DataFrame based on similar patterns of missing values

        Returns:
            matplotlib.axes.Axes
            A matplotlib axes object of the generated plot

        Usage Recommendations:
            1. Use 'bar' for plotting the volume of missing data vs non-missing data, before filling/dropping rows or columns with null values. 
            2. Use 'matrix' to identify patterns to see if missing data is missing randomly or in a structured manner 
            3. Use 'heatmap' for revealing relationships between missing values (if missingness is linked across columns).
            4. Use 'dendrogram' for identifying columns grouped together by similarity of missingness

        Considerations:
            1. This function uses missingno library under the hood. Just make sure you have it installed or use 'pip install missingno'
            2. For assistance with handling missing values, use missing_data_guide() along with this function for better decision making.

        '''
        import missingno as msno
        import matplotlib

        self.viz_type = viz_type
        
        if self.viz_type is not None:

            if self.viz_type == 'heatmap':
                return msno.heatmap(self.df)
            
            elif self.viz_type == 'bar':
                return msno.bar(self.df)
            
            elif self.viz_type == 'matrix':
                return msno.matrix(self.df)
            
            elif self.viz_type == 'dendrogram':
                return msno.dendrogram(self.df)

    def plot_histogram(self, n_bins=30, density=False):
        import numpy as np
        import plotly.express as px

        histograms = Distribution(self.df[self.columns]).compute_histogram(n_bins=n_bins, density=density)

        for column, histogram in histograms.items():

            bin_width = np.diff(histogram['bin_centers']).mean()
            fig= px.bar(x = histogram['bin_centers'], y = histogram['counts'])

            fig.update_traces(width=bin_width, marker_line_width=0)
            fig.update_layout(bargap=0)
            fig.show()