import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('simple_bd.db')
    cur = base.cursor()
    if base:
        print('Data base connect OK!')
    base.execute('CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                 'product_id INT UNIQUE,'
                 'img TEXT,'
                 'name TEXT,'
                 'description TEXT,'
                 'price INT)')

    base.execute('CREATE TABLE IF NOT EXISTS cart(id         INTEGER PRIMARY KEY AUTOINCREMENT,'
                 'user_id    INT,'
                 'name       TEXT,'
                 'product_id INT,'
                 'count      INT)')
    base.commit()

async def add_users(user_id, name):
    cur.execute("""INSERT INTO users(user_id, name) VALUES (?,?)""",
                                       [user_id, name])
    base.commit()

#the admin adds the product to the menu
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO products(product_id, category_id, img, name, description, price) VALUES (?,?,?,?,?, ?)', tuple(data.values()))
        base.commit()
#
#async def sql_read(message):
#    for ret in cur.execute('SELECT * FROM products').fetchall():
#        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')

async def sql_read2():
    return cur.execute('SELECT * FROM products').fetchall()

async def get_product(category_id):
    return cur.execute('SELECT * FROM products WHERE category_id == ?',
                       [category_id]).fetchall()

async def get_user_product(product_id):
    return cur.execute('SELECT * FROM products WHERE product_id == ?', [product_id]).fetchall()

async def get_cart(user_id):
    return cur.execute('SELECT * FROM cart WHERE user_id == ?', [user_id]).fetchall()

async def add_to_cart(user_id, name, product_id):
    cur.execute('INSERT INTO cart (user_id, name, product_id, count) VALUES (?,?,?, ?)',
                       [user_id, name, product_id, 1])
    base.commit()

async def empty_cart(user_id):
    cur.execute('DELETE FROM cart WHERE user_id == ?', [user_id])
    base.commit()

#async def empty_cart(user_id):
#    return cur.execute('DELETE FROM products WHERE user_id=(?)', [user_id])

async def sql_delete_command(data):
    cur.execute('DELETE FROM products WHERE name == ?', (data,))
    base.commit()

async def get_categories():
    return cur.execute('SELECT * FROM categories').fetchall()

async def get_count_in_cart(user_id, product_id):
    return cur.execute('SELECT count FROM cart WHERE user_id == ?  AND product_id == ?',
                       [user_id, product_id]).fetchall()
async def get_count_in_cart1(user_id):
    return cur.execute('SELECT count FROM cart WHERE user_id == ?',
                       [user_id]).fetchall()


async def get_count_in_stock(product_id):
    return cur.execute("""SELECT count FROM products WHERE product_id=(?)""",
                       [product_id]).fetchall()


async def remove_one_item(product_id, user_id):
    cur.execute('DELETE FROM cart WHERE product_id == ? AND user_id == ?',
                       [product_id, user_id])
    base.commit()

async def change_count(count, product_id, user_id):
    cur.execute('UPDATE cart SET count=(?) WHERE product_id== ? AND user_id == ?',
                       [count, product_id, user_id])
    base.commit()