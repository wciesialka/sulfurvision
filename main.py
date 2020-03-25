import configparser, os

PATH = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(PATH,"config")
CONFIG_FILE = os.path.join(CONFIG_PATH,"the_generator_config.ini")
KEY_CONFIG_KEY = "GoogleCustomSearchJSONAPIKey"
CONFIG = configparser.ConfigParser()
API_KEY = None

def get_users_key():
    print("=============================")
    print("Please enter your Google Custom Search JSON API Key.")
    print("You can generate one at\n\thttps://developers.google.com/custom-search/v1/overview")
    print("Please do not share this key with anyone.")
    return input("Your key: ")

def update_key():
    global API_KEY
    API_KEY = get_users_key()
    os.makedirs(CONFIG_PATH,exist_ok=True)
    CONFIG['DEFAULT'][KEY_CONFIG_KEY] = API_KEY
    with open(CONFIG_FILE,"w") as f:
        CONFIG.write(f)

def KEY():
    global API_KEY, CONFIG
    if API_KEY == None:
        if(os.path.isfile(CONFIG_FILE)):
            CONFIG.read(CONFIG_FILE)
            API_KEY = CONFIG['DEFAULT'][KEY_CONFIG_KEY]
        else:
            update_key()
    return API_KEY

def main():
    print(KEY())

if __name__=="__main__":
    main()