from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER

class AashikaMusicBot(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="AashikaMusicBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )
        self.logger_channel_id = None  # Will store the resolved channel ID

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # Resolve the channel username to ID
        try:
            if config.LOGGER_ID.startswith("@"):
                chat = await self.get_chat(config.LOGGER_ID)
                self.logger_channel_id = chat.id
            else:
                self.logger_channel_id = int(config.LOGGER_ID)
        except errors.ChatIdInvalid as e:
            LOGGER(__name__).error(
                "Invalid chat ID or username provided. Error: %s", e
            )
            exit()
        except Exception as e:
            LOGGER(__name__).error(
                "Failed to resolve channel ID from username. Error: %s", e
            )
            exit()

        # Notify the start of the bot
        try:
            await self.send_message(
                chat_id=self.logger_channel_id,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
                parse_mode=ParseMode.HTML
            )
        except errors.ChannelInvalid as e:
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel. Error: %s", e
            )
            exit()
        except errors.PeerIdInvalid as e:
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel due to an invalid peer ID. Error: %s", e
            )
            exit()
        except Exception as e:
            LOGGER(__name__).error(
                "An unexpected error occurred while accessing the log group/channel. Error: %s", e
            )
            exit()

        # Check bot's status in the channel
        try:
            a = await self.get_chat_member(self.logger_channel_id, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Please promote your bot as an admin in your log group/channel."
                )
                exit()
        except errors.ChatAdminRequired as e:
            LOGGER(__name__).error(
                "Bot is not an administrator in the log group/channel. Error: %s", e
            )
            exit()
        except errors.ChannelInvalid as e:
            LOGGER(__name__).error(
                "The channel ID or username is invalid. Please check the LOGGER_ID. Error: %s", e
            )
            exit()
        except Exception as e:
            LOGGER(__name__).error(
                "An unexpected error occurred while checking bot's status in the log group/channel. Error: %s", e
            )
            exit()

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
