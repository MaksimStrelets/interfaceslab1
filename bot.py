# Set encoding to utf-8
# coding=utf-8

import requests
import threading
from time import sleep

bot_token = "885350301:AAEitRVCmE8jcQkdJjnsMCQu48Z69IHdbtg"


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.names = []
        self.new_offset = None

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_user_list(self):
        for n in self.names:
            print "{0} - {1}".format(self.names.index(n) + 1, n[0])

    def get_last_update(self):
        try:
            get_result = self.get_updates()

            if len(get_result) > 0:
                return get_result[-1]

        except Exception, e:
            print str(e)

        return None

    def run(self):
        print "bot started"
        while True:
            try:
                sleep(1)
                self.get_updates(self.new_offset)
                last_update = self.get_last_update()

                if last_update is None:
                    continue

                last_update_id = last_update['update_id']
                last_chat_text = last_update['message']['text']
                last_chat_id = last_update['message']['chat']['id']
                last_chat_name = last_update['message']['chat']['first_name']

                temp = (last_chat_name, last_chat_id)
                if temp not in self.names:
                    self.names.append(temp)

                self.new_offset = last_update_id + 1

                print "{0}: {1}".format(last_chat_name, last_chat_text.encode('cp866'))

            except Exception, e:
                print str(e)


class User:
    def __init__(self, bot):
        self.bot = bot
        self.help()

    def set_id(self, id):
        if id >= len(self.bot.names) or id < 0:
            print "Selected chat not exist. Please, select another one"
        else:
            self.id = id
            print "You chats with {0}".format(self.bot.names[id][0])

    def help(self):
        print "Commands:\n" \
              "-list                to show contact list\n" \
              "-send to <number>    to select chat\n" \
              "-help                to show commands list\n" \
              "-stop                to terminate the program\n"

    def run(self):
        line = ""
        while True:
            line = raw_input()

            if line.startswith("-send to"):
                try:
                    id = int(line[(line.rindex("to") + 3):]) - 1
                    self.set_id(id)
                    continue
                except:
                    print "You should use '-send to number' blueprint"

            if line == "-help":
                self.help()
                continue

            if line == "-list":
                self.bot.get_user_list()
                continue

            if line == "-stop":
                break

            if not hasattr(self, 'id'):
                self.set_id(0)

            if hasattr(self, 'id'):
                self.bot.send_message(self.bot.names[self.id][1], line)




def main():
    tgbot = BotHandler(bot_token)
    user = User(tgbot)

    thread1 = threading.Thread(target=tgbot.run)
    thread2 = threading.Thread(target=user.run)

    thread2.setDaemon(True)
    thread1.setDaemon(True)

    thread1.start()
    thread2.start()

    thread2.join()
    exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()