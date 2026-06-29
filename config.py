import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

PRODUCTS = {
    'Sejaro 2.5mg': {
        'price': 68000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 2,5мг/доза 2,4мл + Игла 4шт',
        'photo_url': 'https://drive.google.com/uc?id=1iGm21bVW3k9oxX8cKu1YNaiz37Ficr5H&export=download',
    },
    'Sejaro 5mg': {
        'price': 101000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 5мг/доза 2,4мл + Игла 4шт',
        'photo_url': 'https://drive.google.com/uc?id=1IbfF-6HTq63lCzerhsI3iNnKcyrMxu7Q&export=download',
    },
    'Sejaro 7.5': {
        'price': 125000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 7,5мг/доза 2,4мл + Игла 4шт',
        'photo_url': 'https://drive.google.com/uc?id=17S-OaVbJs0ke5UYIBQz-8DfKf7Gu_vnl&export=download',
    },
    'Sejaro 10mg': {
        'price': 135000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 10мг/доза 2,4мл + Игла 4шт',
        'photo_url': 'https://drive.google.com/uc?id=1vSP84bdF7ThlqujRetEJF5RNM8fsAWaO&export=download',
    },
    'Sejaro 12.5': {
        'price': 145000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 12,5мг/доза 2,4мл + Игла 4шт',
        'photo_url': 'https://drive.google.com/uc?id=1I3C_faPswCVDOmUd6I_RNqhqqBNBbo30&export=download',
    },
    'Sejaro 15mg': {
        'price': 165000,
        'description': 'Седжаро раствор для п/к введ. шприц-ручка 15мг/доза 2,4мл + Игла 4шт',
        'photo_url': 'https://drive.google.com/uc?id=1i_YWrUYJWu2GrzkrFOXhrCvEpXZ8RBgs&export=download',
    }
}
