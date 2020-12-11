import os
import time
import string
import pygame

def translate_to_vietnamese_by_group_of_three_digit(n):
    dic = {
    1: {0: '', 1: 'một', 2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm', 6: 'sáu', 7: 'bảy', 8: 'tám', 9: 'chín'},
    2: {0: 'linh', 1: 'mười', 2: 'hai mươi', 3: 'ba mươi', 4: 'bốn mươi', 5: 'năm mươi', 6: 'sáu mươi', 7: 'bảy mươi', 8: 'tám mươi', 9: 'chín mươi'},
    3: {0: 'không trăm', 1: 'một trăm', 2: 'hai trăm', 3: 'ba trăm', 4: 'bốn trăm', 5: 'năm trăm', 6: 'sáu trăm', 7: 'bảy trăm', 8: 'tám trăm', 9: 'chín trăm'}
    }
    nstr = str(n)
    n_to_read = ''
    len_n = len(nstr)
    while len_n > 0:
        check_for_dic = int(nstr)//pow(10, len_n - 1)
        check_for_break = int(nstr) % pow(10, len_n - 1)
        next_str = ''
        if len_n == 1:  # check for special case
            if check_for_dic == 0 and len(n_to_read) == 0:
                next_str = "không"
            elif check_for_dic == 1 and n_to_read.endswith("mươi "):
                next_str = "mốt"
            elif check_for_dic == 5 and not n_to_read.endswith("linh "):
                next_str = "lăm"
                if n_to_read == '':
                    next_str = "năm"
            else:
                next_str = str(dic[len_n].get(check_for_dic))
        else:
            next_str = str(dic[len_n].get(check_for_dic)) # get the word in dic
        n_to_read = n_to_read + next_str + " "
        if check_for_break == 0:
            break
        nstr = nstr[1:] #remove the first character of the string
        len_n -= 1
    return n_to_read
def integer_to_vietnamese_numeral(n, region = "north", activate_tts=False):
    if isinstance(n,int) == False:
        raise TypeError("Not an integer")
    if n <= 0:
        raise ValueError("Not a positive integer")
    if n > 999999999999:
        raise OverflowError("Integer greater than 999,999,999,999")
    if not isinstance(region,str):
        raise TypeError("Argument 'region' is not a string")
    if not (region == "south" or region =="north"):
        raise ValueError("Argument 'region' has not a correct value")
    if not isinstance(activate_tts,bool):
        raise TypeError("Argument 'activate_tts' is not a boolean")
    dic = ['nghìn','triệu','tỷ']
    result = ''
    i = 0
    n_temp = n
    if n == 0:
        result = 'không '
    while n > 0:
        mod = n%1000
        mod_check = str(n)[-3:]
        if n != n_temp:
            result = dic[i] + " " + result
            i +=1
        if mod != 0:
            result = translate_to_vietnamese_by_group_of_three_digit(mod_check) + result
        n //= 1000
    
    result = result.split()
    len_res = len(result)
    for i in range(len_res-1):
        if result[i] == 'tỷ' and result[i+1] == 'triệu':
            result.remove(result[i+1])
        if result[i] == 'triệu' and result[i+1] == 'nghìn':
            result.remove(result[i+1])
        if result[i] == 'tỷ' and result[i+1] =="nghìn":
            result.remove(result[i+1])
        if len(result) < len_res:
            break
    result = " ".join(result)
    if region == "south":
        result = result.replace("linh","lẻ").replace("nghìn","ngàn")
    if activate_tts == True:
        sound_basedir = "./sounds/vie/north"
        word_to_file_dic = {
            "một":"mot1",
            "mốt":"mot2",
            "hai":"hai",
            "ba":"ba",
            "bốn":"bon",
            "năm":"nam",
            "sáu":"sau",
            "bảy":"bay",
            "tám":"tam",
            "chín":"chin",
            "mười":"muoi1",
            "mươi":"muoi2",
            "lăm":"lam",
            "lẻ":"le",
            "linh":"linh",
            "nghìn":"nghin",
            "ngàn":"ngan",
            "trăm":"tram",
            "triệu":"trieu",
            "tỷ":"ty",
            "không":"khong"
        }
        result_files = [word_to_file_dic[i]+".ogg" for i in result.split()]
        for root, dir, files in os.walk(sound_basedir):
            for f in result_files:
                if f in files:# use 1 in 2 way
                    # way 1
                    pygame.mixer.init()
                    pygame.mixer.music.load(os.path.join(root,f))  
                    pygame.mixer.music.play()
                    time.sleep(1.2)
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    # way 2
                    # time.sleep(1.3)
                    # os.system("start "+sound_basedir+'/'+f +" --play-and-exit")
    return result
# print(integer_to_vietnamese_numeral(109,"south",True))

def integer_to_english(n):
    #Check exceptions --> move to main function to check exception of n arg first
    # if not isinstance(n, int):
    #     raise TypeError('Not an integer')
    # if (n < 0):
    #     raise ValueError('Not positive integer')
    # if (n > 999999999999):
    #     raise ValueError('Integer greater than 999,999,999,999')
    #Add value to check 
    ones = {'0': '','1': 'one ', '2': 'two ','3': 'three ','4': 'four ','5': 'five ','6': 'six ',
    '7': 'seven ','8':'eight ','9': 'nine '}
    teens = {'0': 'ten ','1': 'eleven ', '2': 'twelve ','3': 'thirteen ','4': 'fourteen ','5': 'fifteen ',
    '6': 'sixteen ','7': 'seventeen ','8':'eighteen ','9': 'nineteen '}
    decades = {'0': '', '2': 'twenty ','3': 'thirty ','4': 'fourty ','5': 'fifty ', '6': 'sixty ',
    '7': 'seventy ','8':'eighty ','9': 'ninety '}
    hundreds = {'0': '','1': 'one hundred ', '2': 'two hundred ','3': 'three hundred ','4': 'four hundred ',
    '5': 'five hundred ','6': 'six hundred ','7': 'seven hundred ','8':'eight hundred ','9': 'nine hundred '}
    thousands ={'3': 'thousand, ','6': 'million, ','9': 'billion, '}

    #Set value to solve
    n = str(n)
    word = ''
    intside = n
    intlenght = len(n)
    intchange = len(n)
    change = 3

    #Code to convert
    while intchange > 0:
        if n == '0':
            word = 'zero'
            break
        if n == '1':
            word = 'one'
            break
        if intside[intchange - 2] == '1':
            for digit in ones:
                if intside[intchange - 1] == digit:
                    word = teens[digit] + word
        else:
            for digit_1 in ones:
                if intside[intchange - 1] == digit_1:
                    word = ones[digit_1] + word
            if intchange > 1:
                for digit_2 in decades:
                    if intside[intchange - 2] == digit_2:
                        word = decades[digit_2] + word
        if intchange > 2:
            for digit_3 in hundreds:
                if intside[intchange - 3] == digit_3:
                    word = hundreds[digit_3] + word
        if intchange > 3:
            word = thousands[str(change)] + word
        change += 3
        intchange -= 3
    return word

def integer_to_english_numeral(n, activate_tts=False):
    #Check exceptions
    if not isinstance(n, int):
        raise TypeError('Not an integer')
    if (n < 0):
        raise ValueError('Not positive integer')
    if (n > 999999999999):
        raise ValueError('Integer greater than 999,999,999,999')
    # if activate_tts == None:
    #     activate_tts = False
    if not isinstance(activate_tts, bool):
        raise TypeError('Not boolean value')
    # if activate_tts == False:
    #     return integer_to_english(n)
    word = integer_to_english(n)
    if activate_tts == True:
        # word = integer_to_english(n)
        dir = "./sounds/eng"
        lis = list(word.split(" "))
        rs = []
        i = 0
        while i < len(lis)-1:
            # rs.append(dir + '/' + lis[i] + '.ogg') --> unknow dir --> can't find
            rs.append(lis[i] + '.ogg') 
            i+=1
        i = 0
        # pygame.init()
        # while i < len(rs):
        for root, dir, files in os.walk(dir):
            for f in rs:
                if f in files:
                    pygame.mixer.init()
                    pygame.mixer.music.load(os.path.join(root,f))  
                    pygame.mixer.music.play()
                    time.sleep(1.2)
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                # print(rs[i])
                # sound = pygame.mixer.Sound(rs[i])
                # channel = sound.play()
                # time.sleep(1.2)
                i += 1
    return word 

# print(integer_to_english_numeral(123, True))