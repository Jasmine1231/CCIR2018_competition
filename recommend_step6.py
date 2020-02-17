# -*- coding: utf-8 -*-
# @Time    : 8/3/18 4:38 AM
# @Author  : zxl
# @FileName: recommend.py
import pandas as pd
import operator
from datetime import datetime
import sys

'''
根据 用户 文章 value 三元组生成最终推荐结果

输入:
当天日期,迭代日期

依赖文件:

文章索引字典文件
用户所以呢字典文件
用户阅读历史文件
候选集文件
其他方法生成的在线推荐结果文件

输出:
在线推荐结果
'''

start=datetime.now()
tmp=sys.argv
date=tmp[1]
method=tmp[2]

root='/home/jasmine/projects/final_CCIR2018/data/'
middle_root='/diskc/jasmine/hin_spotlight/'
data_date=str(int(date)-1)
article_dict_file=middle_root+'testing_article_dict_'+date+'.json'
user_dict_file=middle_root+'testing_user_dict_'+date+'.json'

duplicate_dict_file='/home/jasmine/projects/final_CCIR2018/code/output_file/others/GXY/user_all_read_history.json'

candidate_file='/home/jasmine/projects/final_CCIR2018/code2/output_file/'+data_date+'candidate_value.csv'

other_method='/home/jasmine/projects/final_CCIR2018/code/result_fastText_'+data_date+'_v1.csv'#其他方法的结果


#sim_file=middle_root+'sim_spotlight_150_20180804.txt'
sim_file=''
if method=='spotlight':
    sim_file=middle_root+method+'_'+date+'.txt'
else:
    sim_file = middle_root + method + '_' + date + '.res'
#sim_file=middle_root+'sim_spotlight_150_20180804.txt'

result_file=middle_root+'result/'+'result_'+method+'_'+date+'.csv'

article_dict_file=open(article_dict_file)
json_str=article_dict_file.read()
aid2ind=eval(json_str)
ind2aid={}
for key in aid2ind.keys():
    ind2aid[aid2ind[key]]=key

user_dict_file=open(user_dict_file)
json_str=user_dict_file.read()
uid2ind=eval(json_str)
ind2uid={}
for key in uid2ind.keys():
    ind2uid[uid2ind[key]]=key
print ('article dict user dict is load!')

#找到candidate中在test中的文章

candidate_in_test={}#放的时索引
df =pd.read_table(candidate_file,header=None,names=('aid','2','3'),delimiter=',',lineterminator='\n')
for aid in df.aid.values:
    if aid in aid2ind.keys():#这个candidate在test里面
        candidate_in_test[aid2ind[aid]]=True
print('candidate: '+str(len(candidate_in_test.keys())))




#remove the duplicate

duplicate_dict_file=open(duplicate_dict_file)
json_str=duplicate_dict_file.read()
duplicates=eval(json_str)
print('the duplicate file is loaded!')

#find the score

user_article={}
tmp_dic={}
last_uidx=-1
chunksize=2**10
recommend={}
for chunk in pd.read_table(sim_file,header=None,chunksize=chunksize,names=('uidx','iidx','score'),delimiter='\t',lineterminator='\n'):

    for uidx,iidx,score in zip(chunk.uidx,chunk.iidx,chunk.score):

    # if uidx not in user_article.keys():
    #     user_article[uidx]={}
    # user_article[uidx][iidx]=float(score)
        if last_uidx !=uidx  : # a new user
            print(last_uidx)

            if last_uidx!=-1:
                i=0
                cur_uid=ind2uid[last_uidx]
                if cur_uid in duplicates.keys():
                    recommended=duplicates[cur_uid]# we have recommend the user such items
                else:
                    recommended=[]
                last_uid=ind2uid[last_uidx]
                recommend[last_uid]=[]
                sorted_articles = sorted(tmp_dic[last_uidx].items(), key=operator.itemgetter(1), reverse=True)
                for item in sorted_articles:
                    score=float(item[1])
                    if score<0:
                        continue
                    cur_iidx = item[0]
                    if i >= 10:  # 推荐够了
                        break
                    if cur_iidx not in ind2aid.keys():
                        print('not in')
                        continue
                    a=ind2aid[cur_iidx]
                    if a in recommended:# already recommended
                        continue
                    if cur_iidx in candidate_in_test.keys():
                        i += 1
                        recommend[cur_uid].append(a)
            tmp_dic[uidx]={}
        last_uidx=uidx
        tmp_dic[uidx][iidx]=float(score)

#the last user
i=0
cur_uid=ind2uid[last_uidx]
if cur_uid in duplicates.keys():
    recommended=duplicates[cur_uid]# we have recommend the user such items
else:
    recommended=[]
last_uid=ind2uid[last_uidx]
recommend[last_uid]=[]
sorted_articles = sorted(tmp_dic[last_uidx].items(), key=operator.itemgetter(1), reverse=True)
for item in sorted_articles:
    cur_iidx = item[0]
    if i >= 10:  # 推荐够了
        break
    if cur_iidx not in ind2aid.keys():
        print('not in')
        continue
    a=ind2aid[cur_iidx]
    if a in recommended:# already recommended
        continue
    if cur_iidx in candidate_in_test.keys():
        i += 1
        recommend[cur_uid].append(a)


w=open(result_file,'w')







num=0
#原来的结果
df=pd.read_csv(other_method,header=None,delimiter='\t',lineterminator='\n',names=('uid','result',))
for uid ,result in zip(df.uid,df.result):

    if uid in recommend.keys():
        my_result=recommend[uid]
    else:
        my_result=[]
    # other_result=[]
    # for a in result.split(','):
    #     a=a[:32]
    #     other_result.append(a)

    if len(my_result)<10:
        num+=1
        print('other results: '+str(10-len(my_result)))
        for other_result in result.split(','):
            other_a=other_result[:32]
            if other_a not in my_result:
                my_result.append(other_a)
            if len(my_result)==10:
                break

    my_result_str=''
    index=1
    for r in my_result:
        my_result_str+=r+'@'+str(index)
        index+=1
        my_result_str+=','
    my_result_str=my_result_str[:-1]
    w.write(uid+'\t'+my_result_str+'\n')
w.close()

print('use other result: '+str(num))
end=datetime.now()
print('seconds: '+str((end-start).seconds))
