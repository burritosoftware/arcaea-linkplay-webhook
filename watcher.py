# Import the journal module from systemd package
from systemd import journal
import select

# Create a journal reader object
j = journal.Reader()

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
            # Print the timestamp and the message to the console
            print(str(entry["__REALTIME_TIMESTAMP"]) + " " + entry["MESSAGE"])
