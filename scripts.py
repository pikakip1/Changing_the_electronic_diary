from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Chastisement, Commendation, Lesson, Mark
import random

COMMENDABLE_REVIEWS = (
        'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!', 'Отлично!',
        'С каждым разом у тебя получается всё лучше!'
    )


def remove_chastisements(schoolkid):
    schoolkid_name = get_schoolkid(schoolkid)
    Chastisement.objects.filter(schoolkid=schoolkid_name).delete()


def fix_marks(schoolkid):
    schoolkid_name = get_schoolkid(schoolkid)
    Mark.objects.filter(points__lt=4, schoolkid=schoolkid_name).update(points=5)


def create_commendation(schoolkid, lesson_subject):
    random_praise = random.choice(COMMENDABLE_REVIEWS)

    schoolkid_name = get_schoolkid(schoolkid)
    year_of_study, group_letter = schoolkid_name.year_of_study, schoolkid_name.group_letter

    lessons = Lesson.objects.filter(
        year_of_study=year_of_study, group_letter=group_letter, subject__title=lesson_subject
    )

    last_lesson = lessons.order_by('date').last()

    try:
        Commendation.objects.create(
            text=random_praise, created=last_lesson.date, schoolkid=schoolkid_name, subject=last_lesson.subject,
            teacher=last_lesson.teacher
        )
    except AttributeError:
        raise ValueError('Неверное название предмета')


def get_schoolkid(schoolkid):
    errors = {
        'MultipleObjectsReturned': 'Больше одного совпадения, добавьте отчество',
        'DoesNotExist': f'Ученик {schoolkid} не найден'
    }

    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid)
    except (MultipleObjectsReturned, ObjectDoesNotExist) as er:
        raise type(er)(errors[er.__class__.__name__])
