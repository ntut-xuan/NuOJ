import unittest
import json
import random
import database_util
import hashlib
import os
import re
import base64
import crypto_util
from error_code import ErrorCode
from uuid import uuid4
from nuoj_service import app
from auth_util import password_cypto

test_client = app.test_client()

def register_test(handle, email, password):
    data = json.dumps({"handle": handle, "email": email, "password": crypto_util.Encrypt(password)})
    resp = test_client.post("/register", data=data, headers={"content-type": "application/json"})
    return (json.loads(resp.data), resp.headers["Set-Cookie"])

def login_test(account, password):
    data = json.dumps({"account": account, "password": crypto_util.Encrypt(password)})
    resp = test_client.post("/login", data=data, headers={"content-type": "application/json"})
    return (json.loads(resp.data), resp.headers["Set-Cookie"])

def get_cookie(cookie_header):
    cookie_color = re.match('^session=([\\w.]+)', cookie_header)
    cookie_match = str(cookie_color.group(1))
    return cookie_match

''' LOGIN TEST START '''
class LoginUnitTest(unittest.TestCase):

    def setUp(self) -> None:
        hash = hashlib.sha512(str("uriahxuan99").encode("utf-8")).hexdigest()
        database_util.command_execute("INSERT INTO `user`(user_uid, handle, password, email, role, email_verified) VALUES(%s, %s, %s, %s, %s, %s)", (str(uuid4()), "uriahxuan", password_cypto(hash), "nuoj@test.net", 0, True))
        return super().setUp()
    
    def test_login_empty_handle(self):
        data = login_test("", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_INVALID.value)
 
    def test_login_invalid_handle_1(self):
        data = login_test("__uriahxuan__", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_INVALID.value)
    
    def test_login_invalid_handle_2(self):
        data = login_test("uriah__xuan", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_INVALID.value)
    
    def test_login_invalid_handle_3(self):
        data = login_test("uriah--xuan", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_INVALID.value)
    
    def test_login_invalid_handle_4(self):
        data = login_test("        ", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_INVALID.value)

    def test_login_invalid_email_1(self):
        data = login_test("nuoj@ntut", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.EMAIL_INVALID.value)
    
    def test_login_invalid_email_2(self):
        data = login_test("nuoj@@ntut", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.EMAIL_INVALID.value)
    
    def test_login_invalid_email_3(self):
        data = login_test("nuoj@@ntut.", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.EMAIL_INVALID.value)

    def test_login_regular_1(self):
        hash = hashlib.sha512(str("uriahxuan99").encode("utf-8")).hexdigest()
        data = login_test("uriahxuan", hash)
        self.assertEqual(data[0]["status"], "OK")
    
    def test_login_regular_2(self):
        hash = hashlib.sha512(str("uriahxuan99").encode("utf-8")).hexdigest()
        data = login_test("nuoj@test.net", hash)
        self.assertEqual(data[0]["status"], "OK")
    
    def tearDown(self) -> None:
        database_util.command_execute("DELETE FROM `user` WHERE handle='uriahxuan'", ())
        return super().tearDown()

''' REGISTER TEST START '''
class RegisterUnitTest(unittest.TestCase):

    def test_register_handle_empty(self):
        data = register_test("", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_INVALID.value)

    def test_register_invalid_handle_1(self):
        data = register_test("__uriahxuan__", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_INVALID.value)
    
    def test_register_invalid_handle_2(self):
        data = register_test("uriah__xuan", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_INVALID.value)
        
    def test_register_invalid_handle_3(self):
        data = register_test("uriah@@xuan", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_INVALID.value)

    def test_register_invalid_handle_4(self):
        data = register_test("        ", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_INVALID.value)
    
    def test_register_invalid_handle_3(self):
        data = register_test("uriahuriahuriahuriahuriahuriahuriahuriahuriahuriahuriahuriah", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_INVALID.value)

    def test_register_email_empty(self):
        data = register_test("uriahxuan", "", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.EMAIL_INVALID.value)
    
    def test_register_invalid_email_1(self):
        data = register_test("uriahxuan", "nuoj@test", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.EMAIL_INVALID.value)

    def test_register_invalid_email_2(self):
        data = register_test("uriahxuan", "nuoj@test.", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.EMAIL_INVALID.value)
    
    def test_register_invalid_email_3(self):
        data = register_test("uriahxuan", "nuoj@@test.", str(uuid4()))
        self.assertEqual(data[0]["code"], ErrorCode.EMAIL_INVALID.value)

    def test_register_password_invalid(self):
        data = register_test("uriahxuan", "nuoj@test.net", "")
        self.assertEqual(data[0]["code"], ErrorCode.PASSWORD_INVALID.value)

    def test_register_regular(self):
        hash = hashlib.sha512(str("uriahxuan99").encode("utf-8")).hexdigest()
        data = register_test("uriahxuan", "nuoj@test.net", hash)
        self.assertEqual(data[0]["status"], "OK")

    def test_register_repeat_handle(self):
        data = register_test("uriahxuan", "nuoj@test.net", "uriahxuan99")
        self.assertEqual(data[0]["code"], ErrorCode.HANDLE_EXIST.value)
    
    def test_register_repeat_email(self):
        data = register_test("uriahxuan88", "nuoj@test.net", "uriahxuan99")
        self.assertEqual(data[0]["code"], ErrorCode.EMAIL_EXIST.value)

    def test_random_data_post(self):
        data = json.dumps({"uriahxuan": "=="})
        resp = test_client.post("/register", data=data, headers={"content-type": "application/json"}).data
        self.assertEqual(json.loads(resp)["code"], ErrorCode.INVALID_DATA.value)

''' SUBMIT TEST START '''
class SubmitUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        # add problem
        database_util.command_execute("INSERT INTO `problem`(ID, problem_pid, problem_author) VALUES(%s, %s, %s)", (99999, os.urandom(10).hex(), "uriahxuan"))

        # add account
        database_util.command_execute("INSERT INTO `user`(user_uid, handle, password, email, role, email_verified) VALUES(%s, %s, %s, %s, %s, %s)", (str(uuid4()), "uriahxuan", password_cypto(crypto_util.Encrypt(str("uriahxuan99"))), "nuoj@test.net", 0, True))
        
        # login account
        data = json.dumps({"account": "uriahxuan", "password": crypto_util.Encrypt(str("uriahxuan99"))})
        resp = test_client.post("/login", data=data, headers={"content-type": "application/json"})
        return super().setUp()
    
    def test_invalid_id(self):
        data = json.dumps({"code": "test123", "problem_id": 48763})
        resp = test_client.post("/submit", data=data, headers={"content-type": "application/json"}).data
        self.assertEqual(json.loads(resp)["code"], ErrorCode.INVALID_DATA.value)

    def test_invalid_id(self):
        data = json.dumps({"code": "test123", "problem_id": "AAABB"})
        resp = test_client.post("/submit", data=data, headers={"content-type": "application/json"}).data
        self.assertEqual(json.loads(resp)["code"], ErrorCode.INVALID_DATA.value)
    
    def test_invalid_column(self):
        data = json.dumps({"rrr": "hehe"})
        resp = test_client.post("/submit", data=data, headers={"content-type": "application/json"}).data
        self.assertEqual(json.loads(resp)["code"], ErrorCode.UNEXCEPT_ERROR.value)
    
    def test_invalid_normal_submit(self):
        data = json.dumps({"code": "#include<bits/stdc++.h>using namespace std;int main(){int a, b;cin >> a >> b;cout << a + b << endl;}", "problem_id": 99999})
        resp = test_client.post("/submit", data=data, headers={"content-type": "application/json"}).data
        self.assertEqual(json.loads(resp)["status"], "OK")
    
    def tearDown(self) -> None:
        database_util.command_execute("DELETE FROM `problem` WHERE ID=99999", ())
        return super().tearDown()

if __name__ == "__main__":
    crypto_util.GenerateKey()
    unittest.main()
