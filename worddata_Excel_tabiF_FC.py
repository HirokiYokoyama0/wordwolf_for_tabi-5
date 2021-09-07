import openpyxl
import random

def create_word_TF(GENRUNUM = 1):

    workbook = openpyxl.load_workbook('ワードウルフ単語_TF.xlsx')
    sheet = workbook["General"]
    max_row_num = sheet.max_row
    word_data = []
    qest_data = []
    genre_data = []


        ##ジャンル取得
        #print(" max_row_num----> ",max_row_num)

    for k in range(2,8):
        genre = sheet.cell(row=k, column=1).value
        genre_data.append(genre)


    #word取得
  

    for j in range(2,13):  #word
        word = sheet.cell(row=GENRUNUM+1, column=j).value
        if word is None:
            break
        else:
            print("word ---> ",word)
            word_data.append(word)

    
    for j in range(14,17): #質問例
        qest = sheet.cell(row=GENRUNUM+1, column=j).value
        if  qest is None:
            qest_data.append(qest)
        else:
            qest_data.append("")


    selected_word = random.sample(word_data,2)
    print("selected_word ==>",selected_word)
    
    return selected_word,qest_data

  



