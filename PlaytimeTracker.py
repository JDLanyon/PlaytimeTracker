# http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=440&key=6E38C23649700FB51916D8A9F29BD315&steamid=SOSFILMZ&format=json
# http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=6E38C23649700FB51916D8A9F29BD315&steamids=76561198123603534
import json
import urllib.request
import schedule
import time
import csv
from datetime import date

class MissingIDError(Exception):
    pass

def logPlaytime():
    # Test last date
    with open("PlaytimeData.csv", 'r') as f:
        reader = csv.reader(f, delimiter = ',')
        if list(reader)[-1][0] == str(date.today().strftime("%d/%m/%Y")):
            print(str(date.today().strftime("%d/%m/%Y")) + " is already logged.")
            return

    try:
        f = open("GameID.txt", 'r').read()
        targetID = int(f)
    except:
        raise MissingIDError

    playtime = None # total playtime

    # Get playtime for the target game id
    webURL = urllib.request.urlopen("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=6E38C23649700FB51916D8A9F29BD315&steamid=76561198123603534&format=json")
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    jsonObject = json.loads(data.decode(encoding))
    gameList = jsonObject["response"]["games"]
    for game in gameList:
        if game.get("appid") == targetID:
            playtime = game.get("playtime_forever")
            break
    if playtime is None:
        raise MissingIDError

    # append to csv
    with open("PlaytimeData.csv", 'a') as f:
        f.write(str(date.today().strftime("%d/%m/%Y")) + f",{playtime}\n") # write date and playtime
    print(f"logged game id: {targetID} for " + str(date.today().strftime("%d/%m/%Y")) + ".")


def main():
    logPlaytime()
    input()
    # uncomment for repeatition (and comment above)
    # schedule.every(1).days.do(logPlaytime)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(300)

    # TODO: delta time and shit and interpolation oh god wtf don't study math.


if __name__ == "__main__":
    main()