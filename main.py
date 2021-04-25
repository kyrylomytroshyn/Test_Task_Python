from random import randint  # Импортируем метод для определения случайного целого числа

# Константы, для определения шанса выпадения того или иного шага.
MIN_STEP = 1  # Минимальный шаг
MAX_STEP = 3  # Максимальный шаг
BOOST_STEP = 2  # Бонусный шанс для излечения (т.к. идет проверка на шанс больше 2)
MIN_HEAL_DAMAGE = 18  # Минимальный урон умеренного лечения/удара
MAX_HEAL_DAMAGE = 25  # Максимальный урон умеренного лечения/удара
MIN_DAMAGE = 10  # Минимальный урон простого удара
MAX_DAMAGE = 35  # Минимальный урон простого удара
DEFAULT_HP = 100  # Стандартное кол-во ОЗ (Очков Здоровья)


# Класс игрока (неважно, компьютер или человек)
class Player:
    __hp = DEFAULT_HP  # Здоровье персонажа

    def __init__(self, name, is_bot):
        """Инициализация персонажа. (конструктор класса)"""
        self.__name = name  # Имя персонажа
        self.__is_bot = is_bot  # Является ли игрок ботом?

    def fight(self, opponent):
        """Производит один шаг боя двух игроков.
        Если у компьютера меньше 35 ОЗ - запускается метод оппонента для снижения ОЗ с повышеным шанком на лечение.
        Иначе вызывается обычная функция нанесения урона. Обе функции возвращают True или False.
        Если True - игра идет дальше, если False - завершается."""

        if self.__hp <= 35 and self.__is_bot:
            return opponent.damage_player(self.__name, self.choose_skill(MIN_STEP, MAX_STEP + BOOST_STEP))
        else:
            return opponent.damage_player(self.__name, self.choose_skill(MIN_STEP, MAX_STEP))

    def choose_skill(self, min_step, max_step):
        """Метод выбора скилла и урона от него.
        Если выпадает число 1 или 2 - метод возвращает количество урона.
        Если выпадает число от 3 - вызывается метод лечения игрока и возвращается нулевой урон.
        """
        this_step = randint(min_step, max_step)  # Получаем случайное число
        if this_step > 2:  # Если выпало лечение
            self.heal_player(randint(MIN_HEAL_DAMAGE, MAX_HEAL_DAMAGE))
            return 0
        elif this_step == 1:  # Если же умеренный урон
            return randint(MIN_HEAL_DAMAGE, MAX_HEAL_DAMAGE)
        else:  # Если обычный урон
            return randint(MIN_DAMAGE, MAX_DAMAGE)

    def heal_player(self, power):
        """Функция нанесения урона, power - мощность урона."""
        self.__hp += power
        print(f"Игрок {self.__name} произвел самолечение на {power} единиц; ")
        if self.__hp > DEFAULT_HP:  # Если налечило на более, чем 100 ОЗ - сброс до 100
            self.__hp = DEFAULT_HP

    def damage_player(self, enemy_name, power):
        """Функция нанесения урона.
        enemy_name - имя противника, для информирования,
        power - мощность урона. Если здоровье меньше 1 - возвращает False. Иначе - True"""
        if power > 0:
            self.__hp -= power
            print(f"Игрок {enemy_name} нанес {power} урона игроку {self.__name};")
            if self.__hp < 1:
                print(f"{self.__name} проиграл поединок.")
                return False
        return True

    def get_hp(self):
        """Функция, возвращающая кол-во здоровья."""
        return self.__hp

    def get_name(self):
        """Функция возвращающая имя игрока."""
        return self.__name

    def inform_hp(self, opponent):
        """Функция, информирующая о состоянии здоровья игроков.
        Передается объект оппонента для получения его информации."""
        print(f"У игрока {self.__name} осталось {self.__hp} единиц здоровья; ")
        print(f"У игрока {opponent.get_name()} осталось {opponent.get_hp()} единиц здоровья; ")
        print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


if __name__ == '__main__':
    # Обьявляем игроков - Человек и Бот.
    # name - имя персонажа,
    # is_bot - тип игрока, False - человек, True - компьтер.
    # Если игрок является компьтер - шанс излечения при здоровье меньше 35 увеличен.
    first_player = Player(name="Human", is_bot=False)
    second_player = Player(name="Bot", is_bot=True)

    # Цикл завершится только в том случае, если функция вернет значение False,
    # это случится в том случае если кто-то проиграет.
    while True:
        if randint(1, 2) == 1:
            print(f"Ход игрока {first_player.get_name()}:")
            if not first_player.fight(second_player):  # Если False - завершается цикл
                break
        else:
            print(f"Ход игрока {second_player.get_name()}:")
            if not second_player.fight(first_player):  # Если False - завершается цикл
                break

        first_player.inform_hp(second_player)

    print("GAME OVER!")
