import pandas as pd
import time
import json
import sys

start=time.time()
tmp=sys.argv
date=tmp[1]
root='/home/jasmine/projects/final_CCIR2018/data/'+date+'/'
date=str(int(date)-1)
test_file=root+'testing_set_'+date+'_insight.txt'
user_file=root+'user_infos_'+date+'_insight.txt'
ofile_name='../code2/output_file/'+date+'user_in_test_like_topic.json'

users_dic={}
chunksize=2**20
print('start loading users.csv.............')
for chunk in pd.read_table(test_file,error_bad_lines=False,chunksize=chunksize,delimiter='\t',lineterminator='\n'):
    chunk.columns=['user_id','read_num','hist','search_num','search_hist']
    for user_id in zip(chunk.user_id):
        users_dic[user_id[0]]=True
print('load users.csv finished!')

user_num=0
user_without_topic_num=0
user_notin_user_info_num=0
user_like_topic_dic={}
index=0
chunksize=2**20
for chunk in  pd.read_table(user_file,chunksize=chunksize,error_bad_lines=False,delimiter='\t',lineterminator='\n',
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
        if user_id not in users_dic.keys():
            user_notin_user_info_num+=1
            continue
        try:
            #print(topic_list)
            #tmp=topic_list.split(',')
            #print(len(tmp))
            user_num+=1
            tmp=topic_list.split(',')
            user_like_topic_dic[user_id]=tmp
            
        except Exception as e:
            print(topic_list)
           # print(e)
            user_without_topic_num+=1
            pass

print('testing join user_info: '+str(user_num))
print('user_info - testing num: '+str(user_notin_user_info_num))
print('user like topic num: '+str(len((user_like_topic_dic.keys()))))
print('user without topic number: '+str(user_without_topic_num))
ofile=open(ofile_name,'w')
json.dump(user_like_topic_dic,ofile)

end=time.time()
print('finished!')
print('saved in '+ofile_name)
print('time: ',end-start)
