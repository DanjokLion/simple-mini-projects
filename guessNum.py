import random

number = random.randint(1,100)
count = 0
print('Угадай число от 1 до 100 за наименьшее количество попыток', 'Введи свое первое число: ', sep = '\n')
while True:
    guess = int(input())

    if guess == number:
        print('Поздравляю, ты угадал!')
        print(f'Твое количество попыток: {count}')
        break
    elif guess < number:
        print('Загаданное число больше')
    else:
        print('Загаданное число меньше')
    count += 1