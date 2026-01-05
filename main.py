import os

try:
    from channels import CHANNELS
except ImportError:
    CHANNELS = {"SYSTEM ERROR: channels.py missing": ["", "System"]}

def generate_iptv_html():
    grid_html = ""
    sorted_channels = dict(sorted(CHANNELS.items()))
    
    for name, data in sorted_channels.items():
        url, cat = data[0], data[1]
        grid_html += f"""
        <div class="channel-card" onclick="playChannel('{url}', '{name}')">
            <div class="channel-cat">{cat}</div>
            <div class="channel-name">{name}</div>
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
        
        /* Fixed Player at Top */
        .player-container {{ 
            width: 100%; aspect-ratio: 16/9; background: #000; 
            position: relative; z-index: 1; /* Keeping video on base layer */
        }}
        .video-js {{ width: 100%; height: 100%; }}

        /* Elevating UI to prevent "Blackout" */
        .ui-overlay {{ 
            position: relative; z-index: 100; /* Higher priority than video */
            background: #000; padding-bottom: 50px;
        }}
        
        .header {{ padding: 20px; border-bottom: 1px solid #333; }}
        .logo {{ color: #3eaf7c; font-weight: bold; font-size: 22px; }}
        .grid {{ 
            display: grid; padding: 20px;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; 
        }}
        .channel-card {{ 
            background: #111; padding: 15px; border-radius: 8px; 
            cursor: pointer; border: 1px solid #222; 
        }}
        .channel-card:hover {{ border-color: #3eaf7c; background: #1a1a1a; }}
        .channel-cat {{ font-size: 10px; color: #3eaf7c; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="ui-overlay">
        <div class="header">
            <div class="logo">NZ-IPTV // PRO</div>
            <div id="status" style="font-size: 12px; color: #888; margin-top: 5px;">SELECT A CHANNEL</div>
        </div>
        <div class="grid">{grid_html}</div>
    </div>
    
    <div class="player-container">
        <video id="main-player" class="video-js vjs-default-skin" controls preload="auto" muted playsinline></video>
    </div>

    <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
    <script>
        var player = videojs('main-player');
        function playChannel(url, name) {{
            player.src({{ src: url, type: 'application/x-mpegURL' }});
            player.play();
            document.getElementById('status').innerText = "LIVE: " + name;
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}
    </script>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("🚀 Re-generated with UI Z-Index fixes!")

if __name__ == "__main__":
    generate_iptv_html()
