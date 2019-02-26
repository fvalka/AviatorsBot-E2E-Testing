import unittest

from aviatorsbot_e2e.util import MetarUtil
from config.config import TIMEOUTS
from tests.base import TelegramConversationInitializer


class WxTestCase(unittest.TestCase, TelegramConversationInitializer):
    def test_validWeatherResponse(self):
        with self.initConvo() as conv:
            conv.send_message("/wx LOWW")

            answer = conv.get_response(timeout=TIMEOUTS['wx'])

            self.assertIsNotNone(answer, "Response was None")
            age = MetarUtil.age(answer.message)
            self.assertTrue(-5 < age < 65)
            self.assertIn("LOWW", answer.message, "Response didn't contain the station name")
            self.assertIn("TAF", answer.message, "Response didn't contain the TAF for the station")


class SubscriptionTestCase(unittest.TestCase, TelegramConversationInitializer):
    def test_subscriptionControlMechanism(self):
        with self.initConvo() as conv:
            # Create new subscription
            conv.send_message("/add EDDM")
            self.assertIn("Subscription is active", conv.get_response().message)

            # Check that it was stored
            conv.send_message("/ls")
            self.assertIn("EDDM", conv.get_response().message)

            # Delete it
            conv.send_message("/rm EDDM")
            self.assertIn("Unsubscribed successfully", conv.get_response().message)

            # Check that it is not there anymore
            conv.send_message("/ls")
            self.assertNotIn("EDDM", conv.get_response().message)

    def test_subscriptionSendsNewMessages(self):
        with self.initConvo() as conv:
            # Delete everything
            conv.send_message("/rm *")
            self.assertIn("Unsubscribed successfully", conv.get_response().message)

            # Subscribe
            conv.send_message("/add EDDF")
            self.assertIn("Subscription is active", conv.get_response().message)

            # Wait for the first weather update, can take a long time!
            first_weather = conv.get_response(timeout=TIMEOUTS["subscription"]).message
            self.assertIn("EDDF", first_weather)
            self.assertIn("TAF", first_weather)

            first_weather_time = MetarUtil.time_convert(first_weather)
            first_weather_age = MetarUtil.age(first_weather)
            self.assertTrue(-5 < first_weather_age < 65, "METAR was too old age: %s " % first_weather_age)

            # Wait for the second weather update, takes even longer than waiting for the first update
            second_weather = conv.get_response(timeout=TIMEOUTS["subscription"]).message
            self.assertIn("EDDF", second_weather)
            second_weather_time = MetarUtil.time_convert(second_weather)
            second_weather_age = MetarUtil.age(second_weather)
            self.assertTrue(-5 < second_weather_age < 65, "METAR was too old age: %s" % second_weather_age)

            # Actually the bot also implements the case that the METAR change without the issue at date changing
            # and still sends an update in that situation, which should not happen according to METAR publishing
            # standards. In this test case we assume that EDDF doesn't mess this up, otherwise the test will fail.
            # Reason to check this is to ensure that the new METAR is sent and not the old one
            self.assertTrue(second_weather_time > first_weather_time, "New METAR wasn't newer than the first "
                                                                      "subscription update. ")


if __name__ == '__main__':
    unittest.main()
