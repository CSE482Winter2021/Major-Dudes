def print_unique(df):
    """
    Helper function to print the unique values in each column in a dataframe.
    """

    for col in df:
        try:
            u = df[col].unique()
            print(f'{col}: {len(df[col])}, {len(u)} unique')
            print(u, '\n')
        except TypeError:
            print(f'{col}: {len(df[col])}, unhashable')


def parse_collection(entry, collection_type, element_type):
    """
    Helper furnction to parse collections stored as entries in a CSV or similar
    text file.
    """

    return collection_type([element_type(x) for x in entry[1:-1].split(',')])
