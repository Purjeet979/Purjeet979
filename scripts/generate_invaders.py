import os
import json
import urllib.request
from datetime import datetime, timedelta

USERNAME = os.environ["GITHUB_REPOSITORY_OWNER"]
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""

data = json.dumps({
    "query": QUERY,
    "variables": {"login": USERNAME}
}).encode()

request = urllib.request.Request(
    "https://api.github.com/graphql",
    data=data,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Contribution-Invaders"
    }
)

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read())

calendar = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]

days = []

for week in calendar["weeks"]:
    for day in week["contributionDays"]:
        days.append({
            "date": day["date"],
            "count": day["contributionCount"]
        })

days = days[-364:]

# Contribution intensity
max_count = max([d["count"] for d in days] or [1])

def intensity(count):
    if count == 0:
        return 0
    if count <= max_count * 0.25:
        return 1
    if count <= max_count * 0.5:
        return 2
    if count <= max_count * 0.75:
        return 3
    return 4


# --------------------------------------------------
# SVG
# --------------------------------------------------

WIDTH = 900
HEIGHT = 330

svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

<style>
.title {{
    font-family: monospace;
    font-weight: bold;
    font-size: 22px;
    fill: #f0f6fc;
}}

.text {{
    font-family: monospace;
    font-size: 13px;
    fill: #8b949e;
}}

.enemy {{
    animation: float 2s ease-in-out infinite;
}}

.alien-2 {{ animation-delay: .2s; }}
.alien-3 {{ animation-delay: .4s; }}
.alien-4 {{ animation-delay: .6s; }}

@keyframes float {{
    0%,100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(7px); }}
}}

@keyframes laser {{
    0% {{ transform: translateY(0); opacity: 1; }}
    100% {{ transform: translateY(-90px); opacity: 0; }}
}}

.laser {{
    animation: laser 1.5s linear infinite;
}}

@keyframes pulse {{
    0%,100% {{ opacity: .35; }}
    50% {{ opacity: 1; }}
}}

.alien {{
    animation: pulse 1.8s ease-in-out infinite;
}}
</style>

</defs>

<!-- Background -->
<rect width="900" height="330" rx="16"
fill="#0d1117"
stroke="#30363d"/>

<!-- Header -->
<text x="30" y="38" class="title">
👾 CONTRIBUTION INVADERS
</text>

<text x="30" y="61" class="text">
{calendar["totalContributions"]} contributions • defending the GitHub galaxy
</text>

<!-- Stars -->
<g fill="#30363d">
<circle cx="80" cy="95" r="1.5"/>
<circle cx="170" cy="130" r="1"/>
<circle cx="280" cy="92" r="1.5"/>
<circle cx="390" cy="120" r="1"/>
<circle cx="510" cy="88" r="1.5"/>
<circle cx="640" cy="125" r="1"/>
<circle cx="760" cy="92" r="1.5"/>
<circle cx="840" cy="145" r="1"/>
</g>

<!-- INVADERS -->

<!-- Alien 1 -->
<g transform="translate(170 90)">
  <g class="enemy alien alien-1">
    <rect x="10" y="0" width="30" height="8" rx="2" fill="#58a6ff"/>
    <rect x="4" y="8" width="42" height="18" rx="3" fill="#58a6ff"/>
    <rect x="10" y="26" width="8" height="8" fill="#58a6ff"/>
    <rect x="32" y="26" width="8" height="8" fill="#58a6ff"/>
    <rect x="12" y="13" width="6" height="6" fill="#0d1117"/>
    <rect x="32" y="13" width="6" height="6" fill="#0d1117"/>
  </g>
</g>

<!-- Alien 2 -->
<g transform="translate(330 90)">
  <g class="enemy alien alien-2">
    <rect x="10" y="0" width="30" height="8" rx="2" fill="#7ee787"/>
    <rect x="4" y="8" width="42" height="18" rx="3" fill="#7ee787"/>
    <rect x="10" y="26" width="8" height="8" fill="#7ee787"/>
    <rect x="32" y="26" width="8" height="8" fill="#7ee787"/>
    <rect x="12" y="13" width="6" height="6" fill="#0d1117"/>
    <rect x="32" y="13" width="6" height="6" fill="#0d1117"/>
  </g>
</g>

<!-- Alien 3 -->
<g transform="translate(490 90)">
  <g class="enemy alien alien-3">
    <rect x="10" y="0" width="30" height="8" rx="2" fill="#d2a8ff"/>
    <rect x="4" y="8" width="42" height="18" rx="3" fill="#d2a8ff"/>
    <rect x="10" y="26" width="8" height="8" fill="#d2a8ff"/>
    <rect x="32" y="26" width="8" height="8" fill="#d2a8ff"/>
    <rect x="12" y="13" width="6" height="6" fill="#0d1117"/>
    <rect x="32" y="13" width="6" height="6" fill="#0d1117"/>
  </g>
</g>

<!-- Alien 4 -->
<g transform="translate(650 90)">
  <g class="enemy alien alien-4">
    <rect x="10" y="0" width="30" height="8" rx="2" fill="#ffa657"/>
    <rect x="4" y="8" width="42" height="18" rx="3" fill="#ffa657"/>
    <rect x="10" y="26" width="8" height="8" fill="#ffa657"/>
    <rect x="32" y="26" width="8" height="8" fill="#ffa657"/>
    <rect x="12" y="13" width="6" height="6" fill="#0d1117"/>
    <rect x="32" y="13" width="6" height="6" fill="#0d1117"/>
  </g>
</g>

<!-- Lasers -->
<g class="laser">
<rect x="444" y="140" width="4" height="55" rx="2"
fill="#f85149"/>
<rect x="444" y="140" width="4" height="55" rx="2"
fill="#ff7b72"/>
</g>

<!-- Contribution field -->
<text x="30" y="180" class="text">
CONTRIBUTION FIELD
</text>

"""

# Contribution grid
start_x = 30
start_y = 195

cell = 10
gap = 3

for i, day in enumerate(days):
    x = start_x + (i % 52) * (cell + gap)
    y = start_y + (i // 52) * (cell + gap)

    level = intensity(day["count"])

    fills = {
        0: "#161b22",
        1: "#0e4429",
        2: "#006d32",
        3: "#26a641",
        4: "#39d353"
    }

    svg += f"""
    <rect
        x="{x}"
        y="{y}"
        width="{cell}"
        height="{cell}"
        rx="2"
        fill="{fills[level]}">
        <title>{day["date"]}: {day["count"]} contributions</title>
    </rect>
    """

# Player
svg += """

<!-- Player -->
<g transform="translate(415 285)">

<path d="
M 0 25
L 8 8
L 18 8
L 25 0
L 32 8
L 42 8
L 50 25
Z"
fill="#58a6ff"/>

<rect x="20" y="13" width="10" height="6"
fill="#0d1117"/>

</g>

<text x="480" y="304" class="text">
↑ COMMIT TO SHOOT
</text>

<!-- Footer -->
<text x="30" y="318" class="text">
0
</text>

<text x="820" y="318" class="text">
365 DAYS
</text>

</svg>
"""

os.makedirs("assets", exist_ok=True)

with open("assets/contribution-invaders.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Contribution Invaders generated successfully!")
