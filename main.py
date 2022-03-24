from card import WriterCard
from custom_field import CustomField
from custom_field_options import CustomFieldOption
from database import database_connection
import constants


def main(data, context):
    CustomField.instantiate_from_list(database_connection.get_custom_fields())
    CustomFieldOption.instantiate_from_list(database_connection.get_custom_field_options())

    WriterCard.instantiate_from_json()

    database_connection.insert_writer_details(WriterCard.convert_add_cards_to_db_list())
    WriterCard.archive_cards_in_list(constants.ADD_WRITER_LIST)

    database_connection.update_writer_details(WriterCard.convert_update_cards_to_db_list())
    WriterCard.archive_cards_in_list(constants.UPDATE_WRITER_LIST)

    database_connection.connection.close()


if __name__ == '__main__':
    main('', '')
