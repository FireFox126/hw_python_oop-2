class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type,
                 duration, distance,
                 speed, calories) -> None:
        self.training_type = training_type
        self.duartion = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def show_info_message(self):
        return ('Тип тренировки: ' f'{self.training_type};'
                ' Длительность: '
                f'{self.duration} ч.;'
                ' Дистанция: ' f'{self.get_distance()} км;'
                ' Ср.скорость: '
                f'{self.get_mean_speed()} км/ч;'
                ' Потрачено ккал: ' f'{self.get_spent_calories()}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    training_type = ''

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage.show_info_message(self)
        return info


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


class Swimming(Training):
    """Тренировка: плавание."""
    cf_sw_1 = 1.1
    cf_sw_2 = 2

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
        self.LEN_STEP = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_1 = self.length_pool * self.count_pool
        self.speed = speed_1 / super().M_IN_KM / self.duration
        return self.speed

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
    print(training.show_training_info())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
