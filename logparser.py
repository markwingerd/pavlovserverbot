import asyncio
import re


LOG_FILE = '/home/steam/pavlovserver/Pavlov/Saved/Logs/Pavlov.log'
# LOG_FILE = 'test.txt'

RE_USER_LOGIN = '^\[(.{23})\]\[...]PavlovLog: TicketValidation succeed for: (\d+) (.+)'
RE_USER_LOGOUT = '^\[(.{23})\]\[...]PavlovLog: Ending auth session for: (\d+) (.+)'


current_players = [
    # (name, steam_id, login_time),
]


async def log_parser(wait_time=5):
    with open(LOG_FILE, 'r') as f:
        while True:
            lines = f.readlines()
            print('{} lines read'.format(len(lines)))
            print(lines)
            for line in lines:
                parse(line)

            print(current_players)
            await asyncio.sleep(wait_time)


def parse(line):
    m = re.search(RE_USER_LOGIN, line)
    if m:
        current_players.append((m.group(3), m.group(2), m.group(1)))

    m = re.search(RE_USER_LOGOUT, line)
    if m:
        for i, player in enumerate(current_players):
            print(player[0], m.group(3))
            if player[0] == m.group(3):
                del current_players[i]


if __name__ == '__main__':
    asyncio.run(log_parser())
