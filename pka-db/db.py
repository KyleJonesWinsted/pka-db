"""DB interaction"""

import sqlite3
from typing import Tuple, List

#TODO figure out how to add 136.5


def all_episode_events(cur: sqlite3.Cursor, show: str, ep_num: int) -> List[Tuple[int, str]]:

    show = show.lower()
    show_id = 0
    if show == 'pka':
        show_id = 1
    elif show == 'pkn':
        show_id = 2
    else:
        #TODO throw exception?
        return

    return cur.execute('''
    select timestamp, description from events
    where show = ? and episode = ?
    ''', (show_id, ep_num)).fetchall()

def all_episode_guests(cur: sqlite3.Cursor, show: str, ep_num: int) -> List[Tuple[int, str]]:
    '''Gets all guests that were on a given episode

    :param cur: DB cursor

    :param show: Name of the show ('pka' or 'pkn')

    :param ep_num: Episode number
    '''
    show = show.lower()
    show_id = 0
    if show == 'pka':
        show_id = 1
    elif show == 'pkn':
        show_id = 2
    else:
        #TODO specify exception
        raise Exception()
    
    return cur.execute('''
    select guest_id, name from guests
    where guest_id in (
        select guest_id from appearances
        where appearances.show = ? and appearances.episode = ?
    )
    ''', (show_id, ep_num)).fetchall()


def all_guest_appearances_by_id(cur: sqlite3.Cursor, guest_id: int) -> List[Tuple[int, int]]:
    '''Finds all apperances of a given guest id

    :param cur: DB cursor

    :param guest_id: Guest id in the DB
    '''
    return cur.execute('''
    select show, episode from appearances
    where appearances.guest_id in (
	    select guest_id from guests
	    where guests.guest_id = ?
    )
    order by episode desc
    ''', (guest_id,))

def guest_name_by_id(cur: sqlite3.Cursor, guest_id: int) -> str:

    return cur.execute('''
    select name from guests
    where guest_id = ?
    ''', (guest_id,)).fetchone()[0]

def total_guest_runtime(cur: sqlite3.Cursor, guest_id: int) -> int:

    pka_runtime = cur.execute('''
    select sum(runtime) from episodes
    where episode in (
        select episode from appearances
        where guest_id = ?
    )
    and show = 1
    ''', (guest_id,)).fetchone()[0]

    print(f'pka runtime: {pka_runtime}', flush=True)

    pkn_runtime = cur.execute('''
    select sum(runtime) from episodes
    where episode in (
        select episode from appearances
        where guest_id = ?
    )
    and show = 2
    ''', (guest_id,)).fetchone()[0]

    if pka_runtime is None:
        pka_runtime = 0

    if pkn_runtime is None:
        pkn_runtime = 0



    print(f'pkn runtime: {pkn_runtime}', flush=True)

    return pka_runtime + pkn_runtime



"""
#TODO change this toa  search
def all_guest_appearances_by_name(cur: sqlite3.Cursor, guest_name: str) -> List[Tuple[int, int]]:
    '''Get each apperance (show_id, episode_num) of all guests that match `guest_name`

    :param cur: Database cursor

    :param guest_name: Guest name to search in the database
    '''
    guest_name = f'%{guest_name}%'

    return cur.execute('''
    select show, episode from appearances
    where appearances.guest_id in (
	    select guest_id from guests
	    where guests.name like ?
    )
    order by episode asc''', (guest_name,)).fetchall()
"""
#print(2 + 2)
#print(all_guest_appearances_by_name(sqlite3.connect('main.db').cursor(), 'Awz'))
