import logging
import urllib.parse


CLIENT_ID = '4b484733-593b-4c61-a950-cc8574c78110'
REDIRECT_URI = 'http://localhost'  
AUTH_CODE_URL = "https://id.alfabank.ru/oidc/authorize"
SCOPE = 'transactions'  
STATE = 'random_state_string'  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_auth_url(client_id, redirect_uri, scope, state):
    query_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'state': state
    }
    full_url = f"{AUTH_CODE_URL}?{urllib.parse.urlencode(query_params)}"
    return full_url

if __name__ == "__main__":
    auth_url = get_auth_url(CLIENT_ID, REDIRECT_URI, SCOPE, STATE)
    logger.info(f"Ссылка для получения кода авторизации: {auth_url}")
