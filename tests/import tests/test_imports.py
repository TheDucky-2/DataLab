## Basic tests to check whether datalab modules are importing.abs

def testing_datalab_imports():

    import datalab 
    import datalab.tabular.data_loader
    import datalab.tabular.data_diagnosis
    import datalab.tabular.data_cleaner
    import datalab.tabular.data_preprocessor
    import datalab.tabular.data_visualization
    import datalab.tabular.data_analysis
    import datalab.tabular.computations
    import datalab.tabular.utils

    print("Tests Successful!")
