import re
import unittest
from datetime import timedelta
from aviatorsbot_e2e.util import MetarUtil
from config.config import TIMEOUTS
from tests.base import TelegramConversationInitializer


class WxTestCase(unittest.TestCase, TelegramConversationInitializer):
    def test_validWeatherResponse(self):
        with self.initConvo() as conv:
            conv.send_message("/wx LOWW")

            answer = conv.get_response(timeout=TIMEOUTS['wx'])

            self.assertIsNotNone(answer, "Response was None")

            metarIssuedAtMatch = re.search("^.*([0-9]{6})Z", answer.message)
            self.assertIsNotNone(metarIssuedAtMatch, "Returned METAR didn't contain an issuedAt date")
            metarIssuedAt = metarIssuedAtMatch.group(1)
            age = MetarUtil.metar_date_time_age(metarIssuedAt)

            print(metarIssuedAt)

            self.assertTrue(timedelta(minutes=-5) < age < timedelta(65))

            self.assertIn("LOWW", answer.message, "Response didn't contain the station name")
            self.assertIn("TAF LOWW", answer.message, "Response didn't contain the TAF for the station")


if __name__ == '__main__':
    unittest.main()
