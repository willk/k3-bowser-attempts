# How many attempts did it take?
This is a quick an dirty attempt to determine how many attempts it took [BarbarousKing](https://twitch.com/barbarousking) to beat Kiazo 3 Bowser in the 27+ hours he attempted the boss. This includes all his attempts and not just his no hit attempts.

## Replication
Download the 160p vods to save disk space.
```shell
yt-dlp -f 'best[height<=160]' -o '%(upload_date)s-%(id)s.%(ext)s' -a videos.txt
```

Use `ffmpeg` to extract the parts of the video we care about. We'll remove the audio, and extra portions of the screen we don't care about. We only care about the portion of the frame that contains Bowser's portrait on the wall.
```shell
mkdir output

```

Combine the videos together.
```shell

```

Run `main.py`
```shell
python3 main.py output.mp4 port.png
```

## Future work
1. Use a more accurate measure to determine an attempt.
2. Determine how much time each attempt took.