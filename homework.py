from dataclasses import dataclass, asdict
from typing import Dict, Type, ClassVar


@dataclass
class InfoMessage:
    """
    Класс для создания объектов сообщений.
    Информационное сообщение о тренировке.
    """

    training_type: str  # Название тренировки
    duration: float     # Длительность (в часах)
    distance: float     # Дистанция в (в км)
    speed: float        # Скорость (в км/ч)
    calories: float     # Килокалории
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    # числовые значения округляются при выводе до тысячных долей с помощью
    # format specifier (.3f)
    def get_message(self) -> str:
        """Метод возвращает строку сообщения"""
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    training_type = ''

    action: int         # Действие
    duration: float     # Продолжительность
    weight: float       # Вес

    def get_distance(self) -> float:
        """
        Возвращает дистанцию (в километрах), которую преодолел пользователь
        за время тренировки.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    # возвращает значение средней скорости движения во время тренировки в км/ч
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # формула из задания
        # преодоленная_дистанция_за_тренировку / время_тренировки
        return self.get_distance() / self.duration

    # метод определяется в дочерних классах, расчет калорий отличается
    # в зависимости от тренировки
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Требуется определить get_spent_calories()")

    def show_training_info(self) -> InfoMessage:
        """
        Возвращает объект класса - информационное сообщение
        о выполненной тренировке.
        """
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    cf_run_1 = 18
    cf_run_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        Training.__init__(self, action, duration, weight)
        self.training_type = 'RUN'

    def get_spent_calories(self) -> float:
        cal = self.cf_run_1 * self.get_mean_speed() - self.cf_run_2
        calories = cal * self.weight / self.M_IN_KM * self.duration * 60
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cf_walk_1 = 0.035
    cf_walk_2 = 2
    cf_walk_3 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        Training.__init__(self, action, duration, weight)
        self.height = height
        self.training_type = 'WLK'

    def get_spent_calories(self) -> float:
        calories_1 = self.cf_walk_1 * self.weight
        calories_2 = self.get_mean_speed()**2 // self.height
        calories_3 = calories_2 * self.cf_walk_3 * self.weight
        calories = (calories_1 + calories_3) * self.duration * 60
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    cf_sw_1 = 1.1
    cf_sw_2 = 2
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        Training.__init__(self, action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.training_type = 'SWM'

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        calories_1 = self.get_mean_speed() + self.cf_sw_1
        calories = calories_1 * self.cf_sw_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    elif workout_type == 'RUN':
        return Running(data[0], data[1], data[2])
    elif workout_type == 'WLK':
        return SportsWalking(data[0], data[1], data[2], data[3])


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)