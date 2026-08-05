import pandas
import requests as rq
import re
url='https://push2.eastmoney.com/api/qt/clist/get?np=1&fltt=1&invt=2&cb=jQuery371013196730427954917_1776693857300&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A81%2Bs%3A262144%2Bf%3A!2&fields=f12%2Cf13%2Cf14%2Cf1%2Cf2%2Cf4%2Cf3%2Cf152%2Cf5%2Cf6%2Cf7%2Cf15%2Cf18%2Cf16%2Cf17%2Cf10%2Cf8%2Cf9%2Cf23&fid=f3&pn=1&pz=20&po=1&dect=1&ut=fa5fd1943c7b386f172d6893dbfba10b&wbp2u=%7C0%7C0%7C0%7Cweb&_=1776693857302'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'}
try:
    response=rq.get(url,headers=headers,timeout=15)
    response.raise_for_status()
    print("请求成功！")
except rq.exceptions.ConnectionError:
    print("连接失败！")
except rq.exceptions.Timeout:
    print("请求超时！")
except rq.exceptions.HTTPError as e:
    print(f"http错误:{e}")
except Exception as e:
    print(f"未知错误:{e}")
namelist=re.findall(r'"f14":"(.*?)","f15"',response.text)
increasing=re.findall(r'"f3":(.*?),"f4"',response.text)
for i in range(len(namelist)):
    print(namelist[i],increasing[i])

