import pipelines.p5_orca_rates as p5


def get_data():
    data = p5.run_pipeline()
    return {str(int(row[0])): row[3] for row in data.to_numpy()}
