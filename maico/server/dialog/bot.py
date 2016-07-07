class Bot(object):
    def __init__(self):
        self.state = 0
        self.file_name = 'state.pkl'

    def is_yes(self, utt):
        return 'はい' in utt

    def is_no(self, utt):
        return 'いいえ' in utt

    def generate_response(self, usr_utt):
        if self.state == 0:
            if self.is_yes(usr_utt):
                utt = '賞品の説明。ご予算はどれくらいですか？'
            elif self.is_no(usr_utt):
                utt = 'そうですか、ごゆっくりどうぞ'
            else:
                utt = 'pass'
        elif self.state == 1:
            if self.is_yes(usr_utt):
                utt = '動画や音楽の作成に使用する予定はありますか？'
            else:
                utt = 'pass'
        elif self.state == 2:
            if self.is_yes(usr_utt):
                utt = 'パソコンのセットアップはおひとりでできそうですか？'
            elif self.is_no(usr_utt):
                utt = 'パソコンのセットアップはおひとりでできそうですか？'
            else:
                utt = 'pass'
        elif self.state == 3:
            if self.is_yes(usr_utt):
                utt = 'それでしたらこちらのパソコンAをおすすめします。'
            elif self.is_no(usr_utt):
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
