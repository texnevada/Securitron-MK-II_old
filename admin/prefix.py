#import discord py library
import discord
#Imports commands
from discord.ext import commands
#import permissions
from discord.ext.commands import has_permissions
import sqlite3

class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def prefix(self, ctx, arg:str):
        if ctx.author.guild_permissions.manage_channels:
            conn = sqlite3.connect("databases/ServerConfigs.db")
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM prefixes WHERE GuildID = ?", (ctx.guild.id, ))
            response = c.fetchone()
            oldprefix = []
            if response:
                oldprefix.append(response["Prefix"])
                isprefixold = True
                c.execute("DELETE FROM prefixes WHERE GuildID = ?", [ctx.guild.id])
            if not response:
                isoldprefix = False
            c.execute("INSERT INTO prefixes (GuildID,GuildName,Prefix) VALUES (?,?,?)", (ctx.guild.id, ctx.guild.name, arg,))
            conn.commit()
            conn.close()

            embed = discord.Embed(
                color = 0xe7e9d3
            )

            embed.set_footer(text="This was brought to you by Enclave Database automated reply system")
            #embed.set_image(url="")
            embed.set_thumbnail(url="https://static1.squarespace.com/static/5bf3d1670dbda3ebca76e890/t/5bf3d4911ae6cfcc40a70d62/1547021826210/?format=1500w")
            embed.set_author(name="Securitron MK II systems", icon_url=self.client.icon_url)
            if isprefixold == True:
                embed.add_field(name="Your server prefix has changed!", value="Your prefix is now changed\n**Old:** {}\n**New:** {}\nYou can also use \"@Securitron MK\" II for commands even if you forget your prefix".format(oldprefix[0], arg))
            elif isprefixold == False:
                embed.add_field(name="Your server prefix has changed!", value="Your prefix is now changed\n**New:** {}".format(arg) )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Strip secure.")

def setup(client):
    client.add_cog(prefix(client))