from aviatorsbot_e2e.client import TelegramE2EClient
from config.config import BOT_CONFIG, TIMEOUTS


class TelegramConversationInitializer:
    def initConvo(self):
        return TelegramE2EClient() \
            .client \
            .conversation(BOT_CONFIG["name"], timeout=TIMEOUTS["local"])
