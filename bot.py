import asyncio
import os

from discord.ext import commands
import discord
import json

import dotenv
dotenv.load_dotenv()

intents = discord.Intents.none()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Ready!")

    # await bot.tree.sync()

@bot.tree.command(name="create", description="チケットパネルを作成します。")
@discord.app_commands.default_permissions(manage_channels=True, manage_guild=True)
async def ticket_panel_create(interaction: discord.Interaction, embeds_json: str, button_label: str, button_emoji: str, post_channel: discord.TextChannel):
    await interaction.response.defer(ephemeral=True)

    embeds = []
    for embed in json.loads(embeds_json):
        embeds.append(discord.Embed.from_dict(embed))
    await interaction.channel.send(embeds=embeds, view=discord.ui.View(timeout=None).add_item(discord.ui.Button(label=button_label, emoji=button_emoji, custom_id=f"post_{post_channel.id}")))

    await interaction.followup.send(content="✅️ 作成しました。")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    try:
        if interaction.data["component_type"] == 2:
            try:
                custom_id = interaction.data["custom_id"]
            except:
                return

            if custom_id.startswith("post_"):
                await interaction.response.defer(ephemeral=True)
                channel_id = custom_id.split("_")[1]
                channel = interaction.guild.get_channel(int(channel_id))
                await channel.send(f"$new {interaction.user.id} Ticket support")

                def check(channel: discord.abc.GuildChannel):
                    return channel.guild.id == interaction.guild_id and channel.name.startswith("ticket-") and channel.permissions_for(interaction.user)

                try:
                    ticket_channel = await bot.wait_for("guild_channel_create", check=check, timeout=10)
                except asyncio.TimeoutError:
                    await interaction.followup.send(embed=discord.Embed(title="❌️チケットが作成できませんでした", description="すでにチケットを開いている\n可能性があります。", color=discord.Color.red()), ephemeral=True)
                    return

                await interaction.followup.send(embed=discord.Embed(title="✅️チケットを作成しました！", description=f"<#{ticket_channel.id}>", color=discord.Color.green()).add_field(name="💡間違えてチケットを作りましたか？", value=f"間違えてチケットを作成した場合は、\n<#{ticket_channel.id}> で、閉じるボタンを押してください。"), ephemeral=True)
    except Exception as e:
        print(e)

bot.run(os.environ.get('DISCORD_TOKEN'))