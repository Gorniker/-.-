# Введение
Сама задача диспетчеризации конвертерного цеха сводится к построению допустимых и оптимальных с точки зрения затрат маршрутов от каждого конвертера через агрегаты внепечной обработки к каждой установке непрерывной разливки стали (УНРС). Эти маршруты строятся из так называемых суточных заданий, то есть серий разливки стали на всех УНРС. Задача назначения маршрутов сводится к ЗЛП. В силу того, что в этой задаче имеется большое количество ограничений, возникающих как из-за особенностей технического процесса, так и из-за специфики конкретного цеха, и того что эта задача уже решена, пытаться ее решить эвристическими алгоритмами представляется иррациональным. Однако, существует задача, которую на данный момент не удолось свести к задаче линейного программирования, и на данном этапе предлагается решать эвристическими методами.
# Задача
Суточные задания строятся технологами завода, на основании выпуска определенного объема стали определенных марок. Однако, эти суточные задания зачастую оказываются нерешаемыми в контексте существующей модели. На данный момент, в таких случаях технологам приходится собственноручно изменять задания пока не будет найдено задание с существующим решением. Задача состоит в том, чтобы некий алгоритм мог автоматически подобрать структуру суточного здадания с максимальным количеством существующих решений. Как уже упоминалось ранее, простых решений для сведения такой задачи к ЗЛП пока обнаружено не было, поэтому предлагается использовать стохастические методы. 
# Входные данные
Входные данные находятся в файле input.json. Это пример суточного задания, для которого решения не существует. Оно состоит из серий разливки, и промежутков технического обсуживания. Для каждой серии известен номер УНРС, на которой сталь будет разливаться, количество плавок в серии, время начала разливки стали на УНРС (в формате timestamp), максимальной и минимальной выдежек (допустимый интервал времени между моментом отправления плавки с конвертера и ее прибытипм на УНРС), а также цикла разливки (периодичность, с которой обрабатываются плавки на УНРС). Остальные параметры не важны в контексте решаемой задачи. 
Для изменения суточного задания разрешается менять время начала разливки для каждой серии в пределах получаса в каждую сторону, а также можно увеличить цикл разливки каждой серии до получаса. 
# Функционал
Для того, чтобы оценить пригодность полученного решения применяется проецирование (с учетом выдержек) каждой серии на пространство конвертеров, и расчитывается "плотность" плавок на этом промежутке для данной серии. Далее в местах пересений этих проекций значения их плотностей складываются. Предполагается, что решение должно существовать, если максимальное значений на всем изучаемом временном промежутке меньше одного. В силу особенностей модели диспетчеризации это не всегда так, однако, чем ниже максимальная плотность, тем больше шанс существования решения. Таким образом задача сводится к минимизации максимального значения описанной функции. 
# FPA

