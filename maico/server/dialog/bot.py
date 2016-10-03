import pickle
import re


def matches_money(text):
    pattern = r"じゅう|\d+|\d+円|\d+千円|\d+万円|\d+えん|\d+せんえん|\d+まんえん"
    matchOB = re.search(pattern, text)
    return True if matchOB else False


def is_yes(text):
    pattern = r'はい|お願い'
    matchOB = re.search(pattern, text)
    return True if matchOB else False


def is_no(text):
    pattern = r'いいえ|ない|ありません'
    matchOB = re.search(pattern, text)
    return True if matchOB else False


class Bot(object):
    in_automatic_dialog = False
    in_manual_dialog = False

    def __init__(self):
        self.state = 0
        self.file_name = 'state.pkl'

    def generate_response(self, usr_utt):
        if self.state == 0:
            if is_yes(usr_utt):
                utt = 'パソコンAはお買い得なお値段です。パソコンBは性能が非常に高いです。パソコンCはデザインに優れています。ちなみにご予算はどれくらいですか？'
            elif is_no(usr_utt):
                utt = 'そうですか、ごゆっくりどうぞ'
            else:
                utt = 'pass'
        elif self.state == 1:
            if matches_money(usr_utt):
                utt = 'なるほど、それでは動画や音楽の作成に使用する予定はありますか？'
            else:
                utt = 'pass'
        elif self.state == 2:
            if is_yes(usr_utt):
                utt = 'なるほど、それではパソコンのセットアップはおひとりでできそうですか？'
            elif is_no(usr_utt):
                utt = 'なるほど、それではパソコンのセットアップはおひとりでできそうですか？'
            else:
                utt = 'pass'
        elif self.state == 3:
            if is_yes(usr_utt):
                utt = 'それでしたらこちらのパソコンAをおすすめします。'
            elif is_no(usr_utt):
                utt = 'それでしたらこちらのパソコンBをおすすめします。'
            else:
                utt = 'pass'
        else:
            utt = 'どういたしまして'
        self.state += 1
        return {'utt': utt}

    def read_states(self):
        try:
            with open(self.file_name, 'rb') as f:
                states = pickle.load(f)
        except FileNotFoundError as e:
            print(e.strerror)
            states = {}
        except EOFError:
            states = {}
        return states

    def read_state(self, session_id):
        states = self.read_states()
        self.state = states.get(session_id)

    def write_state(self, session_id):
        states = self.read_states()
        states[session_id] = self.state
        with open(self.file_name, 'wb') as f:
            pickle.dump(states, f)