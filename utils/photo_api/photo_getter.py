import os

async def get_teacher_photo(faculty_ukr: str, teacher_id: int):
    try:
        file = open(f'photos/{faculty_ukr}/{teacher_id}.jpg', 'rb')
    except Exception as e:
        file = open(f'photos/default_picture/default_picture.jpg', 'rb')

    return file

