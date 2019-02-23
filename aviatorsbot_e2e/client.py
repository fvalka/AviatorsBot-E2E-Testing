import os

from telethon import TelegramClient, sync


class TelegramE2EClient(object):
    """
    Singleton class for instantiating the Telegram client for all tests

    Connects to the telegram API based upon the already existing session, api id and api hash.

    The api id and api hash are configured using the environment variables: TELEGRAM_API_ID and TELEGRAM_API_HASH.
    Session data needs to be injected into the secrets folder in the file telegram.session
    """
    class __TelegramE2EClient:
        bot_under_test: str
        client: TelegramClient

        def __init__(self):
            api_id = os.environ["TELEGRAM_API_ID"]
            api_hash = os.environ["TELEGRAM_API_HASH"]
            self.client = TelegramClient('../secrets/telegram', api_id, api_hash)
            self.client.start()

    instance = None

    def __new__(cls):
        if not TelegramE2EClient.instance:
            TelegramE2EClient.instance = TelegramE2EClient.__TelegramE2EClient()
        return TelegramE2EClient.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
