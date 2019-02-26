import re
from datetime import datetime, timedelta
from pytz import timezone


class MetarUtil:

    @staticmethod
    def time_convert(full_metar, base_time=None):
        """
        Converts the issued at date-time in the METAR into a Python datetime object

        :param full_metar: Complete METAR string. Can include a TAF.
        :param base_time: Current time, uses now() if None is provided
        :return: METARs issued at time as a datetime object
        """
        if base_time is None:
            time = datetime.now(timezone('UTC'))
        else:
            time = base_time

        extracted = MetarUtil._extract(full_metar)
        return MetarUtil._convert_extracted_time(extracted, time)

    @staticmethod
    def age(full_metar, base_time=None) -> float:
        """
        Calculates the METARs age in minutes

        :param full_metar: Complete METAR string, can also include a TAF
        :param base_time: Different base time, uses now() if None is provided
        :return: Age of the METAR in minutes
        """
        if base_time is None:
            time = datetime.now(timezone('UTC'))
        else:
            time = base_time

        extracted = MetarUtil._extract(full_metar)
        return MetarUtil._age_from_extracted(extracted, time).total_seconds() / 60.0

    @staticmethod
    def _extract(full_metar) -> str:
        metar_issued_at_match = re.search("^.*([0-9]{6})Z", full_metar)

        if not metar_issued_at_match:
            raise ValueError("METAR didn't contain an issue date/time string")
        metar_issued_at = metar_issued_at_match.group(1)
        return metar_issued_at

    @staticmethod
    def _convert_extracted_time(metar_date_time: str, base_time) -> datetime:
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
    def _age_from_extracted(metar_date_time, base_time) -> timedelta:
        metar_date_time_parsed = MetarUtil._convert_extracted_time(metar_date_time, base_time)

        return base_time - metar_date_time_parsed
