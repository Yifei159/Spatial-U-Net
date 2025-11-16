import os
from flask import Flask, send_from_directory, render_template_string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

SNR_INFO = {
    "Example_01": "-20 dB",
    "Example_02": "-25 dB",
    "Example_03": "-30 dB",
}

AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}

NAME_MAP = {
    "noisy_input": "Input",
    "enhanced_output": "Enhanced Output of Spatial-U-Net",
    "speech_only": "Clean Target",
}


def build_examples():
    examples = []

    for example_name, snr in SNR_INFO.items():
        dir_path = os.path.join(BASE_DIR, example_name)
        if not os.path.isdir(dir_path):
            continue

        audio_files = []

        for filename in sorted(os.listdir(dir_path)):
            ext = os.path.splitext(filename)[1].lower()
            if ext not in AUDIO_EXTENSIONS:
                continue

            stem = os.path.splitext(filename)[0]
            display_label = NAME_MAP.get(stem, filename)

            rel_path = os.path.join(example_name, filename).replace(os.sep, "/")

            audio_files.append(
                {
                    "file": filename,
                    "label": display_label,
                    "rel_path": rel_path,
                }
            )

        order = {
            "Clean Target": 0,
            "Input": 1,
            "Enhanced Output of Spatial-U-Net": 2,
        }
        audio_files.sort(key=lambda x: order.get(x["label"], 99))

        if audio_files:
            examples.append(
                {
                    "name": example_name,
                    "snr": snr,
                    "files": audio_files,
                }
            )

    examples.sort(key=lambda x: x["name"])
    return examples


INDEX_HTML = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Deep Learning-Based Multi-Channel Speech Enhancement for Low Signal-to-Noise Ratio Scenario</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, system-ui, "SF Pro Text", "Segoe UI", sans-serif;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            align-items: stretch;
            justify-content: center;
            background: #47236E;
            color: #f9f5ff;
        }
        .page {
            width: 100%;
            max-width: 640px;
            padding: 20px 14px 24px;
        }
        .shell {
            background: rgba(14, 7, 30, 0.78);
            border-radius: 24px;
            padding: 22px 18px 18px;
            box-shadow:
                0 20px 50px rgba(0, 0, 0, 0.55),
                0 0 0 1px rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(16px);
        }
        .header {
            margin-bottom: 18px;
        }
        .title {
            font-size: 20px;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin: 0 0 4px;
        }
        .subtitle {
            font-size: 13px;
            color: #c9c0e3;
            margin: 0;
        }
        .grid {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .example-card {
            background: radial-gradient(circle at top left, #ffffff, #f4f4fb);
            border-radius: 18px;
            padding: 12px 12px 10px;
            color: #171321;
            box-shadow:
                0 12px 26px rgba(0, 0, 0, 0.2),
                0 0 0 1px rgba(255, 255, 255, 0.55);
        }
        .example-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }
        .example-title {
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.06em;
            color: #302445;
        }
        .tag {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 2px 9px 3px;
            border-radius: 999px;
            font-size: 11px;
            background: linear-gradient(135deg, #f3f0ff, #e7f5ff);
            color: #1f3b77;
            white-space: nowrap;
        }
        .file-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .file-row {
            display: flex;
            flex-direction: column;
            gap: 6px;
            padding: 8px 9px;
            border-radius: 12px;
            background: rgba(246, 246, 252, 0.96);
        }
        .file-meta {
            display: flex;
            flex-direction: column;
            gap: 2px;
            min-width: 0;
        }
        .file-label {
            font-size: 13px;
            font-weight: 500;
            color: #211832;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .file-name {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 11px;
            color: #8c879b;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .file-audio {
            width: 100%;
        }
        audio {
            width: 100%;
        }
        .no-examples {
            margin-top: 12px;
            padding: 14px 16px;
            border-radius: 16px;
            background: rgba(255, 245, 230, 0.95);
            border: 1px solid rgba(255, 212, 150, 0.9);
            color: #7a510c;
            font-size: 13px;
        }
        .footer {
            margin-top: 16px;
            font-size: 11px;
            color: #b8aedc;
            text-align: right;
        }
        @media (min-width: 768px) {
            .page {
                max-width: 720px;
                padding: 28px 18px 32px;
            }
            .shell {
                padding: 26px 22px 20px;
            }
        }
    </style>
</head>
<body>
<div class="page">
    <div class="shell">
        <div class="header">
            <h1 class="title">Deep Learning-Based Multi-Channel Speech Enhancement for Low Signal-to-Noise Ratio Scenario</h1>
        </div>

        {% if examples %}
        <div class="grid">
            {% for ex in examples %}
            <div class="example-card">
                <div class="example-header">
                    <div class="example-title">Input SNR = {{ ex.snr }}</div>
                </div>
                <div class="file-list">
                    {% for f in ex.files %}
                    <div class="file-row">
                        <div class="file-meta">
                            <div class="file-label">{{ f.label }}</div>
                        </div>
                        <div class="file-audio">
                            <audio controls preload="none">
                                <source src="{{ url_for('serve_audio', path=f.rel_path) }}">
                                Your browser does not support the audio tag.
                            </audio>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="no-examples">
            No audio files were found in <code>Example_01</code>, <code>Example_02</code>, or <code>Example_03</code>.
            Please ensure these folders exist and contain valid audio files.
        </div>
        {% endif %}

        <div class="footer">
            <div class="footer-row">
                <span class="footer-label">Author:</span>
                <span> Yifei Wei</span>
                <span class="footer-email">yifei.wei@student.uq.edu.au</span>
            </div>
            <div class="footer-row">
                <span class="footer-label">Supervisor:</span>
                <span> Jihui (Aimee) Zhang</span>
                <span class="footer-email">jihuiaimee.zhang@uq.edu.au</span>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""



@app.route("/")
def index():
    examples = build_examples()
    return render_template_string(INDEX_HTML, examples=examples)

@app.route("/audio/<path:path>")
def serve_audio(path):
    return send_from_directory(BASE_DIR, path, as_attachment=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
