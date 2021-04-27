# pattern = input('Masukkan input: ')
# def prefix(dest,inputUser):
#     prefix = []
#     temp = ''
#     for i in range(0, dest):
#         temp += inputUser[i]
#         prefix.append(temp)
#     return prefix
#
# def suffix(init,dest,inputUser):
#     suffix = []
#     if(len(inputUser)>1):
#         temp = inputUser[dest-1]
#         suffix.append(temp)
#         temp3 = ''
#         for i in range(dest-2,init-1,-1):
#             temp3 = inputUser[i] + temp3
#             suffix.append(temp3+temp)
#     return suffix
# x = prefix(len(pattern),pattern)
# y = suffix(1,len(pattern),pattern)
# print(x)
# print(y)

import re
import csv
from datetime import date, datetime

class KMP:
    def partial(self, pattern):
        """ Calculate partial match table: String -> [Int]"""
        ret = [0]

        for i in range(1, len(pattern)):
            j = ret[i - 1]
            while j > 0 and pattern[j] != pattern[i]:
                j = ret[j - 1]
            ret.append(j + 1 if pattern[j] == pattern[i] else j)
        return ret


    def search(self, T, P):
        """
        KMP search main algorithm: String -> String -> [Int]
        Return all the matching position of pattern string P in T
        """
        partial, ret, j = self.partial(P), [], 0

        for i in range(len(T)):
            while j > 0 and T[i] != P[j]:
                j = partial[j - 1]
            if T[i] == P[j]: j += 1
            if j == len(P):
                ret.append(i - (j - 1))
                j = partial[j - 1]

        return ret



def convertDate(txt):
    res = ""
    if len(txt) == 8 or len(txt) == 10:
        date_obj = datetime.strptime(txt, '%d/%m/%y')
        res = date_obj.strftime('%d/%m/%Y')
    else:
        date_obj = datetime.strptime(txt,"%d %B %Y")
        res = date_obj.strftime('%d/%m/%Y')
    return res

def tryConvertDate(txt):
    date = ''
    try:
        date = convertDate(txt)
    except:
        date = txt
    finally:
        return date
def getDates(txt):
    dates = re.findall(
        '([1-9]|1[0-9]|2[0-9]|3[0-1]|0[0-9])(-|\/|\s)([1-9]|1[0-2]|0[0-9]|[A-Z][a-z]+)(-|\/|\s)([0-9][0-9][0-9][0-9]|[0-9][0-9])',
        txt)
    dates = [''.join(dates[i]) for i in range(len(dates))]
    return dates

def getMatkul(txt):
    kode_matkul = re.findall('[A-Z]{2}\d{4}', txt) #Mata Kuliah harus diawali dengan 2 Huruf besar diikuti 4 angka
    return kode_matkul

def getTopik(txt):
    topic = re.findall('[\"\'](.*)[\"\']', txt) #asumsi topik dalam text diapit oleh tanda petik 2 ("<Topik>")
    return topic

def isContainKeyInText(txt,key):
    kmp = KMP()
    kata_kunci_fix = []
    for i in range(len(key)):
        a = kmp.search(txt, key[i])
        if (len(a) != 0):
            kata_kunci_fix.append(key[i])
    return kata_kunci_fix

def printData(data):
    print("(ID: {})".format(data[0]), end=' ')
    for i in range(1, len(data) - 1):
        print(data[i], '-', end=' ')
    print(data[len(data) - 1])

def saveData(data,file):
    with open(file, mode='a') as csv_file:
        writer = csv.writer(csv_file,delimiter=',')
        writer.writerow(data)

def loadData(file):
    data = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            if len(row) != 0:
                data.append(row)
    return data

def contain(array,kata):
    ada = False
    for i in range(len(array)):
        if array[i] == kata:
            ada = True
            break
    return ada


# no 1
kata_kunci = ["Kuis", "Ujian", "Tucil","Tubes","Praktikum","deadline"]
load = loadData("data.csv")
try:
    id = int(load[len(load)-1][0])
except:
    id = 0

while True:
    load = loadData("data.csv")
    text = input()
    # text = "Tubes IF2211 topik \"String Matching\" pada 14 April 2021 dan Kuis pada 15/05/2021"
    # "halo bot, tolong ingetin kalau ada Kuis IF3310 topik:'bab 2 sampai 3' pada 22 April 2014"
    # print(text)
    dates = getDates(text)
    mataKuliah = getMatkul(text)
    topik = getTopik(text)
    key = isContainKeyInText(text,kata_kunci)
    data = []
    if (len(dates) != 0 and len(mataKuliah) != 0 and len(topik)!= 0 and len(key) != 0): #No 1
        id+=1
        date = dates[0]
        date = tryConvertDate(date)
        data.append(id)
        data.append(date)
        data.append(mataKuliah[0])
        data.append(key[0])
        data.append(topik[0])
        saveData(data,'data.csv')
        print("[Task Berhasil dicatat]")
        printData(data)
    elif((contain(key,"deadline") and contain(key,"Tucil")) or (contain(key,"deadline") and contain(key,"Tubes"))): #No 2
        print(key)
        print(mataKuliah[0])
        print(load)
        ada = False
        index = 0
        for i in range(len(load)):
            for j in range(len(key)):
                if (key[j] == load[i][3]):
                    ada = True
                    index = i
                    break
        if(ada):
            print(load[index][1])
        else:
            print("Data tidak ditemukan")



    else:
        print("Pesan Tidak diterima")

# Tubes IF2250 dengan topik "aduh" pada tanggal 12 June 2021
# deadline Tubes IF2250

