import requests_pkcs12
import logging

CLIENT_ID = '4b484733-593b-4c61-a950-cc8574c78110'
CLIENT_SECRET_URL = f"https://baas.alfabank.ru/oidc/clients/{CLIENT_ID}/client-secret"
P12_FILE = r"C:\lesson_Un\alfa_api\IP_Tsap_Yaroslav_Olegovich.pfx"  
P12_PASSWORD = "QyEgZ6u6pyB4KHvw" 

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_client_secret():
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        response = requests_pkcs12.post(
            url=CLIENT_SECRET_URL,
            headers=headers,
            pkcs12_filename=P12_FILE,
            pkcs12_password=P12_PASSWORD
        )
        if response.status_code != 200:
            logger.error(f"Ошибка: {response.status_code}, Тело ответа: {response.text}")
            return None
        return response.json()
    except Exception as e:
        logger.exception(f"Ошибка при выполнении запроса: {e}")
        return None

if __name__ == "__main__":
    result = get_client_secret()
    if result:
        logger.info(f"Успешный ответ: {result}")
