import datetime

from google.cloud import bigquery
import pandas
import pytz
import os
from google.oauth2 import service_account


def load(dataframe):

    credentials = service_account.Credentials.from_service_account_file("credentials/adam_service_account.json")
    client = bigquery.Client(credentials=credentials)

    # TODO(developer): Set table_id to the ID of the table to create.
    table_id = "adam-wirski-locations.interview.LOCATION_INTERVIEW"

    job_config = bigquery.LoadJobConfig(
        # Specify a (partial) schema. All columns are always written to the
        # table. The schema is used to assist in data type definitions.
        schema=[
            # Specify the type of columns whose type cannot be auto-detected. For
            # example the "title" column uses pandas dtype "object", so its
            # data type is ambiguous.
            # bigquery.SchemaField("Name", bigquery.enums.SqlTypeNames.STRING),
            # bigquery.SchemaField("Longitude", bigquery.enums.SqlTypeNames.NUMERIC),
            # bigquery.SchemaField("Latitude", bigquery.enums.SqlTypeNames.NUMERIC),

            # # Indexes are written if included in the schema by name.
            # bigquery.SchemaField("wikidata_id", bigquery.enums.SqlTypeNames.STRING),
        ],
        # Optionally, set the write disposition. BigQuery appends loaded rows
        # to an existing table by default, but with WRITE_TRUNCATE write
        # disposition it replaces the table with the loaded data.
        write_disposition="WRITE_TRUNCATE",
    )

    job = client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )  # Make an API request.
    job.result()  # Wait for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )