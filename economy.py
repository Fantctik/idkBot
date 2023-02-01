import sqlite3
import random
import time

#подключение переменных

conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()

def createTable():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (name TEXT, balance BIGINT, balanceBank BIGINT)""")
    conn.commit()

#создание кошелька

def createUser(name:str):
    cursor.execute(f"SELECT name FROM users WHERE name = '{name}'")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{name}', '{100}', {0})")
        conn.commit()
    else:
        return 1

#add-money

def add_money(user:str, count:int):
    cursor.execute(f"SELECT name FROM users WHERE name = '{user}'")
    if cursor.fetchone() is None:
        createUser()
    else:
        cursor.execute(f"UPDATE users SET balance = balance + {count} WHERE name = '{user}'")
        conn.commit()

#remove-money

def remove_money(user:str, count:int):
    cursor.execute(f"SELECT name FROM users WHERE name = '{user}'")
    if cursor.fetchone() is None:
        createUser()
    else:
        cursor.execute(f"UPDATE users SET balance = balance - {count} WHERE name = '{user}'")
        conn.commit()

#work

def work(user:str):
    timer = round(int(time.time()))
    cursor.execute(f"UPDATE users SET balanceBank = {timer} WHERE name = '{user}'") #balanceBank используется как таймер, потому что не нашлось приминения в проекте
    conn.commit()
    count = random.randint(1, 1000)
    cursor.execute(f"SELECT name FROM users WHERE name = '{user}'")
    if cursor.fetchone() is None:
        createUser()
    else:
        cursor.execute(f"UPDATE users SET balance = balance + {count} WHERE name = '{user}'")
        conn.commit()
        return count

#casino

def casino(user:str, count:int):
    win_or_lose = random.randint(0, 1)
    if count >= 100:
        cursor.execute(f"SELECT name FROM users WHERE name = '{user}'")
        if cursor.fetchone() is None:
            createUser()
        else:
            cursor.execute(f"SELECT balance FROM users WHERE name = '{user}'")
            if cursor.fetchone()[0] >= count:
                if win_or_lose == 1:
                    cursor.execute(f"UPDATE users SET balance = balance + {count} WHERE name = '{user}'")
                    conn.commit()
                    return 2
                else:
                    cursor.execute(f"UPDATE users SET balance = balance - {count} WHERE name = '{user}'")
                    conn.commit()
                    return 0
            else:
                return 4
    else:
        return 3

def balance(user:str):
    cursor.execute(f"SELECT name FROM users WHERE name = '{user}'")
    if cursor.fetchone() is None:
        createUser()
    else:
        many_money = cursor.execute(f"SELECT CAST(balance AS INT) FROM users WHERE name = '{user}'")
        result = cursor.fetchone()
        return result[0]

createTable()

if __name__ == "__main__":
    for value in cursor.execute("SELECT * FROM users"):
        print(value)