# Вариант 1


import logging
import math
import os
import sys

# папка для логов. если её нет, то логироваться будет некуда
if not os.path.exists("logs"):
    os.makedirs("logs")

# настраиваем логирование сразу в консоль и в файл
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | [%(levelname)-7s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/triangle.log", encoding="utf-8")
    ]
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")


class Triangle:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def get_type(self):
        if self.a == self.b and self.b == self.c:
            return "равносторонний"
        elif self.a == self.b or self.a == self.c or self.b == self.c:
            return "равнобедренный"
        else:
            return "разносторонний"

    def get_points(self):
        # делим все стороны на самую большую сторону.
        # треугольник от этого не меняется, зато числа получаются небольшими
        biggest = max(self.a, self.b, self.c)
        a = self.a / biggest
        b = self.b / biggest
        c = self.c / biggest

        # первая вершина будет в левом нижнем углу
        x1 = 0
        y1 = 0

        # вторая вершина справа от первой на расстоянии a
        x2 = a
        y2 = 0

        # третью вершину считаем по теореме косинусов.
        # она находится на расстоянии c от первой вершины и b от второй
        x3 = (a**2 + c**2 - b**2) / (2 * a)
        y3_squared = c**2 - x3**2

        # если треугольник почти вырожденный, то под корнем может оказаться минус
        if y3_squared < 0:
            y3_squared = 0
        y3 = math.sqrt(y3_squared)

        # нахожу самую большую координату, чтобы по ней масштабировать
        max_x = max(x1, x2, x3)
        max_y = max(y1, y2, y3)

        if max_x > max_y:
            scale = 96 / max_x
        else:
            scale = 96 / max_y

        # переводим координаты в целые числа
        # ось y в программе смотрит вниз, поэтому y считаем наоборот
        points = []
        points.append((round(x1 * scale) + 2, round((max_y - y1) * scale) + 2))
        points.append((round(x2 * scale) + 2, round((max_y - y2) * scale) + 2))
        points.append((round(x3 * scale) + 2, round((max_y - y3) * scale) + 2))

        return points


def main():
    # если стороны пришли не числами, то координаты будут такие
    bad_data = [(-2, -2), (-2, -2), (-2, -2)]
    # если числа неправильные, то координаты будут такие
    bad_numbers = [(-1, -1), (-1, -1), (-1, -1)]

    print("Введите длину стороны A: ")
    side_a = input()
    print("Введите длину стороны B: ")
    side_b = input()
    print("Введите длину стороны C: ")
    side_c = input()

    logging.debug("Стороны: " + str(side_a) + ", " + str(side_b) + ", " + str(side_c))

    # превращаем строки в числа
    try:
        a = float(side_a)
        b = float(side_b)
        c = float(side_c)
    except ValueError as error:
        logging.error("Неуспешный запрос: сторона не является числом, " + str(error))
        logging.exception("Трассировка:")
        print("Вид треугольника: ")
        print("Координаты вершин: " + str(bad_data))
        return

    # проверяем что все три числа нормальные
    for side in [a, b, c]:
        if math.isnan(side) or math.isinf(side):
            logging.error("Неуспешный запрос: сторона " + str(side) + " не обычное число")
            print("Вид треугольника: не треугольник")
            print("Координаты вершин: " + str(bad_numbers))
            return

        if side <= 0:
            logging.error("Неуспешный запрос: сторона " + str(side) + " должна быть больше нуля")
            print("Вид треугольника: не треугольник")
            print("Координаты вершин: " + str(bad_numbers))
            return

    # сумма двух сторон должна быть больше третьей, иначе это не треугольник
    if a + b <= c or a + c <= b or b + c <= a:
        logging.error("Неуспешный запрос: стороны " + str(a) + ", " + str(b) + ", " + str(c) +
                      " не образуют треугольник")
        print("Вид треугольника: не треугольник")
        print("Координаты вершин: " + str(bad_numbers))
        return

    # всё проверили, теперь делаем треугольник и спрашиваем у него ответ
    triangle = Triangle(a, b, c)
    triangle_type = triangle.get_type()
    triangle_points = triangle.get_points()

    logging.info("Успешный запрос: стороны " + str(a) + ", " + str(b) + ", " + str(c) +
                 " -> " + triangle_type + ", вершины " + str(triangle_points))

    print("Вид треугольника: " + triangle_type)
    print("Координаты вершин: " + str(triangle_points))


if __name__ == "__main__":
    main()
