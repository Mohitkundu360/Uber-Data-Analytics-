import db_dtypes
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(data, **kwargs) -> None:
    """
    Template for exporting data to a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery
    """

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    BigQuery_client = BigQuery.with_config(ConfigFileLoader(config_path, config_profile))

    print("Keys in data (tables being exported):", list(data.keys()))

    for key, value in data.items():
        table_id = f'uber-data-model-454314.uber_data_engineering_yt.{key}'

        print(f"\nExporting table: {table_id}")
        print(value.head())  # Print first few rows to verify the structure

        BigQuery_client.export(
            DataFrame(value),
            table_id,
            if_exists='replace',  # Replace table if it exists
        )

    print("\n✅ All tables exported successfully to BigQuery!")# Specify resolution policy if table name already exists
