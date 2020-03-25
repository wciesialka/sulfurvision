import configparser, os, argparse, getpass, ImageSearch

PATH = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(PATH,"config")
CONFIG_FILE = os.path.join(CONFIG_PATH,"the_generator_config.ini")
BASE_IMAGE_PATH = os.path.join(PATH,"data","base.jpg")
OUT_PATH = os.path.join(PATH,"out")
KEY_CONFIG_KEY = "GoogleCustomSearchJSONAPIKey"
CX_CONFIG_KEY = "GoogleCustomSearchCX"
CONFIG = configparser.ConfigParser()
API_KEY = None
API_CX = None

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
            try:
                API_KEY = CONFIG['DEFAULT'][KEY_CONFIG_KEY]
            except:
                update_key()
        else: # otherwise, make a key and a config file if needed
            update_key()
    return API_KEY

# I could probably abstract these next three functions, but whatever.
def get_users_cx():
    print("=============================")
    print("Please enter your Google Custom Search Engine CX.")
    print("You can generate one at\n\thttps://cse.google.com/cse/all")
    print("Make sure that you have Image Search and Search the Entire Web on.")
    print("Please do not share this with anyone.")
    inp = getpass.getpass("Your CX: ") # use getpass so that the input is hidden
    print("=============================")
    print()
    return inp

def update_cx(): # create or update a key
    global API_CX
    API_CX = get_users_cx()
    if not os.path.isdir(CONFIG_PATH):
        os.makedirs(CONFIG_PATH) # make directories to the config path if they dont exist so that
                                 # we can write our file to where we expect it to.
    CONFIG['DEFAULT'][CX_CONFIG_KEY] = API_CX
    with open(CONFIG_FILE,"w") as f:
        CONFIG.write(f) # write our new api key to config file

def CX():
    global API_CX, CONFIG
    if API_CX == None:
        if(os.path.isfile(CONFIG_FILE)): # if the config file exists, read from it
            CONFIG.read(CONFIG_FILE)
            try:
                API_CX = CONFIG['DEFAULT'][CX_CONFIG_KEY]
            except:
                update_cx()
        else: # otherwise, make a key and a config file if needed
            update_cx()
    return API_CX

def main(args:argparse.Namespace):
    if not os.path.isdir(OUT_PATH): # if .././out doesn't exist, make it
        os.makedirs(OUT_PATH)
    if(args.update_key): # if the users wants to update their key, let them
        update_key()
        update_cx()
    searcher = ImageSearch.ImageSearch(KEY(),CX())



if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Generate a \"THE\" image.")
    parser.add_argument('-u','--update_key',default=False,action='store_true',help="Start with a prompt to update the user's API key.")
    args = parser.parse_args()
    main(args)