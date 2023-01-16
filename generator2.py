import json  # Сохранение словарей
import os  # Переход в директорию бота
import graphviz  # Отрисовка графа

def print_adj_list(lst):
    """Функция вывода списка смежности"""
    print('Сейчас список смежости бота выглядит так (индексация с нуля):')
    for i, l in enumerate(lst):
        print(f'Из вершины {i} можно попасть в вершины: ', *l)


# Переход в папку бота
sep = '\\' if os.name == 'nt' else '/'
file = input('Введите адрес папки для бота:\n')
s = file + f'{sep}TelegramBotData{sep}static'
os.chdir(s)

# Считывание списка смежности
adj_list = json.load(open('adjacency_list.json', 'r'))

# Вывод списка смежности
print_adj_list(adj_list)

# Удаление ребер
for _ in range(int(input('Введите количество удалений, которое хотите сделать: '))):
    v = int(input('Введите индекс вершины, у которой хотите удалить связь: '))
    u = int(input('Введите индекс вершины, связь с которой хотите удалить: '))
    while u in adj_list[v]:
        adj_list[v].remove(u)

# Вывод списка смежности
print_adj_list(adj_list)

# Добавление новых ребер
for _ in range(int(input('Введите количество ребер в графе, которое вы хотите сейчас добавить: '))):
    u, v = list(map(int, input('Введите номера вершин, между которыми есть ребро (из первой во вторую) (индексация '
                               'идет с нуля): \n').split()))
    adj_list[u].append(v)

# Сохранение изменений
open('adjacency_list.json', 'w').write(json.dumps(adj_list, indent=4, ensure_ascii=False))

# Указание путя для отрисовки графов
os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'

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
