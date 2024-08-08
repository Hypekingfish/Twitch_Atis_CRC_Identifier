import requests
import asyncio
from twitchio.ext import commands
from datetime import datetime, timedelta, timezone
from config import TWITCH_TOKEN, TWITCH_CLIENT_ID, CHANNEL_NAME, CID, ATIS_URLS
import logging
import aiohttp
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Log to file
logging.basicConfig(filename='ATIS-BOT.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_and_print(message, level=''):
    """
    Logs and prints a message simultaneously.
    :param message: The message to log and print.
    :param level: The logging level ('info', 'warning', 'error', etc.).
    """
    if level == 'info':
        logging.info(message)
        message = f"{Fore.GREEN}{message}{Style.RESET_ALL}"  # Colorize info messages in green
    elif level == 'warning':
        logging.warning(message)
        message = f"{Fore.YELLOW}{message}{Style.RESET_ALL}"  # Colorize warning messages in yellow
    elif level == 'error':
        logging.error(message)
        message = f"{Fore.RED}{message}{Style.RESET_ALL}"  # Colorize error messages in red
    elif level == 'debug':
        logging.debug(message)
    else:
        logging.log(logging.INFO, message)
    
    print(message)

async def get_current_position_from_vatsim(cid):
    """
    Fetches the current position of a controller from VATSIM data.
    :param cid: The CID of the controller.
    :return: The ICAO code corresponding to the controller's position, or None if not found.
    """
    vatsim_url = 'https://data.vatsim.net/v3/vatsim-data.json'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(vatsim_url) as response:
                if response.status == 200:
                    data = await response.json()
                    log_and_print(f"Fetched VATSIM data", level='debug')
                    controllers = data.get('controllers', [])
                    if isinstance(controllers, list):
                        for controller in controllers:
                            controller_cid = str(controller.get('cid', ''))
                            controller_callsign = str(controller.get('callsign', ''))
                            if not controller_callsign:
                                continue
                            if controller_cid == cid or controller_callsign.startswith(f"{cid}_OBS"):
                                log_and_print(f"Found matching controller: {controller}", level='info')
                                callsign = controller.get('callsign', '')
                                if '_OBS' in callsign:
                                    icao_code = callsign.split('_')[0]
                                    log_and_print(f"Extracted ICAO code: {icao_code}", level='info')
                                    return icao_code
                                return callsign.split('_')[0] if '_' in callsign else callsign
                    else:
                        log_and_print(f"Expected 'controllers' to be a list, got {type(controllers)}", level='error')
                else:
                    log_and_print(f"Failed to fetch VATSIM data. Status code: {response.status}", level='error')
    except Exception as e:
        log_and_print(f"Error fetching VATSIM data: {e}", level='error')
    return None

async def get_controller_info(cid):
    """
    Fetches the information of a controller from VATSIM data.
    :param cid: The CID of the controller.
    :return: A dictionary with the controller's information, or None if not found.
    """
    vatsim_url = 'https://data.vatsim.net/v3/vatsim-data.json'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(vatsim_url) as response:
                if response.status == 200:
                    data = await response.json()
                    log_and_print(f"Fetched VATSIM data", level='debug')
                    controllers = data.get('controllers', [])
                    if isinstance(controllers, list):
                        for controller in controllers:
                            if str(controller.get('cid', '')) == cid:
                                log_and_print(f"Found controller info: {controller}", level='info')
                                return controller
                    else:
                        log_and_print(f"Expected 'controllers' to be a list, got {type(controllers)}", level='error')
                else:
                    log_and_print(f"Failed to fetch VATSIM data. Status code: {response.status}", level='error')
    except Exception as e:
        log_and_print(f"Error fetching VATSIM data: {e}", level='error')
    return None

class ATISBot(commands.Bot):

    def __init__(self):
        super().__init__(token=TWITCH_TOKEN, client_id=TWITCH_CLIENT_ID, prefix='!', initial_channels=[CHANNEL_NAME])
        self.last_update_times = {icao: datetime.min.replace(tzinfo=timezone.utc) for icao in ATIS_URLS.keys()}
        self.last_atis_infos = {icao: None for icao in ATIS_URLS.keys()}

    async def startup(self):
        await self.update_atis()  # Start updating ATIS data

    async def event_ready(self):
        log_and_print(f'Logged in as | {self.nick}', level='info')
        log_and_print(f'User id is | {self.user_id}', level='info')
        await self.startup()  # Start the startup process

    async def event_error(self, error, *args, **kwargs):
        log_and_print(f'An error occurred: {error}', level='error')

    async def fetch_atis(self, icao):
        atis_url = ATIS_URLS.get(icao)
        if atis_url:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(atis_url) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            log_and_print(f"Failed to fetch ATIS data for {icao}. Status code: {response.status}", level='error')
            except Exception as e:
                log_and_print(f"Error fetching ATIS data for {icao}: {e}", level='error')
        return None

    async def update_atis(self):
        while True:
            try:
                current_icao = await get_current_position_from_vatsim(CID)
                log_and_print(f"Current position: {current_icao}", level='info')
                if current_icao in ATIS_URLS:
                    atis_data = await self.fetch_atis(current_icao)
                    if atis_data:
                        log_and_print(f"Fetched ATIS data for {current_icao}: {atis_data}", level='debug')
                        atis_info = atis_data.get('combined')
                        if atis_info and atis_info != self.last_atis_infos[current_icao]:
                            current_time_utc = datetime.now(timezone.utc)
                            self.last_update_times[current_icao] = current_time_utc
                            self.last_atis_infos[current_icao] = atis_info
                            await self.post_atis_to_chat(atis_info, current_icao)
                        else:
                            log_and_print("No new ATIS information found in response or ATIS data is the same as last fetched.", level='warning')
                    else:
                        log_and_print("No ATIS information found in response.", level='warning')
                else:
                    log_and_print(f"Current position {current_icao} is not in the list of ATIS URLs.", level='warning')

                # Wait for the next update check (every 60 seconds)
                await asyncio.sleep(300)

            except Exception as e:
                log_and_print(f"Error in update_atis: {e}", level='error')
                await asyncio.sleep(60)  # Wait 1 minute before retrying in case of an error

    async def post_atis_to_chat(self, atis_info, icao):
        try:
            channel = self.get_channel(CHANNEL_NAME)
            if channel:
                message = f"ATIS for {icao}: {atis_info}"
                if len(message) > 500:  # Twitch message length limit
                    log_and_print(f"ATIS message too long, truncating: {len(message)}", level='warning')
                    message = message[:497] + "..."  # Truncate and add ellipsis
                await channel.send(message)
                log_and_print(f"Posted ATIS update for {icao} to chat.", level='info')
            else:
                log_and_print(f"Failed to get channel: {CHANNEL_NAME}", level='error')
        except Exception as e:
            log_and_print(f"Error in post_atis_to_chat for {icao}: {e}", level='error')

    async def event_message(self, message):
        if message.author and message.author.name.lower() != self.nick.lower():
            await self.handle_commands(message)

bot = ATISBot()
try:
    log_and_print("Starting bot...")
    bot.run()
except Exception as e:
    log_and_print(f"Error: {e}", level='error')
    with open("error_log.txt", "w") as log_file:
        log_file.write(str(e))
