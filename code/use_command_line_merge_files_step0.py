#直接在命令行中运行文件，将不同文件合并
import sys



tmp=sys.argv
date=tmp[1]
o_date=str(int(tmp[1])-1)
oo_date=str(int(tmp[1])-2)


#合并candidate
with open('../data/combine_candidate/candidate_merge_'+o_date+'.txt', 'w') as outFile:
    with open('../data/'+date+'/candidate_online_'+o_date+'.txt', 'r') as com, open('../data/combine_candidate/candidate_merge_'+oo_date+'.txt', 'r') as fort13:
        outFile.write(com.read())
        outFile.write(fort13.read())
print('succeed in merging candidate_infos!')

'''
#合并answer_infos
with open('../data/combine_answer_info/answer_infos_merge_'+o_date+'.txt', 'w') as outFile:
    with open('../data/'+date+'/answer_infos_'+o_date+'.txt', 'r') as com, open('../data/combine_answer_info/answer_infos_merge_'+oo_date+'.txt', 'r') as fort13:
        outFile.write(com.read())
        outFile.write(fort13.read())
print('succeed in merging answer infos!')
'''

#合并testing set
with open('../data/'+date+'/testing_set_'+o_date+'_merge.txt','w') as outFile:
    with open('../data/'+date+'/testing_set_'+o_date+'__LT_zyc.txt', 'r') as a, open('../data/'+date+'/testing_set_'+o_date+'_98K.txt', 'r') as b, open('../data/'+date+'/testing_set_'+o_date+'_大佬们加油！！！.txt', 'r') as c, open('../data/'+date+'/testing_set_'+o_date+'_广告位招租.txt', 'r') as d, open('../data/'+date+'/testing_set_'+o_date+'_了不起的盖茨比.txt', 'r') as e, open('../data/'+date+'/testing_set_' + o_date + '_南七技校了解一下.txt', 'r') as f, open('../data/' + date + '/testing_set_' + o_date + '_炮灰组合.txt', 'r') as g, \
          open('../data/' + date + '/testing_set_' + o_date + '_小渣渣.txt', 'r') as h, open('../data/' + date + '/testing_set_' + o_date + '_鱼丸.txt', 'r') as i, open('../data/' + date + '/testing_set_' + o_date + '_ARy.txt', 'r') as j, open('../data/' + date + '/testing_set_' + o_date + '_Baseline.txt', 'r') as k, open('../data/' + date + '/testing_set_' + o_date + '_DeepError.txt', 'r') as l, open('../data/' + date + '/testing_set_' + o_date + '_hfut_mars.txt', 'r') as m, open('../data/' + date + '/testing_set_' + o_date + '_insight.txt', 'r') as n, open('../data/' + date + '/testing_set_' + o_date + '_Lee.txt', 'r') as o, \
            open('../data/' + date + '/testing_set_' + o_date + '_papapa.txt', 'r') as p, open('../data/' + date + '/testing_set_' + o_date + '_RecSys_flappyBird.txt', 'r') as q, open('../data/' + date + '/testing_set_' + o_date + '_single_single_dog.txt', 'r') as r, open('../data/' + date + '/testing_set_' + o_date + '_Sunshine.txt', 'r') as s:
                outFile.write(a.read())
                outFile.write(b.read())
                outFile.write(c.read())
                outFile.write(d.read())
                outFile.write(e.read())
                outFile.write(f.read())
                outFile.write(g.read())
                outFile.write(h.read())
                outFile.write(i.read())
                outFile.write(j.read())
                outFile.write(k.read())
                outFile.write(l.read())
                outFile.write(m.read())
                outFile.write(n.read())
                outFile.write(o.read())
                outFile.write(p.read())
                outFile.write(q.read())
                outFile.write(r.read())
                outFile.write(s.read())

with open('../data/' + date + '/testing_set_' + o_date + '_merge.txt', 'a') as outFile:
    with open('../data/' + date + '/testing_set_' + o_date + '_Windchaser.txt', 'r') as u, open('../data/' + date + '/testing_set_' + o_date + '_trump.txt', 'r') as t:
        outFile.write(u.read())
        outFile.write(t.read())
print('succeed in merging testing set!')




