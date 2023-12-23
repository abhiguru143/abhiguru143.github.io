import os
import requests
from flask import Flask, render_template

video_id = "6329538956112"
ACCOUNT_ID = os.environ.get("ACCOUNT_ID", "6206459123001")
BCOV_POLICY = os.environ.get("BCOV_POLICY", "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhY2NpZCI6IjY0MTU2MzY2MTEwMDEiLCJleHAiOjE3MDMzNTkxNTcsImlhdCI6MTcwMzI3Mjc1NywiY29uaWQiOiI2MzI0Njc3NTIyMTEyIiwibWF4aXAiOjF9.W9ryGCVpodejb8oDDdV2ck4Q0cnC3UqVML8pL4gurnvTEZSEBlXZHcB-IOu9XSiAqkwsLPmz_Jd6Y9yfN19cdMTGR7jx48PzF_sl_bejVTIrl012TMvoa9to6WrsY0QUREyA5w7BwYByJsfanzYfTNduR04IMmaFkURRZBfqOrfGma9THss6e36RFSP5KoldMWzpMFYcWM9b79BKJp8kpi5HDy8qRtTiOHSjzW2AvcLGlcg1qdXP4STU2xiJZNxD0yiz7FewRHWR6knf7QmPhTLQvdP8GJr1yNOlicV406TOwopGnI1Wa-ufkZoo1JRCyVWMp7ZKhfHMxCjoRym6dw")

bc_url = f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"
bc_hdr = {"BCOV-POLICY": BCOV_POLICY}

jw_url = "https://cdn.jwplayer.com/v2/media"

app = Flask(__name__)

@app.route("/<int(fixed_digits=13):video_id>")
def brightcove(video_id):
    video_response = requests.get(f"{bc_url}/{video_id}", headers=bc_hdr)

    if video_response.status_code != 200:
        return "<font color=red size=20>Wrong Video ID</font>"

    video = video_response.json()
    video_name = video["name"]

    video_source = video["sources"][3]
    video_url = video_source["src"]
    widevine_url = ""
    microsoft_url = ""
    if "key_systems" in video_source:
        widevine_url = video_source["key_systems"]["com.widevine.alpha"]["license_url"]
        microsoft_url = video_source["key_systems"]["com.microsoft.playready"]["license_url"]

    track_url = video["text_tracks"][1]["src"]
    return render_template(
        "template.html",
        type="brightcove",
        video_name=video_name,
        video_url=video_url,
        track_url=track_url,
        widevine_url=widevine_url,
        microsoft_url=microsoft_url,
    )
