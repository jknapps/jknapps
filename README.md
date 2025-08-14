# Chronicles of Darkness Dice Bot

This repository contains a simple Discord bot that rolls Chronicles of Darkness dice pools using [random.org](https://random.org) for true randomness.

## Features
- 10-again by default, with optional 9-again or 8-again rules
- Results that trigger an additional roll are highlighted
- Outputs total successes (8-10)

## Usage
```bash
pip install -r requirements.txt
export DISCORD_TOKEN="your-discord-token"
export RANDOM_ORG_API_KEY="your-random-org-key"
python bot.py
```
Use the bot in Discord with:
```
!roll <pool> [again]
```
where `again` is `10`, `9`, or `8` (default `10`).

