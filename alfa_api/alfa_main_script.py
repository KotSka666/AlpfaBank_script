from datetime import datetime, timedelta, timezone
import requests_pkcs12
import logging
import time

BASE_URL = "https://baas.alfabank.ru/api/statement/transactions"
REFRESH_TOKEN_URL = "https://baas.alfabank.ru/oidc/token"  
CLIENT_ID = "4b484733-593b-4c61-a950-cc8574c78110"  
CLIENT_SECRET = "737M9e8#sW,B)$A1)K6d75nm5"
TOKEN_FILE = "txt.txt"

TEST_ACCOUNTS = ["40802810126010014397"]

P12_FILE = r"C:\lesson_Un\alfa_api\IP_Tsap_Yaroslav_Olegovich.pfx"
P12_PASSWORD = "QyEgZ6u6pyB4KHvw"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

processed_transactions = set()


def load_tokens_from_file(filepath):
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
            access_token = lines[0].strip().split(": ")[1]
            refresh_token = lines[1].strip().split(": ")[1]
            return access_token, refresh_token
    except Exception as e:
        logger.error(f"Ошибка при чтении токенов из файла {filepath}: {e}")
        return None, None


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


def update_tokens(new_access_token, new_refresh_token):

    global ACCESS_TOKEN, REFRESH_TOKEN

    with open(TOKEN_FILE, "w") as f:
        f.write(f"Обновленный токен доступа: {new_access_token}\n")
        f.write(f"Обновленный refresh_token: {new_refresh_token}\n")

    logger.info("Токены успешно обновлены и сохранены в файл.")

    ACCESS_TOKEN, REFRESH_TOKEN = load_tokens_from_file(TOKEN_FILE)
    logger.info("Токены успешно загружены из файла.")


def get_recent_transactions(account_number, p12_file, p12_password):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json"
    }

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(seconds=30)

    params = {
        "accountNumber": account_number,
        "statementDate": now.strftime("%Y-%m-%d")
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
            transactions = response.json().get("transactions", [])
            recent_transactions = []

            for tx in transactions:
                operation_time = datetime.fromisoformat(tx["operationDate"].replace("Z", "+00:00"))
                if operation_time >= start_time and tx["transactionId"] not in processed_transactions:
                    recent_transactions.append(tx)

            return recent_transactions
        else:
            logger.error(f"Ошибка получения данных для счета {account_number}: {response.status_code}, {response.text}")
            return []
    except Exception as e:
        logger.exception(f"Ошибка при запросе данных для счета {account_number}: {e}")
        return []


if __name__ == "__main__":
    ACCESS_TOKEN, REFRESH_TOKEN = load_tokens_from_file(TOKEN_FILE)

    if not ACCESS_TOKEN or not REFRESH_TOKEN:
        logger.error("Не удалось загрузить токены. Проверьте файл txt.txt или обновите токены вручную.")
        exit(1)

    token_response = refresh_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET, P12_FILE, P12_PASSWORD)
    if token_response:
        new_access_token = token_response.get("access_token")
        new_refresh_token = token_response.get("refresh_token")
        update_tokens(new_access_token, new_refresh_token)

    last_refresh_time = datetime.now()

    try:
        while True:
            # Обновление токенов каждые 45 минут
            if datetime.now() - last_refresh_time >= timedelta(minutes=45):
                token_response = refresh_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET, P12_FILE, P12_PASSWORD)
                if token_response:
                    new_access_token = token_response.get("access_token")
                    new_refresh_token = token_response.get("refresh_token")
                    update_tokens(new_access_token, new_refresh_token)
                    last_refresh_time = datetime.now()

            for account in TEST_ACCOUNTS:
                transactions = get_recent_transactions(account, P12_FILE, P12_PASSWORD)

                if transactions:
                    for tx in transactions:
                        amount = tx["amount"]["amount"]
                        transaction_id = tx["transactionId"]

                        print(f"Сумма транзакции: {amount}")
                        processed_transactions.add(transaction_id)
                else:
                    logger.info(f"Нет новых транзакций для счета {account}.")

            #time.sleep(3)  # Пауза перед следующим циклом
    except KeyboardInterrupt:
        logger.info("Программа остановлена пользователем.")
