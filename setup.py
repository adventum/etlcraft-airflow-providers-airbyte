"""Setup.py for the airbyte-airflow-provider-advm package."""

from setuptools import find_namespace_packages, setup

version = "1.2.8"

setup(
    name="airbyte-airflow-provider-advm",
    version=version,
    install_requires=[
        "psycopg2-binary",
        "airbyte-cdk",
        "apache-airflow",
        "apache-airflow-providers-airbyte",
        "jsonpath-ng",
        "pydantic",
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
