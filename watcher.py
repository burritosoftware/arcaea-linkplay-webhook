# Import the journal module from systemd package
from systemd import journal
import select
from dotenv import load_dotenv
import os
from discord_webhook import DiscordWebhook, DiscordEmbed

load_dotenv()

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
                    linkPlayEmbed = DiscordEmbed(title="Link Play Room", description="New Link Play room created!", color="2ecc71")
                    linkPlayEmbed.add_embed_field(name=room_code, value=f"**Joined Players**\n👑 {player}")

                    webhook.add_embed(linkPlayEmbed)
                    webhook.execute()