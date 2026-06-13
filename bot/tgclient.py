import logging
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from tg.config import Config

# Logger setup
logger = logging.getLogger(__name__)

# Global Filter: သတ်မှတ်ထားတဲ့ Group ID မဟုတ်ရင် ဘာ Message မှ လက်မခံရန် တားဆီးခြင်း
@Client.on_message(~filters.chat(-1002439446144), group=-1)
async def restrict_all_chats(client, message):
    message.stop_propagation()

class TgClient(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            name,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=Config.WORKERS,
            plugins=dict(root="tg/plugins"),
            parse_mode=ParseMode.DEFAULT,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        logger.info(f"Bot started as @{me.username}")

    async def stop(self, *args):
        await super().stop()
        logger.info("Bot stopped.")
