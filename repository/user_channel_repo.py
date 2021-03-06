from datetime import datetime

from repository.base_repository import BaseRepository
from repository.database import session
from repository.database.user_channels import UserChannel


class UserChannelRepository(BaseRepository):
    # unknown - pending - verified - kicked - banned

    def increment(
        self, channel_id: int, user_id: int, guild_id: int, last_message_id: int, last_message_at: datetime,
    ):
        """Increment user_channel count, 
        if it doesn't exist, create it"""
        user_channel = (
            session.query(UserChannel)
            .filter_by(channel_id=channel_id, user_id=user_id, guild_id=guild_id)
            .one_or_none()
        )
        if not user_channel:
            session.add(
                UserChannel(
                    channel_id=channel_id,
                    user_id=user_id,
                    last_message_at=last_message_at,
                    last_message_id=last_message_id,
                    guild_id=guild_id,
                )
            )

        else:
            user_channel.count = user_channel.count + 1
            if user_channel.last_message_at < last_message_at:
                user_channel.last_message_at = last_message_at
                user_channel.last_message_id = last_message_id

        session.commit()

    def decrement(
        self, channel_id: int, user_id: int, guild_id: int, last_message_id: int, last_message_at: datetime,
    ):
        """Decrement user_channel count."""
        user_channel = (
            session.query(UserChannel)
            .filter_by(channel_id=channel_id, user_id=user_id, guild_id=guild_id)
            .one_or_none()
        )
        if not user_channel:
            session.add(
                UserChannel(
                    channel_id=channel_id,
                    user_id=user_id,
                    count=0,
                    last_message_at=last_message_at,
                    last_message_id=last_message_id,
                    guild_id=guild_id,
                )
            )

        else:
            user_channel.count = user_channel.count - 1
            if user_channel.last_message_at < last_message_at:
                user_channel.last_message_at = last_message_at
                user_channel.last_message_id = last_message_id

        session.commit()

    def get_user_channels(self):
        """Retrieves the whole table"""
        channels = session.query(UserChannel).all()
        result = []

        if channels is not None:
            for ch in channels:
                result.append(ch.__dict__)
        else:
            result = None
        return result

    def get_channel(self, channel_id: int):
        """Retrieves table, filtered by channel id"""
        channels = session.query(UserChannel).filter_by(channel_id=channel_id).all()
        result = []

        if channels is not None:
            for ch in channels:
                result.append(ch.__dict__)
        else:
            result = None
        return result

    def get_user(self, user_id: int):
        """Retrieves table, filtered by user id"""
        users = session.query(UserChannel).filter_by(user_id=user_id).all()
        result = []

        if users is not None:
            for usr in users:
                result.append(usr.__dict__)

        else:
            result = None
        return result
