import unittest
from datetime import datetime, timedelta
from pytz import timezone

from aviatorsbot_e2e.util import MetarUtil


class MetarUtilTestCase(unittest.TestCase):

    def test_selfTestMetarAgeSameDay(self):
        base_time = datetime(2019, 2, 2, 12, 25, 30, 9, tzinfo=timezone('UTC'))
        metar_time_string = "021210"

        result = MetarUtil._age_from_extracted(metar_time_string, base_time)

        self.assertTrue(timedelta(minutes=15) <= result < timedelta(minutes=16))

    def test_selfTestOnDayOldMetar(self):
        base_time = datetime(2019, 2, 2, 12, 25, 30, 9, tzinfo=timezone('UTC'))
        metar_time_string = "011210"

        result = MetarUtil._age_from_extracted(metar_time_string, base_time)

        self.assertTrue(timedelta(days=1, minutes=15) <= result < timedelta(days=1, minutes=16))

    def test_selfTestMetarFromPreviousMonth(self):
        base_time = datetime(2019, 2, 1, 12, 25, 30, 9, tzinfo=timezone('UTC'))
        metar_time_string = "311210"

        result = MetarUtil._age_from_extracted(metar_time_string, base_time)

        self.assertTrue(timedelta(days=1, minutes=15) <= result < timedelta(days=1, minutes=16))

    def test_selfTestMetarUtilExtraction(self):
        msg = "EDDM ✅ 231150Z 08014KT CAVOK 03/M09 Q1039 NOSIG\n" \
              "TAF EDDM 231100Z 2312/2418 07012KT CAVOK TEMPO 2312/2314 08015G25KT BECMG 2314/2316 07007KT"

        result = MetarUtil._extract(msg)

        self.assertEquals(result, "231150", "Extracted string didn't match actual issue date/time")

if __name__ == '__main__':
    unittest.main()
