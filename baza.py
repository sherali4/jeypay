import sqlite3

async def db_connect()-> None:
    global db, cur
    db = sqlite3.connect('bot.sqlite')
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS products(name TEXT, photo TEXT)')
    db.commit()

database = sqlite3.connect('bot.sqlite')
cursor = database.cursor()

async def add_zakaz(id_client, id_tovar):
    # print(id_client, id_tovar)
    # print(id_client, id_tovar)
    # print(type(id_client), type(id_tovar))
    cursor.execute("INSERT INTO zakaz (id_client, id_tovar) VALUES (?, ?)", (id_client, id_tovar,))
    database.commit()
def zakaz_otmen(id_client, id_tovar, user_id):
    cursor.execute('UPDATE zakaz SET sotib_olishi = 2,  delete_user = ? WHERE id_client= ? AND id_tovar = ?', (int(user_id), int(id_client), int(id_tovar),))
    database.commit()
    # print(id_client, id_tovar)
    # print(type(id_client), type(id_tovar), type(user_id))


def del_tovar(id_tovar, user_id):
    cursor.execute('UPDATE zakaz SET sotib_olishi = 2,  delete_user = ? WHERE id_client= ? AND id_tovar = ?', (int(user_id), int(id_client), int(id_tovar),))
    database.commit()
    # print(id_client, id_tovar)
    # print(type(id_client), type(id_tovar), type(user_id))


def zakaz_oladi(id_client, id_tovar, user_id):
    cursor.execute('UPDATE zakaz SET sotib_olishi = 1,  delete_user = ? WHERE id_client= ? AND id_tovar = ?', (int(user_id), int(id_client), int(id_tovar),))
    database.commit()
    # print(id_client, id_tovar)
    # print(type(id_client), type(id_tovar), type(user_id))


async def add_item(state):
    async with state.proxy() as data:
        # print(tuple(data.values()))
        send = tuple(data.values())
        # print(send[0], send[1], send[2], send[3], send[4])
        cursor.execute("INSERT INTO tovar (name, ulchov, narx, tarifi, photo, user_id) VALUES (?, ?, ?, ?, ?, ?)", (send[0], send[1], send[2], send[3], send[4], send[5],))
        # cursor.execute("INSERT INTO tovar (name, ulchov, narx, photo, tarifi) VALUES (?, ?, ?, ?, ?)", (data['name'], data['ulchov'], data['narx'], data['photo'], data['tarifi']))
        database.commit()

# cursor.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER, name TEXT, numb INTEGER)')
# database.commit()
# database.close()

def add_tovar(message):
    cursor.execute('INSERT INTO tovar (name) VALUES(?);', (message,))
    database.commit()

def katalog(message):
    cursor.execute("SELECT * FROM tovar")
    tovar = cursor.fetchall()
    for x in range(len(tovar)):
        print(x)
        # for y in range(tovar[x]):
        #     print(tovar[x][y])
        # print(tovar[0])
        # print(tovar[x])

    # print(list(tovar))

def delete_tovar(message):
    cursor.execute("DELETE FROM tasks WHERE id=?", (message,))
    database.commit()

def add_user(message):
    try:
        cursor.execute("SELECT * FROM 'users' WHERE id =?", (message.chat.id,))
        user = cursor.fetchone()
        # print(message.from_user.language_code)
        if not user:
            cursor.execute('INSERT INTO users (id, name, numb, lang) VALUES(?, ? ,?, ?);', (message.chat.id, message.chat.first_name, '14521', message.from_user.language_code))
            database.commit()
        else:
            cursor.execute('UPDATE users SET name=? && lang =? WHERE id=?', (message.chat.first_name, message.from_user.language_code, message.chat.id))
            return False
    except:
        pass
def add_user_name(message):
    cursor.execute('UPDATE users SET name=? WHERE id=?', (message.text, message.chat.id, ))
    database.commit()


def add_user_numb(message):
    cursor.execute('UPDATE users SET numb=? WHERE id=?', (message.contact.phone_number, message.chat.id, ))
    database.commit()
def add_user_location(message):
    cursor.execute('UPDATE users SET long=?, lat=? WHERE id=?', (message.location.longitude, message.location.latitude, message.chat.id, ))
    database.commit()

# def update_user(message):
#     cursor.execute('UPDATE users SET name=? WHERE id=?', (message.text, message.chat.id, ))
#     database.commit()
