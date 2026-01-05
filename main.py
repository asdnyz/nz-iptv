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
        
        /* FIX: Reduced Size Player */
        .player-container {{ 
            width: 100%; 
            max-width: 800px; /* Reduces size */
            margin: 0 auto;   /* Centers the window */
            aspect-ratio: 16 / 9; 
            background: #111; 
            position: sticky; 
            top: 0; 
            z-index: 1000; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        }}
        
        .video-js {{ width: 100%; height: 100%; }}

        /* UI Styling */
        .ui-section {{ 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
        }}
        .header {{ border-bottom: 1px solid #222; padding-bottom: 15px; margin-bottom: 20px; }}
        .logo {{ color: #3eaf7c; font-weight: bold; font-size: 1.5rem; }}
        
        .grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); 
            gap: 12px; 
        }}
        .channel-card {{ 
            background: #1a1a1a; padding: 15px; border-radius: 8px; 
            cursor: pointer; border: 1px solid #333; 
        }}
        .channel-card:hover {{ border-color: #3eaf7c; background: #222; }}
        .channel-cat {{ font-size: 9px; color: #3eaf7c; text-transform: uppercase; margin-bottom: 5px; }}
        .channel-name {{ font-size: 13px; font-weight: bold; }}

        @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr 1fr; }} }}
    </style>
</head>
<body>
    <div class="player-container">
        <video id="main-player" class="video-js vjs-default-skin" controls preload="auto" muted playsinline></video>
    </div>

    <div class="ui-section">
        <div class="header">
            <div class="logo">NZ-IPTV // PRO</div>
            <div id="status" style="font-size: 11px; color: #888; margin-top: 5px;">READY</div>
        </div>

        <div class="grid">{grid_html}</div>
    </div>

    <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
    <script>
        var player = videojs('main-player');

        function playChannel(url, name) {{
            if(!url) return;
            document.getElementById('status').innerText = "LOADING: " + name;
            
            player.src({{ src: url, type: 'application/x-mpegURL' }});
            
            player.play().then(() => {{
                document.getElementById('status').innerText = "PLAYING: " + name;
                player.muted(false); // Unmute once play starts
            }}).catch(err => {{
                document.getElementById('status').innerText = "TAP PLAY TO START";
            }});
            
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}
    </script>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("🚀 Dashboard re-sized and generated successfully!")

if __name__ == "__main__":
    generate_iptv_html()
