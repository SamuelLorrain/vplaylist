from vplaylist.service.database import DatabaseService


def clean_database() -> bool:
    database_service = DatabaseService()
    database_service.delete_non_existing_files_from_database()
    return True
