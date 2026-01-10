import pandas as pd
from .BaseCleaner import DataCleaner
from ..utils import BackendConverter
import polars as pl

class TextCleaner(DataCleaner):
    
    def __init__(self, df:pd.DataFrame, columns:list=None):

        import polars as pl
        from ..utils import BackendConverter
        import pandas as pd
        
        if not isinstance(df, (pd.DataFrame, pd.Series)):
            raise TypeError(f'df must be a pandas DataFrame or pandas Series, got {type(df).__name__}')

        if not isinstance(columns, (list, type(None))):
            raise TypeError(f'columns must be a list of strings or type None, got {type(columns).__name__}')
            
        # creating a copy of the original dataframe
        self.df = df.select_dtypes(include = ['object', 'string', 'category']) 
        
        # if user passes a list of columns
        if columns is None: 
            # columns would default to all of the columns of the dataframe
            self.columns = df.columns.to_list()
        else:
            # columns would be the list of columns passed
            self.columns = columns

    def to_lowercase(self: pd.DataFrame) -> pd.DataFrame:

        df=BackendConverter(self.df).pandas_to_polars()
        
        df=df.select((pl.all().str.to_lowercase()))

        return BackendConverter(df).polars_to_pandas()

    def to_uppercase(self: pd.DataFrame) -> pd.DataFrame:

        df = BackendConverter(self.df).pandas_to_polars()

        df = df.select(pl.all().str.to_uppercase())

        return BackendConverter(df).polars_to_pandas()

        
    def replace_multiple_spaces_with_single(self) -> pd.DataFrame:
        '''
        Replaces multiple spaces within characters or words with a single space (" ") for each column of the DataFrame.

        Returns:
            pd.DataFrame
            A pandas DataFrame of columns replaced text.

        Usage Recommendation:
            Use this function when you want to replace multiple spaces within text with a single space.

        Consideration:
            Uses polars's with_columns to apply regex to all string columns

        Example:
            TextCleaner(df).replace_multiple_spaces_with_single()

        '''
        polars_df = BackendConverter(self.df).pandas_to_polars()

        replaced_polars_df = polars_df.with_columns(pl.col(pl.Utf8).str.replace_all(r'\s+', " "))

        replaced_polars_df = BackendConverter(replaced_polars_df).polars_to_pandas()
        
        return replaced_polars_df

    def replace_splitters(self, splitters:list[str]=None, replacement:str=None):
        '''
        Replaces different kinds of splitters present in data, with a single splitter in each column of the DataFrame.

        Parameters:
        -----------
            self

            Optional:

            splitters : list or type None (default is ',')
                A list of splitters you have data separated by

            replacement: str or type None (default is ',')
                A single splitter you want to use for converting splitters to one single type of splitter

        Returns:
        --------
            pd.DataFrame
                A pandas DataFrame

        Usage Recommendation:
        ----------------------
            Use this function when you want to normalize multiple splitters with one kind of splitter

        Consideration:
        ---------------
            Uses polars's with_columns to apply regex to all string columns

        Example:
        --------
        >>>    TextCleaner(df, columns=['user_status]).replace_splitters(splitters = [',', '/', '-'], replacement = ',')

        '''
        from ..utils.BackendConverter import BackendConverter
        
        if splitters is None:
            splitters = [',']
        
        if replacement is None:
            replacement = ','

        if not all(isinstance(splitter, str) for splitter in splitters):
            raise TypeError(f"splitters must be a list of strings like ',', '/' etc., got {type(splitter)}")

        if not isinstance(replacement, str):
            raise TypeError(f"replacement must be a strings like ',' etc., got {type(replacement)}")

        splitters = f'[{"".join(splitters)}]'

        polars_df = BackendConverter(self.df[self.columns]).pandas_to_polars()

        for column in self.columns:
            pattern_mask = polars_df[column].str.contains(splitters)

            cleaned = polars_df[column].str.replace_all(splitters, replacement)

            polars_df = polars_df.with_columns(
                pl.when(pattern_mask)
                .then(cleaned)
                .otherwise(pl.col(column))
            )

        self.df = BackendConverter(polars_df).polars_to_pandas()

        return self.df