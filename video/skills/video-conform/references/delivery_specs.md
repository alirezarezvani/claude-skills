# Delivery specs: what conform.py targets and why

| Setting | Value | Source | Confidence |
|---|---|---|---|
| Broadcast loudness | -23.0 LUFS integrated, ±0.5 LU | EBU R 128 (2014), tech.ebu.ch/docs/r/r128-2014.pdf | 🟢 |
| True-peak ceiling | -1 dBTP | EBU R 128 (2014) | 🟢 |
| Streaming speech / mixed content | -18 LUFS | AES TD1008 (2021), summarized at productionadvice.co.uk/td1008/ | 🟢 |
| Streaming music | -16 LUFS | AES TD1008 (2021) | 🟢 |
| Loudness measurement | ITU-R BS.1770 / EBU Tech 3341 meter (ffmpeg `ebur128`, `loudnorm`) | ffmpeg-filters documentation, ffmpeg.org/ffmpeg-filters.html | 🟢 |
| Video codec | H.264, `yuv420p`, `+faststart` | FFmpeg H.264 encoding guide (trac.ffmpeg.org/wiki/Encode/H.264): yuv420p for player compatibility, faststart for progressive playback | 🟢 |
| Captions | SRT sidecar, max two lines of 42 characters | common subtitle practice (BBC subtitle guidelines use two-line blocks); 42 is a widely used line limit | 🟡 |

Platforms normalize loudness on playback and do not all publish their target.
Mastering to a published recommendation (AES TD1008 for streaming, EBU R 128
for broadcast) is safer than chasing an unofficial platform number.

`loudnorm` in single-pass mode is an approximation; the QC step measures the
result with `ebur128` and fails the export if it lands more than 1 LU off. If
it does, the usual cause is a VO with clipped peaks or long silences.

## Sources

- EBU R 128 (2014), Loudness normalisation and permitted maximum level of audio signals
- AES TD1008 (2021), Recommendations for Loudness of Internet Audio Streaming and On-Demand Distribution
- ITU-R BS.1770, Algorithms to measure audio programme loudness and true-peak audio level
- FFmpeg filters documentation: loudnorm, ebur128, subtitles
- FFmpeg wiki, Encode/H.264
- BBC R&D, "How fast should subtitles be?" (2015), for caption pacing
