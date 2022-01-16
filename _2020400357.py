import re
handle = open('calc.in', 'r')
word_list = []
line_list = []
line_list2 = []

for line in handle:
    for word in line.split():
        word_list.append(word)
        line_list2.append(word)
    if line_list2 == []:
        continue
    else:
        line_list.append(line_list2)
        line_list2 = []
handle.close()
string = ''
for i in line_list:
    for t in i:
        string += t + ' '
    line_list2.append(string.strip())
    string = ''

reserved_list = ['olsun','degeri', 'AnaDegiskenler', 'YeniDegiskenler', 'Sonuc', 'dogru', 'yanlis' , 'nokta', 'ac-parantez',
                 'kapa-parantez', '(', ')','arti','eksi','carpi','+','-','*','ve','veya']
numbers = ['sifir','bir','iki','uc','dort','bes','alti','yedi','sekiz','dokuz']
numbers2 = ['sifir','bir','iki','uc','dort','bes','alti','yedi','sekiz','dokuz']
booleans = ['dogru','yanlis']
number_operations = ['arti','eksi','carpi','+','-','*','nokta']
boolean_operations = ['ve','veya']
for i in range(10):
    for t in range(10):
        a = numbers[i] + ' nokta ' + numbers[t]
        numbers.append(a)
for i in range(10):
    numbers.append(str(i))
    for t in range(10):
        a = i + t/10
        numbers.append(str(a))

def no_error():
    f = open('calc.out','w')
    f.write('Here Comes the Sun')
    f.close()
    return
def error():
    f = open('calc.out','w')
    f.write('Dont Let Me Down')
    f.close()
    return

control = True
while control == True:
    #part control
    if word_list[0] == 'AnaDegiskenler' and line_list2.count('YeniDegiskenler') == 1 and \
            line_list2.count('AnaDegiskenler')==1 and line_list2.count('Sonuc')==1:
        pass
    else:
        control = False
        error()
        break
    #Ana degisken part
    for i in range(len(line_list2)):
        if line_list2[i] == 'YeniDegiskenler':
            yeniDegiskenlerLoc = i
    degiskenDict = {}
    degiskenNumDict = {}
    degiskenBoolDict = {}
    for i in range(1, yeniDegiskenlerLoc):
        if [line_list2[i]] == re.findall("[A-Za-z0-9]+ degeri .* olsun",line_list2[i]):
            list1 = re.findall("([A-Za-z0-9]+) degeri (.*) olsun", line_list2[i])
            if list1[0][1] in numbers and list1[0][0] not in reserved_list + numbers \
                    and list1[0][0] not in degiskenDict.keys() and len(list1[0][0]) <= 10:
                degiskenNumDict[list1[0][0]] = list1[0][1]
                degiskenDict[list1[0][0]] = list1[0][1]
            elif list1[0][1] in booleans and list1[0][0] not in reserved_list + numbers \
                    and list1[0][0] not in degiskenDict.keys() and len(list1[0][0]) <= 10:
                degiskenBoolDict[list1[0][0]] = list1[0][1]
                degiskenDict[list1[0][0]] = list1[0][1]
            else:
                control = False
                error()
                break
        else:
            control = False
            error()
            break

    # Yeni degisken part
    for i in range(len(line_list2)):
        if line_list2[i] == 'Sonuc':
            sonucLoc = i
    for i in range(yeniDegiskenlerLoc+1,sonucLoc):
        if [line_list2[i]] == re.findall("[A-Za-z0-9]+ degeri .* olsun",line_list2[i]):
            list2 = re.findall("([A-Za-z0-9]+) degeri (.*) olsun", line_list2[i])
            if list2[0][0] not in reserved_list + numbers and list2[0][0] not in degiskenDict.keys() and len(list2[0][0]) <= 10:
                if list2[0][1].count('ac-parantez') + list2[0][1].count('(') == list2[0][1].count('kapa-parantez') + list2[0][1].count(')'):
                    list3 = list2[0][1].split()
                    acParantezList = []
                    kapaParantezList = []
                    if list3[0] in ['kapa-parantez',')']:
                        control=False
                        break
                    if list3[-1] in ['ac-parantez','(']:
                        control=False
                        break
                    for t in range(len(list3)):
                        if list3[t] == 'ac-parantez' or list3[t] == '(':
                            acParantezList.append(t)
                        if list3[t] == 'kapa-parantez' or list3[t] == ')':
                            kapaParantezList.append(t)
                    for k in acParantezList:
                        for t in range(len(kapaParantezList)-1,-1,-1):
                            if k == kapaParantezList[t]-1:
                                control = False
                                error()
                                break
                    for t in kapaParantezList:
                        if list3[t-1] in number_operations:
                            control = False
                            break
                    for t in acParantezList:
                        if list3[t+1] in number_operations:
                            control = False
                            break
                    for t in range(len(acParantezList)):
                        if acParantezList[t] < kapaParantezList[t]:
                            pass
                        else:
                            control = False
                            error()
                            break

                    for t in range(len(list3)):
                        if list3[t] == 'nokta':
                            if list3[t-1] in numbers2 and list3[t+1] in numbers2:
                                pass
                            else:
                                control = False
                                break
                    for t in range(len(list3)-1,-1,-1):
                        if list3[t] in ['ac-parantez','kapa-parantez','(',')']:
                            list3.pop(t)
                    operation_list = []
                    value_list = []
                    for t in list3:
                        if t in numbers + booleans or t in degiskenDict.keys():
                            value_list.append(t)
                        if t in number_operations + boolean_operations:
                            operation_list.append(t)
                    if len(operation_list) == len(value_list)-1:
                        pass
                    else:
                        control = False
                        error()
                        break
                    for t in range(len(list3)):
                        if (t % 2 == 0 and list3[t] in degiskenDict.keys()) or (t % 2 == 0 and list3[t] in numbers + booleans) \
                                or (t % 2 == 1 and list3[t] in number_operations+boolean_operations+['ac-parantez', 'kapa-parantez', '(', ')']):
                            continue
                        else:
                            control = False
                            error()
                            break
                    control2 = 0
                    for t in list3:
                        if t in degiskenNumDict.keys() or t in numbers + number_operations:
                            continue
                        else:
                            control2 = 1
                            break
                    if control2 == 0:
                        degiskenNumDict[list2[0][0]] = 'number'
                        degiskenDict[list2[0][0]] = 'number'
                    if control2 == 1:
                        for t in list3:
                            if (t in degiskenBoolDict.keys() or t in booleans + boolean_operations):
                                continue
                            else:
                                control2 = 2
                                break
                    if control2 == 1:
                        degiskenBoolDict[list2[0][0]] = 'bool'
                        degiskenDict[list2[0][0]] = 'bool'
                    if control2 == 2:
                        control= False
                        error()
                        break
                else:
                    control=False
                    error()
                    break
            else:
                control = False
                error()
                break
        else:
            control = False
            error()
            break
    #sonuc part
    if len(line_list2)-sonucLoc-1 > 1:
        control = False
        error()
        break
    for i in range(sonucLoc+1,len(line_list2)):
        if line_list2.count('ac-parantez')+line_list2.count('(') == line_list2.count('kapa-parantez')+line_list2.count(')'):
            list4 = line_list2[i].split()
            acParantezList1 = []
            kapaParantezList1 = []
            if list4[0] in ['kapa-parantez', ')']:
                control = False
                break
            if list4[-1] in ['ac-parantez', '(']:
                control = False
                break
            for t in range(len(list4)):
                if list4[t] == 'ac-parantez' or list4[t] == '(':
                    acParantezList1.append(t)
                if list4[t] == 'kapa-parantez' or list4[t] == ')':
                    kapaParantezList1.append(t)

            for k in acParantezList1:
                for t in range(len(kapaParantezList1) - 1, -1, -1):
                    if k == kapaParantezList1[t] - 1:
                        control = False
                        error()
                        break
            for t in kapaParantezList1:
                if list4[t - 1] in number_operations:
                    control = False
                    break
            for t in acParantezList1:
                if list4[t + 1] in number_operations:
                    control = False
                    break

            for t in range(len(acParantezList1)):
                if acParantezList1[t] < kapaParantezList1[t]:
                    pass
                else:
                    control = False
                    error()
                    break

            for t in range(len(list4)):
                if list4[t] == 'nokta':
                    if list4[t - 1] in numbers2 and list4[t + 1] in numbers2:
                        pass
                    else:
                        control = False
                        break
            for t in range(len(list4)-1,-1,-1):
                if list4[t] in ['ac-parantez', 'kapa-parantez', '(', ')']:
                    list4.pop(t)
            operation_list2 = []
            value_list2 = []
            for t in list4:
                if t in numbers + booleans or t in degiskenDict.keys():
                    value_list2.append(t)
                if t in number_operations + boolean_operations:
                    operation_list2.append(t)
            if len(operation_list2) == len(value_list2) - 1:
                pass
            else:
                control = False
                error()
                break

            for t in range(len(list4)):
                if (t % 2 == 0 and list4[t] in degiskenDict.keys()) or (t % 2 == 0 and list4[t] in numbers+booleans) or \
                        (t % 2 == 1 and list4[t] in number_operations + boolean_operations + ['ac-parantez', 'kapa-parantez', '(', ')']):
                    continue
                else:
                    control = False
                    error()
                    break
            control3 = 0
            for t in list4:
                if (t in degiskenNumDict.keys() or t in numbers + number_operations):
                    continue
                else:
                    control3 = 1
                    break
            if control3 == 1:
                for t in list4:
                    if (t in degiskenBoolDict.keys() or t in booleans + boolean_operations):
                        continue
                    else:
                        control3 = 2
                        break
            if control3 == 2:
                control = False
                error()
                break
        else:
            control=False
            error()
            break
    if control == True:
        no_error()
    if control == False:
        error()
    break
