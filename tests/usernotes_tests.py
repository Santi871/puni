import os
import random
from time import sleep

import praw
import OAuth2Util
from puni import UserNotes, Note
from nose import with_setup

r = praw.Reddit('puni nosetests')
ini_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'oauth.ini'))
o = OAuth2Util.OAuth2Util(r, configfile=ini_path)

my_sub = r.get_subreddit('teaearlgraycold')


def setup_short_timeout():
    r.config.cache_timeout = -1.0


def teardown_short_timeout():
    r.config.cache_timeout = 30.0


@with_setup(setup_short_timeout, teardown_short_timeout)
def test_init_notes():
    """Assert that the puni init_notes function sends new JSON to the wiki page"""

    un = UserNotes(r, my_sub)
    un.init_notes()
    stored_json = un.get_json()

    assert stored_json['ver'] == un.schema
    assert stored_json['users'] == {}
    assert stored_json['constants']['users'] == [x.name for x in my_sub.get_moderators()]
    assert stored_json['constants']['warnings'] == Note.warnings


@with_setup(setup_short_timeout, teardown_short_timeout)
def test_add_note():
    """Assert that notes are added to the usernotes wiki page"""
    un = UserNotes(r, my_sub, lazy_start=True)

    note_message = "test note {}".format(random.random())
    new_note = Note("teaearlgraycold", note_message, warning='gooduser')

    un.add_note(new_note)
    stored_json = un.get_json()

    for note in stored_json['users']['teaearlgraycold']['ns']:
        if note['n'] == note_message:
            break
    else:
        assert False  # Did not reach a note with the sent message


@with_setup(setup_short_timeout, teardown_short_timeout)
def test_get_notes():
    """Assert that the puni get_notes function returns a list of Note objects"""
    un = UserNotes(r, my_sub, lazy_start=True)
    tea_notes = un.get_notes('teaearlgraycold')

    assert isinstance(tea_notes, list)
    assert isinstance(tea_notes[0], Note)


@with_setup(setup_short_timeout, teardown_short_timeout)
def test_remove_note():
    """Assert that notes are removed from the usernotes wiki page"""
    un = UserNotes(r, my_sub, lazy_start=True)
    un.remove_note('teaearlgraycold', 0)

    try:
        un.cached_json['users']['teaearlgraycold']
        assert False  # teaearlgraycold should have no notes, and no entry whatsoever
    except KeyError:
        pass
