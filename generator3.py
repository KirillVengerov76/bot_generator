import json  # Сохранение списков
import os  # Переход в другую директорию
import graphviz  # Отрисовка графа

def print_texts(texts):
    """Функция вывода текстов вершин"""
    print('Сейчас тексты для вершин графа выглядят так:')
    for v, txt in enumerate(texts):
        if txt:
            print(f'Текст для вершины {v} (индексация с нуля): \n"{txt}"')


# Переход в папку бота
sep = '\\' if os.name == 'nt' else '/'
file = input('Введите адрес папки для бота:\n')
s = file + f'{sep}TelegramBotData{sep}static'
os.chdir(s)

# Считывание текстов вершин
text = json.load(open('text.json', 'r'))

# Вывод текстов
print_texts(text)

# Удаление текстов вершин
for _ in range(int(input('Введите количество удалений, которое хотите сделать: '))):
    u = int(input('Введите индекс вершины, текст которой хотите удалить: '))
    text[u] = ''

# Вывод текстов
print_texts(text)

# Обновление текстов вершин
for _ in range(int(input('Введите количество вершин в графе, тексты для которых вы хотите сейчас добавить: '))):
    u = int(input('Введите индекс вершины (индексация с нуля): '))
    t = input('Введите текст для этой вершины:\n')
    text[u] = t

# Сохранение текстов
open('text.json', 'w').write(json.dumps(text, indent=4, ensure_ascii=False))


# Указание путя для отрисовки графов
os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'

adj_list = json.load(open('adjacency_list.json', 'r'))
button_list = json.load(open('button.json', 'r'))
text_list = json.load(open('text.json', 'r'))

# Указание, куда сохранять картинку
s = file + f'{sep}TelegramBotData{sep}graph'
os.chdir(s)

# Создание графа
g = graphviz.Digraph('Graph for bot', comment='Your graph', format='png')

# Создание нормальных окон(не однострочных)
for i in range(len(adj_list)):
    text_split = text_list[i].split()
    text = ''
    l = 0
    for j in range(len(text_split)):
        if l <= 20:
            text += text_split[j]
            l += len(text_split[j])
        else:
            text += '\n'
            text += text_split[j]
            l = 0
            l += len(text_split[j])

    if not text:
        text = f'No text for vertex №{i}'
    else:
        pass
    g.node(f'{i}', text)

for i, h in enumerate(adj_list):
    for j in h:
        g.edge(f'{i}', f'{j}',
               label=button_list[i][j] if button_list[i][j] else f'No text for edge from {i} to {j}')

print('Вы хотите увидеть получившийся граф?(Y/N)')
if input() == 'Y':
    g.view()
else:
    g.render()

print(f'Граф сохранён по адресу {file}{sep}TelegramBotData{sep}graph')
