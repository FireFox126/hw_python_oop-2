# класс который содержит переменные поля
class InfoMessage:
    """Информационное сообщение о тренировке."""
    # инициализация класса, создание нужных переменных
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.duration = duration
    
    # возвращает данные переменных
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

# класс содержащий информацию о тренировке
class Training:
    # константы
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    TRAINING_TYPE = ''

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    # геттеры, возращают определенную переменную
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
    
    # Геттер, возращающий InfoMessage
    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message

# Класс бега который наследует класс тренировки
class Running(Training):
    # добавляются новые константы, старые из Training наследуются
    """Тренировка: бег."""
    CF_RUN_1 = 18
    CF_RUN_2 = 20
    TRAINING_TYPE = 'RUN'

    # У него переписывается только этот геттер, остальные геттеры аналогичны из класса Training
    def get_spent_calories(self) -> float:
        cal = self.CF_RUN_1 * self.get_mean_speed() - self.CF_RUN_2
        calories = cal * self.weight / self.M_IN_KM * self.duration * 60
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CF_WALK_1 = 0.035
    CF_WALK_2 = 2
    CF_WALK_3 = 0.029
    TRAINING_TYPE = 'WLK'
    # переписывается инициализация
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories_1 = self.CF_WALK_1 * self.weight
        calories_2 = self.get_mean_speed()**2 // self.height
        calories_3 = calories_2 * self.CF_WALK_3 * self.weight
        calories = (calories_1 + calories_3) * self.duration * 60
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    CF_SW_1 = 1.1
    CF_SW_2 = 2
    LEN_STEP = 1.38
    TRAINING_TYPE = 'SWM'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_1 = self.length_pool * self.count_pool
        self.speed = speed_1 / super().M_IN_KM / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        calories_1 = self.get_mean_speed() + self.CF_SW_1
        calories = calories_1 * self.CF_SW_2 * self.weight
        return calories

# глобальная функция, возвращает класс с данными (звездочка *data при инициализации классов говорит о том что передаются данные в виде кортежа(как будто в круглых скобках))
# т.е. не Swimming([720, 1, 80, 25, 40]), а Swimming(720, 1, 80, 25, 40)
def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return type_dict[workout_type](*data)

# Выводит на экран текущие поля тренировки, во всех наследниках есть функция show_training_info
def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())

# условие которые выполнится при запуске программы, если этот код небыл импортирован, т.е. выполнится если была введена команда python Novy_textovy_dokument.py
# если будет import Novy_textovy_dokument, то можно пользоваться классами тренировок но это условие не выполнитсся
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    # создает классы тренировок и выводит инфу в консоль
    # packages - массив из кортежей, workout_type - первый элемент кортежа - строка, data - второй элемент массив 
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
