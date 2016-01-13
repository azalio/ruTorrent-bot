import pickle


class ChatIDUser:
    host = ""
    port = "80"
    username = ""
    password = ""

    def dump(self, chat_id):
        with open(chat_id+'.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)


def load(chat_id):
    with open(chat_id+'.pkl', 'rb') as load_input:
        return pickle.load(load_input)