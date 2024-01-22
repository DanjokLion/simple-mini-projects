import subprocess as sp

data = sp.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
profiles = [i.split(':')[1][1:-1] for i in data if 'All User Profile' in i]

for key in profiles:
    result = sp.check_output(['netsh', 'wlan', 'show', 'profile', key, 'key=clear']).decode('utf-8').split('\n')
    result = [value.split(':')[1][1:-1] for value in result if 'Key Content' in value]
    try:
        print('{:<30} | {:<}'.format(key, result[0]))
    except IndexError:
        print('{:<30} | {:<}'.format(key, ''))

input('')