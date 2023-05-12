from vplaylist.service.database import DatabaseService


def update_database() -> bool:
    database_service = DatabaseService()
    database_service.insert_new_elements_in_database()
    return True
