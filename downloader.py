import os
import sys
import requests as req
import shutil
import uuid


def _parse_player_url(url):
    parts = url.split("/")
    host = parts[2]
    v_type = parts[3]
    v_id = parts[4]
    v_hash = parts[5]
    quality = parts[6].replace("p", "")
    return host, v_type, v_id, v_hash, quality


def _get_video_url(player_url):
    host, v_type, v_id, v_hash, quality = _parse_player_url(player_url)
    v_json = req.post(f"https://{host}/get-vid", data={
        "type": v_type,
        "id": v_id,
        "hash": v_hash,
        "hash2": "OErmnYyYA4wHwOP"
    })
    raw_url = v_json.json()["links"][quality][0]["src"].replace(":hls:manifest.m3u8", "")
    return f"https:{raw_url}"


def download_video(player_url, filename=f"{os.getcwd()}/{uuid.uuid1()}.mp4"):
    url = _get_video_url(player_url)
    response = req.get(url, stream=True)
    with open(filename, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
        print(f"Saved to {out_file.name}")
    del response


if __name__ == '__main__':
    if len(sys.argv) == 2:
        download_video(sys.argv[1])
    elif len(sys.argv) == 3:
        download_video(sys.argv[1], sys.argv[2])
