import re
import requests

PLAYLIST_URL = "https://iptv-org.github.io/iptv/countries/bd.m3u"

# Je channel gulo alada korben ebong tader file-er naam
CHANNELS = {
    "Somoy TV": "somoy-tv.m3u8",
    "Jamuna TV": "jamuna-tv.m3u8",
    "Zee Bangla HD": "zee-bangla-hd.m3u8",
    "Zee Bangla": "zee-bangla.m3u8"
}

def fetch_and_save_channels():
    response = requests.get(PLAYLIST_URL)
    if response.status_code != 200:
        print("Playlist download korte porini!")
        return

    playlist_data = response.text.splitlines()

    for channel_name, filename in CHANNELS.items():
        found = False
        i = 0
        while i < len(playlist_data):
            line = playlist_data[i].strip()
            if line.startswith("#EXTINF") and channel_name.lower() in line.lower():
                if i + 1 < len(playlist_data):
                    stream_url = playlist_data[i + 1].strip()
                    if stream_url and not stream_url.startswith("#"):
                        content = f"#EXTM3U\n{line}\n{stream_url}\n"
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(content)
                        print(f"Saved {channel_name} to {filename}")
                        found = True
                        break
            i += 1
        
        if not found:
            print(f"Channel not found: {channel_name}")

if __name__ == "__main__":
    fetch_and_save_channels()
