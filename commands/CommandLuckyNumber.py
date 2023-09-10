import nextcord as discord
from nextcord.ext import commands
from vulcanrequests.get_lucky_number import get_lucky_number
from database.database_requests import get_user_data, get_vulcan_data
from utils import messages
import json


class LuckyNumber(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Szczęśliwy numerek dzisiaj",
                           name="szczesliwy-numer",
                           dm_permission=False,
                           force_global=True)
    async def lucky_number(self, interaction: discord.Interaction):
        user_data = get_user_data(user_id=interaction.user.id, guild_id=interaction.guild_id)
        if not user_data:
            await interaction.response.send_message(messages['need_to_register'])
            return
        message = await interaction.send(messages['connecting_to_vulcan'])
        vulcan = get_vulcan_data(guild_id=interaction.guild_id, school_name=user_data[0][1], class_name=user_data[0][0],
                                 group_name=user_data[0][2])
        keystore: dict = json.loads(vulcan[0][0].replace("'", '"'))
        account: dict = json.loads(vulcan[0][1].replace("'", '"'))

        lucky_number = await get_lucky_number(keystore=keystore, account=account)
        if lucky_number == 0:
            await message.edit(messages['no_education'])
            return
        msg = messages['lucky_number'].replace('{school}', user_data[0][1])
        msg = msg.replace('{number}', lucky_number)
        await message.edit(msg)


def setup(client):
    client.add_cog(LuckyNumber(client))