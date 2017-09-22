import dataset as ds
import datetime
from app.cnf import db_url
db = ds.connect(db_url)
import psycopg2
connect = psycopg2.connect(db_url)
cursor = connect.cursor()

def get_worker_info(user_id):
    users = db['users']
    worker = users.find_one(worker_id=user_id)
    return worker

def get_customer_info(user_id):
    customers = db['customers']
    customer = customers.find_one(customer_id=user_id)
    return customer
    
def insert_worker(user_id, vk_id, qiwi_wallet):
    users = db['users']
    return users.insert(dict(worker_id =user_id, vk_id=vk_id, qiwi_wallet=qiwi_wallet))

def insert_customer(customer_id, qiwi_wallet):
    customers = db['customers']
    return customers.insert(dict(customer_id=customer_id, qiwi_wallet=qiwi_wallet))
    
def insert_new_task(customer_id, amount, object_link, type_task):
    date = datetime.datetime.now()
    status = 1
    tasks = db['tasks']
    return tasks.insert(dict(customer_id=customer_id, type=type_task, amount=amount, object_link=object_link, status=status, date=date))
    
def check_aval_task_for_this_user(user_id):
    cursor.execute("""              
       SELECT id, type, object_link 
       FROM tasks tsk
       WHERE tsk.id not in 
           (SELECT task_id 
            FROM tasks_to_users
            WHERE user_id = {})
            """.format(user_id))
    return cursor
    

def get_task_user(user_id):
    cursor.execute("""  
    SELECT id, task_id
    FROM tasks_to_users
    where user_id = {}""".format(user_id))
    res = cursor.fetchone()
    return res
    
def assign_task_to_user(user_id):
    cursor.execute("""  
    INSERT INTO tasks_to_users
    (task_id, user_id)
    values(1, {0})""".format(user_id))
    return True	