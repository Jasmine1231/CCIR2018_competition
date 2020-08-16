#根据测试集中用户的topic找到推荐给他的相应的文章.冷启动用户推荐分数最高的文章
#改进v1.1 topic answer在输入时已经有序
#改进v1.2 在最终代码的时候，如果用户阅读历史推荐的topic不满100篇，则推荐用户关注的topic，也是按比例推荐文章
#improve v1.2, if user has no like topicis , then recommend his gender topic articles


import pandas as pd
import json
import pprint
import operator
import math
import csv
import time
import sys

'''
生成方法一的推荐结果

输入:
当天日期

依赖文件:
用户这几天的阅读历史
method1.py生成的用户topic文件
其他方法生成的最终结果
用户关注话题
经过排序过的候选集

输出:
在线推荐结果
'''

root='/home/jasmine/projects/final_CCIR2018/code2/output_file/'#该文件存储所有在线测试的文件
middle_root='/diskc/jasmine/hin_spotlight/'#该文件存储
tmp=sys.argv
date=tmp[1]
data_date=str(int(date)-1)
duplicate_dict_file='/home/jasmine/projects/final_CCIR2018/code/output_file/others/GXY/user_all_read_history.json'#用户前几天阅读历史
result_file=middle_root+'result/result_method1_'+date+'.csv'#method1.py生成的用户 topic字典文件
other_method='/home/jasmine/projects/final_CCIR2018/code/result_fastText_'+data_date+'_v1.csv'#其他方法的结果
user_topic_file=middle_root+'user_read_topic_'+date+'.json'
user_follow_topics_file=root+data_date+'user_in_test_like_topic.json'
candidate_file='/home/jasmine/projects/final_CCIR2018/code2/output_file/'+data_date+'candidate_value.csv'

#user_basic_info_file='output_file/others/GXY/user_basic_info.json'
candidate_value_file=root+data_date+'candidate_value.csv'
topic_candidate_file=root+data_date+'sorted_topic_answer.json'

start=time.time()
#导入用户——topic字典

with open(user_topic_file) as f:
    data=json.load(f)


#生成user和关注topic对应的字典

with open(user_follow_topics_file) as f:
    user_follow_topic_di=json.load(f)


#样例文章和值对应的字典

candidate_value_df=pd.read_csv(candidate_value_file)
candidate_value_dict={}
for an,va in zip(candidate_value_df.answer_id,candidate_value_df.value):
    candidate_value_dict[an]=va
new_sorted_candidate = sorted(candidate_value_dict.items(), key=operator.itemgetter(1), reverse=True)

#话题和文章对应的字典

with open(topic_candidate_file) as f:
    topic_answer_di=json.load(f)



#处理空值情况,总的计数去掉空值计数
for user,topics in data.items():
    for name,value in topics.items():
        if name=='topics':
            for a,b in value.items():
                if not a:
                    topics['total']-=b


#remove the duplicate

duplicate_dict_file=open(duplicate_dict_file)
json_str=duplicate_dict_file.read()
duplicates=eval(json_str)

print('the duplicate file is loaded!')

w=open(result_file,'w')
first=True
result=[]
df=pd.read_csv(other_method,header=None,delimiter='\t',lineterminator='\n',names=('uid','result',))
cur_index=0
for user,result in zip(df.uid,df.result):
    print(cur_index)
    cur_index+=1

    count=0
    recommended={}
    if user in duplicates.keys():
        recommended_list=duplicates[user]
        for r in recommended_list:
            recommended[r]=True
    answer_list=[]
    if (user not in data) or (not data[user]['topics']):
        pass
        # count=0
    else:
        topics=data[user]
        totalnum=topics['total']
        for name,value in topics.items():
            #找到topic下的id
            if name=='topics':
                #一个有序的列表，将id-frequency变为（id,frequency）,按照frequency降序排列
                sorted_value = sorted(value.items(), key=operator.itemgetter(1),reverse=True)
                #给一个用户推荐的文章个数统计
                # count=0
                for i in sorted_value:
                    #找热门topic对应的文章
                    if i[0] in topic_answer_di:
                        if count<10:
                            #print('count: '+str(count))
                            fre=i[1]/totalnum
                            #向上取整
                            answer_num=math.ceil(fre*10)
                            #print('answer_num: '+str(answer_num))
                            #找出该topic下所有文章id
                            answers=topic_answer_di[i[0]]
                            #对于一个话题下的文章列表构造一个字典，key为answer id，值为value（即文章价值）
                            try:
                                answer_count = 0
                                for a in answers:
                                    if count == 10:
                                        break
                                    if answer_count < answer_num:
                                        #name = a[:4] + a[-4:]
                                        name=a
                                        if name not in answer_list and name not in recommended.keys() :
                                            answer_list.append(name)
                                            answer_count += 1
                                            count += 1
                            except KeyError as e:
                                print(e)
                                pass

    #如果用户阅读历史推荐的topic不满100篇，则推荐用户关注的topic
    if count<10:
        remaining_num=10-count
        if user in user_follow_topic_di:
            to_recommends=user_follow_topic_di[user]
            follow_topic_number=len(to_recommends)
            for rec in to_recommends:
                if rec in topic_answer_di:
                    if count < 10:
                        fre = 1 / follow_topic_number
                        # 向上取整
                        f_topic_num = math.ceil(fre * remaining_num)
                        #print('f_topic_num: '+str(f_topic_num))
                        # 找出该topic下所有文章id
                        answers = topic_answer_di[rec]
                        # 对于一个话题下的文章列表构造一个字典，key为answer id，值为value（即文章价值）
                        try:
                            answer_count = 0
                            for a in answers:
                                if count == 10:
                                    break
                                if answer_count < f_topic_num:
                                    #name = a[:4] + a[-4:]
                                    name=a
                                    if name not in answer_list and name not in recommended.keys() :
                                        answer_list.append(name)
                                        answer_count += 1
                                        count += 1
                        except KeyError as e:
                            print(e)
                            pass


    #用户标签下的文章推荐完了还没到100,推荐分数最高的文章
    while count<10:
        for a in new_sorted_candidate:
            if count<10:
                name=a[0]
                #name=a[0][:4]+a[0][-4:]
                if name not in answer_list and name not in recommended.keys() :
                    answer_list.append(name)
                    count+=1
            else:
                break
    if count<10:
        other_num=10-count
        print('use other uesult: '+str(other_num))
        other_result = []
        for a in result.split(','):
            a = a[:32]
            other_result.append(a)
        for r in other_result:
            if r not in answer_list:
                answer_list.append(r)
                count+=1
            if count>=10:
                break

    l=user+'\t'
    index=1
    for answer in answer_list[:10]:
        l+=answer+'@'+str(index)
        index+=1
        l+=','
    l=l[:-1]
    l+='\n'
    w.write(l)
    answer_list=[]


#输出到csv文件


end=time.time()

print('time: ',end-start)

print('the result is saved in '+str(result_file))



