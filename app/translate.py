import json
import requests
from flask_babel import _
from flask import current_app

def translate(text, source_lang, dest_lang):
    if 'TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['TRANSLATOR_KEY']:
        return _('Ошибка: сервис перевода не сконфигурирован')
    response = requests.post('https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&lang={}&text={}&format=html'.format(\
        current_app.config['TRANSLATOR_KEY'], ("{}-{}".format(source_lang, dest_lang)), text))
    if response.status_code != 200:
        return _('Ошибка: сервис перевода недоступен')
    answer = json.loads(response.content.decode('utf-8-sig'))
    return {"text": answer["text"][0]}