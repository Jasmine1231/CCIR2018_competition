import pandas as pd
import json
import time
import datetime
import re
import os
from datetime import datetime
import sys
import traceback
'''
在线测试的版本
取当天用户
从这些天这些用户阅读的文章中找到其文章关联话题,作为用户近期喜欢的话题

输入:
当天日期

依赖文件:
step1中生成的用户索引对应文件,topic索引对应文件
每天的answer_infos.txt, answer_id.dict, question_infos.txt, question_id.dict.

输出:
用户与topic的对应文件

输出说明:
用户真实id,topic真实id,输出文件为json格式{'uid':{'topics':{'topic_id':num},'total':''}}
其中uid与topic_id均为用户与topic的真实id,num为该用户阅读文章中含该topic的文章数目,total是该用户阅读所有文章对应所有topic的数量.
'''
# find topic of a article with id equals convert_id
def getTopics(dic,convert_id):
    if convert_id not in dic.keys():
        return []

    topic=dic[convert_id][1]

    topic=topic.replace('\t','').replace(' ','').replace('\n','').replace('\r','').replace('\\','')
    res=topic.split(',')
    if len(topic)<10:
        res=[]

    return res
def isMatch(str):
    pattern=re.compile('^2018.*')
    res=pattern.findall(str)
    if len(res)>0:
        return True
    else:
        return False

#产生短名字和原名的对应字典
def generate_name_dict(file2,di):
    df = pd.read_table(file2, header=None)
    df.columns = ['short_name', 'name']
    for sh, na in zip(df.short_name, df.name):
        di[str(sh)] = [na]

start=datetime.now()
root='/home/jasmine/projects/final_CCIR2018/data/'#此文件夹中存储在线测试生成的所有文件
middle_root='/diskc/jasmine/hin_spotlight/'#此文件夹中存储的是生成的中间文件

tmp=sys.argv
date=tmp[1]
data_date=str(int(date)-1)
user_file=middle_root+'testing_user_dict_'+date+'.json'#step1中的用户索引字典文件
result_file=middle_root+'user_read_topic_'+date+'.json'#输出 用户 topci对应文件
ans_file='data/ans_info.csv'
que_file='data/que_info.csv'


user_dic=json.load(open(user_file,'r'))
print('users: '+str(len(user_dic.keys())))

#生成所有test中用户阅读历史中的文章和对应index的字典
'''
生成文章短id,长id与对应topic的文件
'''
ans_dic={}
for directory in os.listdir(root):
    if not isMatch(directory):#说明不是数据文件夹
        continue
    cur_date=directory
    cur_data_date = str(int(cur_date) - 1)
    if directory=='20180801':
        cur_data_date='20180731'
    answer_dict_file=root+cur_date+'/answer_id_'+cur_data_date+'.dict'
    generate_name_dict(answer_dict_file,ans_dic)

#long_name topics
ans_topic_dic={}
for directory in os.listdir(root):#从这几天的数据中找到article topic
    if not isMatch(directory):#说明不是数据文件夹
        continue
    cur_date=directory
    cur_data_date = str(int(cur_date) - 1)
    if directory=='20180801':
        cur_data_date='20180731'

    file=root+cur_date+'/answer_infos_'+cur_data_date+'.txt'
    df=pd.read_table(file,header=None,names=('aid','2','3','4','5','6','7','8',
                                 '9','10','11','12','13','14','15',
                                 '16','17','topics'),delimiter='\t',lineterminator='\n')
    for aid,topics in zip(df.aid,df.topics):
        ans_topic_dic[aid]=topics
for key in ans_dic.keys():
    long_name=ans_dic[key][0]
    if long_name in ans_topic_dic.keys():
        topics=ans_topic_dic[long_name]
        try:
            if len(topics)<10:
                topics=''
        except Exception as e:
            topics=''
        ans_dic[key].append(topics)
print('answers: '+str(len(ans_dic.keys())))

'''

生成问题的短id 长id与对应topic的对应文件
'''
que_dic={}
for directory in os.listdir(root):
    if not isMatch(directory):#说明不是数据文件夹
        continue
    cur_date=directory
    cur_data_date = str(int(cur_date) - 1)
    if directory=='20180801':
        cur_data_date='20180731'
    question_dict_file=root+cur_date+'/question_id_'+cur_data_date+'.dict'
    generate_name_dict(question_dict_file,que_dic)

#long_name topics
que_topic_dic={}
for directory in os.listdir(root):#从这几天的数据中找到article topic
    if not isMatch(directory):#说明不是数据文件夹
        continue
    cur_date=directory
    cur_data_date = str(int(cur_date) - 1)
    if directory=='20180801':
        cur_data_date='20180731'

    file=root+cur_date+'/question_infos_'+cur_data_date+'.txt'
    df=pd.read_table(file,header=None,names=('aid','2','3','4','5','6','7','topics'),delimiter='\t',lineterminator='\n')
    for aid,topics in zip(df.aid,df.topics):
        que_topic_dic[aid]=topics
for key in que_dic.keys():
    long_name=que_dic[key][0]
    if long_name in que_topic_dic.keys():
        topics=que_topic_dic[long_name]
        try:
            if len(topics)<10:
                topics=''
        except Exception as e:
            topics=''
        que_dic[key].append(topics)


print('question: '+str(len(que_dic.keys())))

user_topic={}
chunksize=2**10

'''
遍历所有的test文件,找到该用户阅读全部文章/问题,进而找到用户 与阅读过的文章/问题对应话题的对应文件.
'''
for directory in os.listdir(root):
    if not isMatch(directory):#说明不是数据文件夹
        continue

    print('test: '+directory)
    cur_data_date=str(int(directory)-1)
    if directory=='20180801':
        cur_data_date='20180731'
    test_file=file=root+directory+'/testing_set_'+cur_data_date+'_insight.txt'
    for chunk in pd.read_table(test_file,header=None,delimiter='\t',error_bad_lines=False,
                           chunksize=chunksize):
        chunk.columns = ['user_id', 'read_number', 'read_history', 'search_number', 'search_history']
        #print('chunk :' +str(index))
        #index+=1
        for user_id,read_num,read_history in zip(chunk.user_id,chunk.read_number,chunk.read_history):
            try:
                if user_id not in user_dic.keys():#not our user
                    continue
                if user_id not in user_topic.keys():
                    user_topic[user_id] = {}
                    user_topic[user_id]['total'] = 0
                    user_topic[user_id]['topics'] = {}

                if read_num == 0:
                    continue

                # read_history = item[2]#read_history
                articles = read_history.split(',')
                for article in articles:
                    arr=article.split('|')
                    if(len(arr)<3):
                        print('arr: '+str(arr))
                    article=arr[0]
                    read_time=arr[2]
                    if read_time==0:#该用户没有阅读过该文章
                        continue
                    art_type = article[0]
                    art_id = article[1:]
                    topics = []
                    if art_type == 'A':
                        topics = getTopics(ans_dic, art_id)
                    else:
                        topics = getTopics(que_dic, art_id)

                    user_topic[user_id]['total'] += len(topics)
                    for topic in topics:
                        if len(topic)==0 or topic=="":
                            user_topic[user_id]['total'] -= 1
                            continue
                        if topic not in user_topic[user_id]['topics'].keys():
                            user_topic[user_id]['topics'][topic] = 0
                        user_topic[user_id]['topics'][topic] += 1
            except Exception as e:
                continue

ofile=open(result_file,'w')
json.dump(user_topic,ofile)
end=datetime.now()

print('time:',str((end-start).seconds)+' seconds')
