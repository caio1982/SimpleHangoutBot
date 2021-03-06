# -*- coding: utf-8 -*-

'''
Hashtag Manager

This addon parses #hashtags and add them to a searchable database
'''

from ..addon import Addon, ADDON
from ..database import Database
import time


_NAME = 'hashtag'


class _HashtagDatabase(Database):

    def __init__(self, addon):
        super().__init__(addon)

    def create_table(self):
        if not self.table_exists('hashtag'):
            self.query('CREATE TABLE hashtag(name VARCHAR, conversation VARCHAR, user VARCHAR, time INTEGER, text VARCHAR);')
            self.commit()

    def insert(self, name, conversation_id, user_id, time, text):
        try:
            self.query("INSERT INTO hashtag(name, conversation, user, time, text) VALUES ('{}','{}','{}',{},'{}');".format(name, conversation_id, user_id, time, text))
            self.commit()
            return True
        except:
            return False

    def get_hashtags(self, conversation_id, max_len=400):
        result = self.query("SELECT DISTINCT name FROM hashtag WHERE conversation='{}';".format(conversation_id))
        list = ''
        for l in result:
            list += ' #' + l[0]
        return list


class _HashtagAddon(Addon):

    version = '(dev)'

    def __init__(self, config, name=_NAME):
        super().__init__(config, name)
        self._db = _HashtagDatabase(self)
        self._db.create_table()

    def get_parsers(self):
        return [
            (r'#(\w+)', self._do_save_text),
            (r'^hashtags$', self._do_list_hashtags)
        ]

    def _do_save_text(self, conversation, from_user, match, reply):
        """Save text"""
        var = match.group(1).lower()
        self.report('save with tag #{}: {}'.format(var, match.string))
        self._db.insert(var, conversation.id_, from_user.id_.chat_id, int(time.time()), match.string)

    def _do_list_hashtags(self, conversation, from_user, match, reply):
        """List existing hashtags"""
        self.report("list hashtags")
        reply(conversation, self._db.get_hashtags(conversation.id_))


ADDON[_NAME] = _HashtagAddon

