from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from datacenter.models import Schoolkid, Chastisement, Commendation, Lesson, Mark
import random


def remove_chastisements(schoolkid):
    schoolkid_name = get_schoolkid(schoolkid)
    person_remark = Chastisement.objects.filter(schoolkid=schoolkid_name)

    for person in person_remark:
        person.delete()


def fix_marks(schoolkid):
    schoolkid_name = get_schoolkid(schoolkid)
    schoolkid_marks = Mark.objects.filter(schoolkid=schoolkid_name)

    for mark in schoolkid_marks:
        if mark.points < 4:
            mark.points = 5
            mark.save()


def create_commendation(schoolkid, lesson_subject):
    praise = (
        'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!', 'Отлично!',
        'С каждым разом у тебя получается всё лучше!'
    )

    random_praise = random.choice(praise)

    schoolkid = get_schoolkid(schoolkid)
    year_of_study, group_letter = schoolkid.year_of_study, schoolkid.group_letter

    lessons = Lesson.objects.filter(
        year_of_study=year_of_study, group_letter=group_letter, subject__title=lesson_subject
    )

    last_lesson = lessons.last()

    try:
        Commendation.objects.create(
            text=random_praise, created=last_lesson.date, schoolkid=schoolkid, subject=last_lesson.subject,
            teacher=last_lesson.teacher
        )
    except AttributeError:
        raise ValueError('Неверное название предмета')


def get_schoolkid(schoolkid):
    errors = {
        'MultipleObjectsReturned': 'Больше одного совпадения',
        'DoesNotExist': 'Совпадений нет'
    }

    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid)
    except (MultipleObjectsReturned, ObjectDoesNotExist) as er:
        raise ValueError(errors[er.__class__.__name__])
