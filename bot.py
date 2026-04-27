import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

load_dotenv()

class CoinBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            intents=intents
        )
        
        self.admin_role_id = int(os.getenv('ADMIN_ROLE_ID', '1485667541631242251'))
        self.coins_file = 'coins.json'
        self.load_coins()
    
    def load_coins(self):
        """Load coins data from JSON file"""
        try:
            with open(self.coins_file, 'r') as f:
                self.coins_data = json.load(f)
        except FileNotFoundError:
            self.coins_data = {}
            self.save_coins()
    
    def save_coins(self):
        """Save coins data to JSON file"""
        with open(self.coins_file, 'w') as f:
            json.dump(self.coins_data, f, indent=4)
    
    def get_user_coins(self, user_id):
        """Get coins for a user"""
        return self.coins_data.get(str(user_id), 0)
    
    def set_user_coins(self, user_id, amount):
        """Set coins for a user"""
        self.coins_data[str(user_id)] = amount
        self.save_coins()
    
    def add_user_coins(self, user_id, amount):
        """Add coins to a user"""
        current = self.get_user_coins(user_id)
        self.set_user_coins(user_id, current + amount)
    
    def remove_user_coins(self, user_id, amount):
        """Remove coins from a user"""
        current = self.get_user_coins(user_id)
        new_amount = max(0, current - amount)
        self.set_user_coins(user_id, new_amount)
        return new_amount
    
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is in {len(self.guilds)} servers')
        
        # Sync commands
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

bot = CoinBot()

@bot.tree.command(name="add_coins", description="Add coins to a user (Admin only)")
@discord.app_commands.describe(
    user="The user to add coins to",
    amount="The amount of coins to add"
)
async def add_coins(interaction: discord.Interaction, user: discord.Member, amount: int):
    # Check if user has admin role
    admin_role = interaction.guild.get_role(bot.admin_role_id)
    if admin_role not in interaction.user.roles:
        await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
        return
    
    if amount <= 0:
        await interaction.response.send_message("Amount must be a positive number!", ephemeral=True)
        return
    
    bot.add_user_coins(user.id, amount)
    new_balance = bot.get_user_coins(user.id)
    
    embed = discord.Embed(
        title="Coins Added",
        description=f"Added {amount} coins to {user.mention}",
        color=discord.Color.green()
    )
    embed.add_field(name="New Balance", value=f"{new_balance} coins", inline=False)
    embed.set_footer(text=f"Added by {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="remove_coins", description="Remove coins from a user (Admin only)")
@discord.app_commands.describe(
    user="The user to remove coins from",
    amount="The amount of coins to remove"
)
async def remove_coins(interaction: discord.Interaction, user: discord.Member, amount: int):
    # Check if user has admin role
    admin_role = interaction.guild.get_role(bot.admin_role_id)
    if admin_role not in interaction.user.roles:
        await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
        return
    
    if amount <= 0:
        await interaction.response.send_message("Amount must be a positive number!", ephemeral=True)
        return
    
    current_balance = bot.get_user_coins(user.id)
    if current_balance < amount:
        await interaction.response.send_message(f"{user.mention} only has {current_balance} coins!", ephemeral=True)
        return
    
    bot.remove_user_coins(user.id, amount)
    new_balance = bot.get_user_coins(user.id)
    
    embed = discord.Embed(
        title="Coins Removed",
        description=f"Removed {amount} coins from {user.mention}",
        color=discord.Color.red()
    )
    embed.add_field(name="New Balance", value=f"{new_balance} coins", inline=False)
    embed.set_footer(text=f"Removed by {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="set_coins", description="Set a user's coins to a specific amount (Admin only)")
@discord.app_commands.describe(
    user="The user to set coins for",
    coins="The amount of coins to set"
)
async def set_coins(interaction: discord.Interaction, user: discord.Member, coins: int):
    # Check if user has admin role
    admin_role = interaction.guild.get_role(bot.admin_role_id)
    if admin_role not in interaction.user.roles:
        await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
        return
    
    if coins < 0:
        await interaction.response.send_message("Coins cannot be negative!", ephemeral=True)
        return
    
    old_balance = bot.get_user_coins(user.id)
    bot.set_user_coins(user.id, coins)
    
    embed = discord.Embed(
        title="Coins Set",
        description=f"Set {user.mention}'s coins to {coins}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Previous Balance", value=f"{old_balance} coins", inline=False)
    embed.add_field(name="New Balance", value=f"{coins} coins", inline=False)
    embed.set_footer(text=f"Set by {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="view_coins", description="View a user's coin balance")
@discord.app_commands.describe(
    user="The user to view coins for"
)
async def view_coins(interaction: discord.Interaction, user: discord.Member):
    balance = bot.get_user_coins(user.id)
    
    embed = discord.Embed(
        title="Coin Balance",
        description=f"{user.mention}'s coin balance",
        color=discord.Color.gold()
    )
    embed.add_field(name="Balance", value=f"{balance} coins", inline=False)
    embed.set_thumbnail(url=user.display_avatar.url if user.display_avatar else None)
    
    await interaction.response.send_message(embed=embed)

# Run the bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: DISCORD_TOKEN not found in environment variables!")
        print("Please create a .env file with your bot token")
    else:
        bot.run(token)
