import random, string

chars = ""

try:
    quantLen = int(input('Введите количество паролей для генерации: '))
    onePassLen = int(input('Введите длину одного пароля: '))
except:
    print('Вы ввели недопустимое число или вовсе не число')

isDig = input('Включать цифры? (y/n) ')
isLower = input('Включать буквы нижнего регистра? (y/n) ')
isUpper = input('Включать буквы верхнего регистра? (y/n) ')
isPunc = input('Включать символы пунктуации и специальные символы? (y/n) ')
exOff = input('Исключать неодноднозначные символы : "il1LoO0" ? (y/n)') 

if isDig == 'y': chars += string.digits
if isLower == 'y': chars += string.ascii_lowercase
if isUpper == 'y': chars += string.ascii_uppercase
if isPunc == 'y': chars += string.punctuation
if exOff == 'y':
    for i in 'il1LoO0':
        chars.replace(i, '')

def genPass(onePassLen, chars):
    password = ''
    for i in range(onePassLen):
        password += random.choice(chars)
    return password

for _ in range(quantLen):
    print(genPass(onePassLen, chars))