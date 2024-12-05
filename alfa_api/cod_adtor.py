import requests_pkcs12
import logging


# Конфигурация
CLIENT_ID = '4b484733-593b-4c61-a950-cc8574c78110'
REDIRECT_URI = 'http://localhost'  
TOKEN_URL = "https://baas.alfabank.ru/oidc/token"
P12_FILE = r"C:\lesson_Un\alfa_api\IP_Tsap_Yaroslav_Olegovich.pfx"
P12_PASSWORD = "QyEgZ6u6pyB4KHvw"  

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def exchange_code_for_token(auth_code, client_id, client_secret, redirect_uri):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    try:
        response = requests_pkcs12.post(
            url=TOKEN_URL,
            headers=headers,
            data=payload,
            pkcs12_filename=P12_FILE,
            pkcs12_password=P12_PASSWORD
        )
        if response.status_code != 200:
            logger.error(f"Ошибка при обмене кода: {response.status_code}, Тело ответа: {response.text}")
            return None
        return response.json()
    except Exception as e:
        logger.exception(f"Ошибка при выполнении запроса: {e}")
        return None

if __name__ == "__main__":
    AUTH_CODE = '94e1d35e-6c78-487d-b0c3-289f0ed9c94b'  
    CLIENT_SECRET = "737M9e8#sW,B)$A1)K6d75nm5"  
    token_data = exchange_code_for_token(AUTH_CODE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    if token_data:
        logger.info(f"Токен успешно получен: {token_data}")
    else:
        logger.error("Не удалось получить токен.")
