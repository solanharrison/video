from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [{
                'quality': f.get('format_note', 'unknown'),
                'ext': f.get('ext'),
                'url': f.get('url')
            } for f in info['formats'] if f.get('vcodec') != 'none']
            return jsonify({'success': True, 'formats': formats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
