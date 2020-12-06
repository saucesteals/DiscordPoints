import json
import discord
from datetime import datetime
import random

class Points:
    def __init__(self, client):
        self.client = client
        self.data = json.load(open('data/points_data.json'))
        if "guilds" not in self.data:
            self.data["guilds"] = {}
            self.dump_data()

    def dump_data(self):
        json.dump(self.data, open("data/points_data.json", "w"))

    def add_user(self, member:discord.Member):
        self.data["guilds"][str(member.guild.id)]["members"][str(member.id)] = {'points':0, 'raffles_won':0}
        self.dump_data()
        
    def add_guild(self, guild:discord.Guild):
        self.data["guilds"][str(guild.id)] = {"members":{}, "raffles":0}
        self.dump_data()

    def __check_db__(self, member:discord.Member=None, guild:discord.Guild=None):
        if guild:
            if str(guild.id) not in self.data["guilds"]:
                self.add_guild(guild)
            return

        if str(member.guild.id) not in self.data["guilds"]:
            self.add_guild(member.guild)
        if str(member.id) not in self.data["guilds"][str(member.guild.id)]["members"]:
            self.add_user(member)

    def add_points(self, member:discord.Member, amount:int=1) -> int:
        self.__check_db__(member)
        self.data["guilds"][str(member.guild.id)]["members"][str(member.id)]["points"] += amount
        self.dump_data()

        return self.data["guilds"][str(member.guild.id)]["members"][str(member.id)]["points"]

    def remove_points(self, member:discord.Member, amount:int=1) -> int:
        self.__check_db__(member)
        self.data["guilds"][str(member.guild.id)]["members"][str(member.id)]["points"] -= amount
        self.dump_data()

        return self.data["guilds"][str(member.guild.id)]["members"][str(member.id)]["points"]

    def add_raffle(self, member:discord.Member, amount:int=1):
        self.__check_db__(member)
        self.data["guilds"][str(member.guild.id)]["members"][str(member.id)]["raffles_won"] += amount
        self.data["guilds"][str(member.guild.id)]["raffles"] += amount

    def get_members(self, guild:discord.guild) -> dict:
        self.__check_db__(guild=guild)
        return self.data["guilds"][str(guild.id)]["members"]

    def member_embed(self, member:discord.Member) -> discord.Embed:
        self.__check_db__(member)
        member_data = self.data["guilds"][str(member.guild.id)]["members"][str(member.id)]
        embed = discord.Embed(color=self.client.color, title=str(member), timestamp=datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Points", value=member_data["points"])
        embed.add_field(name="Raffles Won", value=member_data["raffles_won"])
        embed.set_footer(icon_url=member.guild.icon_url_as(format="png"), text="Points System")
        return embed
    
    def get_leaderboard(self, guild:discord.Guild) -> discord.Embed:
        self.__check_db__(guild=guild)
        members = self.get_members(guild)
        members_points = {}
        for member in members:
            members_points[str(guild.get_member(int(member)))] = members[member]["points"]

        embed = discord.Embed(color=self.client.color, title=guild.name, timestamp=datetime.utcnow())
        embed.set_thumbnail(url=guild.icon_url_as(format="png"))
        embed.set_footer(icon_url=guild.icon_url_as(format="png"), text="Points System")

        for elem in sorted(members_points.items(), reverse=True,  key=lambda x: x[1]):
            embed.add_field(name=elem[0], value=f"Points: {elem[1]}", inline=False)
            if len(embed.fields) == 10:
                break

        return embed
            
    def random_raffle(self, guild:discord.Guild):
        self.__check_db__(guild=guild)
        members = self.get_members(guild)
        members_list = []
        for member in members:
            for _ in range(members[member]["points"]):
                members_list.append(member)
        
        if members_list:
            winner = guild.get_member(int(random.choice(members_list)))
            self.add_raffle(winner)
            return winner

        return None
        


    def reset_guild(self, guild:discord.Guild):
        self.add_guild(guild)