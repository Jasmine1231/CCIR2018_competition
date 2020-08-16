# -*- coding: utf-8 -*-


import pandas as pd
import json
import os
import re
import sys

'''
输入:
当天日期

依赖文件:
今天及以前的test文件,文章短id与长id对应文件

输出:
#生成三个中间文件
#今天的用户id与索引对应字典文件
#今天用户这几天看的文章对应的字典文件,用户与文章均为索引值.
#所有的话题id与索引对应字典文件

输出说明:
以上索引均为从1开始的整数.

'''
def extract_read_answer_id(read_history):
    line_content=[]
    result=[]
    for i in read_history.split(','):
        line_content.append(i)
    for a in line_content:
        article=a.split("|")
        read_time=int(article[2])
        if read_time==0:
            continue
        if article[0][0]=='A':
            if article[0][1:] not in result:
                result.append(article[0][1:])
    return result

#产生短名字和原名的对应字典
def generate_name_dict(file2,di):
    df = pd.read_table(file2, header=None)
    df.columns = ['short_name', 'name']
    for sh, na in zip(df.short_name, df.name):
        di[str(sh)] = na

def isMatch(str):
    pattern=re.compile('^2018.*')
    res=pattern.findall(str)
    if len(res)>0:
        return True
    else:
        return False

'''
所有文件夹的用户字典
'''
root='/home/jasmine/projects/final_CCIR2018/data/'#存储在线测试数据的文件夹
middle_root='/diskc/jasmine/hin_spotlight/'#存储生成的中间文件的文件夹
tmp=sys.argv
date=tmp[1]
data_date=str(int(date)-1)

testing_user_dict_file=middle_root+'testing_user_dict_'+date+'.json'
user_article_dict_file=middle_root+'user_article_'+date+'.txt'
testing_article_dict_file=middle_root+'testing_article_dict_'+date+'.json'

'''
生成test用户id和index对应的字典
'''
user_di={}
i=1
for directory in os.listdir(root):
    if not directory==date:#只要今天的用户
        continue
    if not isMatch(directory):#说明不是数据文件夹
        continue
    print('test: '+directory)
    cur_data_date=str(int(directory)-1)
    if directory=='20180801':
        cur_data_date='20180731'
    file=root+directory+'/testing_set_'+cur_data_date+'_insight.txt'
    with open(file,encoding='utf-8') as f:
        content = f.readlines()
    for index,line in enumerate(content):
        user_id=line.split('\t')[0]
        if user_id not in user_di.keys():
            user_di[user_id]=i
            i+=1

with open(testing_user_dict_file, 'w',) as fp:
    json.dump(user_di, fp,ensure_ascii=False)

print('total  user: '+str(len(user_di.keys())))


'''
#生成所有test中用户阅读历史中的文章和对应index的字典
'''
answer_dict={}
for directory in os.listdir(root):
    if not isMatch(directory):#说明不是数据文件夹
        continue
    print('answer_dict: '+directory)
    cur_data_date = str(int(directory) - 1)
    if directory=='20180801':
        cur_data_date='20180731'
    answer_dict_file=root+directory+'/answer_id_'+cur_data_date+'.dict'
    generate_name_dict(answer_dict_file,answer_dict)

'''
# 生成所有的article字典
'''

testing_answer_idx_dic={}

'''
生成user_index article_index 文件
'''
i=1
w=open(user_article_dict_file,'w')
for directory in os.listdir(root):
    if not isMatch(directory):#说明不是数据文件夹
        continue
    cur_data_date = str(int(directory) - 1)
    if directory=='20180801':
        cur_data_date='20180731'

    print('test: '+directory)
    file = root + directory + '/testing_set_' + cur_data_date + '_insight.txt'
    test_df=pd.read_table(file,header=None,delimiter='\t')
    test_df.columns=['user_id','read_number','read_history','search_number','search_history']
    for id,read in zip(test_df.user_id,test_df.read_history):
        if id not in user_di.keys():
            continue
        uidx=user_di[id]
        if not pd.isnull(read):
            articles=extract_read_answer_id(read)
            for a in articles:#短id
                if a in answer_dict.keys():
                    real=answer_dict[a]#长id
                    idx=0
                    if real not in testing_answer_idx_dic.keys():
                        testing_answer_idx_dic[real] = i
                        i += 1

                    idx=testing_answer_idx_dic[real]
                    w.write(str(uidx)+' '+str(idx)+'\n')


w.close()


print('testing_anser_idx_dic.len:'+str(len(testing_answer_idx_dic.keys())))
with open(testing_article_dict_file, 'w') as fp:
    json.dump(testing_answer_idx_dic, fp,ensure_ascii=False)

print('generate name dict finished!')
print('answer in answer info: '+str(len(answer_dict.keys())))






