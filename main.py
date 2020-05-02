import configparser, os, argparse, getpass, ImageSearch, urllib, TheMaker, sys
from PIL import Image

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

def wget_image(url:str):
    if isinstance(url,str):
        r = urllib.request.urlopen(url)
        return Image.open(r)
    else:
        raise TypeError(f"url should be type str, not type {type(url)}")

def wget_best_image(searcher:ImageSearch.ImageSearch, query:str):
    if not isinstance(searcher,ImageSearch.ImageSearch):
        raise TypeError(f"searcher should be type ImageSearch, not type {type(searcher)}")
    if not isinstance(query,str):
        raise TypeError(f"query should be type str, not type {type(query)}")
    img = None
    i = 0
    while img == None and i < 5: # don't perform more than 5 searches
        n = (i*10) + 1
        try:
            results = searcher.search(query,start=n)
        except ImageSearch.UnsuccessfulRequest as ex:
            print("Error while retrieving image results:\n\t",ex)
            if(ex.response_code == 400):
                print("Are your API Key and CX correct?")
            exit()
        else:
            for result in results: # loop through results and try to find a valid one
                try:
                    url = result['link']
                    img = wget_image(url)
                except:
                    continue
                else:
                    break
        i += 1

    if img == None:
        raise RuntimeError("Could not find valid image in less than fifty results.")
    else:
        return img

def main(args:argparse.Namespace):
    if(args.update_key): # if the users wants to update their key, let them
        update_key()
        update_cx()

    if args.cx:
        cx = args.cx
    else:  
        cx = CX()
    
    if args.key:
        key = args.key
    else:
        key = KEY()

    query = args.query
    # create our searcher
    searcher = ImageSearch.ImageSearch(key,cx)
    img = wget_best_image(searcher,query)
    
    maker = TheMaker.TheMaker(img,query.upper())
    maker.overlay_image()
    maker.overlay_text()

    if not os.path.isdir(OUT_PATH): # if .././out doesn't exist, make it
        os.makedirs(OUT_PATH)
    basename = " ".join(("the",query))

    if(args.output):
        out = args.output
    else:
        out = open(os.path.join(OUT_PATH,".".join((basename,"jpg"))),'wb')
    
    try:
        maker.save(out)
    except Exception as ex:
        print("Unexpected error while saving file:", sys.exc_info()[0])
        print("\t",ex)
        if(isinstance(ex,ValueError)):
            print("Make sure your file has an extension.")
    finally:
        out.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Generate a \"THE\" image.")
    parser.add_argument('-u','--update_key',default=False,action='store_true',help="Start with a prompt to update the user's API key.")
    parser.add_argument('-o','--output',type=argparse.FileType('wb'),help="Output file.")
    parser.add_argument('-k','--key',type=str,help="Force use provided API key.")
    parser.add_argument('-c','--cx',type=str,help="Force use provided CX.")
    parser.add_argument('query',help='Search query.',type=str)
    args = parser.parse_args()
    main(args)