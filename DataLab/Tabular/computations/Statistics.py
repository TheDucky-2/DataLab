from .Computation import Computation

import pandas as pd
import numpy as np


class Statistics(Computation):
    
    def __init__(self, df:pd.DataFrame, columns:list=None):
        import pandas as pd
        import numpy as np

        '''
        Initializing the Statistics Computation

        Parameters:
        -----------
        df: pd.DataFrame
            A pandas dataframe you wish to diagnose

        columns: list
            A list of columns you wish to apply numerical cleaning on
        '''

        super().__init__(df, columns)

        self.df = df.copy()
        self.columns = [column for column in self.columns if column in self.df.columns]
    
    def max(self):

        return self.df.max()

    def min(self):
    
        return self.df.min()

    def Range(self):

        Range= Statistics(self.df).max() - Statistics(self.df).min()

        return Range

    def mean(self) -> pd.Series:
        '''
        Computes the mean (Average) for each column of the DataFrame passed.

        Parameters:
            df: pd.DataFrame
                A pandas DataFrame

            columns : list
            A list of column names

        Return:
            pd.Series
            A pandas Series of mean values for each column
            

        Usage Recommendation:
            Use this function when you want to find the average value of each column

        Considerations:
            This function keeps null values and np.nan, but converts them to <NA> (Int64Dtype)

        >>> Example: 
                Statistics(df).mean()
                ->
                age                     48.998814
                income               76426.897317
                expenses             47351.295358
                savings              24495.968469
                loan_amount          11340.452913
                credit_score           699.995727
                num_of_dependents        2.500065
                years_at_job            20.013299
                risk_score               0.128864
                dtype: Float64

        '''

        return self.df[self.columns].mean()
    
    def median(self):

        return self.df[self.columns].median()

    def std_dev(self):

        return self.df[self.columns].std()

    def quantiles(self, q:float, groupby:str = None, **kwargs)->pd.DataFrame:
        
        if groupby:
            grouped_df = self.df.groupby(groupby)
            return grouped_df.quantile(q=q, **kwargs)

        else:
            return self.df.quantile(q=q, **kwargs)

            
    def IQR(self):

        Q1 = Statistics(self.df).quantiles(0.25)
        Q3 = Statistics(self.df).quantiles(0.75)

        IQR = Q3 - Q1 

        return IQR

    def variance(self, method='sample'):
            
        if method == 'sample':

            sample_variance_dict={}

            n = len(self.df) # n is size of population

            for column in self.df[self.columns]:
                
                sample_variance_dict[column] = ((self.df[column] - self.df[column].mean()) ** 2).sum()/(n-1) # (n-1) for Sample

            return sample_variance_dict

        elif method == 'population':

            population_variance_dict={}

            n = len(self.df) # n is size of population

            for column in self.df[self.columns]:
                
                population_variance_dict[column] = ((self.df[column] - self.df[column].mean()) ** 2).sum()/(n) # (n) for Population

            return population_variance_dict

    def covariance(self):
        
        n = len(self.df)
        centered_df = self.df - self.df.mean()

        covar_matrix = (centered_df.T @ centered_df) / (n-1)

        return covar_matrix

    def MAD(self) -> int|float:
    
        # Since MAD is Median Absolute Deviation, we calculate MAD as 'median of(x - median of x)'
        MAD_dict = {}

        for column in self.df[self.columns]:
            
            MAD_dict[column] = np.median(self.df[column] - np.median(self.df[column]))

        return MAD_dict

    def scaled_MAD(self):
        
        MAD_values = np.array(list(Statistics(self.df).MAD().values()))
        scaled_MAD = 1.4826 * MAD_values
        
        return scaled_MAD