import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

PRODUCTS = {
    'Sejaro 2.5mg': {
        'price': 68000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 2,5мг/доза 2,4мл + Игла 4шт',
        'photo_id': 'AgACAgIAAxkDAAIB1mpCClu3IDPZ9gQ_UeIBtvcNZA_uAAL3FmsbO7MQSvYn5ZoJH_abAQADAgADbQADPAQ',
    },
    'Sejaro 5mg': {
        'price': 101000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 5мг/доза 2,4мл + Игла 4шт',
        'photo_id': 'AgACAgIAAxkDAAIB2GpCC32lC1SPM_zrHZfX0IKEZruNAAL7FmsbO7MQSvPU7gWiXSbrAQADAgADbQADPAQ',
    },
    'Sejaro 7.5': {
        'price': 125000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 7,5мг/доза 2,4мл + Игла 4шт',
        'photo_id': 'AgACAgIAAxkDAAIB2WpCC4CjqqcBi9dEzDikiOOovu_JAAL8FmsbO7MQSlkrD0WAAX1JAQADAgADbQADPAQ',
    },
    'Sejaro 10mg': {
        'price': 135000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 10мг/доза 2,4мл + Игла 4шт',
        'photo_id': None,
    },
    'Sejaro 12.5': {
        'price': 145000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 12,5мг/доза 2,4мл + Игла 4шт',
        'photo_id': 'AgACAgIAAxkDAAIB2mpCC4VrdCqNt18HY3Zznpna0XtcAAL9FmsbO7MQSqkHaz0J-A8iAQADAgADbQADPAQ',
    },
    'Sejaro 15mg': {
        'price': 165000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 15мг/доза 2,4мл + Игла 4шт',
        'photo_id': 'AgACAgIAAxkDAAIB22pCC4eWzcz_QAs_WlW7i3HvZNHVAAL-FmsbO7MQSljjgSbpmfvwAQADAgADbQADPAQ',
    },
}
