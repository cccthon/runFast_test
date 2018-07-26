#========================================================
#+++++++++++++++++  测试用例信息   ++++++++++++++++
# 用例  ID: QS_runFast_Register_Login_Load_Test
# 用例标题: 注册-登陆-加载
# 预置条件: 
# 测试步骤:
#   1.连接PHP；2.注册；3.登陆；4.load
# 预期结果:
#   1.获取sesskey；2.获取sesskeymid；3.获取到连接游戏服务的ip和port。
# 脚本作者: baoxiufen
# 写作日期: 20180412
#=========================================================


import requests
import json
import time
import sys
import yaml
import os
import unittest
sys.path.append("../../lib/runFast")
sys.path.append("../../lib/common")
import QS_pack,QS_runFast,QS_net_tcp,QSCommon

confData = yaml.load(open('../../conf/runFast/runFast.yml','r',encoding='utf-8')) 

class php_Register_Login_Load(unittest.TestCase):
    def setUp(self):
        '''注册php,登陆php,load.php'''
        pass

    def test_RegisterPhp(self):
        
        Register_json = {'sitemid':confData["sitemid"], 'method':'Amember.login', 'site':confData["site_id"], 
        'channel':confData["channel_id"], 'gp':confData["gp_id"],'pass':''}

        Register = requests.get( confData["php_base_url"] + json.dumps(Register_json) )
        RegisterSesskey = json.loads(Register.text)["data"]["sesskey"]


    def test_LoginPhp(self):
        login_json = {'sitemid': confData["sitemid"], 'method':'Amember.login', 'site': confData["site_id"], 
        'channel': confData["channel_id"], 'gp': confData["gp_id"], 'pass': ''}
        login = requests.get( confData["php_base_url"] + json.dumps(login_json) )
        loginSesskey = json.loads(login.text)["data"]["sesskey"]
        loginSesskey1 = json.loads(login.text)


    def test_load(self):
        login_json = {'sitemid': confData["sitemid"], 'method':'Amember.login', 'site': confData["site_id"], 
        'channel': confData["channel_id"], 'gp': confData["gp_id"], 'pass': ''}
        login = requests.get( confData["php_base_url"] + json.dumps(login_json) )
        loginSesskey = json.loads(login.text)["data"]["sesskey"]

        load_json = {'method':'Amember.load','sesskey':loginSesskey}
        load = requests.get(confData["php_base_url"] + json.dumps(load_json) )


    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
