"""Setup.py for the airbyte-airflow-provider-advm package."""

from setuptools import find_namespace_packages, setup

version = "1.3.3"

setup(
    name="airbyte-airflow-provider-advm",
    version=version,
    install_requires=[
        "psycopg2-binary",
        "airbyte-cdk",
        "apache-airflow",
        "apache-airflow-providers-airbyte",
        "jsonpath-ng",
        "pydantic>=2.7,<3",
    ],
    packages=find_namespace_packages(
        include=[
            "airbyte_api",
            "airbyte_api.*",
            "airbyte_airflow_provider_advm",
            "airbyte_airflow_provider_advm.*",
        ]
    ),
)
