import requests
import json

from config import url_create_client, url_get_clients


class Client:
    def create_client(self, username):
        client_id = None
        response = json.loads(requests.get(url_get_clients).content)['response']
        print('Try to find client')
        for i in response:
            if username == i['lastname']:
                client_id = i['client_id']
                print('The client was found')
                return client_id
            else:
                pass

        if client_id == None:
            data = {'client_name': str(username),
                    'client_sex': '0',
                    'client_groups_id_client': '7',
                    'card_number': None,
                    'discount_per': None,
                    'phone': None,
                    'email': None,
                    'birthday': None,
                    'bonus': None,
                    'total_payed_sum': None
                    }

            response = json.loads(requests.post(url_create_client, data).content)['response']
            print('The client was create')

        return response

