
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
    'ICAO1': 'https://url-to-atis-data-for-ICAO1',
    'ICAO2': 'https://url-to-atis-data-for-ICAO2',
    # Add more ICAO-to-URL mappings as necessary
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
