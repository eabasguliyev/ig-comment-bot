
import os
import json

counter = 0
dir_path = os.path.dirname(os.path.realpath(__file__))
accounts_path = os.path.join(dir_path, 'accounts.json')
posts_path = os.path.join(dir_path, 'posts.json')

def add_account(id = 0):
    data = []
    counter = id
    while(True):
        username = input("Username: ")
        password = input("Password: ")
        comment = input("Comment: ")
        acc = {}

        
        if(username != None and password != None and comment != None):
            acc['id'] = counter
            acc['username'] = username
            acc['password'] = password
            acc['comment'] = comment
            counter = counter + 1

        print("Do you want to exit?")
        resp = input("y/n: ")
        data.append(acc)
        if(resp == 'y'):
            return data

def add_posts(id = 0):
    data = []
    counter = id
    while(True):
        link = input("Enter link: ")
        post = {}

        if(link != None):
            post['id'] = counter
            post['link'] = link
            counter = counter + 1

        print("Do you want to exit?")
        resp = input("y/n: ")
        data.append(post)
        if(resp == 'y'):
            return data

def add_texts(id = 0):
    data = []
    counter = id
    while(True):
        text = input("Enter text: ")
        texts = {}

        if(text != None):
            texts['id'] = counter
            texts['text'] = text
            counter = counter + 1

        print("Do you want to exit?")
        resp = input("y/n: ")
        data.append(texts)
        if(resp == 'y'):
            return data

def write_accounts_to_json():
    print("Add Accounts:\n")
    if not os.path.isfile(accounts_path):
        acc = add_account()
        with open(accounts_path, mode='w') as f:
            f.write("""{
            "accounts": """)
            data = json.dumps(acc, indent = 4)
            for line in data:
                f.write(line)
            f.write("\n}")
    else:
        try:
            with open(accounts_path) as json_file: 
                data = json.load(json_file) 
                counter2 = 0
                for id in data['accounts']:
                    if(id != None):
                        counter2 += 1
                acc = add_account(id = counter2)
                temp = data['accounts']
                for account in acc:
                    temp.append(account)
                        
                with open(accounts_path,'w') as f: 
                    json.dump(data, f, indent=4)
        except json.decoder.JSONDecodeError:
            acc = add_account()
            with open(accounts_path, mode='w') as f:
                f.write("""{
                "accounts": """)
                data = json.dumps(acc, indent = 4)
                for line in data:
                    f.write(line)
                f.write("\n}")    

def write_posts_to_json():
    print("Add Posts:\n")
    if not os.path.isfile(posts_path):
        posts = add_posts()
        with open(posts_path, mode='w') as f:
            f.write("""{
            "posts": """)
            data = json.dumps(posts, indent = 4)
            for line in data:
                f.write(line)
            f.write("\n}")
    else:
        try:
            with open(posts_path) as json_file: 
                data = json.load(json_file) 
                counter2 = 0
                for id in data['posts']:
                    if(id != None):
                        counter2 += 1
                posts = add_posts(id = counter2)
                temp = data['posts']

                for post in posts:
                    temp.append(post)
                        
                with open(posts_path,'w') as f: 
                    json.dump(data, f, indent=4)
        except json.decoder.JSONDecodeError:
            posts = add_posts()
            with open(posts_path, mode='w') as f:
                f.write("""{
                "posts": """)
                data = json.dumps(posts, indent = 4)
                for line in data:
                    f.write(line)
                f.write("\n}")


def data_manage():
    while(True):
        choice = int(input("\n1)Show Data\n2)Add Data\n3)Remove Data\n4)Main Menu\n>> "))

        if(choice == 1):
            while(True):
                #print("\t1) Show Accounts\n\t2) Show Posts\n\t3) Show Texts")
                print("\t1) Show Accounts\n\t2) Show Posts\n\t3) Main Menu")
            
                choice = int(input(">> "))
                if(choice == 1):
                    with open(accounts_path) as json_file:
                        accounts = json.load(json_file)
                        json_file.close()
                    for line in accounts['accounts']:
                        print("Id: {0}\nUsername: {1}\nPassword: {2}\nComment: {3}\n".format(line['id'],line['username'], line['password'],line['comment']))
                        print("---------------------------------\n")
                elif(choice == 2):
                    with open(posts_path) as json_file:
                        posts = json.load(json_file)
                        json_file.close()
                    for line in posts['posts']:
                        print("Id: {0}\nLink: {1}\n".format(line['id'],line['link']))
                        print("---------------------------------\n")
                elif(choice == 3):
                    break
                else:
                    print("\nWrong choice\n")
                    continue
        elif(choice == 2):
            while(True):
                #print("\t1) Add Accounts\n\t2) Add Posts\n\t3) Add Texts")
                print("\t1) Add Accounts\n\t2) Add Posts\n\t3) Main Menu")
                choice = int(input(">> "))
                
                if(choice == 1):
                    write_accounts_to_json()
                elif(choice == 2):
                    write_posts_to_json()
                elif(choice == 3):
                    break
                else:
                    print("\nWrong Choice\n")
                    continue
        elif(choice == 3):
            while(True):
                #print("\t1) Remove Accounts\n\t2) Remove Posts\n\t3) Remove Texts")
                print("\t1) Remove Accounts\n\t2) Remove Posts\n\t3) Main Menu")
                choice = int(input(">>"))
                
                counter = 0
                if(choice == 1):
                    with open(accounts_path) as json_file:
                        accounts = json.load(json_file)
                        json_file.close()
                    
                    for line in accounts['accounts']:
                        print("Id: {0}\nUsername: {1}\nPassword: {2}\nComment: {3}\n".format(counter,line['username'], line['password'], line['comment']))
                        print("---------------------------------\n")
                        counter += 1
                        

                    if(counter == 0):
                        print("\nThere is no account! Create new account(s)\n")
                        write_accounts_to_json()
                    elif(counter == 1):
                        print("\nMinimum number of accounts must be 1")
                    else:
                        id = int(input("Enter id: "))
                        
                        try:
                            del accounts['accounts'][id]
                        except IndexError:
                            print("\nWrong id! Try again\n")
                            continue
                        with open(accounts_path,'w') as json_file: 
                            json.dump(accounts, json_file, indent=4)
                elif(choice == 2):
                    with open(posts_path) as json_file:
                        posts = json.load(json_file)
                        json_file.close()
                    
                    for line in posts['posts']:
                        print("Id: {0}\nLink: {1}\n".format(counter,line['link']))
                        print("---------------------------------\n")
                        counter += 1
                        

                    if(counter == 0):
                        print("\nThere is no post! Create new post(s)!\n")
                        write_posts_to_json()
                    elif(counter == 1):
                        print("\nMinimum number of posts must be 1")
                    else:
                        id = int(input("Enter id: "))
                        
                        try:
                            del posts['posts'][id]
                        except IndexError:
                            print("\nWrong id! Try again!\n")
                            continue
                        with open(posts_path,'w') as json_file: 
                            json.dump(posts, json_file, indent=4)
                elif(choice == 3):
                    break
                else:
                    print("\nWrong choice\n")
                    continue
        elif(choice == 4):
            return 0
        else:
            print("\nWrong Choice\n")
            continue
