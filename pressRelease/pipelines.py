# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import json
# import csv
import codecs
import MySQLdb

class PressreleasePipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect(host="localhost", user="", passwd="", db="", charset="utf8", use_unicode=True)
		self.cursor = self.conn.cursor()
		# self.file = csv.writer(open('output.csv', 'wb'))
		# self.file.writerow(['title', 'url', 'datetime', 'content'])
		# self.file = codecs.open('items.jl', 'wb', encoding='utf8')

	def process_item(self, item, spider):
		try:
			self.cursor.execute("""INSERT INTO news (title, url, datetime, content) VALUES (%s, %s, %s, %s)""", (item['title'].encode('utf-8'), item['url'].encode('utf-8'), item['datetime'].encode('utf-8'), item['content'].encode('utf-8')))
			self.conn.commit()

		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		# self.file.writerow([item['title'].encode('utf-8'),
  #                                   item['url'].encode('utf-8'),
  #                                   item['datetime'].encode('utf-8'),
  #                                   item['content'].encode('utf-8')])
		# line = json.dumps(dict(item), ensure_ascii=False) + "\n"
		# self.file.write(line)
		# return item
