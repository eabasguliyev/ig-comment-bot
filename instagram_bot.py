from InstagramAPI import InstagramAPI
import requests
import json
from time import sleep
import os
from Data.data_manage import data_manage, write_accounts_to_json, write_posts_to_json

dir_path = os.path.dirname(os.path.realpath(__file__))
accounts_path = os.path.join(dir_path, 'Data/accounts.json')
posts_path = os.path.join(dir_path, 'Data/posts.json')

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def get_media_id(url):
    req = requests.get('https://api.instagram.com/oembed/?url={}'.format(url))
    media_id = req.json()['media_id']
    return media_id

def get_ads_media_id(url):
    import re
    from lxml import html
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'})
    tree = html.fromstring(page.content)

    script = tree.xpath('/html/body/script[1]')[0]

    match = re.search(r'reshare":(.*?),"owner":{"id":"(.*?)"', script.text)
    match2 = re.search(r'graphql":{"shortcode_media":{"__typename":"(.*?)","id":"(.*?)"', script.text)
    
    if(match and match2):
        temp_id = html.fromstring(match.group(2))
        temp_media = html.fromstring(match2.group(2))
        id = temp_id.text_content()
        media = temp_media.text_content()
        media_id = media + '_' + id
        return media_id

def get_data():

    with open(accounts_path) as json_file:
        accounts = json.load(json_file)
        json_file.close()

    with open(posts_path) as json_file:
        posts = json.load(json_file)
        json_file.close()

    account_counts = 0
    for acc in accounts['accounts']:
        account_counts +=1

    post_counts = 0
    for post in posts['posts']:
        post_counts +=1
    
    return accounts, account_counts, posts, post_counts

def get_posts_id(posts, post_counts, method):
    data = []
    if(method == 0):
        for link in posts['posts']:
            try:
                post_media_id = get_ads_media_id(link['link']) # get_media_id(url)

            except json.decoder.JSONDecodeError:
                # post silinibse ya da gizlidirse silsin
                del posts['posts'][j]
                post_counts -= 1
                with open('posts.json','w') as f: 
                    json.dump(posts, f, indent=4)
            
            data.append(post_media_id)
    else:
        for link in posts['posts']:
            try:
                post_media_id = get_media_id(link['link']) # get_media_id(url)
            except json.decoder.JSONDecodeError:
                # post silinibse ya da gizlidirse silsin
                del posts['posts'][j]
                post_counts -= 1
                with open('posts.json','w') as f: 
                    json.dump(posts, f, indent=4)
            data.append(post_media_id)
    return data, post_counts

def check_file1():
    with open(accounts_path, 'r') as file:
        data = json.load(file)
        for line in data['accounts']:
            if(line):
                return True
            else:
                return False

def check_file2():
    with open(posts_path, 'r') as file:
        data = json.load(file)
        for line in data['posts']:
            if(line):
                return True
            else:
                return False


if __name__ == "__main__":
    cls()

    if not os.path.isfile(accounts_path):
        print("\nAccounts.json not found. Please create new account(s)!\n")
        write_accounts_to_json()

    if not os.path.isfile(posts_path):
        print("\nPosts.json not found. Please create new post(s)!\n")
        write_posts_to_json()

    if not check_file1():
        print("\n There is no account. Please create new account(s)!\n")
        write_accounts_to_json()

    if not check_file2():
        print("\n There is no post. Please create new post(s)!\n")
        write_posts_to_json()

    accounts = get_data()[0]
    account_counts = get_data()[1]
    posts = get_data()[2]
    post_counts = get_data()[3]

    i = 0 # for accounts and i account's post

    cls()


    while(True):
        choice = int(input("\n1) Start bot for instagram ads posts\n2) Start bot for instagram posts\n3) Info\n4) Data Manage\n5) Exit\n\n>> "))
        if(choice == 1 or choice == 2):

            choice -= 1

            post_data, post_counts = get_posts_id(posts, post_counts, choice)

            stime = int(input("Sleep: "))

            input("Press enter to start bot!")


            while(True):
                counter = 0
                account_blocked = False
                j = 0 # for posts

                try:
                    username = accounts['accounts'][i]['username']
                    password = accounts['accounts'][i]['password']
                except IndexError:
                    print("There is no useable account")
                    break

                
                api = InstagramAPI(username, password)

                print("Trying to login {0}".format(accounts['accounts'][i]['username']))

                if(api.login()):
                    cls()
                    print("Logged in {}".format(username))
                    while(True):
                
                        post_media_id = post_data[j]
                        comment = accounts['accounts'][i]['comment']
                            
                        #komment yazsin stime saniye arayla

                        resp = api.comment(post_media_id, comment)
                        
                        if(resp):
                            counter += 1
                            print("{0}. Commented\n".format(counter))
                            print("Username: {0}\n".format(accounts['accounts'][i]['comment']))
                            print("Post: {0}\n".format(posts["posts"][j]['link']))
                            print("Comment: {0}".format(comment))
                            print("---------------------------------------------------")
                            sleep(stime)
                        else:
                            print("Account blocked")
                            account_blocked = True
                            break
                            
                        j += 1
                        k = 0
                        if(j == post_counts):
                            j = 0
                
                i += 1
                if(account_blocked):
                    del accounts['accounts'][j]
                    i -= 1
                    account_counts -= 1
                    with open(accounts_path,'w') as f: 
                        json.dump(accounts, f, indent=4)
                    
                if(i == account_counts):
                    i = 0
                    
        elif(choice == 3):
            print("\nTotal Accounts: {0}\nTotal Posts: {1}".format(account_counts, post_counts))
            continue           
        elif(choice == 4):
            data_manage()
        elif(choice == 5):
            exit()

