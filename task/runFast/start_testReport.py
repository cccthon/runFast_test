import os,re

#获取本机ip
ipList = os.popen("ipconfig |findstr IPv4|findstr 192.168")
getIP = re.findall('192.168' + '.\d+.\d+',ipList.read())
localIP = str(", ".join(tuple(getIP)))

print(localIP)

curr_path = os.getcwd()
# main_path = os.path.dirname(os.getcwd())

print(curr_path)
main_path = curr_path.split('task')[0]

#停止测试报告，如果存在
killTestReport = "docker rm -f testReport"
testReportTask = "docker ps -a |findstr testReport"
testReport = os.system(testReportTask)
# print(testReport)

if 0 == testReport:
    os.system(killTestReport)

#启动测试报告
# startTestReport = '''docker run -d -v %s/report:[Finished in 0.2s]/home -p %s:9527:9527 --restart=always --name testReport test_report sh -c "nginx -c /etc/nginx/nginx.conf;tail -f /etc/nginx/nginx.conf"''' % (curr_path,localIP)
startTestReport = '''docker run -d -v %s/report:/home -p %s:9527:9527 --restart=always --name testReport test_report sh -c "nginx -c /etc/nginx/nginx.conf;tail -f /etc/nginx/nginx.conf"''' % (main_path,localIP)
# print(startTestReport)[Finished in 0.2s]
os.system(startTestReport)
os.system(testReportTask)
if 1 == os.system(testReportTask):
    print("testReport start fail.")
else:
    print("testReport start succ.")
