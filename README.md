# downloads_org.py

A simple Python script that automatically sorts files in your Downloads folder into subfolders by type.

## What it does

When run, the script scans your Downloads folder and moves each file into a subfolder based on its extension:

| Folder | Extensions |
|---|---|
| Images | `.jpg` `.jpeg` `.png` `.gif` `.webp` |
| Videos | `.mp4` `.mkv` `.mov` |
| Audio | `.mp3` `.wav` `.flac` |
| Documents | `.pdf` `.docx` `.txt` |
| Archives | `.zip` `.tar` `.gz` |
| Programs | `.py` `.html` `.js` `.css` |
| Other | anything not listed above |

Files with unrecognised extensions are moved to `Other/` and logged to the console. Any errors are appended to `~/work/download_organizer/error.txt`.

---

## Changing the target folder

Open `downloads_org.py` and find this line near the top:

```python
folder = os.path.expanduser("~/Downloads")
```

Replace `~/Downloads` with any path you want, for example:

```python
folder = "/mnt/data/my_files"
```

`os.path.expanduser()` handles `~` automatically, so you can keep using that shorthand for paths inside your home directory.

---

## Changing the error log location

Find this line in the `except` block:

```python
with open("/home/willow/work/download_organizer/error.txt", "a", encoding="utf-8") as f:
```

Replace the path with wherever you want errors logged. Make sure the directory exists first, or add an `os.makedirs(..., exist_ok=True)` call before it.

---

## Adding new file types

Find the `categories` dictionary and add a new entry:

```python
".ext": "FolderName",
```

For example, to send `.iso` files to Archives:

```python
".iso": "Archives",
```

---

## Running it manually

Make the script executable (one-time):

```bash
chmod +x /usr/local/bin/downloads_org.py
```

Then run it:

```bash
downloads_org.py
# or
python3 /usr/local/bin/downloads_org.py
```

---

## Running automatically with systemd (every 30 minutes)

You need two files: a **service** (what to run) and a **timer** (when to run it).

### 1. Create the service file

```bash
sudoedit /etc/systemd/system/downloads-org.service
```

Paste this in:

```ini
[Unit]
Description=Downloads folder organiser

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /usr/local/bin/downloads_org.py
```

- `Type=oneshot` means systemd runs the script once and considers it done — correct for a script that isn't a long-running daemon.
- Adjust the path in `ExecStart` if your script lives somewhere else.

### 2. Create the timer file

```bash
sudoedit /etc/systemd/system/downloads-org.timer
```

Paste this in:

```ini
[Unit]
Description=Run downloads organiser every 30 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=30min

[Install]
WantedBy=timers.target
```

- `OnBootSec=5min` — runs the script 5 minutes after boot, so it doesn't fire immediately on startup.
- `OnUnitActiveSec=30min` — then repeats every 30 minutes after each run.

### 3. Enable and start the timer

Reload systemd so it sees the new files:

```bash
sudo systemctl daemon-reload
```

Enable the timer to start on boot:

```bash
sudo systemctl enable downloads-org.timer
```

Start it now without rebooting:

```bash
sudo systemctl start downloads-org.timer
```

### 4. Verify it's working

Check the timer is active and see when it will next fire:

```bash
systemctl status downloads-org.timer
```

List all active timers:

```bash
systemctl list-timers --all | grep downloads
```

Check the service ran without errors:

```bash
journalctl -u downloads-org.service -n 20
```

### Stopping or disabling

Stop the timer for the current session:

```bash
sudo systemctl stop downloads-org.timer
```

Disable it from running on boot:

```bash
sudo systemctl disable downloads-org.timer
```
