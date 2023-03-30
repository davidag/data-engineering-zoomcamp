import html
from pathlib import Path
import re

import numpy as np
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_sqlalchemy import SqlAlchemyConnector
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer


BUCKET_BLOCK_NAME = "gc-storage-data-lake"


@task(log_prints=True)
def fetch_from_db() -> dict[str, pd.DataFrame]:
    """Read data from MySQL database"""
    data = {}
    db_block = SqlAlchemyConnector.load("mysql-db")
    with db_block as db:
        data["nodes"] = pd.read_sql_query(
            """
            SELECT n.nid, n.uid, n.type, n.created, n.title, fdb.body_value as content,
                nc.totalcount as view_counter
            FROM node n JOIN field_data_body fdb ON n.nid = fdb.entity_id
                JOIN node_counter nc ON n.nid = nc.nid
            ORDER BY n.nid
            """,
            db.get_engine(),
            dtype={
                "nid": np.int32,
                "uid": np.int32,
                "type": "string",
                "created": np.int32,
                "title": "string",
                "content": "string",
                "view_counter": np.int32,
            },
        )
        data["comments"] = pd.read_sql_query(
            """
            SELECT c.cid, c.nid, c.uid, SUBSTRING_INDEX(fdcb.bundle, '_', -1) as type,
                c.created, fdcb.comment_body_value as content
            FROM comment c JOIN field_data_comment_body fdcb ON c.cid = fdcb.entity_id
            ORDER BY c.cid
            """,
            db.get_engine(),
            dtype={
                "cid": np.int32,
                "nid": np.int32,
                "uid": np.int32,
                "type": "string",
                "created": np.int32,
                "content": "string",
            },
        )
        data["users"] = pd.read_sql_query(
            """
            SELECT u.uid, MD5(u.name) as name, u.created
            FROM users u
            ORDER BY u.uid
            """,
            db.get_engine(),
            dtype={
                "uid": np.int32,
                "name": "string",
                "created": np.int32,
            },
        )
    return data


@task(log_prints=True)
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove invalid rows"""

    # Remove rows with empty content
    if "content" in df and "title" in df:
        df = df[(df["title"].str.len() > 0) | (df["content"].str.len() > 0)]
    elif "content" in df:
        df = df[df["content"].str.len() > 0]

    # Nodes of type different from blog or forum
    if "type" in df:
        df = df[(df["type"] == "blog") | (df["type"] == "forum")]

    # Transform newlines to html breaks
    if "content" in df:
        df["content"] = df["content"].apply(html.unescape)
        df["content"] = df["content"].apply(cleanhtml)
        df["content"] = df["content"].apply(stem)
        df.rename(columns={"content": "stems"}, inplace=True)

    # Parse unix timestamps
    if "created" in df:
        df["created"] = pd.to_datetime(df["created"], unit="s")
        df.insert(
            df.columns.get_loc("created") + 1,
            "year",
            df["created"].apply(lambda d: d.year),
        )
        df.insert(
            df.columns.get_loc("created") + 2,
            "month",
            df["created"].apply(lambda d: d.month),
        )

    return df


@task()
def write_parquet_files(dfs: dict[str, pd.DataFrame]) -> list[Path]:
    """Write DataFrames out locally as parquet files"""
    files = []
    for name, df in dfs.items():
        path = Path(f"data/{name}.parquet")
        df.to_parquet(path, index=False, compression="gzip")
        files.append(path)
    return files


@task()
def upload_to_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load(BUCKET_BLOCK_NAME)
    gcs_block.upload_from_path(from_path=path, to_path=f"data/{path.name}")


@flow(name="Processing Flow")
def etl_db_to_local():
    """The main ETL function"""
    filepaths = list(Path("./data").glob("*.parquet"))

    if len(filepaths) == 0:
        dfs = fetch_from_db()

        for name, df in dfs.items():
            dfs[name] = clean_data(df)

        filepaths = write_parquet_files(dfs)

    for path in filepaths:
        upload_to_gcs(path)


# https://stackoverflow.com/a/12982689/11441
def cleanhtml(raw_html: str) -> str:
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


stemmer = SnowballStemmer("spanish")


def stem(content: str) -> str:
    stems = [stemmer.stem(word) for word in word_tokenize(content, language="spanish")]
    return " ".join(stems)


if __name__ == "__main__":
    etl_db_to_local()
