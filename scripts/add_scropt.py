from loader import scheduler, cursor, con, bot, Bot
import os
import json
from scripts.scheduler_training import scheduler_training

def add(bot: Bot):
    scheduler.remove_all_jobs()
    dir_files = os.listdir('data/user_json')
    for file in dir_files:
        if 'sample' not in file:
            with open(f'data/user_json/{file}', 'r', encoding='utf-8') as file_:
                data = json.loads(file_.read())
            id_user = data['id_user']
            sc = scheduler.add_job(scheduler_training, trigger='cron', hour=data['time_training'].split(':')[0],
                                   minute=data['time_training'].split(':')[1],
                                   kwargs={'bot': bot, 'id_user': id_user})
            cursor.execute('update users set id_scheduler=(?) where id=(?)', (sc.id, id_user))
            con.commit()
    print(scheduler.get_jobs())
