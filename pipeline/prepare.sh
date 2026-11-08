#!/usr/bin/env bash
# Prepare one inbox walkthrough for review.
# Usage: pipeline/prepare.sh inbox/<folder> <work_dir>
# Makes: work_dir/frames/fNNN.jpg (1 per second), work_dir/sheetNN.jpg contact sheets,
#        work_dir/walkthrough.mp4 (web-playable), work_dir/img/poster.jpg,
#        work_dir/transcript.txt (speech-to-text, 20-second chunks).
set -euo pipefail
SRC="$1"; W="$2"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
V="$SRC/$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['video_file'])" "$SRC/answers.json")"
mkdir -p "$W/frames" "$W/img"

echo "== duration"; ffprobe -v error -show_entries format=duration -of default=nw=1 "$V"
ffmpeg -v error -y -i "$V" -vf "fps=1,scale=360:640:force_original_aspect_ratio=decrease,pad=360:640:(ow-iw)/2:(oh-ih)/2" -q:v 3 "$W/frames/f%03d.jpg"
ffmpeg -v error -y -i "$V" -vf "scale=-2:960,fps=30" -c:v libx264 -preset veryfast -crf 26 -g 30 -keyint_min 30 -sc_threshold 0 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 96k "$W/walkthrough.mp4" \
  || ffmpeg -v error -y -i "$V" -vf "scale=-2:960,fps=30" -c:v libx264 -preset veryfast -crf 26 -g 30 -pix_fmt yuv420p -movflags +faststart -an "$W/walkthrough.mp4"
ffmpeg -v error -y -ss 0.5 -i "$W/walkthrough.mp4" -frames:v 1 -q:v 3 "$W/img/poster.jpg"

python3 -I - "$W" <<'EOF'
import sys, os, glob
from PIL import Image, ImageDraw
W = sys.argv[1]
fs = sorted(glob.glob(os.path.join(W, 'frames', 'f*.jpg')))
cols, rows, tw, th = 7, 3, 360, 640
per = cols * rows
for si in range(0, len(fs), per):
    sheet = Image.new('RGB', (cols * tw, rows * th), 'black')
    d = ImageDraw.Draw(sheet)
    for k, f in enumerate(fs[si:si + per]):
        x, y = (k % cols) * tw, (k // cols) * th
        sheet.paste(Image.open(f).convert('RGB'), (x, y))
        t = si + k
        d.rectangle([x, y, x + 56, y + 20], fill='black')
        d.text((x + 5, y + 4), f"{t // 60}:{t % 60:02d}", fill='yellow')
    sheet.save(os.path.join(W, f"sheet{si // per + 1:02d}.jpg"), quality=80)
print("frames:", len(fs), "sheets:", (len(fs) + per - 1) // per)
EOF

# Audio: skip if the video has no audio track
if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$V" | grep -q .; then
  ffmpeg -v error -y -i "$V" -vn -ac 1 -ar 16000 "$W/a16k.wav"
  ASR="${ASR_DIR:-/tmp/walkthru-asr}"
  mkdir -p "$ASR"
  python3 -c "import sherpa_onnx" 2>/dev/null || pip install --break-system-packages -q sherpa-onnx
  if [ ! -d "$ASR/sherpa-onnx-whisper-base.en" ]; then
    curl -sSL -o "$ASR/w.tar.bz2" https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.en.tar.bz2
    tar xjf "$ASR/w.tar.bz2" -C "$ASR"
  fi
  python3 -I - "$W" "$ASR/sherpa-onnx-whisper-base.en" <<'EOF'
import sys, os, glob, wave
import numpy as np, sherpa_onnx
W, md = sys.argv[1], sys.argv[2]
enc = (glob.glob(md + '/*encoder.int8.onnx') or glob.glob(md + '/*encoder.onnx'))[0]
dec = (glob.glob(md + '/*decoder.int8.onnx') or glob.glob(md + '/*decoder.onnx'))[0]
tok = glob.glob(md + '/*tokens.txt')[0]
r = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=enc, decoder=dec, tokens=tok, language='en', task='transcribe', num_threads=4)
w = wave.open(os.path.join(W, 'a16k.wav')); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
out = []
for s0 in range(0, len(x), sr * 20):
    st = r.create_stream(); st.accept_waveform(sr, x[s0:s0 + sr * 21]); r.decode_stream(st)
    t = s0 // sr
    out.append(f"[{t // 60}:{t % 60:02d}] {st.result.text.strip()}")
open(os.path.join(W, 'transcript.txt'), 'w').write("\n".join(out))
print("\n".join(out))
EOF
else
  echo "No audio track (likely recorded during a call)." | tee "$W/transcript.txt"
fi
ls "$W"
