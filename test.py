import sqlite3 as sq


with sq.connect("baza_bot.db") as con:
    cur = con.cursor()

sql_request = """CREATE TABLE IF NOT EXISTS users (
    id TEXT NOT NULL,
    name TEXT,
    first_part INTEGER DEFAULT 0,
    nostalgist INTEGER DEFAULT 0,
    patriot INTEGER DEFAULT 0,
    antagonist INTEGER DEFAULT 0
)"""

con.execute(sql_request)


with sq.connect("baza_bot.db") as con:
    sql_request = "INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)"
con.execute(sql_request, (89532752588, 'user_name', 5, 6, 7, 8))
con.commit()


with sq.connect("baza_bot.db") as con:
    cur = con.cursor()

cur.execute(
    "SELECT first_part, nostalgist, patriot, antagonist FROM users WHERE id = 89532752588")

rows = cur.fetchall()

rows2 = rows[0]

first_part, nostalgist, patriot, antagonist = rows2

print(first_part)
print(nostalgist)
print(patriot)
print(antagonist)
