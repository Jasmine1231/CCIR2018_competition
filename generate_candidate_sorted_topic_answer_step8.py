#将原先的topic answer中每个topic对应的answer按照值大小排个序

import json
import operator
import pandas as pd
import sys

tmp=sys.argv
date=str(int(tmp[1])-1)

#!edit
topic_candidate_file='output_file/'+date+'candidate_topic_answer.json'
with open(topic_candidate_file) as f:
    topic_answer_di=json.load(f)

#样例文章和值对应的字典
#!edit
candidate_value_file='output_file/'+date+'candidate_value.csv'
candidate_value_df=pd.read_csv(candidate_value_file)
candidate_value_dict={}
for an,va in zip(candidate_value_df.answer_id,candidate_value_df.value):
    candidate_value_dict[an]=va

#要考虑万一有的文章不在candidate value那个文件中，要特殊处理。有时候不能偷懒不用循环，会出现很大的问题、如果直接一行写掉的话，很多情况无法区别对待
result_dict={}
for new_topic,answers in topic_answer_di.items():
    line_dict={}
    for j in answers:
        if j in candidate_value_dict:
            line_dict[j]=candidate_value_dict[j]
    sorted_dict = sorted(line_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_list=[]
    for a in sorted_dict:
        sorted_list.append(a[0])
    result_dict[new_topic]=sorted_list.copy()



import json
#!edit
with open('output_file/'+date+'sorted_topic_answer.json', 'w') as dump:
    dump.write(json.dumps(result_dict))
