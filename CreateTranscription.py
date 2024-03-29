import requests
import json
from config import (url_create_transaction, url_add_prod_in_transaction,
                    url_get_transaction_product, url_remove_transaction,
                    url_leftovers, url_close_transaction, url_add_client_in_trans,
                    url_get_transaction)


class Transcription:
    def create_t(self, cafe_id):
        data = {'spot_id': str(cafe_id),
                'spot_tablet_id': '1',
                'table_id': '1',
                'user_id': '3',
                'guests_count': '1'
                }
        tran_id = json.loads(requests.post(url_create_transaction, data).content)['response']['transaction_id']
        return tran_id

    def add_client(self, cafe_id, trans_id, client_id ):
        data = {'spot_id': str(cafe_id),
                'spot_tablet_id': '1',
                'transaction_id': str(trans_id),
                'client_id': str(client_id)
               }

        err_code = json.loads(requests.post(url_add_client_in_trans, data).content)['response']['err_code']
        return err_code

    def change_cafe_to_nova(self, sessions, update, cafe_id, trans_id, context):
        pass

    def add_product(self, cafe_id, transaction_id, product_id, modification):
        data = {'spot_id': str(cafe_id),
                'spot_tablet_id': '1',
                'transaction_id': str(transaction_id),
                'product_id': str(product_id),
                'modificator_id': str(modification)
                }
        transaction_product = json.loads(requests.post(url_add_prod_in_transaction, data).content)
        return transaction_product

    def add_drink(self, cafe_id, transaction_id, product_id):
        data = {'spot_id': str(cafe_id),
                'spot_tablet_id': '1',
                'transaction_id': str(transaction_id),
                'product_id': str(product_id),
                }
        transaction_product = json.loads(requests.post(url_add_prod_in_transaction, data).content)
        return transaction_product

    def get_t(self, transaction_id):
        transaction = json.loads(requests.get(url_get_transaction_product + f'&transaction_id={transaction_id}').content)['response']
        data = {}
        for i in transaction:
            data[i['product_name']] = (str(int(int(i['product_sum'])/100)), str(int(float(i['num']))))
        return data

    def get_t_sum(self, transaction_id):
        data = json.loads(requests.get(url_get_transaction + f'&transaction_id={transaction_id}').content)['response'][0]['sum']

        return data

    def get_t_status(self, transaction_id):
        data = json.loads(requests.get(url_get_transaction + f'&transaction_id={transaction_id}').content)['response'][0]['status']

        return data

    def remove_t(self, transaction_id):
        data = {'spot_tablet_id': '1',
                'transaction_id': str(transaction_id),
                'user_id': '3'
                }
        response = json.loads(requests.post(url_remove_transaction, data).content)['response']['err_code']

        return response

    def close_t(self, cafe_id, transaction_id, payed_card):
        data = {'spot_id': str(cafe_id),
                'spot_tablet_id': '1',
                'transaction_id': str(transaction_id),
                'payed_card': str(payed_card)
                }
        response = json.loads(requests.post(url_close_transaction, data).content)['response']['err_code']
        return response




