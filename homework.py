class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories):
        self.training_type = training_type
        self.duration = duration / 60
        self.distance = round(distance, 3)
        self.speed = round(speed, 3)
        self.calories = round(calories, 3)

    def get_message(self):
        return f"Тип тренировки: {self.training_type}; Длительность: {self.duration} ч.; Дистанция: {self.distance} км; Ср. скорость {self.speed} км/ч; Потрачено ккал: {self.calories}."


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration * 60
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self), self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (self.coeff_calorie_1 * self.get_mean_speed() - self.coeff_calorie_2) * self.weight / self.M_IN_KM * self.duration

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    walk_coeff_calorie_1 = 0.035
    walk_coeff_calorie_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height


    def get_spent_calories(self) -> float:
        return (self.walk_coeff_calorie_1 * self.weight + (self.get_mean_speed()**2 // self.height) * self.walk_coeff_calorie_2 * self.weight) * self.duration


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.weight

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + 1.1) * 2 * self.weight



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

