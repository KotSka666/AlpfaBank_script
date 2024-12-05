import requests_pkcs12
import logging


REFRESH_TOKEN_URL = "https://baas.alfabank.ru/oidc/token"  
CLIENT_ID = "4b484733-593b-4c61-a950-cc8574c78110"  
CLIENT_SECRET = "737M9e8#sW,B)$A1)K6d75nm5"  
REFRESH_TOKEN = "a0971d2f-eb9d-4bc8-b8fa-44b188c90007"  
P12_FILE = r"C:\lesson_Un\alfa_api\IP_Tsap_Yaroslav_Olegovich.pfx"  
P12_PASSWORD = "QyEgZ6u6pyB4KHvw"  


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def refresh_access_token(refresh_token, client_id, client_secret, p12_file, p12_password):
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }

    try:
        response = requests_pkcs12.post(
            url=REFRESH_TOKEN_URL,
            headers=headers,
            data=payload,
            pkcs12_filename=p12_file,
            pkcs12_password=p12_password
        )

        if response.status_code == 200:
            logger.info("Токен успешно обновлен.")
            return response.json()  
        else:
            logger.error(f"Ошибка обновления токена: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logger.exception(f"Ошибка при запросе на обновление токена: {e}")
        return None

if __name__ == "__main__":
    token_response = refresh_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET, P12_FILE, P12_PASSWORD)
    if token_response:
        access_token = token_response.get("access_token")
        refresh_token = token_response.get("refresh_token")
        logger.info(f"Обновленный токен доступа: {access_token}")
        logger.info(f"Обновленный refresh_token: {refresh_token}")
    else:
        logger.error("Не удалось обновить токен.")
