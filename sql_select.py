#!/bin/env python
# coding:utf-8
import requests
import json
import time
import smtplib
import os
import pymysql.cursors
import sys
import importlib
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

importlib.reload(sys)

# 时间戳转为日期
def timestamp_to_utc_datetime(timestamp):
    utc_datetime = datetime.fromtimestamp(timestamp)
    utc_datetime = utc_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return utc_datetime


# 日期转为时间戳
def utc_datetime_to_timestamp(time_str):
    dtime = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    timestamp = time.mktime(dtime.timetuple())
    return int(timestamp)


logger = set_log('info')


def get_api_data(query_sql):

    headers = {
        'cache-control': "",
        'postman-token': ""
    }
    url = "http://xxx/query/select_sql"
    querystring = {
        "sql": query_sql
    }
    res = requests.get(url, headers=headers, params=querystring)
    res_data = res.json()["data"]

    return  res_data


def get_top10_anchoruid(start_time, end_time,uid):
    sql_text = "SELECT sum(value)/sum(_cnt) AS `卡比`,intDiv(toUInt32(its), 20) * 20 * 1000 AS time_msec FROM `view`.`dis_video_video_bad_quality_ratio_207` WHERE  its >= %s AND its <= %s AND day >= toDate(toDateTime(%s)) AND day <= toDate(toDateTime(%s)) and anchoruid = %s GROUP BY `anchoruid` ORDER BY `卡比`  desc   FORMAT JSON " % (start_time, end_time, start_time, end_time,uid)
   
    data = get_api_data(sql_text)

    print(data)


if __name__ == '__main__':

    for i in range(1,10):
        base_time = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        dt_time = utc_datetime_to_timestamp(base_time + ' 00:00:00')
        start_time = utc_datetime_to_timestamp(base_time + ' 20:00:00')
        end_time = utc_datetime_to_timestamp(base_time + ' 23:59:59')
        print(base_time)
        get_top10_anchoruid(start_time, end_time)
