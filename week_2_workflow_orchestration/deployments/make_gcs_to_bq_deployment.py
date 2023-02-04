import asyncio
from prefect.deployments import Deployment
from flows.etl_gcs_to_bq import etl_gcs_to_bq


async def build():
    deployment = await Deployment.build_from_flow(
        flow=etl_gcs_to_bq,
        name="green-2019-02..03",
        parameters={"color": "yellow", "year": 2019, "months": [2, 3]},
        tags=["week-2"],
    )

    dep_id = await deployment.apply()
    print(f"Registered with API: {dep_id}")


if __name__ == "__main__":
    asyncio.run(build())
