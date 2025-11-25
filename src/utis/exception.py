class CustomException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class CottageBooked(CustomException):
    detail = 'ER'

class AccessDenied(CustomException):
    detail = "Недостаточно прав"

class TypeNumberError(CustomException):
    detail = "Неверный формат телефона"

class IncorrectData(CustomException):
    detail = "Некоректные данные"

class OrganizationNotFound(IncorrectData):
    detail = "Организация не существует"

class FacilitiesNotFound(CustomException):
    detail = "Удобство не найдено."

class IncorrectDataCottage(CustomException):
    detail = "Некоректные данные коттеджа"

class UserHasNotPermission(CustomException):
    detail = "Пользователь не имеет право на редактирование"

class KeyDuplication(CustomException):
    detail = "Объект уже существует"

class ObjectNotFound(CustomException):
    detail = "Объект не найден"

class CottageNotFound(ObjectNotFound):
    detail = "Коттедж не найден"

class CottageBook(CustomException):
    detail = "Коттедж забронирован"