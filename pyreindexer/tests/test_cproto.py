import unittest

import shutil
import pyreindexer

# TODO Add more tests. Just checking that builtin binding is installed for sure


class TestCproto(unittest.TestCase):
    def setUp(self):
        self.db = pyreindexer.RxConnector('cproto://127.0.0.1:6534/db1')
        self.namespace = 'test_namespace'

        try:
            self.db.namespace_open(self.namespace)
        except Exception as ex:
            self.fail('open_namespace raised: ' + str(ex))

    def tearDown(self):
        self.db.namespace_close(self.namespace)
        self.db.close()

    def test_item_select(self):
        try:
            self.db.index_add(self.namespace, dict(name='id',json_paths=['id'],
                              is_pk=True,field_type='int',
                              index_type='hash'))
            self.db.item_insert (self.namespace,{'id':100, 'val':"testval"})
            ret = list (self.db.select ("SELECT * FROM " + self.namespace + " WHERE id=" + str(100)))
            assert (len(ret) == 1)
            assert (ret[0]['id'] == 100)
            assert (ret[0]['val'] == 'testval')

        except Exception as ex:
            self.fail('test_item_select raised: ' + str(ex))
