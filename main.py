import os

# --- SAFE IMPORT ---
try:
    from channels import CHANNELS
except ImportError:
    # If file is missing, create a fake one so the UI doesn't crash
    CHANNELS = {"ERROR: channels.py not found": ["", "System"]}

def generate_iptv_html():
    grid_html = ""
    # Only build grid if channels exist
    if CHANNELS:
        sorted_channels = dict(sorted(CHANNELS.items()))
        for name, data in sorted_channels.items():
            url, cat = data[0], data[1]
            grid_html += f"""
            <div class="channel-card" data-name="{name.lower()}" data-cat="{cat.lower()}" onclick="playChannel('{url}', '{name}')">
                <div class="channel-cat">{cat}</div>
                <div class="channel-name">{name}</div>
                <div class="play-overlay">▶ PLAY</div>
            </div>"""

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NZ-IPTV PRO</title>
    <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
    <style>
        body {{ margin: 0; background: #000; color: #fff; font-family: sans-serif; }}
        .player-container {{ width: 100%; aspect-ratio: 16/9; background: #111; position: sticky; top: 0; z-index: 100; }}
        .video-js {{ width: 100%; height: 100%; }}
        .header {{ padding: 20px; border-bottom: 1px solid #222; }}
        .logo {{ color: #3eaf7c; font-weight: bold; font-size: 20px; }}
        .container {{ padding: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; }}
        .channel-card {{ background: #1a1a1a; padding: 15px; border-radius: 8px; cursor: pointer; border: 1px solid #333; }}
        .channel-card:hover {{ border-color: #3eaf7c; }}
        .channel-cat {{ font-size: 10px; color: #3eaf7c; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="player-container">
        <video id="main-player" class="video-js vjs-default-skin" controls preload="auto" muted playsinline></video>
    </div>

    <div class="header">
        <div class="logo">NZ-IPTV // PRO</div>
        <div id="status" style="font-size: 12px; color: #888; margin-top: 5px;">READY</div>
    </div>

    <div class="container">
        <div class="grid">{grid_html}</div>
    </div>

    <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
    <script>
        // Initialize player safely
        var player = videojs('main-player');

        function playChannel(url, name) {{
            if(!url) return alert("Broken Link");
            
            document.getElementById('status').innerText = "LOADING: " + name;
            player.src({{ src: url, type: 'application/x-mpegURL' }});
            
            player.play().then(() => {{
                document.getElementById('status').innerText = "PLAYING: " + name;
            }}).catch(err => {{
                document.getElementById('status').innerText = "TAP PLAY TO START";
            }});
        }}
    </script>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("🚀 Fixed! Check index.html now.")

if __name__ == "__main__":
    generate_iptv_html()
