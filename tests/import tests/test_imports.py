## Basic tests to check whether datalab modules are importing.
def test_datalab_imports():
    import pytest

    modules = ['datalab',
               'datalab.tabular.data_loader',
               'datalab.tabular.data_diagnosis',
               'datalab.tabular.data_cleaner',
               'datalab.tabular.data_preprocessor',
               'datalab.tabular.data_visualization',
               'datalab.tabular.computations',
               'datalab.tabular.utils']

    modules_not_found = []
    
    for module in modules:
        try:
            __import__(module)

        except ModuleNotFoundError as error:
            modules_not_found.append(module)

    if modules_not_found:
        pytest.fail(f'The following modules could not be imported: {", ".join(modules_not_found)}')

