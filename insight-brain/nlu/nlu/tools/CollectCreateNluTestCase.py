#!/usr/bin/env python
# coding=utf-8
"""
@Author  : gaosongbo
@Contact : gaosongbo@knowin.com
@File    : CollectCreateNluTestCase.py
@Time    : 2020/3/5 4:47 下午
"""

import pymysql
from pymysql.cursors import DictCursor
import yaml
import re
import json


def create_testcase():
    conn = pymysql.connect(
        host='39.100.203.200',
        port=3306,
        user='rd',
        password='qQun1lIeg0cR',
        db='nlu',
        # charset='utf8mb4'
    )
    cur = conn.cursor(cursor=DictCursor)
    cur.execute(
        'select i.intent, p.re_pattern, p.pattern_id,p.re_group from t_pattern p join t_intent i on p.intentid = i.intentid;')
    datas = cur.fetchall()
    testcases = []
    t_id = 1
    for d in datas:
        assert_list = [{'eq': '$.intents.0.domain, iot'}]
        slots = re.findall(re.compile('\((.*?)\)'), d['re_pattern'])
        for index, re_group in enumerate(eval(d['re_group'])):
            assert_list.append(
                {
                    'contain': '$.intents.0.slots, {}'.format(json.dumps(
                        {
                            'name': re_group,
                            'values': [slots[index]]
                        }, ensure_ascii=False
                    ))
                }
            )
        testcases.append({
            'test':
                {
                    'id': t_id,
                    'pattern_id': d['pattern_id'],
                    'request': {
                        're_pattern': d['re_pattern'],
                        'query': ''
                    },
                    'assert_rule': '',
                    'assert': assert_list,
                    'api': '/nlu',
                    'host': 'http://39.100.203.200:8020'
                }
        }
        )
        t_id += 1
    yaml.dump(testcases, file('/Users/songbogao/Documents/code/github/KnowinTest/insight-brain/nlu/case/case.yml', 'w'),
              encoding='utf-8', allow_unicode=True)
    cur.close()


if __name__ == '__main__':
    create_testcase()
