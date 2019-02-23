import unittest
from datetime import datetime, timedelta
from pytz import timezone

from aviatorsbot_e2e.util import MetarUtil


class SelfTestCase(unittest.TestCase):
    def test_selfTestMetarAgeSameDay(self):
        base_time = datetime(2019, 2, 2, 12, 25, 30, 9, tzinfo=timezone('UTC'))
        metar_time_string = "021210"

        result = MetarUtil.metar_date_time_age(metar_time_string, base_time)

        self.assertTrue(timedelta(minutes=15) <= result < timedelta(minutes=16))

    def test_selfTestOnDayOldMetar(self):
        base_time = datetime(2019, 2, 2, 12, 25, 30, 9, tzinfo=timezone('UTC'))
        metar_time_string = "011210"

        result = MetarUtil.metar_date_time_age(metar_time_string, base_time)

        self.assertTrue(timedelta(days=1, minutes=15) <= result < timedelta(days=1, minutes=16))

    def test_selfTestMetarFromPreviousMonth(self):
        base_time = datetime(2019, 2, 1, 12, 25, 30, 9, tzinfo=timezone('UTC'))
        metar_time_string = "311210"

        result = MetarUtil.metar_date_time_age(metar_time_string, base_time)

        self.assertTrue(timedelta(days=1, minutes=15) <= result < timedelta(days=1, minutes=16))


if __name__ == '__main__':
    unittest.main()
