from flask import Flask, render_template, request, g
from . import db
import sqlite3
import os
import datetime
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "main.db")
#DATABASE_PATH = 'main.db'


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/pka/<episode>', methods=['GET'])
def get_pka_epsiode(episode):
    '''Page consisting of list of guests present on the episode and a list of
    events from that episode.

    :param episode: Episode number
    '''
    cur = get_db().cursor()

    guest_list = db.all_episode_guests(cur, 'pka', episode)

    guest_list = [{'id': x[0], 'name': x[1]} for x in guest_list]
  
    
    
    cur.close()

    return render_template(
        'episode.html',
        show_name='PKA',
        episode=episode,
        guest_list=guest_list
    )


@app.route('/guest/id/<guest_id>', methods=['GET'])
def get_guest(guest_id: int):
    cur = get_db().cursor()
    
    # get list of dicts of episode appearances
    tmp_appearances = db.all_guest_appearances_by_id(cur, guest_id)
    appearance_list = [{'show_name': 'PKA' if x[0] == 1 else 'PKN','episode': x[1]} for x in tmp_appearances]
    
    # get total runtime and convert to a nicer format
    total_runtime = db.total_guest_runtime(cur, guest_id)

    seconds = total_runtime % 60
    total_runtime = total_runtime // 60
    minutes = total_runtime % 60
    hours = total_runtime // 60

    runtime_str = f'{hours} hours, {minutes} minutes, and {seconds} seconds'

    # get the guest's name    
    guest_name = db.guest_name_by_id(cur, guest_id)

    cur.close()

    return render_template(
        'guest.html', 
        appearance_list=appearance_list, 
        runtime=runtime_str,
        guest_name=guest_name    
    )



"""
#TODO change this to a search
@app.route('/guest/name/<guest_name>')
def get_guest_by_name(guest_name):
    cur = get_db().cursor()
    guest_list = db.all_guest_appearances_by_name(cur, guest_name)
    cur.close()
    return '\n'.join(map(lambda x: f'<li>{x[1]}</li>', guest_list))
"""







# get database from context
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
    return db

# destroy database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()