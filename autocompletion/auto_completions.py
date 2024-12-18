from typing import List, Union

import nextcord as discord

from database.database_requests import schools_list, class_list, group_list, SchoolNotFoundError


def schools_autocompletion(interaction: discord.Interaction, school_input: str) -> List[str]:
    schools: List[str] = schools_list(guild_id=interaction.guild_id)
    if not school_input:
        return schools

    get_schools_by_input: List[str] = [school for school in schools if school.lower().startswith(school_input.lower())]
    return get_schools_by_input


def classes_autocompletion(interaction: discord.Interaction, class_name: str) -> List[Union[str, None]]:
    try:
        if interaction.data['options'][0]['value']:
            if not class_name:
                return class_list(guild_id=interaction.guild_id,
                                  school_name=interaction.data['options'][0]['value'])
            get_class_by_input: List[str] = [name for name in class_list(
                guild_id=interaction.guild_id,
                school_name=interaction.data['options'][0]['value']) if name.lower().startswith(class_name.lower())]
            return get_class_by_input
        return []
    except (IndexError, SchoolNotFoundError):
        return []


def groups_autocompletion(interaction: discord.Interaction, group_name: str) -> List[Union[str, None]]:
    try:
        if interaction.data['options'][0]['value'] and interaction.data['options'][1]['value']:
            if not group_name:
                return group_list(guild_id=interaction.guild_id,
                                  school_name=interaction.data['options'][0]['value'],
                                  class_name=interaction.data['options'][1]['value'])
            get_group_by_input: List[str] = [name for name in group_list(
                guild_id=interaction.guild_id,
                school_name=interaction.data['options'][0]['value'],
                class_name=interaction.data['options'][1]['value']) if name.lower().startswith(group_name.lower())]
            return get_group_by_input
        return []
    except IndexError:
        return []
