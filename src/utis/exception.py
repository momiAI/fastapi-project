class BasesException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class CottageBooked(BasesException):
    detail = 'ER'

class TypeNumberError(BasesException):
    detail = "Неверный формат телефона"

class KeyDuplication(BasesException):
    detail = "Объект уже существует"

class ObjectNotFound(BaseException):
    detail = "Объект не найден"