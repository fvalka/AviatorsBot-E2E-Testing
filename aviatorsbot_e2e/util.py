from datetime import datetime, timedelta
from pytz import timezone


class MetarUtil:
    @staticmethod
    def metar_date_time_convert(metar_date_time: str, base_time=datetime.now(timezone('UTC'))) -> datetime:
        if len(metar_date_time) != 6:
            raise ValueError("Unexpected format for metar date and time, the length doesn't equal 6")

        # Example input: 120305Z
        day = int(metar_date_time[0:2])
        hour = int(metar_date_time[2:4])
        minute = int(metar_date_time[4:6])

        converted = base_time.replace(hour=hour, minute=minute, second=0, microsecond=0, tzinfo=timezone('UTC'))

        if day <= base_time.day:  # Conclusion day is in the same month
            converted = converted.replace(day=day)
        else:  # day needs to be in the previous month
            while day > converted.day:
                converted = converted - timedelta(days=1)

        return converted

    @staticmethod
    def metar_date_time_age(metar_date_time, base_time=datetime.now(timezone('UTC'))) -> timedelta:
        metar_date_time_parsed = MetarUtil.metar_date_time_convert(metar_date_time, base_time)

        return base_time - metar_date_time_parsed
