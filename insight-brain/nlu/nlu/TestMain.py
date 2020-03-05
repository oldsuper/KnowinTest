#!/usr/bin/env python
# coding=utf-8
"""
@Author  : gaosongbo
@Contact : gaosongbo@knowin.com
@File    : TestMain.py
@Time    : 2020/3/5 1:37 下午
"""
import nose.tools as ntls
import yaml
import requests
import uuid
import json
from jsonpath import jsonpath

TestCaseFile = 'insight-brain/nlu/case/case.yml'


def test_generator():
    testcases = yaml.load(file(TestCaseFile), Loader=yaml.FullLoader)
    for testcase in testcases:
        yield run, testcase['test']


def run(testcase):
    url = '{}{}'.format(testcase['host'], testcase['api'])
    params = {'query': testcase['request']['query'],
              'requestId': uuid.uuid4().__str__()}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json.dumps(params), headers=headers)
    for Assert in testcase['assert']:
        xpath = Assert.values()[0][0]
        expect = Assert.values()[0][1]
        response_value = get_value(response.json(), xpath)
        eval(Assert.keys()[0])(response_value, expect)


def eq(response, expect):
    ntls.assert_equal(response, expect, {'response': response, 'expect': expect})


def contain(response, expect):
    ntls.assert_in(expect, response, {'response': response, 'expect': expect})


def get_value(data, xpath):
    value = jsonpath(data, xpath)
    ntls.assert_not_equal(data, False, 'GetValueByXpathError_{}'.format(xpath))
    return value[0]
