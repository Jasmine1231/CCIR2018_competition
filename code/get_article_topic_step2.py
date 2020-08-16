import pandas as pd
import traceback
import os
import re
import sys
'''
输入:
当天日期

依赖文件:
今天及以前的test文件,文章短id与长id对应文件

输出:
article_topic 元组

输出说明:
假设在线测试开始日期为D1,今天日期为D2,那么这份代码得到的时D2当天的用户从D1到D2这几天数据中看的所有文章和其对应topic的字典.
其中文章和topic均为索引(其id与索引id对应关系由step1生成)
输入:step1中 得到的topic字典,测试集中article字典
在线测试每天的answer_info文件
'''

def clean_str(s):
    s=s.replace('\t','').replace(' ','')
    return s

def isMatch(str):
    pattern=re.compile('^2018.*')
    res=pattern.findall(str)
    if len(res)>0:
        return True
    else:
        return False

root='/home/jasmine/projects/final_CCIR2018/data/'#该文件夹下存有在线测试给的每天的数据
middle_root='/diskc/jasmine/hin_spotlight/'#该文件夹下面存储的是step1生成的中间文件
tmp=sys.argv
date=tmp[1]
data_date=str(int(date)-1)
article_dict_file=middle_root+'testing_article_dict_'+date+'.json'#step1生成的文章字典
topic_dict_file=root+'../code2/output_file/topic_dict.json'#step1生成的主题字典
article_topic_ofile=middle_root+'article_topic_'+date+'.txt'#输出文件
candidate_file='/home/jasmine/projects/final_CCIR2018/code2/output_file/'+data_date+'candidate_value.csv'

article_dict_file=open(article_dict_file)
json_str=article_dict_file.read()
article_index_dic=eval(json_str)

topic_dict_file=open(topic_dict_file)
json_str=topic_dict_file.read()
topic_index_dic=eval(json_str)
print('article dict and topic dict  is loaded!')




'''
从answer info 中找到答案对应的topic
'''

w=open(article_topic_ofile,'w')
for directory in os.listdir(root):#从这几天的数据中找到article topic
    if not isMatch(directory):#说明不是数据文件夹
        continue
    data_date = str(int(directory) - 1)
    if directory=='20180801':
        data_date='20180731'
    print(directory)
    file=root+directory+'/answer_infos_'+data_date+'.txt' #每天的answer_info文件
    df=pd.read_table(file,names=('aid','2','3','4','5','6','7','8',
                                 '9','10','11','12','13','14','15',
                                 '16','17','topics'),delimiter='\t',lineterminator='\n',header=None)
    for aid,topics in zip(df.aid,df.topics):
        if aid not in article_index_dic.keys():
            continue
        aidx=article_index_dic[aid]
        try:
            if len(topics)<10:#没有topic
                continue
            for topic in topics.split(','):
                if topic not in topic_index_dic.keys():
                    continue
                tidx=topic_index_dic[topic]
                w.write(str(aidx)+' '+str(tidx)+'\n')#写入
        except Exception as e:
            print(e)
            continue



w.close()
