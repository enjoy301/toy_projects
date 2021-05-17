import hangul_utils

ja = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
mo = ['ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ','ㅐ','ㅒ','ㅔ','ㅖ','ㅢ','ㅚ','ㅟ']
mo1 = ['ㅗ', 'ㅜ']
mo2 = ['ㅏ', 'ㅐ']
mo3 = ['ㅓ', 'ㅔ']
mo4 = ['ㅘ', 'ㅙ', 'ㅝ', 'ㅞ']
ssang = ['ㄱ','ㄷ','ㅂ','ㅅ','ㅈ']
jong = [['ㄱ', 'ㅅ', 'ㄳ'], ['ㄴ', 'ㅈ', 'ㄵ'], ['ㄴ', 'ㅎ', 'ㄶ'], ['ㄹ', 'ㄱ', 'ㄺ'], ['ㄹ', 'ㅁ', 'ㄻ'],
        ['ㄹ', 'ㅂ', 'ㄼ'], ['ㄹ', 'ㅅ', 'ㄽ'], ['ㄹ', 'ㅌ', 'ㄾ'], ['ㄹ', 'ㅍ', 'ㄿ'], ['ㄹ', 'ㅎ', 'ㅀ'],
        ['ㅂ', 'ㅅ', 'ㅄ']]
checker1 = 0
checker2 = 0
temp_ch = ''
my_word = ''
while True:
    ch = input()
    if ch != temp_ch:
        if ch in ja: #자음입력
            for i in range(0, 11):
                if ch == jong[i][1] and temp_ch == jong[i][0]:
                    my_word = my_word[:-1]
                    my_word += jong[i][2]
                    checker1 = 1
                    checker2 = 1
                    break
            if checker1 == 0: # 자음특수한 경우가 아닐때
                checker2 = 0
                my_word += ch
            temp_ch = ch
            print(hangul_utils.join_jamos(my_word))
            checker1 = 0
        elif ch in mo: #모음입력
            if temp_ch == 'ㅗ' and ch in mo2: # ㅗ였고 ㅏorㅐ이면
                my_word = my_word[:-1]
                temp_ch = ch
                ch = mo4[mo2.index(ch)]
            elif temp_ch == 'ㅜ' and ch in mo3: # ㅜ였고 ㅓorㅔ이면
                my_word = my_word[:-1]
                temp_ch = ch
                ch = mo4[mo3.index(ch) + 2]
            else: # 그냥 모음
                if checker2 == 1:
                    l = my_word[-1]
                    my_word = my_word[:-1]
                    for i in range(0, 11):
                        if jong[i][2] == l:
                            my_word+=jong[i][0]
                            my_word+=jong[i][1]
                            break
                    checker2 = 0
                else:
                    temp_ch = ch
            my_word += ch
            print(hangul_utils.join_jamos(my_word))
        else: # a or b 입력
            checker2 = 0
            if ch == 'a':
                if temp_ch in ssang:
                    my_word = my_word[:-1]
                    my_word += chr(ord(temp_ch) + 1)
            elif ch == 'c':
                my_word = my_word[:-1]
            elif ch == 'd':
                my_word += ' '
            temp_ch = ch
            print(hangul_utils.join_jamos(my_word))