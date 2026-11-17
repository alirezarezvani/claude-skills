## Trigger-rate gate

Base `9edcb8e9`, model `sonnet`, 2 runs per prompt per round, spent $2.40.

| Skill | New? | Verdict | Detail | Exam |
|---|---|---|---|---|
| `video/skills/video-animatic` | yes | **PASS** | fired 2/4 | drafted from the new description |
| `video/skills/video-beat-board` | yes | **BELOW_FLOOR** | fired 0/8, floor is 50% (pooled over 2 rounds) | drafted from the new description |
| `video/skills/video-conform` | yes | **PASS** | fired 4/4 | drafted from the new description |
| `video/skills/video-director` | yes | **PASS** | fired 4/4 | drafted from the new description |

**How to fix:** say what the skill is for in the user's words ("Use whenever the user ..." with 2-4 situations); for a false fire, narrow the description so it no longer claims the near-miss job. The exam prompts and transcripts are in the workflow artifact. Recipe: `scripts/evals/README.md`.

<details><summary>Drafted exam cases (review and add to <code>scripts/evals/cases/heldout_cases.json</code> in a later PR)</summary>

```json
{
 "video/skills/video-animatic": {
  "pos": [
   "can you make a little animated bar chart that grows year by year and render it as an mp4? just use code",
   "I have sales.csv with quarterly revenue for 2021-2024 (16 rows). Build a 20 second 1080p kinetic-type animation that counts up the totals, then render it frame-exact to MP4 and check the text stays readable and nothing flashes."
  ],
  "neg": "Write me a CSS keyframes animation that makes a button pulse when hovered on my React landing page."
 },
 "video/skills/video-beat-board": {
  "pos": [
   "my voice-over script is way too long for a 30 second reel, can you tell me what to trim?",
   "Here's my 60 second explainer script, 9 beats, about 190 words of narration plus on-screen titles. Turn it into a timed shot list and tell me how many words I have to cut so each beat has enough time."
  ],
  "neg": "Proofread my 500-word blog post intro and tighten the wording so it reads more punchy, no word limit in mind."
 },
 "video/skills/video-conform": {
  "pos": [
   "the video is done, can you mix the narration over the music and make the volume levels right before I upload?",
   "I have final_cut.mp4 (58 s), vo.wav and theme.mp3. Duck the music under the voice, normalize loudness to -14 LUFS for YouTube, burn in captions from subs.srt, and export an MP4 that plays on iPhone and fails if it's off-length."
  ],
  "neg": "Write an ffmpeg command to extract frames from a screen recording every 2 seconds and save them as PNG files."
 },
 "video/skills/video-director": {
  "pos": [
   "I want to make a short promo video for my app launch, where do we start?",
   "Turn this changelog for v3.2 (6 bullet points: dark mode, faster sync, new export, etc.) into a 30 second vertical teaser for Instagram Reels with a voice-over, and take it all the way to a finished MP4."
  ],
  "neg": "Give me tips on how to edit my wedding footage in DaVinci Resolve so the color grading looks warm and cinematic."
 }
}
```
</details>
