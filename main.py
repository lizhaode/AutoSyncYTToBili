import json
import shlex
import subprocess
from datetime import datetime

import feedparser


def check_yt_update(channel_id: str) -> list[str]:
    download_video_urls = []
    with open('last_date.txt') as f:
        last_update_date = f.read()
    fp = feedparser.parse(f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}')
    for entry in fp.entries:
        if datetime.fromisoformat(entry.published) > datetime.fromisoformat(last_update_date):
            download_video_urls += (entry.link,)
    # with open('last_date.txt', 'w') as f:
    #     f.write(fp.entries[0].published)
    return download_video_urls


if __name__ == '__main__':
    for video_url in check_yt_update('UCT1YrR_CLpwosODYagzhm7Q'):
        video_info = json.loads(subprocess.check_output(shlex.split(f'you-get --json {video_url}')))
        best_video_itag = sorted(
            filter(lambda x: x.get('container') == 'webm', video_info.get('streams').values()),
            key=lambda x: x.get('size') if x.get('size') else 0,
            reverse=True,
        )[0].get('itag')
        subprocess.call(shlex.split(f'you-get --itag={best_video_itag} {video_url}'))
