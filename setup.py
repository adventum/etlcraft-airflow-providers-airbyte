"""Setup.py for the airbyte-airflow-provider-advm package."""

from setuptools import find_namespace_packages, setup

version = '1.0.0'


def do_setup():
    """Perform the package airbyte-airflow-provider-advm setup."""
    setup(
        name='airbyte-airflow-provider-advm',
        version=version,
        install_requires=[
            'airbyte-cdk',
            'apache-airflow',
            'apache-airflow-providers-airbyte'
        ],
        packages=find_namespace_packages(
            include=[
                'airbyte_api',
                'airbyte_api.*',
                'airbyte_airflow_provider_advm',
                'airbyte_airflow_provider_advm.*'
            ]
        ),
    )


if __name__ == "__main__":
    do_setup()
