'''
考虑candidate中所有涉及到的topic，每个topic作为key，对应的文章作为value生成字典；将字典输出到csv文件
'''

import pandas as pd
import pprint
import sys

tmp=sys.argv
date=str(int(tmp[1])-1)

#!edit
file='output_file/'+date+'candidate_feature.csv'
df=pd.read_csv(file,header=None)
df.columns = ['line_num','answer_id', 'question_id', 'anonymous', 'author_id', 'best_answer', 'editor_recommend',
                 'answer_create_time', 'has_Picture', 'has_Video', 'Thank_num', 'like_num', 'answer_comment_num',
                 'save_num', 'Reject_num', 'report_num', 'not_helpful_num', 'answer_text', 'answer_topic_id']

answer_topic={}
for a_id,t_id in zip(df.answer_id,df.answer_topic_id):
    if pd.isnull(t_id)!=True:
        for i in t_id.split(','):
            if i.strip() not in answer_topic:
                answer_topic[i.strip()]=[]
                answer_topic[i.strip()].append(a_id.strip())
            else:
                answer_topic[i.strip()].append(a_id.strip())

pprint.pprint(answer_topic)
import json

#!edit
with open('output_file/'+date+'candidate_topic_answer.json', 'w') as dump:
    dump.write(json.dumps(answer_topic))

