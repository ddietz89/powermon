#!/usr/bin/python

from drivers import mysql
from datetime import datetime

db = mysql.Database()

db.connect("localhost", "powermon", "powermongem", "powermon")

aggregates = db.query("SELECT id, channel_id, datetime, aggregate FROM aggregate_status WHERE aggregate = 'MINUTE'");

for agg in aggregates:
    start = "0000-00-00 00:00:00"
    if agg['datetime']:
        start = agg['datetime']

    data = db.query("SELECT wattsec, voltage, UNIX_TIMESTAMP(datetime) AS ts, seconds FROM channel_packet WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime >= '" + str(start) + "'")

    min_time = 99999999999999999
    max_time = 0
    for packet in data:
        if packet['ts'] > max_time:
	   max_time = packet['ts']
        if packet['ts'] < min_time:
	   min_time = packet['ts']

    # Round times to nearest minute
    min_time = int(min_time/60 * 60)
    max_time = int(max_time/60 * 60) + 60

    print "Aggregating by minute"
    print "Channel_id: " + str(agg['channel_id'])
    print datetime.fromtimestamp(min_time).strftime("%Y-%m-%d %H:%M:%S") + " -> " + datetime.fromtimestamp(max_time).strftime("%Y-%m-%d %H:%M:%S") 
    print

    buckets = {}
    for time in range(min_time, max_time, 60):
        start_ws = None
	end_ws = None
	points = 0
	volts = 0
        for i in range(0, len(data)):
	    if data[i]['ts'] >= time and data[i]['ts'] < time+60:
	        start_ws = data[i]['wattsec']
		break

        for j in range(i, len(data)):
	    if data[j]['ts'] < time+60:
	        end_ws = data[j]['wattsec']
		points += 1
		volts += data[j]['voltage']
            else:
	        break

        if start_ws and end_ws:
	    total_ws = end_ws - start_ws
	    volts = volts / points
	    watts = total_ws / (data[j]['seconds'] - data[i]['seconds'])
	else:
	    total_ws = 0
	    volts = 0
	    watts = 0


	existing = db.query("SELECT id FROM aggregate_by_minute WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "'")

        if existing:
	    sql = "UPDATE aggregate_by_minute SET wattsec = '" + str(total_ws) + "', voltage = '" + str(volts) + "', watt = '" + str(watts) + "' WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "'"
     	    print sql
	    db.execute(sql)
	else:
	    sql = "INSERT INTO aggregate_by_minute (channel_id, datetime, wattsec, voltage, watt) VALUES ('" + str(agg['channel_id']) + "','" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "','" + str(total_ws) + "','" + str(volts) + "','" + str(watts) + "')"
     	    print sql
	    db.execute(sql)

        sql = "UPDATE aggregate_status SET datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "' WHERE id = '" + str(agg['id']) + "'"
	db.execute(sql)


        
        
# 15 Minute

aggregates = db.query("SELECT id, channel_id, datetime, aggregate FROM aggregate_status WHERE aggregate = '15MINUTE'");

for agg in aggregates:
    start = "0000-00-00 00:00:00"
    if agg['datetime']:
        start = agg['datetime']

    data = db.query("SELECT wattsec, voltage, UNIX_TIMESTAMP(datetime) AS ts, seconds FROM channel_packet WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime >= '" + str(start) + "'")

    min_time = 99999999999999999
    max_time = 0
    for packet in data:
        if packet['ts'] > max_time:
	   max_time = packet['ts']
        if packet['ts'] < min_time:
	   min_time = packet['ts']

    # Round times to nearest 15 minute
    min_time = int(min_time/900 * 900)
    max_time = int(max_time/900 * 900) + 900

    print "Aggregating by 15 minute"
    print "Channel_id: " + str(agg['channel_id'])
    print datetime.fromtimestamp(min_time).strftime("%Y-%m-%d %H:%M:%S") + " -> " + datetime.fromtimestamp(max_time).strftime("%Y-%m-%d %H:%M:%S") 
    print

    buckets = {}
    for time in range(min_time, max_time, 900):
        start_ws = None
	end_ws = None
	points = 0
	volts = 0
        for i in range(0, len(data)):
	    if data[i]['ts'] >= time and data[i]['ts'] < time+900:
	        start_ws = data[i]['wattsec']
		break

        for j in range(i, len(data)):
	    if data[j]['ts'] < time+900:
	        end_ws = data[j]['wattsec']
		points += 1
		volts += data[j]['voltage']
            else:
	        break

        if start_ws and end_ws:
	    total_ws = end_ws - start_ws
	    volts = volts / points
	    watts = total_ws / (data[j]['seconds'] - data[i]['seconds'])
	else:
	    total_ws = 0
	    volts = 0
	    watts = 0


	existing = db.query("SELECT id FROM aggregate_by_15minute WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "'")

        if existing:
	    sql = "UPDATE aggregate_by_15minute SET wattsec = '" + str(total_ws) + "', voltage = '" + str(volts) + "', watt = '" + str(watts) + "' WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "'"
     	    print sql
	    db.execute(sql)
	else:
	    sql = "INSERT INTO aggregate_by_15minute (channel_id, datetime, wattsec, voltage, watt) VALUES ('" + str(agg['channel_id']) + "','" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "','" + str(total_ws) + "','" + str(volts) + "','" + str(watts) + "')"
     	    print sql
	    db.execute(sql)

        sql = "UPDATE aggregate_status SET datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "' WHERE id = '" + str(agg['id']) + "'"
	db.execute(sql)


        
        

# 60 Minute

aggregates = db.query("SELECT id, channel_id, datetime, aggregate FROM aggregate_status WHERE aggregate = 'HOUR'");

for agg in aggregates:
    start = "0000-00-00 00:00:00"
    if agg['datetime']:
        start = agg['datetime']

    data = db.query("SELECT wattsec, voltage, UNIX_TIMESTAMP(datetime) AS ts, seconds FROM channel_packet WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime >= '" + str(start) + "'")

    min_time = 99999999999999999
    max_time = 0
    for packet in data:
        if packet['ts'] > max_time:
	   max_time = packet['ts']
        if packet['ts'] < min_time:
	   min_time = packet['ts']

    # Round times to nearest hour
    min_time = int(min_time/3600 * 3600)
    max_time = int(max_time/3600 * 3600) + 3600

    print "Aggregating by hour"
    print "Channel_id: " + str(agg['channel_id'])
    print datetime.fromtimestamp(min_time).strftime("%Y-%m-%d %H:%M:%S") + " -> " + datetime.fromtimestamp(max_time).strftime("%Y-%m-%d %H:%M:%S") 
    print

    buckets = {}
    for time in range(min_time, max_time, 3600):
        start_ws = None
	end_ws = None
	points = 0
	volts = 0
        for i in range(0, len(data)):
	    if data[i]['ts'] >= time and data[i]['ts'] < time+3600:
	        start_ws = data[i]['wattsec']
		break

        for j in range(i, len(data)):
	    if data[j]['ts'] < time+3600:
	        end_ws = data[j]['wattsec']
		points += 1
		volts += data[j]['voltage']
            else:
	        break

        if start_ws and end_ws:
	    total_ws = end_ws - start_ws
	    volts = volts / points
	    watts = total_ws / (data[j]['seconds'] - data[i]['seconds'])
	else:
	    total_ws = 0
	    volts = 0
	    watts = 0


	existing = db.query("SELECT id FROM aggregate_by_hour WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "'")

        if existing:
	    sql = "UPDATE aggregate_by_hour SET wattsec = '" + str(total_ws) + "', voltage = '" + str(volts) + "', watt = '" + str(watts) + "' WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "'"
     	    print sql
	    db.execute(sql)
	else:
	    sql = "INSERT INTO aggregate_by_hour (channel_id, datetime, wattsec, voltage, watt) VALUES ('" + str(agg['channel_id']) + "','" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "','" + str(total_ws) + "','" + str(volts) + "','" + str(watts) + "')"
     	    print sql
	    db.execute(sql)

        sql = "UPDATE aggregate_status SET datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "' WHERE id = '" + str(agg['id']) + "'"
	db.execute(sql)


        
        

# Day

aggregates = db.query("SELECT id, channel_id, datetime, aggregate FROM aggregate_status WHERE aggregate = 'DAY'");

for agg in aggregates:
    start = "0000-00-00 00:00:00"
    if agg['datetime']:
        start = agg['datetime']

    data = db.query("SELECT wattsec, voltage, UNIX_TIMESTAMP(datetime) AS ts, seconds FROM channel_packet WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime >= '" + str(start) + "'")

    min_time = 99999999999999999
    max_time = 0
    for packet in data:
        if packet['ts'] > max_time:
	   max_time = packet['ts']
        if packet['ts'] < min_time:
	   min_time = packet['ts']

    # Round times to nearest day
    min_time = int(min_time/86400 * 86400) + 14400
    max_time = int(max_time/86400 * 86400) + 86400 + 14400

    print "Aggregating by day"
    print "Channel_id: " + str(agg['channel_id'])
    print datetime.fromtimestamp(min_time).strftime("%Y-%m-%d %H:%M:%S") + " -> " + datetime.fromtimestamp(max_time).strftime("%Y-%m-%d %H:%M:%S") 
    print

    buckets = {}
    for time in range(min_time, max_time, 86400):
        start_ws = None
	end_ws = None
	points = 0
	volts = 0
        for i in range(0, len(data)):
	    if data[i]['ts'] >= time and data[i]['ts'] < time+86400:
	        start_ws = data[i]['wattsec']
		break

        for j in range(i, len(data)):
	    if data[j]['ts'] < time+86400:
	        end_ws = data[j]['wattsec']
		points += 1
		volts += data[j]['voltage']
            else:
	        break

        if start_ws and end_ws:
	    total_ws = end_ws - start_ws
	    volts = volts / points
	    watts = total_ws / (data[j]['seconds'] - data[i]['seconds'])
	else:
	    total_ws = 0
	    volts = 0
	    watts = 0


	existing = db.query("SELECT id FROM aggregate_by_day WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "'")

        if existing:
	    sql = "UPDATE aggregate_by_day SET wattsec = '" + str(total_ws) + "', voltage = '" + str(volts) + "', watt = '" + str(watts) + "' WHERE channel_id = '" + str(agg['channel_id']) + "' AND datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "'"
     	    print sql
	    #db.execute(sql)
	else:
	    sql = "INSERT INTO aggregate_by_day (channel_id, datetime, wattsec, voltage, watt) VALUES ('" + str(agg['channel_id']) + "','" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "','" + str(total_ws) + "','" + str(volts) + "','" + str(watts) + "')"
     	    print sql
	    #db.execute(sql)

        sql = "UPDATE aggregate_status SET datetime = '" + str(datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")) + "' WHERE id = '" + str(agg['id']) + "'"
	#db.execute(sql)


        
        

