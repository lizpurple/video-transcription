from flask import Flask, request, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller  # Automatically installs the right ChromeDriver version
import subprocess
import os
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Renders your HTML form.

@app.route('/process', methods=['POST'])
def process():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'Por favor, insira um URL válido.'})

    # Install ChromeDriver automatically
    chromedriver_autoinstaller.install()

    # Configure Chrome options (do not set binary_location)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    try:
        driver.get(url)
        driver.implicitly_wait(10)

        # Look for the video link using the provided CSS selector.
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.secondaryButton')
        if not buttons:
            driver.quit()
            return jsonify({'error': 'Nenhum vídeo encontrado.'})

        video_url = buttons[0].get_attribute("href")
        driver.quit()

        # Use ffmpeg to extract subtitles from the video URL.
        output_srt = '/tmp/sub.srt'
        result = subprocess.run(
            ['ffmpeg', '-i', video_url, '-y', output_srt],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({'error': f"FFmpeg failed: {result.stderr}"})

        if not os.path.exists(output_srt):
            return jsonify({'error': 'O vídeo não possui legendas.'})

        # Process the subtitle file
        with open(output_srt, 'r') as file:
            srt = file.read()

        srt = re.sub(r'<.+?>|{.+?}', '', srt)
        srt = re.sub(r'\d+\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '', srt)
        srt = re.sub('\n', ' ', srt)
        srt = re.sub(r'  ', ' ', srt)
        srt = re.sub(r'([.?!]) ', r'\1\n\n', srt)

        os.remove(output_srt)
        return jsonify({'subtitle': srt})

    except Exception as e:
        driver.quit()
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
