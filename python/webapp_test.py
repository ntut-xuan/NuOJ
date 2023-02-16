# from cgi import test
# # import unittest
# import json
# import random
# import database_util
# import hashlib
# import os
# import re
# import base64
# import crypto_util
# import auth_util
# from flask import request
# from error_code import ErrorCode
# from uuid import uuid4
# from app import create_app
# from auth_util import password_cypto
# from tunnel_code import TunnelCode

# test_client = create_app()

# def register_test(handle, email, password):
#     data = json.dumps({"handle": handle, "email": email, "password": crypto_util.Encrypt(password)})
#     resp = test_client.post("/register", data=data, headers={"content-type": "application/json"})
#     return json.loads(resp.data)

# def login_test(account, password):
#     data = json.dumps({"account": account, "password": crypto_util.Encrypt(password)})
#     resp = test_client.post("/login", data=data, headers={"content-type": "application/json"})
#     return json.loads(resp.data)

# def get_cookie(cookie_header):
#     cookie_color = re.match('^session=([\\w.]+)', cookie_header)
#     cookie_match = str(cookie_color.group(1))
#     return cookie_match

# ''' LOGIN TEST START '''
# class LoginUnitTest(unittest.TestCase):

#     def setUp(self) -> None:
#         hash = hashlib.sha512(str("uriahxuan99").encode("utf-8")).hexdigest()
#         database_util.command_execute("INSERT INTO `user`(user_uid, handle, password, email, role, email_verified) VALUES(%s, %s, %s, %s, %s, %s)", (str(uuid4()), "uriahxuan", password_cypto(hash), "nuoj@test.net", 0, True))
#         return super().setUp()

#     def test_login_empty_handle(self):
#         data = login_test("", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.HANDLE_INVALID.value)
 
#     def test_login_invalid_handle_1(self):
#         data = login_test("__uriahxuan__", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.HANDLE_INVALID.value)
    
#     def test_login_invalid_handle_2(self):
#         data = login_test("uriah__xuan", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.HANDLE_INVALID.value)
    
#     def test_login_invalid_handle_3(self):
#         data = login_test("uriah--xuan", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.HANDLE_INVALID.value)
    
#     def test_login_invalid_handle_4(self):
#         data = login_test("        ", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.HANDLE_INVALID.value)

#     def test_login_invalid_email_1(self):
#         data = login_test("nuoj@ntut", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.EMAIL_INVALID.value)
    
#     def test_login_invalid_email_2(self):
#         data = login_test("nuoj@@ntut", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.EMAIL_INVALID.value)
    
#     def test_login_invalid_email_3(self):
#         data = login_test("nuoj@@ntut.", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.EMAIL_INVALID.value)

#     def test_login_regular_1(self):
#         hash = hashlib.sha512(str("uriahxuan99").encode("utf-8")).hexdigest()
#         data = login_test("uriahxuan", hash)
#         self.assertEqual(data["status"], "OK")
#         cookie_exist = next((cookie for cookie in test_client.cookie_jar if cookie.name == "SID"), None)
#         self.assertIsNotNone(cookie_exist)
#         cookie_encode = str(cookie_exist.value).encode()
#         self.assertEqual(auth_util.jwt_valid(cookie_encode), True)
#         self.assertEqual(auth_util.jwt_decode(cookie_encode)["handle"], "uriahxuan")
#         self.assertEqual(auth_util.jwt_decode(cookie_encode)["email"], "nuoj@test.net")
    
#     def test_login_regular_2(self):
#         hash = hashlib.sha512(str("uriahxuan99").encode("utf-8")).hexdigest()
#         data = login_test("nuoj@test.net", hash)
#         self.assertEqual(data["status"], "OK")
#         cookie_exist = next((cookie for cookie in test_client.cookie_jar if cookie.name == "SID"), None)
#         self.assertIsNotNone(cookie_exist)
#         cookie_encode = str(cookie_exist.value).encode()
#         self.assertEqual(auth_util.jwt_valid(cookie_encode), True)
#         self.assertEqual(auth_util.jwt_decode(cookie_encode)["handle"], "uriahxuan")
#         self.assertEqual(auth_util.jwt_decode(cookie_encode)["email"], "nuoj@test.net")
    
#     def tearDown(self) -> None:
#         database_util.command_execute("DELETE FROM `user` WHERE handle='uriahxuan'", ())
#         return super().tearDown()

# ''' REGISTER TEST START '''
# class RegisterUnitTest(unittest.TestCase):

#     def test_register_handle_empty(self):
#         data = register_test("", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.HANDLE_INVALID.value)

#     def test_register_invalid_handle_1(self):
#         data = register_test("__uriahxuan__", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.HANDLE_INVALID.value)
    
#     def test_register_invalid_handle_2(self):
#         data = register_test("uriah__xuan", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.HANDLE_INVALID.value)
        
#     def test_register_invalid_handle_3(self):
#         data = register_test("uriah@@xuan", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.HANDLE_INVALID.value)

#     def test_register_invalid_handle_4(self):
#         data = register_test("        ", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.HANDLE_INVALID.value)
    
#     def test_register_invalid_handle_3(self):
#         data = register_test("uriahuriahuriahuriahuriahuriahuriahuriahuriahuriahuriahuriah", str(uuid4()) + "@nuoj-unittest.net", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.HANDLE_INVALID.value)

#     def test_register_email_empty(self):
#         data = register_test("uriahxuan", "", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.EMAIL_INVALID.value)
    
#     def test_register_invalid_email_1(self):
#         data = register_test("uriahxuan", "nuoj@test", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.EMAIL_INVALID.value)

#     def test_register_invalid_email_2(self):
#         data = register_test("uriahxuan", "nuoj@test.", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.EMAIL_INVALID.value)
    
#     def test_register_invalid_email_3(self):
#         data = register_test("uriahxuan", "nuoj@@test.", str(uuid4()))
#         self.assertEqual(data["code"], ErrorCode.EMAIL_INVALID.value)

#     def test_register_password_invalid(self):
#         data = register_test("uriahxuan", "nuoj@test.net", "")
#         self.assertEqual(data["code"], ErrorCode.PASSWORD_INVALID.value)

#     def test_register_regular(self):
#         hash = hashlib.sha512(str("uriahxuan99").encode("utf-8")).hexdigest()
#         data = register_test("uriahxuan", "nuoj@test.net", hash)
#         self.assertEqual(data["status"], "OK")

#     def test_register_repeat_handle(self):
#         data = register_test("uriahxuan", "nuoj@test.net", "uriahxuan99")
#         self.assertEqual(data["code"], ErrorCode.HANDLE_EXIST.value)
    
#     def test_register_repeat_email(self):
#         data = register_test("uriahxuan88", "nuoj@test.net", "uriahxuan99")
#         self.assertEqual(data["code"], ErrorCode.EMAIL_EXIST.value)

#     def test_random_data_post(self):
#         data = json.dumps({"uriahxuan": "=="})
#         resp = test_client.post("/register", data=data, headers={"content-type": "application/json"}).data
#         self.assertEqual(json.loads(resp)["code"], ErrorCode.INVALID_DATA.value)
# '''
# SUBMIT TEST START
# class SubmitUnitTest(unittest.TestCase):

#     def setUp(self) -> None:

#         self.problem_pid = os.urandom(10).hex()
        
#         # add problem
#         database_util.command_execute("INSERT INTO `problem`(problem_pid, problem_author) VALUES(%s, %s)", (self.problem_pid, "uriahxuan"))

#         # add account
#         self.uid = str(uuid4())
#         database_util.command_execute("INSERT INTO `user`(user_uid, handle, password, email, role, email_verified) VALUES(%s, %s, %s, %s, %s, %s)", (self.uid, "uriahxuan", password_cypto(crypto_util.Encrypt(str("uriahxuan99"))), "nuoj@test.net", 0, True))
        
#         # login account
#         data = json.dumps({"account": "uriahxuan", "password": crypto_util.Encrypt(str("uriahxuan99"))})
#         resp = test_client.post("/login", data=data, headers={"content-type": "application/json"})

#         return super().setUp()
    
#     def test_invalid_id(self):
#         data = json.dumps({"code": "test123", "problem_id": 48763})
#         resp = test_client.post("/submit", data=data, headers={"content-type": "application/json"}).data
#         self.assertEqual(json.loads(resp)["code"], ErrorCode.INVALID_DATA.value)

#     def test_invalid_id(self):
#         data = json.dumps({"code": "test123", "problem_id": "AAABB"})
#         resp = test_client.post("/submit", data=data, headers={"content-type": "application/json"}).data
#         self.assertEqual(json.loads(resp)["code"], ErrorCode.INVALID_DATA.value)
    
#     def test_invalid_column(self):
#         data = json.dumps({"rrr": "hehe"})
#         resp = test_client.post("/submit", data=data, headers={"content-type": "application/json"}).data
#         self.assertEqual(json.loads(resp)["code"], ErrorCode.UNEXCEPT_ERROR.value)
    
#     def test_invalid_normal_submit(self):
#         # fetch problem id
#         ID = database_util.command_execute("SELECT ID FROM `problem` WHERE problem_author='uriahxuan'", ())[0]["ID"]
#         data = json.dumps({"code": "#include<bits/stdc++.h>using namespace std;int main(){int a, b;cin >> a >> b;cout << a + b << endl;}", "problem_id": ID})
#         resp = test_client.post("/submit", data=data, headers={"content-type": "application/json"}).data
#         self.assertEqual(json.loads(resp)["status"], "OK")
    
#     def tearDown(self) -> None:
#         database_util.command_execute("DELETE FROM `user` WHERE handle='uriahxuan'", ())
#         database_util.command_execute("DELETE FROM `problem` WHERE problem_author='uriahxuan'", ())
#         database_util.command_execute("DELETE FROM `submission` WHERE user_uid=%s", (self.uid))
#         return super().tearDown()
# '''

# ''' PROFILE TEST START '''
# class ProfileUnitTest(unittest.TestCase):
#     def setUp(self) -> None:
#         # add account and profile info
#         user_uid = str(uuid4())
#         database_util.command_execute("INSERT INTO `user`(user_uid, handle, password, email, role, email_verified) VALUES(%s, %s, %s, %s, %s, %s)", (user_uid, "uriahxuan", password_cypto(str("uriahxuan99")), "nuoj@test.net", 0, True))
#         database_util.command_execute("INSERT INTO `profile`(user_uid, email, school, bio) VALUES(%s, %s, %s, %s)", (user_uid, "nuoj@test.net", "", ""))
#         return super().setUp()
    
#     def test_regular_profile_info_put(self):
#         # login account
#         data = json.dumps({"account": "uriahxuan", "password": crypto_util.Encrypt("uriahxuan99")})
#         resp = test_client.post("/login", data=data, headers={"content-type": "application/json"})
#         resp_json = json.loads(resp.data)
#         self.assertEqual(resp_json["status"], "OK")

#         # update info
#         data = {"email": "nuoj_test_32767@nuoj.net", "school": "nuoj test university", "bio": "unit test start"}
#         json_data = json.dumps(data)
#         resp = test_client.put("/profile/uriahxuan/", data=json_data, headers={"content-type": "application/json"})
#         resp_json = json.loads(resp.data)
#         self.assertEqual(resp_json["status"], "OK")

#         # check data is correct
#         user_uid = database_util.command_execute("SELECT user_uid FROM `user` WHERE handle='uriahxuan'", ())[0]["user_uid"]
#         profile_data = database_util.command_execute("SELECT * FROM `profile` where user_uid=%s", (user_uid))[0]
#         self.assertEqual(profile_data["email"], data["email"])
#         self.assertEqual(profile_data["school"], data["school"])
#         self.assertEqual(profile_data["bio"], data["bio"])

#     def test_regular_profile_put(self):
#         # login account
#         data = json.dumps({"account": "uriahxuan", "password": crypto_util.Encrypt("uriahxuan99")})
#         resp = test_client.post("/login", data=data, headers={"content-type": "application/json"})
#         resp_json = json.loads(resp.data)
#         self.assertEqual(resp_json["status"], "OK")

#         # upload image
#         with open("/etc/nuoj/static/index.jpg", "rb") as img:
#             img_data = "data:image/jpg;base64," + base64.b64encode(img.read()).decode("utf-8")
#         data = {"img": img_data, "type": "jpg"}
#         resp = test_client.put("/upload_img", data=json.dumps(data), headers={"content-type": "application/json"})
#         resp_json = json.loads(resp.data)
#         self.assertEqual(resp_json["status"], "OK")

#         # check image is exist
#         user_uid = database_util.command_execute("SELECT user_uid FROM `user` WHERE handle='uriahxuan'", ())[0]["user_uid"]
#         self.assertTrue(database_util.file_storage_tunnel_exist(user_uid + ".jpg", TunnelCode.USER_AVATER))

#         # check image is correct
#         with open("/etc/nuoj/static/index.jpg", "rb") as img:
#             original_img_b64 = base64.b64encode(img.read()).decode("utf-8")
#         saved_img = database_util.byte_storage_tunnel_read(user_uid + ".jpg", TunnelCode.USER_AVATER)
#         saved_img_b64 = base64.b64encode(saved_img).decode("utf-8")
#         self.assertEqual(original_img_b64, saved_img_b64)

#     def tearDown(self) -> None:
#         user_uid = database_util.command_execute("SELECT user_uid FROM `user` WHERE handle='uriahxuan'", ())[0]["user_uid"]
#         database_util.command_execute("DELETE FROM `user` WHERE handle='uriahxuan'", ())
#         database_util.file_storage_tunnel_del(user_uid + ".jpg", TunnelCode.USER_AVATER)
#         return super().tearDown()

# if __name__ == "__main__":
#     crypto_util.GenerateKey()
#     unittest.main()
