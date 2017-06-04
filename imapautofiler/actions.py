#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc

import imapclient


def factory(action_data, cfg):
    "Create an Action instance."
    name = action_data.get('name')
    if name == 'move':
        return Move(action_data, cfg)
    if name == 'delete':
        return Delete(action_data, cfg)
    if name == 'trash':
        return Trash(action_data, cfg)
    raise ValueError('unrecognized rule action {!r}'.format(action_data))


class Action(metaclass=abc.ABCMeta):

    def __init__(self, action_data, cfg):
        self._data = action_data
        self._cfg = cfg

    @abc.abstractmethod
    def invoke(self, conn, message_id, message):
        raise NotImplementedError()


class Move(Action):

    def __init__(self, action_data, cfg):
        super().__init__(action_data, cfg)
        self._dest_mailbox = self._data.get('dest-mailbox')

    def invoke(self, conn, message_id, message):
        conn.copy([message_id], self._dest_mailbox)
        conn.add_flags([message_id], [imapclient.DELETED])


class Trash(Move):

    def __init__(self, action_data, cfg):
        super().__init__(action_data, cfg)
        if self._dest_mailbox is None:
            self._dest_mailbox = cfg.get('trash-mailbox')
        if self._dest_mailbox is None:
            raise ValueError('no "trash-mailbox" set in config')


class Delete(Action):

    def invoke(self, conn, message_id, message):
        conn.add_flags([message_id], [imapclient.DELETED])
