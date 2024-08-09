"""Setup.py for the airbyte-airflow-provider-advm package."""

from setuptools import find_namespace_packages, setup

version = "1.4.2"

setup(
    name="airbyte-airflow-provider-advm",
    version=version,
    install_requires=[
        "requests",
        "apache-airflow >= 2.9.2, <3.0.0",
        "apache-airflow-providers-airbyte >= 3.8.1, <4.0.0",
        "jsonpath-ng",
        "pydantic>=2.7,<3.0",
    ],
    tests_require=["pytest"],
    packages=find_namespace_packages(
        include=[
            "airbyte_api",
            "airbyte_api.*",
            "airbyte_airflow_provider_advm",
            "airbyte_airflow_provider_advm.*",
        ]
    ),
)
