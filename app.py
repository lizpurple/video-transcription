from flask import Flask, request, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import os
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # HTML form for user input.

@app.route('/process', methods=['POST'])
def process():
    url = request.form.get('url')

    if not url:
        return jsonify({'error': 'Por favor, insira um URL válido.'})

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        driver.implicitly_wait(10)

        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.secondaryButton')
        if not buttons:
            return jsonify({'error': 'Nenhum vídeo encontrado.'})

        video_url = buttons[0].get_attribute("href")
        driver.quit()

        # Use a temp location for subtitles
        output_srt = '/tmp/sub.srt'
        subprocess.run(['ffmpeg', '-i', video_url, '-y', output_srt])

        if not os.path.exists(output_srt):
            return jsonify({'error': 'O vídeo não possui legendas.'})

        # Process subtitles
        with open(output_srt, 'r') as file:
            srt = file.read()

        srt = re.sub(r'<.+?>', '', srt)
        srt = re.sub(r'{.+?}', '', srt)
        srt = re.sub(r'^\d+\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '', srt, flags=re.M)
        srt = re.sub('\n', ' ', srt)
        srt = re.sub(r'  ', ' ', srt)
        srt = re.sub(r'\. ', '.\n\n', srt)
        srt = re.sub(r'\? ', '?\n\n', srt)
        srt = re.sub(r'\.” ', '.”\n\n', srt)

        os.remove(output_srt)

        return jsonify({'subtitle': srt})

    except Exception as e:
        driver.quit()
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
