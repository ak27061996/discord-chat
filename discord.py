# google: 0~AIzaSyAOhSynDs8bhMIZ_H7ITesMyT4pdRvvWh0 
from flask import session
import requests
import constant
from database.model import User, Chat

class DiscordChat():

    def __init__(self):
        pass
    
    def chat(self, request):
        '''
            return msg response
        '''
        user_id = session['logged_in']
        msg = request.form.get('msg').strip()
        try:
            chat = Chat(msg=msg, user_id=user_id)
            if msg == 'hey':
                return 'hi'
            if msg == '!google':
                return [i.replace('!google', '') for i in chat.find_google_chats_history()]

            if msg.startswith('!google'):
                query = msg.replace('!google', '').strip()
                return self.google_custom_search(query)
            if msg.startswith('!recent'):
                query = msg.replace('!recent', '').strip()
                return [i.replace('!google', '') for i in chat.recent_search(query)]
            else:
                return ['hey', '!google {query}', '!recent {query}', '!recent']# %%
        except Exception:
            pass

        finally:
            chat.save()

    def google_custom_search(self, query):
        '''
            google search api and return top 5 link of results
        '''
        google_top5_response_link = []
        try:
            google_response = requests.get(
                'https://www.googleapis.com/customsearch/v1?key={0}&cx=017576662512468239146:omuauf_lfve&q={1}'.format(
                    constant.GOOGLE_API_KEY ,query)).json()
            google_top5_response_link = [i.get('link') for i in google_response.get('items',[])[:5]]
        except:
            pass
        return google_top5_response_link
    
    


