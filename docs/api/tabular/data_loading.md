# Data Loading API

Welcome to the first step of walking with DataLab!

We will now explore how we can load tabular data using DataLab.

## `load_tabular`

We can load a dataset from **CSV, Excel, Parquet, or JSON** files into a **pandas DataFrame**.

This function supports multiple file types with a single API and is optimized for large datasets (**tested with 5M–10M rows**).

For performance and memory efficiency, the data is first loaded using **Polars** and then converted to a pandas DataFrame.

This ensures stability on low-RAM systems while maintaining **full pandas compatibility**.

Tabular data in DataLab can be loaded using the ``load_tabular()`` method.
> This method always returns a pandas DataFrame.

---

### Import

```python
from datalab import load_tabular

df = load_tabular('your_file.csv')
```

## Parameters

| Name | DataType | Default | Description | Example |
|------|------|---------|-------------|---------|
| `file_path` | `str` | — | Path to your data file or just the file name. | `'path/to/your/file/file_name.csv'`<br>or `'file_name.csv'` |
| `file_type` | `str` | `'csv'` | Supported file types: `'csv'`, `'excel'`, `'parquet'`, `'json'`.<br> Usually automatically detected.<br> Specifying this is completely optional. | `'csv'`, `'excel'`, `'parquet'`, `'json'` |
| `array_type` | `str` | `'auto'` | Determines the array/backend type used in pandas operations:<br> <br>- `'numpy'` -> usual NumPy backend (slower for very large datasets with object types)<br>- `'pyarrow'` -> PyArrow backend for better performance on large datasets<br>- `'auto'` -> automatically selects backend based on input and dataset size | `'numpy'`, `'pyarrow'`, `'auto'` |
| `conversion_threshold` | `int` | `100000` | Number of rows at which Polars -> pandas conversion switches to Arrow-backed pandas arrays for performance.<br> Adjust depending on dataset size and memory availability. | `100000` |


## Returns

``pd.DataFrame`` - A pandas DataFrame

1. Returns **Arrow**-backed pandas DataFrame for datasets above ``conversion_threshold`` (**100,000 rows**).
2. Returns **NumPy**-backed pandas DataFrame for smaller datasets.

## Usage Recommendations

- Use this function to load datasets quickly without memorizing multiple read functions.
- Polars -> pandas conversion ensures efficient memory usage and stability, even on low-RAM systems.

## Considerations

Adjust ``array_type`` and ``conversion_threshold`` for very large datasets to optimize performance and memory usage.

## Examples
``` python
# Load a CSV file (default parameters)
df1 = load_tabular('example.csv')

# Load an Excel file
df2 = load_tabular('example.xlsx', file_type='excel')               # file_type is optional

# Load a Parquet file using PyArrow backend
df3 = load_tabular('example.parquet', array_type='pyarrow')

# Load a large CSV file with custom conversion threshold
df4 = load_tabular('large_dataset.csv', conversion_threshold=2000000)

# Load a JSON file from a subdirectory with auto array backend
df5 = load_tabular('some/path/to/data.json')                        # auto is default
```

## Performance Note

This method has been tested on datasets with **5 million to 10 million rows**.

It provides efficient memory usage and fast loading by automatically converting data from Polars -> Arrow-backed pandas arrays, when the number of rows exceeds the ``conversion_threshold``.

Users can adjust ``conversion_threshold`` based on dataset size and available memory to optimize performance.