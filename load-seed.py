from os import system


print('Essa operação pode sobrescrever os dados da base.')
print('Você deseja carregar os dados? (Y/n)')

user_input = input()

if user_input.lower() == 'y':
    system('python manage.py loaddata kokama_history')

