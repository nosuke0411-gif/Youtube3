from flask import Flask, request, jsonify

app = Flask(__name__)

# -------------------------
# 変換ロジック
# -------------------------
def convert_youtube_url(url: str) -> str:
    base_mobile = "https://m.youtube.com/watch?v="
    base_pc = "https://www.youtube.com/watch?v="

    if url.startswith(base_mobile):
        video_id = url[len(base_mobile):]
        return f"https://youtu.be/{video_id}"

    elif url.startswith(base_pc):
        video_id = url[len(base_pc):]
        return f"https://youtu.be/{video_id}"

    else:
        raise ValueError("対応していないURL形式です")


# -------------------------
# フロント（HTML）
# -------------------------
@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>YouTube URL 変換ツール</title>
    <style>
        body {
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: #f7f7f7;
        }
        .container {
            text-align: center;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 500px;
        }
        input {
            width: 100%;
            padding: 14px;
            font-size: 18px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        button {
            padding: 14px 20px;
            font-size: 18px;
            margin-top: 15px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        #convertBtn {
            background: #007bff;
            color: white;
            width: 100%;
        }
        #copyBtn {
            background: #28a745;
            color: white;
            width: 100%;
            display: none;
        }
        #result {
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
            word-break: break-all;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>YouTube URL 変換ツール</h1>

        <input id="urlInput" type="text" placeholder="URLを入力">
        <button id="convertBtn" onclick="convert()">変換する</button>

        <p id="result"></p>
        <button id="copyBtn" onclick="copyResult()">コピーする</button>
    </div>

    <script>
        async function convert() {
            const url = document.getElementById("urlInput").value;

            const res = await fetch("/convert", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({url})
            });

            const data = await res.json();

            if (data.success) {
                document.getElementById("result").innerText = data.converted;
                document.getElementById("copyBtn").style.display = "block";
            } else {
                document.getElementById("result").innerText = "エラー: " + data.error;
                document.getElementById("copyBtn").style.display = "none";
            }
        }

        function copyResult() {
            const text = document.getElementById("result").innerText;
            navigator.clipboard.writeText(text);
        }
    </script>

</body>
</html>
"""


# -------------------------
# API
# -------------------------
@app.route("/convert", methods=["POST"])
def convert():
    data = request.json
    url = data.get("url")

    try:
        result = convert_youtube_url(url)
        return jsonify({"success": True, "converted": result})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
