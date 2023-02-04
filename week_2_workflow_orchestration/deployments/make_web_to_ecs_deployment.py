import asyncio
from prefect.deployments import Deployment
from flows.etl_web_to_gcs import etl_web_to_gcs


async def build():
    deployment = await Deployment.build_from_flow(
        flow=etl_web_to_gcs,
        name="green-2020-01",
        schedule={"cron": "0 5 1 * *", "timezone": "UTC"},
        parameters={"color": "green", "year": 2020, "month": 1},
        tags=["week-2"],
    )

    dates = await deployment.schedule.get_dates(3)
    dates = [str(d) for d in dates] + ["..."]
    print(f"Created deployment scheduled for: {dates}]")

    dep_id = await deployment.apply()
    print(f"Registered with API: {dep_id}")


if __name__ == "__main__":
    asyncio.run(build())
