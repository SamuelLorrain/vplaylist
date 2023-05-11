from vplaylist.service.database import delete_non_existing_files_from_database


def clean_database() -> bool:
    return delete_non_existing_files_from_database()
