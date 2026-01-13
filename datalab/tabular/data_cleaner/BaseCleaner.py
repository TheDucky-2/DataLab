import pandas as pd

class DataCleaner:
    
    def __init__(self, df:pd.DataFrame, columns:list=None):

        if not isinstance(df, (pd.DataFrame, pd.Series)):
            raise TypeError(f'df must be a pandas DataFrame or pandas Series, got {type(df).__name__}')

        if not isinstance(columns, (list, type(None))):
            raise TypeError(f'columns must be a list of strings or type None, got {type(columns).__name__}')
            
        # creating a copy of the original dataframe
        self.df = df.copy()  
        
        # if user passes a list of columns
        if columns is None: 
            # columns would default to all of the columns of the dataframe
            self.columns = df.columns.to_list()
        else:
            # columns would be the list of columns passed
            self.columns = columns

        self.not_cleaned = {}

    def validate_columns(self):
        '''
        This function just makes sure that the columns passed by the user actually exist in the dataframe
        ''' 
        # if the column passed by the user is not in dataframe
        missing_columns = [column for column in self.columns if column not in self.df.columns] 

        if missing_columns:
            raise TypeError(f'Columns not found in dataframe: {missing_columns}')

    def drop_duplicates(self, in_columns=None):

        return self.df.drop_duplicates(subset=in_columns)
    
    def track_not_cleaned(self, method=None, col:'str'=None, before: pd.Series=None, mask:pd.Series=None, after:pd.Series=None):

        # if conversion failed, 
        cleaning_failed = mask & (before == after)

        if cleaning_failed.any():
            self.not_cleaned.setdefault(col, {})
            self.not_cleaned[col].setdefault(method, set() )

            self.not_cleaned[col][method].update(before[cleaning_failed].tolist())






    