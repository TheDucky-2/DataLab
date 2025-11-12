from ..data_loader import load_tabular
from ..computations import Statistics

from ..utils import ProjectHelpers

from pathlib import Path

import pandas as pd
import numpy as np


class Diagnosis:

    def __init__(self, df: pd.DataFrame, columns:list = None):
        '''
        Initializing the Diagnosis

        Parameters:
        -----------
        df: pd.DataFrame
            A pandas dataframe you wish to diagnose

        columns: list
            A list of columns you wish to apply numerical cleaning on
        '''

        # making sure that the passed df is a pandas DataFrame
        if isinstance(df, pd.DataFrame):
            df = df.copy()     # using a copy to avoid modifying original df

        elif isinstance(df, (str, Path)):
            df = load_tabular(df)     # reading if a file  

        else:
            raise TypeError(f'df must be a pandas DataFrame or a file path, got {type(df).__name__}')

        if columns is None:
            columns = df.columns.to_list()
        # ensuring that the columns passed are in a list
        elif not isinstance(columns, list):
            raise TypeError(f'columns must be a list of column names, got {type(self.columns).__name__}')

        self.df = df
        self.columns = [column for column in columns if column in df.columns]

        ProjectHelpers().print_temporarily(f'Diagnosis initialized with columns: {self.columns}')
    
    def data_summary(self):

        summary = {

            'shape'        : self.df.shape,
            'columns'      : self.columns,
            'dtypes'       : self.df.dtypes,
            'index'        : self.df.index
        }

        return summary

    def show_memory_usage(self, usage_by='total'):

        if usage_by == 'total':

            total_usage = self.df.memory_usage(deep=True).sum()/(1024**2)
            print(f'Total Memory Usage: {self.df.memory_usage(deep=True).sum()/(1024**2):.2f} MB')
            return total_usage
        
        elif usage_by == 'separate':

            separate_usage = self.df.memory_usage(deep=True)/(1024**2)
            print('Data Usage in MB:\n')
            return separate_usage

    def detect_column_types(self) -> dict [str, list[str]]:

        '''
        Detect the column types (Categorical, Numerical, Datetime) for each column of a DataFrame
            
        Returns:
        --------
        Return a dictionary with list of column types.
            
            dict    
                Numerical  : List of Numerical type columns
                Datetime   : List of Datetime type columns
                Categorical: List of Categorical or object type columns

        Usage Recommendation:
        ---------------------
            1. Use this function to check whether a column is categorized as 'Categorical or text', 'Numerical', or Datetime.
            2. Use 'dl.ColumnConverter' to change column types if column type is not detected correctly.

        '''

        self.column_types = {'Numerical': [], 'Datetime' :[], 'Categorical':[]}

        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                self.column_types['Numerical'].append(col)

            elif pd.api.types.is_datetime64_any_dtype(self.df[col]):
                self.column_types['Datetime'].append(col)

            elif pd.api.types.is_object_dtype(self.df[col]) or pd.api.types.is_categorical_dtype(self.df[col]):
                self.column_types['Categorical'].append(col)

        return self.column_types 

    def show_unique_values(self) -> dict[list[str]]:
        '''
        Return a dictionary of unique values in each column. 
            {'column_name': df[column].unique()}
        
        Returns:
            dict
            A dictionary of key, value pairs of column and unique values present in that column

        Usage Recommendation:
            Use this function when you want to see what unique values are present in the column.

        Example: 
            show_unique_values()['Item'] -> {'Item': ['Coffee', 'Cake', 'Cookie', 'Salad', 'Smoothie', 'UNKNOWN','Sandwich', nan, 'ERROR', 'Juice', 'Tea']}
        
        '''
        self.unique_values = {}

        for col in self.df.columns:
            self.unique_values[f'{col}'] = col
            self.unique_values[col] = self.df[col].unique()

        return self.unique_values  

    def check_sparsity(self, value: int|float) -> pd.Series:
            '''
            Checks the ratio of a specific number (usually 0) present in the selected column of the DataFrame

            Parameters:
                df   :       pd.DataFrame, a pandas DataFrame
                value:       int or float , an integer or a decimal number

            Returns:
                pd.Series
                A pandas Series of the columns passed in, along with the ratio of the value. 
                
            Usage Recommendation:
                1. Use this function only for Exploratory Data Analysis.  
                2. Mostly used to check how many values are 0 in a certain column. However, you can also use integers like 3 or floats like 5.888
                3. This function is intended to help you get an overview of which column may and may not contribute meaningfully to the analysis or ML.

            Considerations:
                Pass numeric values after converting datatypes to int or float, instead of using strings.
                

            >>> Example: 
                        Input : NumericalCleaner(df).check_sparsity(0)
                        Output: age                  0.000000
                                income               0.000000
                                expenses             0.000000
                                savings              0.000000
                                loan_amount          0.000000
                                credit_score         0.000000
                                num_of_dependents    0.147308
                                years_at_job         0.021907
                                risk_score           0.335651           <- 33.5% values in column 'risk_score' are 0 (or 0.00).
                                dtype: float64
            '''
            self.value = value
            # getting the ratio of value present in the column
            sparsity = self.df[self.columns].apply(lambda column: ((column == self.value).sum()/len(column))*100)

            print(f'\nOccurrence of {self.value} in each column of the dataframe (in %)')
            
            return sparsity

    def detect_outliers(self, method='IQR'):
        
        print("\nUses IQR method by default. If you want to detect outliers using z-score, pass the parameter 'z-score'")
        
        self.method = method

        if self.method == 'IQR':

            outliers = {}

            for column in self.df.columns:

                Q1 = self.df[column].quantile(0.25)
                Q3 = self.df[column].quantile(0.75)

                # Inter Quartile Range
                IQR = Q3 - Q1 

                lower_bound = Q1 - (1.5 * IQR)
                upper_bound = Q3 + (1.5 * IQR)

                outliers[column] = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]

        elif self.method == 'z-score':

            outliers = {}

            for column in self.df.columns:
                mean = self.df[column].mean()
                std_dev = self.df[column].std()

                z_scores = np.abs((self.df[column] - self.df[column].mean())/self.df[column].std())

                outliers_per_column = self.df[column][z_scores > 3].to_list()
                outliers[column] = outliers_per_column
                
        return outliers

    def check_skewness(self)-> pd.Series:
        '''
        Checks the skewness in each column of the DataFrame

            Returns:
                pd.Series
                A pandas Series of all columns of the DataFrame with skewness values.
                
            Usage Recommendation:
                1. Use this function when you want to check how unevenly data is distributed around the mean (skewness).
                2. Use only for numerical columns
    
            >>> Example: 
                    Diagnosis(df).check_skewness()
        
        '''
        print('Skewness in each column of the DataFrame')
        
        return self.df.skew()

    def show_cardinality(self)-> dict:
    
        cardinality={}
        
        for column in self.df[self.columns]:
            cardinality[column] = len(self.df[column].unique())/len(self.df[column])

        return cardinality

    def show_duplicates(self, in_columns=None) -> pd.Series:

        return self.df[self.df[self.columns].duplicated(subset=in_columns)]

    def count_duplicates(self, in_columns=None ):

        return self.df[self.columns].duplicated(subset=in_columns).sum()
    
    def check_zero_variance(self):
            
        if Statistics(self.df).variance() == 0:
            return f'These columns have zero variance: {column}'
        
        elif Statistics(self.df).variance() != 0:
            return f'No columns have zero variance'