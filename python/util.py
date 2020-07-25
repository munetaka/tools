from datetime import datetime, timedelta, timezone
import jpholiday


def is_weekend_or_holiday():
    jst_timezone = timezone(timedelta(hours=+9), 'JST')
    return jpholiday.is_holiday(datetime.now()) or 5 <= datetime.now().weekday()


if __name__ == '__main__':
    print(is_weekend_or_holiday())
