#!/usr/bin/env python3
import random
import time
from flask import Flask, render_template, url_for, request, redirect
from flask_socketio import SocketIO, emit
import datetime
import compression
import sorting
import encryption
import sqlite3
import json
import ast
import re

public_key, private_key, prime_product = encryption.generate_keys() # This will generate the private key, public key and prime product


def create_user(username, privilege): # Creates the user object depending on the privilege

    if privilege == "admin":
        return Admin(username, "admin")

    elif privilege == "general":
        return General(username, "general")



class circular_queue: # Circular queue class for the register requests

    def __init__(self, size):

        self.max_size = size
        self.queue = ["" for i in range(self.max_size)]
        self.front = -1 #contains the index of the element to be dequeued next
        self.rear = -1 # contains the index of the element to be enqueued next

    def check_queue_full(self): # Checks if the queue is full by checking if the modulus of the rear is equal to the front, meaning its full

        if (self.rear + 1) % self.max_size == self.front:
            return True

        else:
            return False

    def check_queue_empty(self): # If the front pointer is -1 then its empty list

        if self.front == -1:
            return True

        else:
            return False

    def get_data_in_order(self): # Gets the data in order, excluding empty elements to put into the json file

        new_list = []

        front = self.front
        rear = self.rear


        if front <= rear:
            distance = rear - front
            for i in range(distance + 1):
                new_list.append(self.queue[front])
                front += 1

            final_list = [i for i in new_list if i != ""]

            return final_list


        elif front > rear:

            distance = self.max_size - self.queue.count("")
            for i in range(distance):
                if front + 1 > self.max_size:
                    front = 0
                    new_list.append(self.queue[front])

                else:
                    new_list.append(self.queue[front])
                    front += 1

            final_list = [i for i in new_list if i != ""]

            return final_list



    def peek(self): # Gets the next value in the queue
        return self.queue[self.front]



    def enqueue(self, data): # Checks if the queue is full, or else will enqueue to the list

        if self.check_queue_full() is True:
            return "full"

        elif self.front == -1:
            self.front = self.rear = 0
            self.queue[self.rear] = data

        else:
            self.rear = (self.rear + 1) % self.max_size
            self.queue[self.rear] = data

    def dequeue(self): # Checks if the queue is empty, else will dequeue from the list

        if self.check_queue_empty() is True:
            return "empty"

        elif self.rear == self.front:
            self.queue[self.front] = ""
            self.front = self.rear = -1

        else:
            self.queue[self.front] = ""
            self.front = (self.front + 1) % self.max_size

user_requests = circular_queue(10) # There can be a maximum of 10 people that register


def initial_queue_update(): # Will update the queue with all the values already in the json file containing register reqeuests

    with open("user_requests.json", "r") as file:

        data = json.load(file)

    for i in data["requests"]:
        user_requests.enqueue(i)


initial_queue_update()




def check_username_in_queue(username): # This function checks if the queue is in register queue already for anyone that is trying to register

    in_queue = False

    queue = user_requests.get_data_in_order()

    if user_requests.check_queue_empty() is True:
        return False

    for i in queue: # Does a linear search

        if i["username"] == username:
            in_queue = True

        else:
            in_queue = False

    return in_queue




app = Flask(__name__) # Makes the server in flask
app.config['SECRET_KEY'] = f"{str(private_key)}"
socketio = SocketIO(app, max_http_buffer_size = 1000 * 1000 * 2) # means that 2 MB of data can be passed in the header



def update_user_requests(): # this will update the register queue with json values in register requsts

    user_queue = user_requests.get_data_in_order()
    final_data = {"requests": user_queue}


    with open("user_requests.json", "w") as file: # dumps it into the register request page
        json.dump(final_data, file, indent = 4)


class General: # General class for user with general privileges

    def __init__(self, username, privilege): # constructor that takes these values
        self.username = username
        self.privilege = privilege

    def get_username(self): # gets the username values
        return self.username

    def get_privilege(self): # gets the privilege
        return self.privilege

    def set_username(self, username): # sets the username
        self.username = username

    def set_privilege(self, privilege): # sets the password
        self.privilege = privilege



class Admin(General): # Inherits from the general class and gets all the properties and methods

    def __init__(self, username, privilege): # Constructor
        super().__init__(username, privilege)



    def get_user_requests(self): # Gets the user requsts that only the admin can do

        with open("user_requests.json", "r") as file:

            return json.load(file)


    def update_queue_with_json(self, data): # updates the queue with the values from the user reqeusts in json

        for i in data["requests"]:
            user_requests.enqueue(i)


    def add_credentials(self, username, password, privilege): # adds the credentials to the class

        connection = sqlite3.connect("files.db") # adds to an sqlite3 table

        crsr = connection.cursor()

        username_id = hash_function(username) # creates the hash value

        sql_command = f"""SELECT username, password, privilege FROM credentials WHERE hash_id = "{username_id}";""" # selects the username, password and privilege based on the hash id

        crsr.execute(sql_command)

        data = crsr.fetchall() # stores the data in the variable


        usernames_list = (ast.literal_eval(data[0][0]))["usernames"]
        usernames_list.append(username)
        new_usernames = {"usernames": usernames_list} # stores the updated username


        passwords_list = (ast.literal_eval(data[0][1]))["passwords"]
        passwords_list.append(password)
        new_passwords = {"passwords": passwords_list} # stores the updated passwords


        privileges_list = (ast.literal_eval(data[0][2]))["privileges"]
        privileges_list.append(privilege)
        new_privileges = {"privileges": privileges_list} # stores the updated privileges


        sql_command = f"""UPDATE credentials set username = "{new_usernames}", password = "{new_passwords}", privilege = "{new_privileges}" WHERE hash_id = "{username_id}";"""
        # sql command that updates the table
        crsr.execute(sql_command)
        connection.commit()
        connection.close()




def hash_function(data): # generates the hash function bassed on username

    total = 1

    for i in data:

        total *= ord(i)

    return total % 223 # hash id is between 0 and 223


def check_if_username_exists(username): # function checks if the username exist by generating hash id and searching that index

        connection = sqlite3.connect("files.db")

        crsr = connection.cursor()

        username_id = hash_function(username)

        sql_command = f"""SELECT username FROM credentials WHERE hash_id = "{username_id}";"""

        crsr.execute(sql_command)

        data = crsr.fetchall()

        usernames = (ast.literal_eval(data[0][0]))["usernames"]

        connection.close()
        # returns if the username exists
        if username in usernames:

            return True

        else:

            return False


def authenticate_user(username, password): # returns a boolean if the the password is correct


    connection = sqlite3.connect("files.db")

    crsr = connection.cursor()

    username_id = hash_function(username) # makes hash id for the username id

    sql_command = f"""SELECT username, password FROM credentials WHERE hash_id = "{username_id}";""" # gets the useranme and passwords at that index

    crsr.execute(sql_command)

    data = crsr.fetchall()

    usernames = (ast.literal_eval(data[0][0]))["usernames"]

    passwords = (ast.literal_eval(data[0][1]))["passwords"]

    connection.close()

    if username == []: return False

    index = 0

    for i in usernames:

        if usernames[index] == username:

            break

        else:

            index += 1


    try: actual_password = passwords[index]
    except: return False

    if actual_password == password: return True

    else: return False
    # returns if the password is correct at that index




def return_credentials(username): # returns the password and privilege for a certain password

    connection = sqlite3.connect("files.db")

    crsr = connection.cursor()

    username_id = hash_function(username)

    sql_command = f"""SELECT username, password, privilege FROM credentials WHERE hash_id = "{username_id}";"""
    # sql statement to get the usernames, passwords and privilegs for the credentials in a certain hash index
    crsr.execute(sql_command)

    data = crsr.fetchall()


    usernames_list = (ast.literal_eval(data[0][0]))["usernames"]

    passwords_list = (ast.literal_eval(data[0][1]))["passwords"]

    privileges_list = (ast.literal_eval(data[0][2]))["privileges"]

    connection.close()


    if usernames_list == []: return False

    index = 0

    for i in usernames_list:

        if i == username:
            break

        else:
            index += 1


    return {"username": username, "password": passwords_list[index], "privilege": privileges_list[index]}

    # returns a json for the websocket to return


@socketio.on("handle_credentials") # on the handle credentials event we get the data
def handle_credentials(data):

    global user
    username = encryption.decrypt(private_key, prime_product, data["username"]) # decrypts the encrypted username
    password = encryption.decrypt(private_key, prime_product, data["password"]) # decryptd the encrypted password

    if username == "" or password == "":
        emit("error_handler", "empty") # checks if the fields are empty


    elif check_if_username_exists(username) is True: # checks if the username exists and sends error message if so

        if authenticate_user(username, password) is True: # authenticats the user


            if (return_credentials(username))["privilege"] == "admin": # updates the credentials as admin with the user, if the user exists and updates the sesssion

                socketio.emit("update_credentials", {"username": username, "privilege": "admin"})

            else:
                socketio.emit("update_credentials", {"username": username, "privilege": "general"}) # otherwise will update the user as general privilege

            emit('redirect', {'url': url_for("file_page")}) # redirects to the file page if the user is authenticated

        else:
            emit("error_handler", "wrong_password") # emits the wrong password if the password is wrong

    else:

        emit("error_handler", "wrong_username") # emits the wrong username if the username does not exist



@socketio.on("handle_register") # works on the handle request event
def handle_register(data):

    username = encryption.decrypt(private_key, prime_product, data["username"]) # decrypts the register username and register password
    password = encryption.decrypt(private_key, prime_product, data["password"])

    banned_characters = [" ", "\"", "\'"]


    if (username == "") or (password == ""): # if it is empty then will return that it is empty
        emit("register_error_handler", "empty")

    elif (len(username) <= 4) or (len(password) <= 4): # if the the length of the fields are less than or equal to 4 then return error
        emit("register_error_handler", "not_enough_characters")

    elif (len(username) >= 18) or (len(password) >= 18): # if the characters are longer than 18, then returns error
        emit("register_error_handler", "too_many_characters")

    elif user_requests.check_queue_full() is True: # check if the queue is full and sends error if it is
        emit("register_error_handler", "queue_full")


    elif any(i in (username or password) for i in banned_characters) is True: # if the username or password has a space then returns error
        emit("register_error_handler", "banned_characters")


    elif check_username_in_queue(username) is True: # if the register request already exists in the register queue then returns that it is already used
         emit("register_error_handler", "username_in_queue")


    elif check_if_username_exists(username) is True: # checks if the username already exists
         emit("register_error_handler", "username_in_database")

    else:

        emit("register_error_handler", "successful") # if all the validation is successful then will enqeueu to the queue
        user_requests.enqueue({"username": username, "password": password})
        update_user_requests()


@app.route("/", methods = ["GET", "POST"])
def sign_in_page(): # returns the html for the sign in page

    return render_template("sign_in.html")



@socketio.on("update_requests") # adds to the credentials database if the admin checks them off
def update_requests(data):

    user = create_user(data["real_username"], data["real_privilege"])

    if data["decision"] == "true":

        if user_requests.check_queue_empty() is False:

            new_user = user_requests.peek()
            user_requests.dequeue()

            user.add_credentials(new_user["username"], new_user["password"], data["privilege"])

            update_user_requests()

        else:
            pass


    elif data["decision"] == "false":

        if user_requests.check_queue_empty() is False:

            user_requests.dequeue()
            update_user_requests()

        else:
            pass




@socketio.on("get_requests")
def get_requests(): # gets the next value in the queue

    if user_requests.check_queue_empty() is True:
        emit("handle_requests", "empty")

    elif user_requests.check_queue_empty() is False:
        emit("handle_requests", user_requests.peek()["username"])




@app.route("/register_requests", methods = ["GET", "POST"])
def register_requests_page(): # gets the register request html page

    return render_template("register.html")



def get_id_values(): # gets the ids of the files in the database

    connection = sqlite3.connect("files.db")
    crsr = connection.cursor()

    sql_command = f"""SELECT id FROM files;""" # gets all the ids from the files in the database

    crsr.execute(sql_command)


    raw_data = crsr.fetchall()

    id_data = []


    for i in raw_data:
        id_data.append(i[0])

    connection.commit()
    connection.close()

    return id_data # gets the list of the id data


def file_insert_data(id_data, username, file_name, file_data, file_tree): # inserts the data into the database


    connection = sqlite3.connect("files.db")

    crsr = connection.cursor()

    now = datetime.datetime.now()

    date = {"day": now.strftime('%d'), "month": now.strftime('%m'), "year": now.strftime('%Y'), "hour": now.strftime('%H'), "minute": now.strftime('%M')}

    sql_command = f"""INSERT INTO files VALUES (?, ?, ?, ?, ?, ?);""" # parameterised sql query to insert into the table

    crsr.execute(sql_command, (id_data, username, file_name, file_data, str(file_tree), str(date))) # inputs the data

    connection.commit()

    connection.close()




@socketio.on("get_html_data")
def get_html_file_data(data): # gets all the data from the files list

    connection = sqlite3.connect("files.db")

    crsr = connection.cursor()

    sql_command = f"""SELECT * FROM files;""" # gets all the file data

    crsr.execute(sql_command)

    raw_data = crsr.fetchall()

    data_to_send = []

    for i in raw_data:

        raw_date_time = ast.literal_eval(i[5])
        final_datetime = f"{raw_date_time['day']}/{raw_date_time['month']}/{raw_date_time['year']}, {raw_date_time['hour']}:{raw_date_time['minute']}"

        data_to_send.append({"id": i[0], "username": i[1], "file_name": i[2], "datetime": final_datetime, "raw_datetime": raw_date_time}) # makes a dictionary with the details

    if data["search_query"] == "": # if there is nothing in the search query then just return everything
        pass

    elif data["search_query"] != "":

        temp_data_to_send = []

        for file in data_to_send:

            final_search_string = ""

            search_string = data["search_query"]


            for character in search_string:

                if character == " ":
                    final_search_string += " *" # puts this as the regular expresssion so that all there can be multiple spaces and it would still do a pattern match

                else:
                    final_search_string += character


            if bool(re.search(final_search_string.lower(), file["file_name"].lower())) is True: # does the regular expresion search

                temp_data_to_send.append(file)

            else:

                pass

        data_to_send = temp_data_to_send

    data_to_send = sorting.merge_sort(data_to_send, sort_by = data["sort_by"])

    socketio.emit("alter_html_data", data_to_send)



@socketio.on("download_or_delete_by_id") # based on the download or delete command, the checked file will have an operation done to it
def download_or_delete_by_id(data):

    connection = sqlite3.connect("files.db")

    crsr = connection.cursor()

    if data["command"] == "download":

        download_data = []

        for id_data in data["id_list"]:

            sql_command = f"""SELECT * FROM files WHERE id = {id_data};"""

            crsr.execute(sql_command)

            download_data.append(crsr.fetchall()[0])



        for file in download_data:

            frequency_tree = ast.literal_eval(file[4])

            tree = compression.get_tree_from_count_freqeuency(frequency_tree)

            file_data_to_add = bytes(compression.decode_data(file[3], tree))


            try:
                with open(f"../Downloads/{file[2]}", "wb") as new_file:

                    new_file.write(file_data_to_add)
            except:
                with open(f"/Downloads/{file[2]}", "wb") as new_file:

                    new_file.write(file_data_to_add)



        connection.close()


    if data["command"] == "delete":

        for id_data in data["id_list"]:

            sql_command = f"""DELETE FROM files WHERE id = {id_data};""" # sql statement to delete data based on the id

            crsr.execute(sql_command)

            connection.commit()

            socketio.emit("delete_file_data", id_data, broadcast = True)

        connection.close()





@socketio.on("send_file")
def send_file(data): # gets the file and decompressses it

    user = create_user(data["username"], data["privilege"]) # creates the user based on the session details of the user

    code, tree = compression.get_code_and_tree(data["file_content"])

    frequency_tree = compression.count_frequency(data["file_content"])

    existing_id = get_id_values()

    while True:

        new_id = str(random.randint(10000, 99999)) # generates random string for the id of the file and checks if it exists

        if new_id not in existing_id:

            break

    file_insert_data(new_id, user.get_username(), data["file_name"], code, frequency_tree) # subroutine will insert the file into the database


    now = datetime.datetime.now()

    date = f"{now.strftime('%d')}/{now.strftime('%m')}/{now.strftime('%Y')}, {now.strftime('%H')}:{now.strftime('%M')}"

    # will emit the file data to the user so that it can be output to the website
    socketio.emit("show_file_data_temp", {"id": new_id, "username": user.get_username(),"file_name": data["file_name"], "datetime": date}, broadcast = True)




@app.route("/file", methods = ["GET", "POST"])
def file_page(): # returns the html for the file page

    return render_template("file.html")



class Room: # room class that stores the room data

    def __init__(self, room_name, content = []): # contains the room name and the content

        self.room_name = room_name
        self.content = content

    def get_data(self): # gets the room data

        connection = sqlite3.connect("files.db")

        crsr = connection.cursor()

        sql_command = f"SELECT * FROM {self.room_name};"

        crsr.execute(sql_command)

        raw_data = crsr.fetchall()

        connection.close()

        self.content = []

        for i in raw_data:

            self.content.append({"username": i[0], "message": i[1], "datetime": i[2]})

        return self.content # also updates the room data



    def insert_data(self, username, message): # inserts the data into the table

        now = datetime.datetime.now()

        datetime_as_string = f"{now.strftime('%d')}/{now.strftime('%m')}/{now.strftime('%Y')}  {now.strftime('%H')}:{now.strftime('%M')}"

        connection = sqlite3.connect("files.db")

        crsr = connection.cursor()

        sql_command = f"INSERT INTO {self.room_name} VALUES (?, ?, ?);"
        # the sql statement is paramterised
        crsr.execute(sql_command, (username, message, datetime_as_string))

        connection.commit()

        connection.close()


general_room = Room("general_room") # creates the general room


@socketio.on("get_encryption_key")
def get_encryption_key(): # sends the public and the prime product to the client to encrypt the data
    socketio.emit("save_encryption_key", {"public_key": public_key, "prime_product": prime_product})



@socketio.on("get_messages")
def get_messages(): # gets the messages from the table

    data = general_room.get_data()

    socketio.emit("handle_messages_from_database", data)



def check_message_valid(message): # checks if the message empty or has too many characters

    if message == "":

        return False, "empty"

    elif len(message) >= 800:

        return False, "full"

    else:

        return True, "no_reason"


@socketio.on("handle_message")
def handle_message(data):

    user = create_user(data["username"], data["privilege"])
    now = datetime.datetime.now()
    datetime_as_string = f"{now.strftime('%d')}/{now.strftime('%m')}/{now.strftime('%Y')}  {now.strftime('%H')}:{now.strftime('%M')}"
    message = encryption.decrypt(private_key, prime_product, data["encrypted_data"]) # decrypts the data using the private key and prime product

    validity, reason = check_message_valid(message) # function checks if the data is valid

    final_data = {}

    if validity is False:

        final_data = {"response_message": reason}

        socketio.emit("handle_errors", final_data) # sends error message to the client

    elif validity is True:

        general_room.insert_data(user.get_username(), message) # if the message is valid, insert it to the database

        final_data = {"username": user.get_username(), "message": message, "datetime": datetime_as_string, "response_message": reason}
        socketio.emit("live_update_messages", final_data, broadcast = True) # updates the data to the website, broadcasts it to every client




@app.route("/chat", methods = ["GET", "POST"])
def chat_page():

    return render_template("chat.html") # renders the chat page html



if __name__ == "__main__":

    socketio.run(app, port = 8000, debug = True, log_output = True)
