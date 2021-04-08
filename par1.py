# 1-й парсер московской биржи
import requests
import datetime
import pathlib
import apimoex
import pandas as pd

board = 'TQBR' # режим торгов

with open('TICKs.txt', mode='r') as TICKs: # открытие файла с тикерами акций
    TICKs = [line.rstrip() for line in TICKs] # собрание массива из тикеров (перебор всех строк и удаление последнего символа \n)

pathlib.Path('/Database/{}'.format(board)).mkdir(parents=True, exist_ok=True) # создание папки (и родителей) если ее не сущ

process = 0 # отображение процесса парсинга

with requests.Session() as session: # создание объекта сессии
    for TICK in TICKs:
        process += 1
        print( (process/len(TICKs)) * 100, '%' )

        data = apimoex.get_board_history(session, TICK, board=board) # получение истории торгов по опред тикеру на опред режиме торгов

        if data == []: # нету истории
            continue

        df = pd.DataFrame(data)
        df = df[['TRADEDATE', 'CLOSE']]
        df.to_excel( '/Database/{}/{}.xlsx'.format(board, TICK), index=False )
