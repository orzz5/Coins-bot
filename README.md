# Discord Coin Bot

A Discord bot that manages coins for users with admin commands and a public view command.

## Features

- **/add_coins** - Add coins to a user (Admin only)
- **/remove_coins** - Remove coins from a user (Admin only) 
- **/set_coins** - Set a user's coins to a specific amount (Admin only)
- **/view_coins** - View any user's coin balance (Everyone can use)

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Enable the following intents:
   - Server Members Intent
   - Message Content Intent
5. Copy the bot token

### 3. Invite Bot to Server
1. In the Developer Portal, go to "OAuth2" → "URL Generator"
2. Select the following scopes:
   - `bot`
   - `applications.commands`
3. Select the following bot permissions:
   - Send Messages
   - Embed Links
   - Use External Emojis
   - Read Message History
4. Copy the generated URL and invite the bot to your server

### 4. Configure Environment
1. Copy `.env.example` to `.env`
2. Fill in your bot token:
```
DISCORD_TOKEN=your_actual_bot_token_here
ADMIN_ROLE_ID=
```

### 5. Run the Bot
```bash
python bot.py
```

## Commands

### Admin Commands (Requires role ID: ADMIN_ROLE_ID)

#### `/add_coins`
- **user**: The user to add coins to (@mention)
- **amount**: The amount of coins to add (positive number)

#### `/remove_coins`
- **user**: The user to remove coins from (@mention)
- **amount**: The amount of coins to remove (positive number)

#### `/set_coins`
- **user**: The user to set coins for (@mention)
- **coins**: The exact amount of coins the user should have (non-negative)

### Public Commands

#### `/view_coins`
- **user**: The user to view coins for (@mention)

## Data Storage

The bot stores coin data in a `coins.json` file in the same directory. This file will be automatically created when the bot first runs.

## Notes

- The admin role ID is set to `1485667541631242251` by default, but can be changed in the `.env` file
- Coin balances cannot go below 0
- All commands provide visual feedback with embedded messages
- The bot will automatically sync slash commands when it starts

## Troubleshooting

- **Commands not showing up**: Make sure the bot has the `applications.commands` scope and restart the bot
- **Permission errors**: Ensure the bot has the required intents enabled in the Developer Portal
- **Token errors**: Double-check your `.env` file contains the correct bot token
