import os
import angular_flask
import unittest
import tempfile
import json
from angular_flask.core import db


class DjCyKoTestCase(unittest.TestCase):

    def setUp(self):
        angular_flask.app.config.from_object('angular_flask.settings.TestingConfig')
        self.db_fd, angular_flask.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = angular_flask.app.test_client()
        db.create_all()


    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(angular_flask.app.config['DATABASE'])
        db.drop_all()

    def test_register(self):
        response = self.register("Testname","password")
        assert 'success' in response.data
        response = self.register("Testname","password")
        assert 'failure' in response.data

    def test_login(self):
        self.register("Testname","password")
        response = self.login("Testname","password")
        assert "true" in response.data

        response = self.login("Not A Name","password")
        assert "false" in response.data

        response = self.login("Testname","Not The Password")
        assert "false" in response.data

    def test_logout(self):
        self.register("Testname","password")
        self.login("Testname","password")
        response = self.logout("Testname")
        assert "success" in response.data

        response = self.logout("Testname")
        assert "success" in response.data

        response = self.logout("Testname")
        assert "success" in response.data

        response = self.logout("Not A Name")
        assert "failure" in response.data


    def register(self, username, password):
        return self.app.post('/api/register',data=json.dumps({
            'username': username,
            'password': password}), content_type='application/json', follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/api/login', data=json.dumps({
            'username': username,
            'password': password}), content_type='application/json', follow_redirects=True)

    def logout(self, username):
        return self.app.post('/api/logout', data=json.dumps({
        'username': username}),content_type='application/json',follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
