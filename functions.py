def final_count(first_part, nostalgist, patriot, antagonist):
    if first_part > nostalgist and first_part > patriot and first_part > antagonist:
        x = '''<b>Вы пятая часть</b>
        Вы – в рядах победителей. 
        По мнению социологов, от развала СССР выиграла только пятая часть населения -- чуть менее 20%. 
        Они сумели встроиться в рынок, а их подушевой доход и уровень жизни близок к среднему классу Восточной Европы.
        
        Текущее положение дел в стране отвечает вашим интересам, и что-либо менять вы не намерены, власть может и не
        всегда права, но справедлива.'''
    elif nostalgist > first_part and nostalgist > patriot and nostalgist > antagonist:
        x = 'Вы коммунист'
    elif patriot > first_part and patriot > nostalgist and patriot > antagonist:
        x = 'Вы патриот'
    elif antagonist > first_part and antagonist > nostalgist and antagonist > patriot:
        x = 'Вы антогонист'
    return x

# Еще проверка слияния веток
