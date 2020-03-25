import configparser, os, argparse, getpass

PATH = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(PATH,"config")
CONFIG_FILE = os.path.join(CONFIG_PATH,"the_generator_config.ini")
BASE_IMAGE_PATH = os.path.join(PATH,"data","base.jpg")
OUT_PATH = os.path.join(PATH,"out")
KEY_CONFIG_KEY = "GoogleCustomSearchJSONAPIKey"
CONFIG = configparser.ConfigParser()
API_KEY = None

def get_users_key():
    print("=============================")
    print("Please enter your Google Custom Search JSON API Key.")
    print("You can generate one at\n\thttps://developers.google.com/custom-search/v1/overview")
    print("Please do not share this key with anyone.")
    inp = getpass.getpass("Your key: ") # use getpass so that the input is hidden
    print("=============================")
    print()
    return inp

def update_key(): # create or update a key
    global API_KEY
    API_KEY = get_users_key()
    if not os.path.isdir(CONFIG_PATH):
        os.makedirs(CONFIG_PATH) # make directories to the config path if they dont exist so that
                                 # we can write our file to where we expect it to.
    CONFIG['DEFAULT'][KEY_CONFIG_KEY] = API_KEY
    with open(CONFIG_FILE,"w") as f:
        CONFIG.write(f) # write our new api key to config file

def KEY():
    global API_KEY, CONFIG
    if API_KEY == None:
        if(os.path.isfile(CONFIG_FILE)): # if the config file exists, read from it
            CONFIG.read(CONFIG_FILE)
            API_KEY = CONFIG['DEFAULT'][KEY_CONFIG_KEY]
        else: # otherwise, make a key and a config file if needed
            update_key()
    return API_KEY

def main(args:argparse.Namespace):
    if not os.path.isdir(OUT_PATH): # if .././out doesn't exist, make it
        os.makedirs(OUT_PATH)
    if(args.update_key): # if the users wants to update their key, let them
        update_key()
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Generate a \"THE\" image.")
    parser.add_argument('-u','--update_key',default=False,action='store_true',help="Start with a prompt to update the user's API key.")
    args = parser.parse_args()
    main(args)