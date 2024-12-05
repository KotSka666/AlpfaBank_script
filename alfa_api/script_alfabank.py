import requests_pkcs12
import logging
from datetime import datetime


BASE_URL = "https://baas.alfabank.ru/api/statement/transactions" 
ACCESS_TOKEN = "eyJraWQiOiJiYWFzLWRlYy0yMDI0IiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI0NDA3YjFhZS1mOGU0LTQ3MzAtOGQ0NC00MmI5Y2E3N2JjZGYiLCJhdWQiOiI0YjQ4NDczMy01OTNiLTRjNjEtYTk1MC1jYzg1NzRjNzgxMTAiLCJpc3MiOiJodHRwczovL2lkLmFsZmFiYW5rLnJ1L29pZGMiLCJleHAiOjE3MzMzMzkwODMsInNjb3BlX3NlcnZpY2VzIjpbInRyYW5zYWN0aW9ucyJdLCJpYXQiOjE3MzMzMzU0ODMsImp0aSI6IjI3MWY2MDBhLTE3ODAtNDY2OC05NzYyLTFkNjhiZWM2OTgyMCIsInNjb3BlX2NsYWltcyI6W119.oi8WIS32kqXgy5XkSl2__y_hffTCgACLygPmw8VILpDutg8gu3ljC9wAKPi5HaUM1FRxNHkU3P67cJDP-EROOW-wUgm0eFBDg2zzxW4v8z5sVbB-olImTuEujGG1pZFou17aIknWkPtiHSHIfHRpK5QQt_06Tomv_8VHJG-CS8D_TUV31LF1flw6HqvccDJh829UEJEnebZ1SnJG2hdgun8mINNxofQdeqRer9VW8-QNJ3oFI0lHhI21ssNGIzL_O5VokhLGLzpTDzZRi-nc-2CePSh1h0ddLzBCkjZ_97ozZp0nAdAxXATcKk4cRF20cuHvl1Pfm5itJYhAJmm5Zg"  # Ваш токен доступа (access_token)
TEST_ACCOUNTS = ["40802810126010014397"]

P12_FILE = r"C:\lesson_Un\alfa_api\IP_Tsap_Yaroslav_Olegovich.pfx"  
P12_PASSWORD = "QyEgZ6u6pyB4KHvw"  


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_account_summary(account_number, p12_file, p12_password):
    """
    Получение информации об оборотах для заданного номера счета.
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json"
    }
    
    statement_date = datetime.now().strftime("%Y-%m-%d")

    params = {
        "accountNumber": account_number,  
        "statementDate": statement_date  
    }

    try:
        response = requests_pkcs12.get(
            BASE_URL,
            headers=headers,
            params=params,
            pkcs12_filename=p12_file,
            pkcs12_password=p12_password
        )
        
        if response.status_code == 200:
            logger.info(f"Информация для счета {account_number} успешно получена.")
            return response.json()
        else:
            logger.error(f"Ошибка получения данных для счета {account_number}: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logger.exception(f"Ошибка при запросе данных для счета {account_number}: {e}")
        return None

if __name__ == "__main__":
    for account in TEST_ACCOUNTS:
        summary = get_account_summary(account, P12_FILE, P12_PASSWORD)
        if summary:
            logger.info(f"Обороты для счета {account}: {summary}")
        else:
            logger.error(f"Не удалось получить данные для счета {account}.")
