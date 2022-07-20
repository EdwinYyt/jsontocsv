#!/usr/bin/python
#-coding: UTF-8-

import sys
import os
import json
import pandas as pd

text1 = sys.argv[1]
text2 = sys.argv[2]

if os.path.exists(text1) == False or os.path.exists(text2) == False:
    print ('file not exists')
    exit(0)

fp1 = open(text1,'r')
fp2 = open(text2,'r')

fline1 = fp1.read()
fline2 = fp2.read()
fp1.close()
fp2.close()

fjson1 = json.loads(fline1)
fjson2 = json.loads(fline2)
res1 = ['关键词']
res2 = ['翻译']
r1 = ['精准']
r2 = ['广泛']
r3 = ['词组']

last = None
for x in fjson1['localizedKeywordResponses']:
    keyword = x['sourceKeyword']['keyword']
    cn_keyword = x['localizedKeywords']['zh_CN']['keyword']
    if last != keyword:#数据去重
        res1.append(str(keyword))
        res2.append(str(cn_keyword))
        last = keyword

for x in res1:
    for y in fjson2['keywordTargetList']:
        if y['keyword'] == x:
            c1 = 0
            c2 = 0
            c3 = 0
            for z in y['bidInfo']:
                if z['theme'] == 'CONVERSION_OPPORTUNITIES':
                    if z['matchType'] == 'EXACT':
                        r1.append(str(z['suggestedBid']['rangeMedian']))
                        c1 += 1
                    if z['matchType'] == 'BROAD':
                        r2.append(str(z['suggestedBid']['rangeMedian']))
                        c2 += 1
                    if z['matchType'] == 'PHRASE':
                        r3.append(str(z['suggestedBid']['rangeMedian']))
                        c3 += 1
            if c1 == 0:#不存在的数据补“-”
                r1.append('-')
            if c2 == 0:
                r2.append('-')
            if c3 == 0:
                r3.append('-')

res1 = pd.DataFrame(res1)
res2 = pd.DataFrame(res2)
r1 = pd.DataFrame(r1)
r2 = pd.DataFrame(r2)
r3 = pd.DataFrame(r3)

fin = pd.concat([res1,res2,r1,r2,r3],axis=1)
fin.to_csv('data.csv',encoding='utf-8')

print ('Done\n')
