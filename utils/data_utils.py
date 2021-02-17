def print_unique(df):
    """
    Helper function to print the unique values in each column in a dataframe.
    """

    for col in df:
        u = df[col].unique()
        print(f'{col}: {len(df[col])}, {len(u)} unique')
        print(u, '\n')
