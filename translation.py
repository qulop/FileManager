import requests


def translate_to_other_lang(language_code: str) -> dict:
    if language_code == 'en':
        return {'Language': 'en', 'Downloads': 'Downloads', 'Pictures': 'Pictures', 'Videos': 'Videos',
                'Music': 'Music', 'Documents': 'Documents'}

    params = {
        'source': 'Downloads.Pictures.Videos.Music.Documents',
        'lang': f'en-{language_code}',
    }

    response = requests.get('https://fasttranslator.herokuapp.com/api/v1/text/to/text', params=params)
    if response.status_code != 200:
        raise 'Failed to translate system directories names on your language.'

    translate = response.json()['data']
    translate = translate.split('.')
    returned = {'Language': language_code,
                'Downloads': translate[0],
                'Pictures': translate[1],
                'Videos': translate[2],
                'Music': translate[3],
                'Documents': translate[4]
                }

    with open('lang.conf', 'a') as config:
        config.write(str(returned) + '\n')

    return returned
