import networkx as nx
import pandas as pd
from pathlib import Path

def load_graph(file_path:str, file_type:str=None, **kwargs):
    '''
    Functionality: 
    --------------
    Use this function for converting your graph data file into a NetworkX Graph object
    
    Note: 
    ------
    The file type is automatically detected from the file extension. 

    Parameters:
    ----------
    file_path: str
        Path of your data file

    Supported file types:
        - "csv"      : Edge list in CSV format (two or three columns: source, target [, weight]).
        - "txt"      : Edge list in plain text format (space or tab separated).
        - "adjlist"  : Adjacency list format (NetworkX-compatible).
        - "graphml"  : GraphML format (XML-based, supports node/edge attributes).

    **kwargs: dict
        Extra arguments you want to pass into a NetworkX reader
    
    Returns:
    --------
    A NetworkX Graph object

        G : networkx.Graph or networkx.DiGraph   (also supports variations of DiGraphs like MultiDiGraph)

    Errors:
    -------
    Raises ValueError:
        If 'file_type' is not supported.

    Examples:
    ---------

    >>>>> G = load_graph('edges.csv')      # auto-detect
    >>>>> G = load_graph('edges.txt')   
    >>>>> G = load_graph('edges.csv', edge_attr = True)    

    '''
    
    if not isinstance(file_path, (str, Path)):
        raise TypeError('file path must be a string or Path!')


    if file_type is None:
        file_type = file_path.split('.')[-1].lower()

    if file_type == 'csv':
        df = pd.read_csv(file_path)
        return nx.from_pandas_edgelist(df, **kwargs)

    if file_type == 'gml':
        return nx.read_gml(file_path, **kwargs)

    if file_type == 'txt':
        return nx.read_adjlist(file_path, **kwargs)

    with open(file_path, 'r') as f:
        for line in f:

            if not line.strip() or line.startswith('#'):
                continue
            parts = line.split(' ')
            n_cols = len(parts)
            break

    if n_cols == 2:
        G = nx.read_edgelist(file_path, **kwargs)
    elif n_cols == 3:
        G = nx.read_weighted_edgelist(file_path, **kwargs)
    else:
        raise ValueError(f'Unsupported file type with {n_cols} columns')

    return G

def show_textfile_preview(file_path:str, preview_lines:input=10):
    '''
    Shows the first N and last N lines of the file for inspection

    Parameters:

        file_path: str
            Path of the input text file

        preview_lines: int
            Number of lines you wish to preview from beginning and end.
    
    '''

    with open(file_path, 'r', encoding = 'utf-8', errors='ignore') as textfile:
        lines = textfile.readlines()
    
    total_lines = len(lines)

    print(f'\n File loaded: {file_path}  ({total_lines:,} lines)\n')
    print(' FILE PREVIEW')
    print(f'\n First {preview_lines} lines')

    for index, line in enumerate(lines[:preview_lines], 1):
        print(f'{index:4}: {line.strip()}')

    print(f'\n Last {preview_lines} lines')

    for index, line in enumerate(lines[-preview_lines:], total_lines):
        print(f'{index:4}: {line.rstrip()}')

