from datetime import datetime
import requests
import constants
from custom_field import CustomField
from custom_field_options import CustomFieldOption

URL = "https://api.trello.com/1/cards"


class WriterCard:
    add_cards = []
    update_cards = []

    def __init__(self, card_id: str, name: str, id_list: str, member: str):
        self.card_id = card_id
        self.name = name
        self.id_list = id_list
        self.writer = member
        self.team = ''
        self.role = ''
        self.daily_word_count = 0
        self.employee_code = 0
        self.joining_date = None
        self.overtime = 0
        self.leaves = 0
        self.set_card_custom_fields()
        if self.id_list == constants.ADD_WRITER_LIST:
            WriterCard.add_cards.append(self)
        elif self.id_list == constants.UPDATE_WRITER_LIST:
            WriterCard.update_cards.append(self)

    @staticmethod
    def instantiate_from_json():
        for list_id in constants.UPDATE_LIST_IDS:
            url = f"https://api.trello.com/1/lists/{list_id}/cards"

            response = requests.request(
                "GET",
                url,
                params=constants.PARAMS,
                headers=constants.HEADERS
            )

            cards_json = response.json()

            for card_json in cards_json:
                WriterCard(
                    card_json['id'],
                    card_json['name'],
                    card_json['idList'],
                    card_json['idMembers'][0]
                )

    def set_card_custom_fields(self):
        proofreading_field_url = URL + f'/{self.card_id}/customFieldItems'

        response = requests.request(
            "GET",
            proofreading_field_url,
            params=constants.PARAMS,
            headers=constants.HEADERS
        )

        for custom_field_json in response.json():
            c_field = CustomField.get_custom_field_by_id(custom_field_json['idCustomField'])
            if c_field is not None:
                if c_field.name == 'Team':
                    cfo = CustomFieldOption.get_custom_field_option_by_id(custom_field_json['idValue'])
                    self.team = cfo.field_value
                elif c_field.name == 'Role':
                    cfo = CustomFieldOption.get_custom_field_option_by_id(custom_field_json['idValue'])
                    self.role = cfo.field_value
                elif c_field.name == 'Daily Word Count':
                    self.daily_word_count = custom_field_json['value']['number']
                elif c_field.name == 'Employee Code':
                    self.employee_code = custom_field_json['value']['text']
                elif c_field.name == 'Date Of Joining':
                    dt = datetime.strptime(custom_field_json['value']['date'], '%Y-%m-%dT%H:%M:%S.%f%z')
                    self.joining_date = dt.strftime('%Y-%m-%d')
                elif c_field.name == 'Overtime':
                    self.overtime = custom_field_json['value']['number']
                elif c_field.name == 'Leaves':
                    self.leaves = custom_field_json['value']['number']

    @staticmethod
    def convert_add_cards_to_db_list():
        db_list = []
        for card in WriterCard.add_cards:
            db_list.append([card.writer, card.name, card.team, card.role, card.daily_word_count, card.overtime,
                            card.joining_date, card.employee_code, card.leaves])

        return db_list

    @staticmethod
    def convert_update_cards_to_db_list():
        db_list = []
        for card in WriterCard.update_cards:
            db_list.append([card.team, card.role, card.daily_word_count, card.overtime, card.employee_code,
                            card.writer])

        return db_list

    @staticmethod
    def archive_cards_in_list(id_list):
        arc_url = f"https://api.trello.com/1/lists/{id_list}/archiveAllCards"

        requests.request(
            "POST",
            arc_url,
            params=constants.PARAMS,
            headers=constants.HEADERS
        )
