import requests_pkcs12
import logging
import urllib.parse as urlparse
import sys

# Конфигурация
CLIENT_ID = '982afbb8-64b7-467d-bb84-80000daf9b4c'
CLIENT_SECRET_URL = f"https://sandbox.alfabank.ru/oidc/clients/{CLIENT_ID}/client-secret"
P12_FILE = r"C:\lesson_Un\KassaAPI_Tbank\alphaAPI\baas_swagger_2025.p12"
P12_PASSWORD = "alfabank"
REDIRECT_URI = "http://localhost:8080"
TOKEN_URL = "https://id-sandbox.alfabank.ru/oidc/token"
SCOPE = "transactions"
STATE = "random_state_string"

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для получения client_secret
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

# Функция для обмена AUTH_CODE на токен
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
    # Шаг 1: Получение client_secret
    client_secret_data = get_client_secret()
    if not client_secret_data:
        logger.error("Ошибка при запросе client_secret.")
        sys.exit(1)

    CLIENT_SECRET = client_secret_data.get('clientSecret')
    if not CLIENT_SECRET:
        logger.error("Не удалось извлечь client_secret из ответа.")
        sys.exit(1)

    logger.info(f"Ваш client_secret успешно получен.")

    # Шаг 2: Ввод AUTH_CODE пользователем
    print("Откройте браузер и перейдите по ссылке для авторизации:")
    print(f"https://id-sandbox.alfabank.ru/oidc/authorize?"
        f"response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}&state={STATE}")
    
    AUTH_CODE = input("Введите AUTH_CODE, который вы получили после авторизации: ").strip()
    if not AUTH_CODE:
        logger.error("AUTH_CODE не был введен.")
        sys.exit(1)

    # Шаг 3: Обмен AUTH_CODE на токен
    token_data = exchange_code_for_token(AUTH_CODE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    if token_data:
        logger.info(f"Токен успешно получен: {token_data}")
        print("Токен доступа:")
        print(token_data)
    else:
        logger.error("Не удалось получить токен.")
