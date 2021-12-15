# Введение
Сама задача диспетчеризации конвертерного цеха сводится к построению допустимых и оптимальных с точки зрения затрат маршрутов от каждого конвертера через агрегаты внепечной обработки к каждой установке непрерывной разливки стали (УНРС). Эти маршруты строятся из так называемых суточных заданий, то есть серий разливки стали на всех УНРС. Задача назначения маршрутов сводится к ЗЛП. В силу того, что в этой задаче имеется большое количество ограничений, возникающих как из-за особенностей технического процесса, так и из-за специфики конкретного цеха, и того что эта задача уже решена, пытаться ее решить эвристическими алгоритмами представляется иррациональным. Однако, существует задача, которую на данный момент не удолось свести к задаче линейного программирования, и на данном этапе предлагается решать эвристическими методами.
# Задача
Суточные задания строятся технологами завода, на основании выпуска определенного объема стали определенных марок. Однако, эти суточные задания зачастую оказываются нерешаемыми в контексте существующей модели. На данный момент, в таких случаях технологам приходится собственноручно изменять задания пока не будет найдено задание с существующим решением. Задача состоит в том, чтобы некий алгоритм мог автоматически подобрать структуру суточного здадания с максимальным количеством существующих решений. Как уже упоминалось ранее, простых решений для сведения такой задачи к ЗЛП пока обнаружено не было, поэтому предлагается использовать стохастические методы. 
# Входные данные
Входные данные находятся в файле input.json. Это пример суточного задания, для которого решения не существует. Оно состоит из серий разливки, и промежутков технического обсуживания. Для каждой серии известен номер УНРС, на которой сталь будет разливаться, количество плавок в серии, время начала разливки стали на УНРС (в формате timestamp), максимальной и минимальной выдежек (допустимый интервал времени между моментом отправления плавки с конвертера и ее прибытипм на УНРС), а также цикла разливки (периодичность, с которой обрабатываются плавки на УНРС). Остальные параметры не важны в контексте решаемой задачи. 
Для изменения суточного задания разрешается менять время начала разливки для каждой серии в пределах получаса в каждую сторону, а также можно увеличить цикл разливки каждой серии до получаса. 
# Функционал
Для того, чтобы оценить пригодность полученного решения применяется проецирование (с учетом выдержек) каждой серии на пространство конвертеров, и расчитывается "плотность" плавок на этом промежутке для данной серии. Далее в местах пересений этих проекций значения их плотностей складываются. Предполагается, что решение должно существовать, если максимальное значений на всем изучаемом временном промежутке меньше одного. В силу особенностей модели диспетчеризации это не всегда так, однако, чем ниже максимальная плотность, тем больше шанс существования решения. Таким образом задача сводится к минимизации максимального значения описанной функции. 
# Ограничения
1) Начало разливки на УНРС и цикл разливки не должны выходить за допустимые границы. 
2) Серии на одной и той же УНРС не должны пересекаться. 
# Реализация
Для всех перечисленных ниже методов справедлив следующий общий алгоритм:
1) Обработка входного (изначального) задания
2) Создание изначально популяции (заданной величины)
3) Расчет значений функционала каждого представителя популяции
4) Изменение популяции/создание новой популяции
5) Удаление представителей, нарушающих ограничения
6) Определение лучшего представителя, его сохранение, обновление значения минимального найденного функционала
7) Возвращение на пункт 3. Остановка если Лучшее значение функционала не обновлялось заданное количество итераций
# FPA
Для FPA методы реализованы алгоритмы глобального и локального поиска (опыления). Тот или иной метод выбирается для каждого представителя на каждой итерации с заданной вероятностью (0.8 вероятность выбора локального поиска).
Процесс локального поиска производится при выборе двух рандомных представителей и прибавлении разницы между их значениями (умноженной на случайное значение [0;1]) к значению рассмтариваемого представителя. Под значениями имеется ввиду каждый из изменямых параметров каждой серии. 
В процессе глобального поиска к значению рассматриваемого представителя прибавляется значение из симуляции "полета Леви" от разницы между значением рассматриваемого представителя и лучшим представителем. 
Если при изменении значений, они вышли за границы допустимых, эти значения заменяются на ближайшие границы. Если при изменении значений представитель нарушает ограничения, то он не изменяется на данной итерации. 
# BB-BC
Для BB-BC методы реализованы алгоритмы "большого взрыва" и "большогот сжатия". 
Первый формирует пространство новых представителей вокруг центра масс прибавлением к каждому значению от -5 до +5 минут. 
"Большое сжатие" реализовано в двух вариантах. В первом варианте за центр масс принимается лучший представитель или указанное количество лучших представителей. Во втором- вычисляется взвешенное среднее по всем значениям и принимается за центр масс. Однако по какой-то причине второй вариант не сходится, так что используется первый. 
# Генетический алгоритм
Реализован также стандартный генетический алгоритм. 
Из всего пространства представителей выбирается заданное количество лучших представителей. Затем эти представители в случайном порядке скрещиваются (порождая заданное количество потомков). Также заданное количество генов (серий суточного задания в контексте задачи) мутируют случайным образом. Лучший представитель всегда сохраняется в неизмененном виде. 
# Результаты 
Суточное задание обладает решением после изменения любым из алгоритмов. Результаты по итогу 10 запусков каждого алгоритма
## Быстродействие 
1) Генетический алгоритм 10 секунд. 
2) FPA 12 секунд
3) BB-BC 15 секунд
## Эффективность (значение функционала)
1) Генетический алгоритм в 8 из 10 случаев сходится к точному значению порядка 0.84. Отличающиеся результаты не больше 0.85
2) BB-BC 5 раз сошелся к одному и тому же значению 0.88. Остальные результаты в диапазоне от 0.84 до 0.88. Стоит отметить, что 2 раза он сошелся к тому же числу, что и генетический алгоритм 8 раз (примерно 0.84).
3) FPA не сходится к определенному значению, среднее значение функционала 0.86. Худший 0.89, лучший- 0.85. 

