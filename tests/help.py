import unittest
from telethon.tl.custom import Message
from tests.base import TelegramConversationInitializer


class HelpTestCase(unittest.TestCase, TelegramConversationInitializer):
    def assertHelpMessage(self, message: Message):
        self.assertIsNotNone(message)
        self.assertIn("/help", message.message)
        self.assertIn("/start", message.message)
        self.assertIn("Subscriptions", message.message)

    def test_validHelpCommand_gives_validResponse(self):
        with self.initConvo() as conv:
            conv.send_message("/help")

            answer = conv.get_response()

            self.assertHelpMessage(answer)

    def test_randomCommandLeadsToHelpMessage(self):
        with self.initConvo() as conv:
            conv.send_message("/ajsd8xjdnd434la")

            answer = conv.get_response()

            self.assertHelpMessage(answer)

    def test_helpAcceptsRandomArgs(self):
        with self.initConvo() as conv:
            conv.send_message("/help notA Valid ARgum Ent")

            answer = conv.get_response()

            self.assertHelpMessage(answer)


if __name__ == '__main__':
    unittest.main()
