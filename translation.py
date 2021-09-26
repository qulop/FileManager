import requests


def translate(language_code: str) -> dict:
    params = {
        'source': 'Downloads.Images.Videos.Music.Documents',
        'lang': f'en-{language_code}',
    }

    response = requests.get('https://fasttranslator.herokuapp.com/api/v1/text/to/text', params=params)
    if response.status_code != 200:
        raise 'failed to translate system directories names on your language.'


    translte = response.json()['data']
    translte = translte.split('.')
    returned = {'Language': language_code,
                'Downloads': translte[0],
                'Pictures': translte[1],
                'Videos': translte[2],
                'Music': translte[3],
                'Documents': translte[4]
                }

    with open('.config', 'a') as config:
        config.write(str(returned) + '\n')

    return returned
