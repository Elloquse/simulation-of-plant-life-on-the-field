class Plant():
    plants = []
    
    def __init__(self, health, soil, height, illum):
        self.health = health
        self.soil = soil
        self.height = height
        self.illum = illum
        
        Plant.plants.append(self)
        
        
import random
import pandas

input_name = input('Input path to your excel file: \n')

# Генерация растений из файла эксель
exl_plants = pandas.read_excel(input_name, 0)
for i, j in exl_plants.iterrows():
    Plant(j[1], j[2], 0, j[3])


# Генерация полей из файла эксель
exl_fields = pandas.read_excel(input_name, 1)
field_dict = {}
for i, j in exl_fields.iterrows():
    field_dict[i+1] = [j[1], j[2]]



# Сортировка растений сначала по свету, потом по здоровью среди сортированных по свету
Plant.plants.sort(key=lambda x: x.illum, reverse=True)
plants_sorted = [[],[],[],[],[],[]]
illum = 5
for i in Plant.plants:
    if i.illum == illum:
        plants_sorted[i.illum].append(i)
    else:
        illum -= 1
        plants_sorted[i.illum].append(i)
for i in plants_sorted:
    i.sort(key=lambda x: x.health)
plants_sorted = [item for elem in plants_sorted for item in elem] # конвертация в обычный список
plants_sorted.reverse() # упорядочивание от большего к меньшему


# Сортировка полей по требованию к свету (от большего к меньшему)
field_dict = dict(sorted(field_dict.items(), key=lambda x: x[1][1], reverse=True))

new_dict = field_dict.copy()

# Рассадка растений на поля с подходящей почвой и освещением (первый приоритет)
for i in plants_sorted:
    for j in new_dict:
        if i.illum <= new_dict[j][1] and i.soil == new_dict[j][0] and isinstance(j, int) == True :
            new_dict[i] = new_dict.pop(j)
            plants_sorted[plants_sorted.index(i)] = 0
            break
plants_sorted = list(filter(lambda x: x != 0, plants_sorted)) # убираем 0, чтобы не было чисел для сортировки


# Замена растений растениями с бОльшим здоровьем
plants_sorted.sort(key=lambda x: x.health, reverse=True)
for i in plants_sorted:
    for j in new_dict:
        if isinstance(j, int) == False and i.health > j.health and i.soil == new_dict[j][0] and i.illum <= new_dict[j][1]:
            plants_sorted.append(j)
            new_dict[i] = new_dict.pop(j)
            plants_sorted[plants_sorted.index(i)] = 0
            break


# Рассадка растений на поле с подходящей почвой (второй приоритет)
for i in plants_sorted:
    if i != 0:
        for j in new_dict:
            if i.soil == new_dict[j][0] and isinstance(j, int) == True :
                new_dict[i] = new_dict.pop(j)
                plants_sorted[plants_sorted.index(i)] = 0
                break


# Рассадка остальных растений
for i in plants_sorted:
    if i != 0:
        for j in new_dict:
            if isinstance(j, int) == True:
                new_dict[i] = new_dict.pop(j)
                plants_sorted[plants_sorted.index(i)] = 0
                break
        
        
final_dict = new_dict.copy()
# Изменения за 10 лет
for year in range (0, 10):
    for plant in new_dict.keys():
        if isinstance(plant, int) == False:
            if plant.illum <= new_dict.get(plant)[1]:
                 plant.height += 1
            if plant.soil == new_dict.get(plant)[0]:
                 plant.health += 1
            else:
                 plant.health -= 1
                 if plant.health == 0: 
                     final_dict[random.choice([x for x in range(1, len(new_dict)) if x not in new_dict.keys()])] = final_dict.pop(plant)


# Вывод на экран финальной рассадки.
final_field = []
for key in final_dict.keys():
    if isinstance(key, int) == True:
        final_field.append(final_dict.get(key)[0])
    else:
        final_field.append([key.health, key.height])
matrix_list = [[x] if isinstance(x, str) == True else x for x in final_field]

print(matrix_list)
    