def test_csv_loading_string_columns():

    import pandas as pd
    import tempfile
    from datalab import load_tabular
    

    # creating a temporary csv file just for testing
    def generate_temporary_csv():

        data = {
            'ID': [1, 2, 3, 4, 5],
            'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'Age': [28, 34, 23, 45, 31],
            'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami'],
            'Salary': [70000, 80000, 50000, 90000, 75000]
            }

        df = pd.DataFrame(data)

        temp_file = tempfile.NamedTemporaryFile(delete = False, suffix = '.csv')

        df.to_csv(temp_file.name, index=False)

        return temp_file.name

    csv = generate_temporary_csv()

    df1 = load_tabular(csv, array_type='numpy')
    df2 = load_tabular(csv, array_type='pyarrow')

    assert all(isinstance(value, str) for value in df1['ID'])
    assert all(isinstance(value, str) for value in df2['ID'])
    assert all(isinstance(value, str) for value in df1['Age'])
    assert all(isinstance(value, str) for value in df2['Age'])
    assert all(isinstance(value, str) for value in df1['Salary'])
    assert all(isinstance(value, str) for value in df2['Salary'])
    

