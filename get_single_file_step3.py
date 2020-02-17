import pandas as pd
import sys


'''
输入:
当天日期

依赖文件:
用户索引对应文件
文章索引对应文件
topic索引对应文件

输出:
用户索引文件
文章索引文件
topic索引文件

输出说明:
每个索引一行
'''


root='/home/jasmine/projects/final_CCIR2018/data/'
middle_root='/diskc/jasmine/hin_spotlight/'
tmp=sys.argv
date=tmp[1]
user_dict_file=middle_root+'testing_user_dict_'+date+'.json'
article_dict_file=middle_root+'testing_article_dict_'+date+'.json'
topic_dict_file=root+'../code2/output_file/topic_dict.json'

user_file=middle_root+'users_'+date+'.txt'
article_file=middle_root+'article_'+date+'.txt'
topic_file=middle_root+'topic_'+date+'.txt'


user_dict_file=open(user_dict_file)
json_str=user_dict_file.read()
user_index_dic=eval(json_str)

article_dict_file=open(article_dict_file)
json_str=article_dict_file.read()
article_index_dic=eval(json_str)

topic_dict_file=open(topic_dict_file)
json_str=topic_dict_file.read()
topic_index_dic=eval(json_str)
print('user_dict topic dic and article dict is loaded!')


user_w=open(user_file,'w')
article_w=open(article_file,'w')
topic_w=open(topic_file,'w')

for key in user_index_dic.keys():
    user_w.write(str(user_index_dic[key])+'\n')
for key in article_index_dic.keys():
    article_w.write(str(article_index_dic[key])+'\n')
for key in topic_index_dic.keys():
    topic_w.write(str(topic_index_dic[key])+'\n')

user_w.close()
article_w.close()
topic_w.close()