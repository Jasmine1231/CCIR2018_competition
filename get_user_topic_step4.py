import pandas as pd
import json
import time
import os
import re
import sys

'''
找到用户关注的topic

输入:
当天日期

依赖文件:
step1中生成的用户索引文件
topic索引字典文件
每天的user_info.txt

输出:
用户主题对应文件

输出说明:
输出的用户与主题均为索引
'''

def isMatch(str):
    pattern=re.compile('^2018.*')
    res=pattern.findall(str)
    if len(res)>0:
        return True
    else:
        return False

root='/home/jasmine/projects/final_CCIR2018/data/'#该文件中存储在线测试所有文件
tmp=sys.argv
date=tmp[1]
middle_root='/diskc/jasmine/hin_spotlight/'#该文件夹中存储step1中生成的中间文件
ofile=middle_root+'user_topic_'+date+'.txt'

'''
以下代码载入用户和topic对应index的文件
'''
user_dict_file=middle_root+'testing_user_dict_'+date+'.json'
topic_dict_file=root+'../code2/output_file/topic_dict.json'
user_dict_file=open(user_dict_file)
json_str=user_dict_file.read()
user_index_dic=eval(json_str)


topic_dict_file=open(topic_dict_file)
json_str=topic_dict_file.read()
topic_index_dic=eval(json_str)
print('user_dict and topic dict is loaded!')


'''
开始处理user 和topic 对应关系
'''

w=open(ofile,'w')
chunksize=2**10
index=0
for directory in os.listdir(root):
    if not isMatch(directory):#说明不是数据文件夹
        continue
    print('test: '+directory)
    data_date=str(int(directory)-1)
    if directory=='20180801':
        data_date='20180731'
    user_file=root+directory+'/user_infos_'+data_date+'_insight.txt'
    for chunk in  pd.read_table(user_file,chunksize=chunksize,header=None,error_bad_lines=False,delimiter='\t',lineterminator='\n',
                          names=('user_id','regist_time','sex','freq',
                                 'following_user_num','following_topic_num','following_que_num','commit_ans_num',
                                 'ask_que_num','commint_comment_num','ans_liked_num','ans_commented_num',
                                 'cons_num','neg_num','reg_type','reg_platform',
                                 'is_android','is_iphone','is_ipad','is_pc',
                                 'is_web','is_model','device_brand','user_platform',
                                 'province','city','topic_list'
                                 )):
        index+=1
        print('chunk:'+str(index))
        for user_id,topic_list in zip(chunk.user_id,chunk.topic_list):
            try:
                if user_id not in user_index_dic.keys():
                    continue
                uidx=user_index_dic[user_id]
                for topic in topic_list.split(','):
                    if topic not in topic_index_dic.keys():
                        continue
                    tidx=topic_index_dic[topic]
                    w.write(str(uidx)+' '+str(tidx)+'\n')
            except Exception as e:
                #print(e)
                pass

w.close()

print('finished!')
