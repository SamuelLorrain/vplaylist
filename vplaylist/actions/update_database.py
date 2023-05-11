from vplaylist.service.database import insert_new_elements_in_database


def update_database() -> bool:
    return insert_new_elements_in_database()
