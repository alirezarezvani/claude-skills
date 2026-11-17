## Trigger-rate gate

Base `9edcb8e9`, model `sonnet`, 2 runs per prompt per round, spent $2.40.

| Skill | New? | Verdict | Detail | Exam |
|---|---|---|---|---|
| `video/skills/video-animatic` | yes | **PASS** | fired 2/4 | drafted from the new description |
| `video/skills/video-beat-board` | yes | **PASS** | fired 2/4 | drafted from the new description |
| `video/skills/video-conform` | yes | **PASS** | fired 4/4 | drafted from the new description |
| `video/skills/video-director` | yes | **BELOW_FLOOR** | fired 2/8, floor is 50% (pooled over 2 rounds) | drafted from the new description |

**How to fix:** say what the skill is for in the user's words ("Use whenever the user ..." with 2-4 situations); for a false fire, narrow the description so it no longer claims the near-miss job. The exam prompts and transcripts are in the workflow artifact. Recipe: `scripts/evals/README.md`.

<details><summary>Drafted exam cases (review and add to <code>scripts/evals/cases/heldout_cases.json</code> in a later PR)</summary>

```json
{
 "video/skills/video-animatic": {
  "pos": [
   "can you make me a little animated bar chart from this sales data that renders to an mp4?",
   "I need a 12-second kinetic type piece in code: three lines of text (\"Ship faster\", \"Break less\", \"Sleep more\") sliding in on a 1920x1080 canvas at 30fps, with no flashing and good contrast, rendered frame-exact to MP4."
  ],
  "neg": "Write an ffmpeg command to trim the first 10 seconds off intro.mp4 and re-encode it as H.264 without changing the resolution."
 },
 "video/skills/video-beat-board": {
  "pos": [
   "my voice-over script is way too long for a 30 second spot, can you check it and tell me what to trim?",
   "I have a 60-second explainer script with 8 scenes and about 190 words of narration plus on-screen titles. Break it into a timed shot list and tell me whether it fits, and if not, how many words to cut."
  ],
  "neg": "Write a 60-second voice-over script for our new coffee subscription product, friendly tone, aimed at young professionals."
 },
 "video/skills/video-conform": {
  "pos": [
   "my video's audio is too quiet compared to the music, can you fix the mix and get it ready to upload?",
   "I've got final.mov, a voice-over WAV and a music track. Mix the voice over the music, normalize to -14 LUFS, burn in the captions from captions.srt, and export an MP4 that's exactly 45 seconds and plays on phones and browsers."
  ],
  "neg": "Transcribe this interview recording and clean up the transcript into readable paragraphs with speaker labels."
 },
 "video/skills/video-director": {
  "pos": [
   "I want a short teaser video for our app launch, can you make one?",
   "Here's our changelog for v3.2 (6 bullet points) and a brand color of #1A73E8. Turn it into a 30-second promo video, starting from a brief, with a timed plan and a final MP4 I can post on social."
  ],
  "neg": "Write a creative brief and campaign messaging for our product launch, including target audience, key messages and channels. No video needed yet."
 }
}
```
</details>
