import os
from datetime import datetime

try:
    from channels import CHANNELS
except ImportError:
    CHANNELS = {"Error": ["", "Missing channels.py"]}

def generate_iptv_html():
    grid_html = ""
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>NZ-IPTV PRO</title>
    <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
        body {{ margin: 0; background: #000; color: #fff; font-family: 'Inter', sans-serif; }}
        .player-container {{ width: 100%; aspect-ratio: 16 / 9; background: #111; position: sticky; top: 0; z-index: 1000; }}
        .video-js {{ width: 100%; height: 100%; }}
        .header {{ padding: 20px 30px; display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-weight: 800; color: #3eaf7c; }}
        .search-container {{ padding: 0 20px 20px; }}
        #channelSearch {{ width: 100%; padding: 12px; border-radius: 8px; background: #1a1a1a; border: 1px solid #333; color: #fff; outline: none; }}
        #channelSearch:focus {{ border-color: #3eaf7c; }}
        .container {{ padding: 0 20px 50px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; }}
        .channel-card {{ background: #1a1a1a; border-radius: 12px; padding: 20px; cursor: pointer; border: 1px solid #222; transition: 0.2s; position: relative; }}
        .channel-card:hover {{ border-color: #3eaf7c; transform: translateY(-3px); background: #222; }}
        .channel-cat {{ font-size: 10px; color: #3eaf7c; text-transform: uppercase; margin-bottom: 5px; font-weight: 800; }}
        .channel-name {{ font-weight: 800; }}
        .play-overlay {{ position: absolute; bottom: 10px; right: 10px; font-size: 10px; opacity: 0.3; }}
        @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr 1fr; }} }}
    </style>
</head>
<body>
    <div class="player-container">
        <video id="main-player" class="video-js vjs-big-play-centered" controls preload="auto" muted playsinline data-setup='{{}}'>
            <p class="vjs-no-js">To view this video please enable JavaScript</p>
        </video>
    </div>

    <div class="header">
        <div class="logo">NZ-IPTV // PRO</div>
        <div id="now-playing" style="font-family: 'JetBrains Mono'; font-size: 11px; color: #888;">READY TO STREAM</div>
    </div>

    <div class="search-container">
        <input type="text" id="channelSearch" placeholder="Search channels..." onkeyup="filterChannels()">
    </div>

    <main class="container">
        <div class="grid" id="channelGrid">{grid_html}</div>
    </main>

    <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
    <script>
        var player = videojs('main-player');

        function playChannel(url, name) {{
            // Force reset the player state
            player.pause();
            player.src({{ src: url, type: 'application/x-mpegURL' }});
            player.load();
            
            // Unmute shortly after play starts (most browsers allow this after user interaction)
            var playPromise = player.play();
            if (playPromise !== undefined) {{
                playPromise.then(_ => {{
                    document.getElementById('now-playing').innerText = "LIVE: " + name.toUpperCase();
                    player.muted(false); // Try to unmute once playing
                }}).catch(error => {{
                    console.log("Autoplay blocked. User interaction required.");
                    document.getElementById('now-playing').innerText = "TAP PLAY BUTTON TO START";
                }});
            }}
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function filterChannels() {{
            let input = document.getElementById('channelSearch').value.toLowerCase();
            let cards = document.getElementsByClassName('channel-card');
            for (let card of cards) {{
                let name = card.getAttribute('data-name');
                let cat = card.getAttribute('data-cat');
                card.style.display = (name.includes(input) || cat.includes(input)) ? "" : "none";
            }}
        }}

        // Error handling for CORS/Expired links
        player.on('error', function() {{
            let error = player.error();
            console.log("Video Error:", error);
            alert("This stream is blocked or expired. Link rotation required.");
        }});
    </script>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("🚀 Dashboard regenerated with playback stability fixes!")

if __name__ == "__main__":
    generate_iptv_html()
