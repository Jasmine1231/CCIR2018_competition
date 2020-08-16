'''
将candidate中所有文章与answer数据中的特征相关联，输出到文件中
'''

import pandas as pd
import csv
import sys



tmp=sys.argv
date=str(int(tmp[1])-1)


#!edit
file='../data/combine_candidate/candidate_merge_'+date+'.txt'
candidate=pd.read_table(file,header=None,delimiter='\t')

candidate.columns=['sample_id']
candidate_list=candidate.sample_id.tolist()
print(len(candidate_list))

#!edit
infofile='../data/combine_answer_info/answer_infos_merge_'+date+'.txt'

candidate_feature=[]
chunk = pd.read_table(infofile,header=None,delimiter='\t',error_bad_lines=False,lineterminator='\n')
chunk.columns=['answer_id','question_id','anonymous','author_id','best_answer',
                    'editor_recommend','answer_create_time','has_Picture','has_Video',
                    'Thank_num','like_num','answer_comment_num','save_num','Reject_num',
                    'report_num','not_helpful_num','answer_text','answer_topic_id']
new_data=chunk.loc[chunk['answer_id'].isin(candidate_list)]
print(new_data.info())

'''
new_list=chunk.answer_id.tolist()
for i in candidate_list:
    if i not in new_list:
        print('have no info ids:'+i)
'''

#!edit
with open('output_file/'+date+'candidate_feature.csv', 'w') as f:
    new_data.to_csv(f, header=False)


'''
#有一些candidate中的文章没有任何info
answer_list=chunk.answer_id.tolist()

for i in candidate_list:
    if i not in answer_list:
        print(i)
'''
