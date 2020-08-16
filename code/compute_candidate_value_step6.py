'''
计算出每个candidate中answer的值，输出到文件（其中计算公式是使用初赛用xgboost计算得到的比例值）
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

#!edit
file='output_file/'+date+'candidate_feature.csv'
df=pd.read_csv(file,header=None)
df.columns=['old_index','answer_id','question_id','anonymous','author_id','best_answer','editor_recommend','answer_create_time','has_Picture','has_Video','Thank_num','like_num','answer_comment_num','save_num','Reject_num','report_num','not_helpful_num','answer_text','answer_topic_id']


an_weight=292/13598
best_weight=205/13598
edit_weight=99/13598
pic_weight=246/13598
vid_weight=363/13598
thank_weight=1838/13598
like_weight=2527/13598
comment_weight=2385/13598
save_weight=2225/13598
reject_weight=1824/13598
report_weight=213/13598
notHelp_weight=1381/13598


candidate_value=[]
for id, an, best, edit, pic, vid, thank, like, comment, save, reject, report, notHelp in zip(df.answer_id,
                                                                                             df.anonymous,
                                                                                             df.best_answer,
                                                                                             df.editor_recommend,
                                                                                             df.has_Picture,
                                                                                             df.has_Video,
                                                                                             df.Thank_num,
                                                                                             df.like_num,
                                                                                             df.answer_comment_num,
                                                                                             df.save_num,
                                                                                             df.Reject_num,
                                                                                             df.report_num,
                                                                                             df.not_helpful_num):
    score=an*an_weight+best*best_weight+edit*edit_weight \
    +pic*pic_weight+vid*vid_weight+thank*thank_weight+like*like_weight \
    +comment*comment_weight+save*save_weight+reject*reject_weight \
    +report*report_weight+notHelp*notHelp_weight
    if pd.isnull(id)!=True:
        single_score=[id,score]
        candidate_value.append(single_score.copy())


new_data=df.loc[df['answer_id'].isin(candidate_list)]
print(new_data.info())

new_list=df.answer_id.tolist()
for i in candidate_list:
    if i not in new_list:
        print(i)
        candidate_value.append([i,0])
print(len(candidate_value))

#!edit
with open("output_file/"+date+"candidate_value.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(['answer_id','value'])
    writer.writerows(candidate_value)
