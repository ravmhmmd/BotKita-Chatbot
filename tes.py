import re
from datetime import date, datetime
from typing import Text
import mariadb
# Python program for KMP Algorithm
def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)
    count =0
    # create lps[] that will hold the longest prefix suffix 
    # values for pattern
    lps = [0]*M
    j = 0 # index for pat[]
  
    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pat, M, lps)
  
    i = 0 # index for txt[]
    while i < N:
        
        if pat[j] == txt[i]:
            i += 1
            j += 1
  
        if j == M:
            #print ("Found pattern at index " + str(i-j))
            count +=1
            return i-j
            j = lps[j-1]
        
        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
        #print(count)
    #return count
def computeLPSArray(pat, M, lps):
    len = 0 # length of the previous longest prefix suffix
  
    lps[0] # lps[0] is always 0
    i = 1
  
    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i]== pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar 
            # to search step.
            if len != 0:
                len = lps[len-1]
  
                # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i += 1

def stemInput(input, str1):
    hasil = input.split()
    found = False
    for elmt in hasil:
        if elmt == str1:
            found = True
            break
    return found

def getDate(date):
    result = re.search(r'(\b\d{1,2}\D{0,3})? (?:(J|j)(?:anuari)|(F|f)(?:ebruari)|(M|m)(?:aret)|(A|a)(?:pril)|(M|m)(?:ei)|(J|j)(?:uni)|(J|j)(?:uli)|(A|a)(?:ugustus)|(S|S)(?:eptember)|(O|o)(?:ktober)|(Nov|Des|nov|des)(?:ember)?) (?:1\d{3}|2\d{3})(?=\D|$)' ,date)
    if result == None:
         res = re.search(r'\b(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/(1\d{1}|2\d{1})$' ,date)
         return res.group()
    return result.group()

def getKodeKuliah(text):
    result = re.search(r'\b(?:IF1\d{3}|IF2\d{3}|IF3\d{3}|IF4\d{3})\b' ,text)
    return result.group()

def deleteSubstring(query, text):
    result = re.sub(query, "", text)
    return result

def convertDate(text):
    res = ""
    if len(text) == 8:
        date_obj = datetime.strptime(text, '%d/%m/%y')
        res = date_obj.strftime('%d/%m/%Y')
    else:
        date_obj = datetime.strptime(text,"%d %B %Y")
        res = date_obj.strftime('%d/%m/%Y')
    return res

def inputValue(text, query):
    stemText = text[KMPSearch(query,text):]
    kodeKuliah = getKodeKuliah(stemText)
    tanggal = getDate(stemText)
    stemText = deleteSubstring(tanggal, stemText)
    stemText = deleteSubstring(kodeKuliah, stemText)
    tanggal = convertDate(tanggal) # convert to dd/mm/yy
    # get deskripsi 
    stemText = stemText.split()
    stemText.pop(0) # remove kata kunci
    stemText.pop(len(stemText)-1)
    deskripsi = ' '.join(stemText)
    return (kodeKuliah, deskripsi, tanggal)

def checkCommand(turn):
    
    inpt = input()
    conn = mariadb.connect(user="root", password="", host="localhost", database="stima")
    cur = conn.cursor()

    if stemInput(inpt, "tubes"):
        (kodeKuliah, deskripsi, tanggal) = inputValue(inpt, "tubes")
        cur.execute("INSERT INTO tubes VALUES (?, ?, ?);", (kodeKuliah, deskripsi, tanggal))
        print("TASK BERHASIL DICATAT")
        print("(ID:",turn,")", tanggal, "-", kodeKuliah,"- Tubes -", deskripsi)

    elif stemInput(inpt, "Tubes"):
        (kodeKuliah, deskripsi, tanggal) = inputValue(inpt, "Tubes")
        cur.execute("INSERT INTO tubes VALUES (?, ?, ?);", (kodeKuliah, deskripsi, tanggal))
        print("TASK BERHASIL DICATAT")
        print("(ID:",turn,")", tanggal, "-", kodeKuliah,"- Tubes -", deskripsi)

    elif stemInput(inpt, "tucil"):
        (kodeKuliah, deskripsi, tanggal) = inputValue(inpt, "tucil")
        cur.execute("INSERT INTO tucil VALUES (?, ?, ?);", (kodeKuliah, deskripsi, tanggal))
        print("TASK BERHASIL DICATAT")
        print("(ID:",turn,")", tanggal, "-", kodeKuliah,"- Tucil -", deskripsi)

    elif stemInput(inpt, "Tucil"):
        (kodeKuliah, deskripsi, tanggal) = inputValue(inpt, "Tucil")
        cur.execute("INSERT INTO tucil VALUES (?, ?, ?);", (kodeKuliah, deskripsi, tanggal))
        print("TASK BERHASIL DICATAT")
        print("(ID:",turn,")", tanggal, "-", kodeKuliah,"- Tucil -", deskripsi)

    elif stemInput(inpt, "ujian"):
        (kodeKuliah, deskripsi, tanggal) = inputValue(inpt, "ujian")
        cur.execute("INSERT INTO ujian VALUES (?, ?, ?);", (kodeKuliah, deskripsi, tanggal))
        print("TASK BERHASIL DICATAT")
        print("(ID:",turn,")", tanggal, "-", kodeKuliah,"- Ujian -", deskripsi)

    elif stemInput(inpt, "Ujian"):
        (kodeKuliah, deskripsi, tanggal) = inputValue(inpt, "Ujian")
        cur.execute("INSERT INTO ujian VALUES (?, ?, ?);", (kodeKuliah, deskripsi, tanggal))
        print("TASK BERHASIL DICATAT")
        print("(ID:",turn,")", tanggal, "-", kodeKuliah,"- Ujian -", deskripsi)

    elif stemInput(inpt, "kuis"):
        (kodeKuliah, deskripsi, tanggal) = inputValue(inpt, "kuis")
        cur.execute("INSERT INTO kuis VALUES (?, ?, ?);", (kodeKuliah, deskripsi, tanggal))
        print("TASK BERHASIL DICATAT")
        print("(ID:",turn,")", tanggal, "-", kodeKuliah,"- Kuis -", deskripsi)

    elif stemInput(inpt, "Kuis"):
        (kodeKuliah, deskripsi, tanggal) = inputValue(inpt, "Kuis")
        cur.execute("INSERT INTO kuis VALUES (?, ?, ?);", (kodeKuliah, deskripsi, tanggal))
        print("TASK BERHASIL DICATAT")
        print("(ID:",turn,")", tanggal, "-", kodeKuliah,"- Kuis -", deskripsi)
    else:        
        print("Maaf, pesan tidak dikenali")
    conn.commit()
turn  = 1
while True:
    checkCommand(turn)
    turn += 1

# "halo bot, tolong ingetin kalau ada kuis IF3310 bab 2 sampai 3 pada 22 april 2014"