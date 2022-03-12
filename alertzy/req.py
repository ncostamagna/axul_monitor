import requests

URL_BASE = "https://alertzy.app"

class Alertzy:
    def __init__(self, token):
        self.token = token

    def Send(self, title, message, group = "", button = "", link = ""):

        data = {'title': title, 'message': message, 'accountKey': self.token}

        if group != "":
            data['group'] = group

        if button != "":
            data['button'] = button
        
        if link != "":
            data['link'] = link

        print(data)
        r = requests.post("{}/send".format(URL_BASE), data=data)
        print(r.text)



def New(token):
    return Alertzy(token)
    


