#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *
import json
import time

times = {}
replyList = []
groupMembers = {}


def getDate():
	return time.strftime("%m%d", time.localtime(time.time()))


def updateLocal():
	local = ""
	with open("swap.out", "r") as f:
		local = f.read()
		f.close()
	if local != "":
		localMembers = json.loads(local)
	else:
		localMembers = {}
	for member in localMembers:
		if member not in groupMembers:
			groupMembers[member] = []
		for date in localMembers[member]:
			if date not in groupMembers[member]:
				groupMembers[member].append(date)
	for member in groupMembers:
		if member not in localMembers:
			localMembers[member] = []
		for date in groupMembers[member]:
			if date not in localMembers[member]:
				localMembers[member].append(date)
	text = json.dumps(localMembers)
	fa = open("swap.out", "w")
	fb = open("swap" + getDate(), "w")
	fa.write(text)
	fb.write(text)
	

class MyWXBot(WXBot):
	def handle_msg_all(self, msg):
		targetId = ""
		for group in self.group_list:
			if group[u"PYQuanPin"] == u"tinglidaka":
				targetId = group[u"UserName"]
		# print self.group_members[targetId]
		for member in self.group_members[targetId]:
			if member[u"DisplayName"] not in groupMembers:
				groupMembers[member[u"DisplayName"]] = []
			
		# print msg["msg_type_id"]
		if msg['msg_type_id'] == 4:
			print msg["user"]["name"]
			if msg["user"]["name"] == u"lcy":
				if msg["user"]["id"] not in times:
					times[msg["user"]["id"]] = 0
				times[msg["user"]["id"]] += 1
				if times[msg["user"]["id"]] >= 3:
					self.send_msg_by_uid(u"你还发上瘾了？！", msg["user"]["id"])
				else:
					self.send_msg_by_uid(u"最近天天发了1条朋友圈，耀耀没点赞:p", msg["user"]["id"])
			if msg["user"]["name"] in replyList:
				# print "recieve user"
				if msg["user"]["id"] not in times:
					times[msg["user"]["id"]] = 0
				times[msg["user"]["id"]] += 1
				if times[msg["user"]["id"]] >= 3:
					self.send_msg_by_uid(u"你还发上瘾了？！", msg["user"]["id"])
				else:
					self.send_msg_by_uid(u"hi!", msg["user"]["id"])
		
		if msg['msg_type_id'] == 3:
			print ("message group:",  msg["user"]["name"], msg["user"]["id"])
			if msg["user"]["name"] == u"听力打卡":
				print msg["content"]["data"]
				print msg["content"]["user"]["name"]
				if msg["content"]["data"] == u"打卡" or msg["content"]["data"] == u"打卡。":
					updateLocal()
					nowDate = getDate()
					if msg["content"]["user"]["name"] not in groupMembers:
						groupMembers[msg["content"]["user"]["name"]] = []
					if nowDate in groupMembers[msg["content"]["user"]["name"]]:
						self.send_msg_by_uid(u"@" + msg["content"]["user"]["name"] + u" 泥今天打过卡啦！", msg["user"]["id"])
					else:
						groupMembers[msg["content"]["user"]["name"]].append(nowDate)
						updateLocal()
						self.send_msg_by_uid(u"@" + msg["content"]["user"]["name"] + u" 打卡成功", msg["user"]["id"])

            
'''
    def schedule(self):
        self.send_msg(u'张三', u'测试')
        time.sleep(1)
'''


def main():
	bot = MyWXBot()
	bot.DEBUG = True
	bot.conf['qr'] = 'tty'
	bot.run()


if __name__ == '__main__':
	main()

