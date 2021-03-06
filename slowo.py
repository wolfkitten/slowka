'''author: Marek Mikołajczyk
Program do nauki slówek języka angielskiego.
Program pozyskuje slowa zestrony google tanslate po jego uruchomiwniu.
Dane przechowyne są w bazie danych MySQL'''

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import random
import data


dictionary_words = data.bd_main.show_words_in_dict('marek', 'pol', 'ang')

words_eng = [word for word in dictionary_words]
words_pol = [dictionary_words[keys] for keys in dictionary_words]

'''zaminienia slowo wpowadzone na liste znakow'''
def list_letter(word):
    for letter in range(len(word)):
        yield word[letter]

'''#spr. dlugosc podannego slowa ze slowem ze zbioru. 
Wyrównuje ich dlugosc, wstawiaja lub usuwajac zanki ze slowa'''
def check_len_word(list_words,find_word,index_random_words):
    list_find_word=list(list_letter(find_word))
    if len(list_words[index_random_words]) == len(list_find_word):
        return list_find_word
    elif len(list_words[index_random_words]) > len(list_find_word):
        list_find_word += '-' * (len(list_words[index_random_words]) - len(list_find_word))
    elif len(list_words[index_random_words]) < len(list_find_word):
        while len(list_find_word) > len(list_words[index_random_words]):
            list_find_word.pop(len(list_find_word)-1)
    return list_find_word

'''spr znaki w słowie uzytym i wpisamyn. 
Tworzy liste ze znakami poprawnymi. w
Źle wpisane znaki zamienia na '-' '''
def check_word(lang_list_words,find_word,index_random_words):
    list_char_word = list()
    for i in range(len(lang_list_words[index_random_words])):
        if lang_list_words[index_random_words][i] == check_len_word(lang_list_words,find_word,index_random_words)[i]:
            list_char_word.append(check_len_word(lang_list_words,find_word,index_random_words)[i])
        else:
            list_char_word.append('-')
    return list_char_word

'''Wybór opcji językowej, okreslenie zbioru poszukiwanego'''
def select_lang_version(lang_version_list,index_random_words):
    if lang_version_list == words_pol: #spr warunku jezykowego (odpoweidz po polsku)
        return words_eng[index_random_words]
    elif lang_version_list == words_eng: #spr warunku jezykowego (odpoweidz po angielsku)
        return words_pol[index_random_words]

''' Pęta az to wpisania pożądanego słowa'''
def loop_looking_word(lang_version_list,index_random_words,find_word = ''):
    while find_word != lang_version_list[index_random_words]:
        find_word = input(select_lang_version(lang_version_list,index_random_words) + ' = '
                          + str(check_word(lang_version_list,find_word,index_random_words))).upper() #szukane (wpisywane) slowo
        print('Podano : ' + find_word)  # wydruk poszukiwanego slowaP
        if find_word == lang_version_list[index_random_words]:
            print('dobrze\n')
            break
        elif find_word == 'N': #po wpisanu n pokazuje slowo szukane
            print(select_lang_version(lang_version_list,index_random_words) + ' = '
                  + lang_version_list[index_random_words]+'\n')  # słówko ang i znaczenie polskie
            break

'''Peta kolejnych słów wpisywanydata.bd_main.show_words_in_dict('slowka','pol','ang')ch + usówanie ze zbioru uzytego slowa'''
def loop_next_word(lang_version_list):
    while len(lang_version_list) > 0:
        index_random_words = random.randint(0, len(lang_version_list) - 1)  # losowanie indexu w zdiorze słóów
        loop_looking_word(lang_version_list,index_random_words,find_word = '') #opdowiedź po polsku, tytaj wybiera sie jezyk w jakim chce sie odpowiadać.
        if lang_version_list == words_eng:
            lang_version_list.pop(index_random_words)
            words_pol.pop(index_random_words)
        elif lang_version_list == words_pol:
            lang_version_list.pop(index_random_words)
            words_eng.pop(index_random_words)

'''zakończenie programu, uruchomienie ponownie, 
pobranie nowego zbioru słów do programy, ponowny wybór wersji językowej '''
def loop_quit_program(lang_version_list,quit_program=''):
    while quit_program != 'y': # pętla do póki nie wybierzes się 'y' przy zakończeniu programu
        loop_next_word(lang_version_list) # tu nalezy określić wersję językową
        quit_program = input('Czy zakończyć (y/n)')
        if quit_program == 'n': # określenie warunków przy wyborze 'n'. Wybór wersji językowej, uzupełnienie słów w zbiorze
            again_words_eng = [word for word in dictionary_words] #ponownie imprementowany zbiór słów ang
            again_words_pol = [dictionary_words[keys] for keys in dictionary_words] #ponownie imprementowany zbiór słów pol
            for words in again_words_eng:
                words_eng.append(words)
            for words in again_words_pol:
                words_pol.append(words)
            loop_next_word(choice_language_version())#ponowny wybór wersji językowej + wpisywanie slów

'''Określenie przez użytkownika wersji językowej'''
def choice_language_version(lang_version_list=''):
    while lang_version_list != 'pol' or lang_version_list != 'ang':
        lang_version_list=input('Wybierz w jakim języku chcesz odpowiadać (pol/ang) ')
        if lang_version_list == 'pol':
            return words_pol
        elif lang_version_list == 'ang':
            return words_eng


#loop_quit_program(choice_language_version())
