from datetime import datetime, timedelta


def today_date(input_date_format: str = '%Y-%m-%d') -> str:
    return datetime.now().strftime(input_date_format)


def n_days_ago_date(last_days_count: int, input_date_format: str = '%Y-%m-%d'):
    return (datetime.now() - timedelta(days=last_days_count-1)
            ).strftime(input_date_format)
