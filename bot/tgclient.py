from config import Config

from pyrogram import Client, filters

from .logger import LOGGER
from .settings import bot_set

# Global Filter: .env ထဲက ID နဲ့ မကိုက်ညီရင် ဘာ Message မှ လက်မခံရန် လမ်းခုလတ်က တားဆီးခြင်း
@Client.on_message(group=-1)
async def restrict_all_chats(client, message):
    if hasattr(Config, "ALLOWED_CHAT") and Config.ALLOWED_CHAT != 0:
        if message.chat.id != Config.ALLOWED_CHAT:
            message.stop_propagation()

plugins = dict(
    root="bot/modules"
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "Project-Siesta",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.TG_BOT_TOKEN,
            plugins=plugins,
            workdir=Config.WORK_DIR,
            workers=100
        )

    async def start(self):
        await super().start()
        await bot_set.login_qobuz()
        await bot_set.login_deezer()
        await bot_set.login_tidal()
        LOGGER.info("BOT : Started Successfully")

    async def stop(self, *args):
        await super().stop()
        for client in bot_set.clients:
            await client.session.close()
        LOGGER.info('BOT : Exited Successfully ! Bye..........')

aio = Bot()
