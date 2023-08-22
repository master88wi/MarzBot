import requests
import json

# login to panel


def get_access_token(UrlPanel, username, password):
    datetoken = {
        'username': username,
        'password': password
    }
    try:
        response = requests.post(
            f"{UrlPanel}/api/admin/token", data=datetoken).text
        try:
            token_data = json.loads(response)
            if token_data.get('access_token'):
                return token_data
            elif token_data.get('detail'):
                return token_data['detail']
        except Exception:
            return "Failed to connect Panel"
    except Exception as e:
        return e


# endpoint

def endpoint(UrlPanel, method, action, username, password, data=None):
    access_tokens = get_access_token(UrlPanel, username, password)
    if access_tokens == "Incorrect username or password":
        return "❌ خطایی رخ داده برای رفع مشکل با پشتیبانی در ارتباط باشید\n\nکد خطا : 1"
    elif access_tokens == "Failed to connect Panel":
        return "❌ خطایی رخ داده برای رفع مشکل با پشتیبانی در ارتباط باشید\n\nکد خطا : 2"
    elif access_tokens.get('access_token'):
        access_token =  access_tokens['access_token']
    methods = ["GET", "POST", "PUT", "DELETE"]
    if method in methods:
        url = f"{UrlPanel}{action}"
        header_value = f'Bearer {access_token}'
        headers = {
            'Accept': 'application/json',
            'Authorization': header_value
        }
        if method == "GET":
            response = requests.get(url, data=data, headers=headers).text
        elif method == "POST":
            response = requests.post(url, data=data, headers=headers).text
        elif method == "PUT":
            response = requests.put(url, data=data, headers=headers).text
        elif method == "DELETE":
            response = requests.delete(url, data=data, headers=headers).text
        return json.loads(response)
    else:
        print("Invalid Method")

# Get Info User


def Data_user(urlPanel, username, password, client_username):
    # simple action /api/user/ and Variable client_username
    # method GET FOR DATA_USER
    # simple url panel http or https://site.com:8000
    return endpoint(urlPanel, "GET", "/api/user/"+client_username, username, password)


# Add User To Marzabn Panel
def Add_user(urlPanel, username, password, data):
    # Description Section
    # Method Post For Add User  To Panel Marzban
    # var Data value 🔽🔽🔽🔽🔽🔽🔽🔽
    # username must have 3 to 32 characters and is allowed to contain a-z, 0-9, and underscores in between
    # expire must be an UTC timestamp
    # data_limit must be in Bytes, e.g. 1073741824B = 1GB
    # proxies dictionary of protocol:settings
    # inbounds dictionary of protocol:inbound_tags, empty means all inbounds
    return endpoint(urlPanel, "POST", "/api/user", username, password, data)

# ModifyUser User For Panel Marzban


def ModifyUser(urlPanel, username, password, client_username, data):
    # Description this Section
    # Method PUT For Modify User  To Panel Marzban
    # var Data value 🔽🔽🔽🔽🔽🔽🔽🔽
    # set expire to 0 to make the user unlimited in time, null to no change
    # set data_limit to 0 to make the user unlimited in data, null to no change
    # proxies dictionary of protocol:settings, empty means no change
    # inbounds dictionary of protocol:inbound_tags, empty means no change
    return endpoint(urlPanel, "PUT", "/api/user/"+client_username, username, password, data)


# Delete User For Panel Marzban
def DeleteUser(urlPanel, username, password, client_username):
    # Description this Section
    # Method DELETE For Delete User  To Panel Marzban
    return endpoint(urlPanel, "DELETE", "/api/user/"+client_username, username, password)

# Reset User Data Usage User For Panel Marzban


def ResetUserData(urlPanel, username, password, client_username):
    # Description this Section
    # Method PUT For Reset User Data Usage User  To Panel Marzban
    return endpoint(UrlPanel, "POST", f"/api/user/{client_username}/reset", username, password)
