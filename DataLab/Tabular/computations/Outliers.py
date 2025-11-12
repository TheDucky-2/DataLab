import pandas as pd
from .Computation import Computation


class Outliers(Computation):
    
    def __init__(self, df:pd.DataFrame, columns:list=None):
        import pandas as pd
        import numpy as np

        '''
        Initializing the Outliers Computation

        Parameters:
        -----------
        df: pd.DataFrame
            A pandas dataframe you wish to diagnose

        columns: list
            A list of columns you wish to apply numerical cleaning on
        '''

        import pandas as pd

        super().__init__(df, columns)

        self.df = df.copy()
        self.columns = [column for column in self.columns if column in self.df.columns]

    def z_score(self):
        import numpy as np
        
        z_scores = {}

        for column in self.df[self.columns]:

            mean = self.df[column].mean()

            std_dev = self.df[column].std()

            z_scores[column] = np.abs((self.df[column] - self.df[column].mean())/self.df[column].std())
            
        z_scores = pd.DataFrame(z_scores)
            
        return z_scores



            