# Import the journal module from systemd package
from systemd import journal
import select
from dotenv import load_dotenv
import os
import json
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

load_dotenv()


# Check if database.json exists
if not os.path.exists("database.json"):
    with open("database.json", "w") as f:
        json.dump({}, f)

# Create a journal reader object
j = journal.Reader()

# Match only the Linkplay service
j.add_match(_SYSTEMD_UNIT=f"{os.getenv('LINKPLAY_SERVICE')}.service")

# Set the log level to INFO
j.log_level(journal.LOG_INFO)

# Optionally, you can add some filters to match the unit or other fields
# For example, j.add_match(_SYSTEMD_UNIT="mydaemon.service")

# Seek to the end of the journal
j.seek_tail()

# Get the previous entry
j.get_previous()

# Create a poll object to monitor the journal events
p = select.poll()
p.register(j, j.get_events())

linkPlayBaseEmbed = DiscordEmbed(title="Link Play Room", color="2ecc71")
linkPlayBaseEmbed.set_footer(text="Room info won't update for closed rooms or left players.")

# Loop indefinitely
while True:
    # Wait for an event
    if p.poll():
        # Check if the journal has new entries
        if j.process() == journal.APPEND:
            # Get the next entry
            entry = j.get_next()
            if entry != {}:
                msg = entry['MESSAGE']
                if "Create room" in msg:
                    rc1 = msg.find("`") # find the index of the first backtick
                    rc2 = msg.find("`", rc1 + 1) # find the index of the second backtick
                    room_code = msg[rc1 + 1:rc2]

                    pl1 = msg.find("`", rc2 + 1) # find the index of the third backtick
                    pl2 = msg.find("`", pl1 + 1) # find the index of the fourth backtick
                    player = msg[pl1 + 1:pl2]

                    webhook = DiscordWebhook(url=os.getenv('DISCORD_WEBHOOK'))
                    linkPlayEmbed = linkPlayBaseEmbed
                    linkPlayEmbed.set_description(description="New Link Play room created!\nThis message will update once another player joins.")
                    info = f"🚪 `{room_code}`\n👥 **Players**\n>>> 👑 {player}"
                    linkPlayEmbed.add_embed_field(name="Room Info", value=info)
                    linkPlayEmbed.set_timestamp()

                    webhook.add_embed(linkPlayEmbed)
                    response = webhook.execute()

                    data = {}
                    with open("database.json", "r") as f:
                        data = json.load(f)

                    data[room_code] = {}
                    data[room_code]['id'] = response.json()['id']
                    data[room_code]['info'] = info
                    data[room_code]['creation'] = time.time()

                    with open("database.json", "w") as f:
                        json.dump(data, f)
                elif "joins room" in msg:
                    pl1 = msg.find("`") # find the index of the first backtick
                    pl2 = msg.find("`", pl1 + 1) # find the index of the second backtick
                    player = msg[pl1 + 1:pl2]

                    rc1 = msg.find("`", pl2 + 1) # find the index of the third backtick
                    rc2 = msg.find("`", rc1 + 1) # find the index of the fourth backtick
                    room_code = msg[rc1 + 1:rc2]

                    data = {}
                    with open("database.json", "r") as f:
                        data = json.load(f)

                    if room_code in data:
                        id = data[room_code]['id']
                        data[room_code]['info'] = data[room_code]['info'] + "\n👤 " + player
                        info = data[room_code]['info']
                        creation = data[room_code]['creation']
                        with open("database.json", "w") as f:
                            json.dump(data, f)
                        webhook = DiscordWebhook(url=os.getenv('DISCORD_WEBHOOK'), id=id)
                        linkPlayEmbed = linkPlayBaseEmbed
                        linkPlayEmbed.set_description(description=f"📥 Last join was <t:{str(int(time.time()))}:R>.")
                        linkPlayEmbed.add_embed_field(name="Room Info", value=info)
                        linkPlayEmbed.set_timestamp(timestamp=creation)
                        webhook.edit()