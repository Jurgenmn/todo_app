import psycopg2

conn = psycopg2.connect(
    host="localhost", database="todo_manager", user='jay', password="password")

cur = conn.cursor()


def interface():
    print("1)   ADD TODO")
    print("2)   LOOKUP TODOS")
    print("3)   DELETE TODO")
    print("4)   UPDATE TODO")
    print("5)   SHOW ALL USERS")
    print("6)   Quit")


def login(cur, username, password):
    query = f"SELECT id, username FROM user_table WHERE username='{username}' AND password='{password}'"
    cur.execute(query)
    record = cur.fetchone()
    # print(record)
    if record == None:
        return None
    else:
        return record[0]


def add_todo(cur, activity, user_id):
    query = f"INSERT INTO activity_table(activity, user_id) VALUES('{activity}', {user_id})"
    print(query)
    cur.execute(query)


def show_todos(cur, user_id):
    query = f"SELECT * FROM activity_table WHERE user_id = {user_id}"
    cur.execute(query)
    records = cur.fetchall()  # list
    print("id         Activity")
    for activity in records:
        print(activity[0], activity[1])


# def delete_todo(cur, activity):
#     query = f"DELETE FROM activity_table WHERE activity = '{activity}'"
#     cur.execute(query)


def delete_todo(cur, id, user_id):
    query = f"DELETE FROM activity_table WHERE id = {id} AND user_id = {user_id}"
    cur.execute(query)


def update_todo(cur, id, user_id, new_activity):
    query = f"UPDATE activity_table SET activity = '{new_activity}' WHERE id = {id} AND user_id = {user_id}"
    cur.execute(query)


def show_all_users(cur):
    query = f"SELECT id, username FROM user_table"
    cur.execute(query)
    records = cur.fetchall()
    for i in records:
        print(i[0], i[1])


user_id = None

while True:
    is_login = input("Do you like to sign-up (1) or log-in (2)?")
    if is_login == "1":
        username = input("What is your username? ")
        password = input("What is your password? ")
        query = f"INSERT INTO user_table(username, password) VALUES ('{username}', '{password}')"
        cur.execute(query)
        user_id = login(cur, username, password)
    else:
        if user_id == None:
            username = input("Username: ")
            password = input("Password: ")
            user_id = login(cur, username, password)
            if user_id == None:
                print("Incorrect credentials")
                continue

    break


while True:

    interface()
    option = input("Select option: ")
    if option == "1":
        activity = input("What is the activity you want to add? ")
        add_todo(cur, activity, user_id)
        print("Todo added")

    elif option == "2":
        show_todos(cur, user_id)

    elif option == "3":
        id = input("Which activity you want to delete? ")
        delete_todo(cur, id, user_id)

    elif option == "4":
        id = input("What id you want to update? ")
        new_activity = input("What is the new activity? ")
        update_todo(cur, id, user_id, new_activity)

    elif option == "5":
        show_all_users(cur)

    elif option == "6":
        print("Goodbye!")
        conn.commit()
        break

    else:
        print("Wrong input")
        continue
