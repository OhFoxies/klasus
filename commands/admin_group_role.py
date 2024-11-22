from typing import List

import nextcord as discord
from nextcord.ext import commands

from autocompletion.auto_completions import schools_autocompletion, classes_autocompletion, groups_autocompletion
from database.database_requests import (set_role,
                                        class_list,
                                        group_list,
                                        is_group_registered,
                                        SchoolNotFoundError,
                                        get_role
                                        )
from utils import messages


class SetRole(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['role_command'],
                           description=messages['role_command_desc'],
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def change_channel(self, interaction: discord.Interaction,
                             school_name: str = discord.SlashOption(name=messages['value_school_name'],
                                                                    description=messages['school_value_desc'],
                                                                    required=True),
                             class_name: str = discord.SlashOption(name=messages['value_class_name'],
                                                                   description=messages['class_value_desc'],
                                                                   required=True),
                             group_name: str = discord.SlashOption(name=messages['value_group_name'],
                                                                   description=messages['group_value_desc'],
                                                                   required=True),
                             role: discord.Role = discord.SlashOption(
                                 name=messages['role_value'],
                                 description=messages['role_value_desc'],
                                 required=False)
                             ):

        try:
            classes: List[str] = class_list(guild_id=interaction.guild_id, school_name=school_name)
            if class_name in classes:
                groups_list: List[str] = group_list(guild_id=interaction.guild_id, school_name=school_name,
                                                    class_name=class_name)
                if group_name in groups_list:
                    if is_group_registered(guild_id=interaction.guild_id,
                                           school_name=school_name,
                                           class_name=class_name,
                                           group_name=group_name):
                        if not role:
                            role_id: int = get_role(guild_id=interaction.guild_id,
                                                    school_name=school_name,
                                                    class_name=class_name,
                                                    group_name=group_name)
                            if role_id != 0:

                                msg: str = (messages['current_role'].replace('{group}', group_name)
                                            .replace('{role}', f"<@&{role_id}>"))
                            else:
                                msg: str = messages['no_role'].replace('{group}', group_name)
                            await interaction.response.send_message(msg, ephemeral=True)
                            return

                        set_role(guild_id=interaction.guild_id,
                                 school_name=school_name,
                                 class_name=class_name,
                                 group_name=group_name,
                                 role_id=role.id)

                        msg: str = messages['set_role'].replace("{role}", role.mention).replace("{group}", group_name)
                        await interaction.response.send_message(msg, ephemeral=True)
                        return
                    await interaction.response.send_message(messages['group_not_connected'], ephemeral=True)
                    return

                await interaction.response.send_message(messages['group_not_found'.replace('{name}', group_name)],
                                                        ephemeral=True)
                return
            await interaction.response.send_message(
                f"{messages['class_not_found']}".replace("{name}", class_name), ephemeral=True)
            return
        except SchoolNotFoundError:
            await interaction.response.send_message(
                f"{messages['school_not_found']}".replace("{name}", school_name), ephemeral=True)
            return

    @change_channel.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))

    @change_channel.on_autocomplete("class_name")
    async def get_classes(self, interaction: discord.Interaction, class_name: str):
        await interaction.response.send_autocomplete(classes_autocompletion(interaction=interaction,
                                                                            class_name=class_name))

    @change_channel.on_autocomplete("group_name")
    async def get_groups(self, interaction: discord.Interaction, group_name: str):
        await interaction.response.send_autocomplete(
            groups_autocompletion(interaction=interaction, group_name=group_name))


def setup(client):
    client.add_cog(SetRole(client))