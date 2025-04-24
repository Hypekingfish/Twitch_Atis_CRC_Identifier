![Python version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![GitHub commit status](https://img.shields.io/github/checks-status/Hypekingfish/Twitch_Atis_CRC_Identifier/70f5efc60cf3d16d93c76cd3dd67dd7fee289dd9)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/Hypekingfish/Twitch_Atis_CRC_Identifier/total)
![GitHub License](https://img.shields.io/github/license/Hypekingfish/Twitch_Atis_CRC_Identifier)
![Version](https://img.shields.io/github/v/release/Hypekingfish/Twitch_Atis_CRC_Identifier)
![GitHub Stars](https://img.shields.io/github/stars/Hypekingfish/Twitch_Atis_CRC_Identifier)



# ATIS Twitch Bot

This is a Twitch bot that automatically fetches and posts ATIS (Automatic Terminal Information Service) data from VATSIM controllers to a specified Twitch channel. The bot will continuously update the ATIS information for the current controller and post it to the chat.

## Features

- Fetches VATSIM controller data based on a given controller ID (CID).
- Retrieves ATIS data from VATSIM for the controller's position (ICAO code).
- Posts ATIS data to a specified Twitch channel every 5 minutes (or as configured).
- Logs all bot activity and errors to a log file with rotating backups.
- Truncates long ATIS messages if they exceed 500 characters before posting to Twitch.

## Requirements

- Python 3.7+
- `aiohttp` library for asynchronous HTTP requests.
- `twitchio` library for interacting with the Twitch API.
- `colorama` library for colored console output.
- A Twitch developer account and valid API credentials.

## Installation

- Download the script from this repo

### Install Dependencies

Ensure you have the required dependencies installed using `pip`:

```bash
pip install -r requirements.txt
```

### Configure the Bot

A Blank `config.py` file is provide for you in the root directory and define the necessary variables:

```python
# config.py

TWITCH_TOKEN = 'your_twitch_token'
TWITCH_CLIENT_ID = 'your_twitch_client_id'
CHANNEL_NAME = 'your_channel_name'
CID = 'your_controller_id'
ATIS_URLS = {
    '[ICAO]': 'https://api.flybywiresim.com/atis/[ICAO]?source=vatsim',
    # Add more ICAO-to-URL mappings as necessary, Replace [ICAO] in both area with actual ICAO. Example('KSLE': 'https://api.flybywiresim.com/atis/KSLE?source=vatsim'), Repeat for each ICAO
}
```

- **TWITCH_TOKEN**: Your OAuth token for authenticating the bot.
- **TWITCH_CLIENT_ID**: Your Twitch client ID.
- **CHANNEL_NAME**: The Twitch channel where the bot will post ATIS updates.
- **CID**: The controller ID for the bot's VATSIM connection.
- **ATIS_URLS**: A dictionary of ICAO codes mapped to the URLs where the ATIS data can be fetched from.

### Run the Bot

Once the bot is configured, you can run it with:

```bash
python atis_bot.py
```

The bot will log in to Twitch, start fetching VATSIM controller data, and begin posting ATIS updates to the chat.

## Logging

The bot uses a rotating log file (`ATIS-BOT.log`) to store all log messages, including errors, updates, and debug information. The log file will rotate when it reaches 5 MB, and up to 3 backup files will be kept.

Log messages are color-coded in the terminal:
- **Green**: Info messages.
- **Yellow**: Warning messages.
- **Red**: Error messages.
- **Cyan**: Debug messages.

---

## Batch File

- Include in the download is a batch file designed to be a one click run instead of opening python everytime! Below is the code for the batch file.

```batch
@echo off
echo Starting ATIS Bot for CRC Identifier
python Twitch_ATIS_BOT_CRC_IDENTIFIER.py
echo ATIS Bot has stopped
pause
```

---


## Common Issues and Troubleshooting

### 1. `Error: "Failed to fetch VATSIM data"`
- **Solution**: Ensure your internet connection is stable and that VATSIM's data feed is up and running. Check the URL endpoint for validity.

### 2. `Error: "No ATIS data found for ICAO"`
- **Solution**: Verify that the ICAO codes in the `ATIS_URLS` dictionary are correct and that the ATIS data URLs are still valid.

### 3. Bot not posting to Twitch chat
- **Solution**: Double-check that the `CHANNEL_NAME` in `config.py` is correct, and ensure the bot has permission to post in the chat.

---

## Contact & Support

Got questions, feedback, or just want to talk about virtual ATC and Twitch bot development? I’d love to hear from you. Whether you're trying to get the bot running, thinking up new features, or ran into something unexpected, I'm here to help.

---

### Technical Support

Running into issues or errors? No worries — I'm just a message away. I can help with:

- Installation or setup guidance  
- Configuration troubleshooting  
- Twitch or VATSIM API integration  
- General Python or asynchronous programming questions related to this project

Don't let bugs or confusion get in the way of your stream. Reach out anytime.

---

### Feature Requests and Ideas

Have an idea that could improve the bot for the VATSIM or Twitch community?  
Want to add something that makes your stream experience more interactive?

I'm actively working on updates and would love to hear your suggestions.  
Even experimental or niche ideas are welcome — that's how innovation happens.

---

### Collaborations

If you're a streamer, developer, or part of a VATSIM event team looking for custom tools or integrations, let’s connect. I’m open to collaborations, custom versions of the bot, or helping you build unique stream utilities.

---

### How to Reach Me

**Discord (DMs open):** Fishnbuckjr02
**Discord Server** [Hype Squad Studio](https://discord.gg/AxeJ6ryn2x)
**Twitch:** [Hypekingfish](https://twitch.tv/Hypekingfish)  

---

### Support the Project

If you find this bot helpful and want to support future development:

- Star this repository  
- Report bugs or request features via GitHub Issues  
- Share it with other controllers or streamers  
- Contribute code via pull requests  
- Optional donation link or coffee support (coming soon)

---

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This bot uses the `twitchio` library to interact with Twitch's chat system.
- ATIS data is sourced from VATSIM's public data feed.

---

If you encounter any issues or need support, please create an issue or contact the repository owner.
