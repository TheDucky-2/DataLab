import pandas as pd
from pathlib import Path
import polars as pl

def load_tabular(file_path: str, file_type: str = None, conversion_threshold:int=None, **kwargs) -> pd.DataFrame:
    '''
    ----- Welcome to the first step of this workflow -------------

    Use this function for loading your tabular data as a pandas DataFrame.
    
    Parameters:
    ------------
    file_path: str
        Path of your data file
  
    file_type: str, default is 'csv'
        Supported File Types: 'csv', 'excel, 'parquet', 'JSON'
    
    conversion_threshold: int (default is 100000)
            The number of rows at which the conversion from Polars to pandas switches to Arrow-backed pandas arrays for performance. 
            Users can increase or decrease this threshold depending on their dataset size and memory availability.
       
    kwargs: dict
        Extra arguments you want to pass into pandas file readers.
     
    Returns:
    ---------
        pd.DataFrame (a pandas DataFrame)
    
    Usage Recommendation:
    ---------------------
        Use this function for loading your dataset without having to memorize multiple functions for reading different data files.

    Considerations:
    -------------- 
        If you get an error while reading parquet file, use **kwargs: engine = 'fastparquet' 
        E.g: load_tabular('your_file_name.parquet', engine='fastparquet')

    Example:
    --------------
    >>>   load_tabular('example.csv')   
    >>>   load_tabular('example.xlsx')
    >>>   load_tabular('some/path/to/my/csv/file.csv')
    >>>   load_tabular('example.json')
    
    '''
    if not isinstance(file_path, (str, Path)):
        raise TypeError('file path must be a string or a file path')

    if not isinstance(conversion_threshold,(int, type(None))):
        raise TypeError(f'conversion threshold must be an integer, got {type(conversion_threshold).__name__} ')

    if file_type is None:
        file_type = file_path.split('.')[-1].lower()
    else:
        file_type = file_type.lower()

    if conversion_threshold is None:
        conversion_threshold = 100_000 

    if file_type == 'csv':
        scanned_df = pl.scan_csv(file_path)
        polars_df = scanned_df.collect()
        num_of_rows = polars_df.height

        if num_of_rows >= conversion_threshold:
            df = polars_df.to_pandas(use_pyarrow_extension_array=True)
        else:
            df = polars_df.to_pandas()
    
    elif file_type in ['xlsx', 'xls']:
        df = pd.read_excel(file_path, **kwargs)
    
    elif file_type == 'parquet':
        df = pd.read_parquet(file_path, **kwargs)
    
    elif file_type == 'json':
        df = pd.read_json(file_path, **kwargs)

    else:
        raise ValueError(f'Unsupported file type: {file_type}')
    
    return df