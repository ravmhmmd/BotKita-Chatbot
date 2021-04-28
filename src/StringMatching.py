import re
from datetime import datetime, date, timedelta
import mariadb

class KMP:
    def partial(self, pattern):

        result = [0]

        for i in range(1, len(pattern)):
            j = result[i-1]
            while j > 0 and pattern[j] != pattern[i]:
                j = result[j - 1]
            result.append(j + 1 if pattern[j] == pattern[i] else j)
        return result


    def search(self, text, query):
        # Mengembalikan semua query posisi yang cocok dari query pada text input
        
        partial = self.partial(query)
        ret = []
        j = 0

        for i in range(len(text)):
            while j > 0 and text[i] != query[j]:
                j = partial[j - 1]
            if text[i] == query[j]: j += 1
            if j == len(query):
                ret.append(i - (j - 1))
                j = partial[j - 1]

        return ret

def getDate(date):
# 
    result = re.search(r'(\b\d{1,2}\D{0,3})? (?:(J|j)(?:anuari)|(F|f)(?:ebruar)|(M|m)(?:aret)|(A|a)(?:pril)|(M|m)(?:ei)|(J|j)(?:uni)|(J|j)(?:uli)|(A|a)(?:ugustus)|(S|S)(?:eptember)|(O|o)(?:ktober)|(Nov|Des|nov|des)(?:ember)?) (?:1\d{3}|2\d{3})(?=\D|$)' ,date)
    if result == None:
         reslt = re.search(r'\b(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/(1\d{1}|2\d{1})$' ,date)
         if reslt == None:
             res = re.search(r'\b(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/(1\d{3}|2\d{3})$' ,date)
             return res.group()
         return reslt.group()
    return result.group()

def getDualDate(date):

    result = re.search(r'\b((0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/(1\d{3}|2\d{3})\s\D+\s(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/(1\d{3}|2\d{3}))$' ,date)
    if result == None:
        return result
    result = result.group().split()
    result.pop(1)
    return result

def getKodeKuliah(text):
    result = re.search(r'\b(?:IF1\d{3}|IF2\d{3}|IF3\d{3}|IF4\d{3})\b' ,text)
    return result

def getId(text):
    result = re.search(r'\b(?:ID: \d{1}|ID: \d{2})\b' ,text)
    return result.group()

def getDeadline(date):
    result = re.search(r'\b(?:((?:[1-4]) (minggu|bulan|Minggu|Bulan)|(?:([1-9]|[12][0-9]|3[01]) (hari|Hari))))\b' ,date)
    return result

def getJenisTask(list1, list2):
    result = checkElmtList(list1, list2)
    return result

def deleteSubstring(query, text):
    result = re.sub(query, "", text)
    return result

def uppercaseTask(text):
    chars = list(text)
    chars[0] = chars[0].upper()
    string = ''.join(chars)
    return string

def convertMonth(date):
    idx = 0
    date = date.split()
    bln = date[1]
    bln = uppercaseTask(bln)
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    for i in range(len(bulan)):
        if bln == bulan[i]:
            idx = i
    date[1] = month[idx]
    date = ' '.join(date)
    return date

def convertDate(date):
    res = ""
    if len(date) == 8:
        date_obj = datetime.strptime(date, '%d/%m/%y')
        res = date_obj.strftime('%d/%m/%Y')
    else:
        convert_date = convertMonth(date)
        date_obj = datetime.strptime(convert_date,"%d %B %Y")
        res = date_obj.strftime('%d/%m/%Y')
    return res

def changeDateToSqlFormat(date):
    date = datetime.strptime(date, "%d/%m/%Y").strftime('%Y-%m-%d')
    return date

def changeDateFormat(date):
    date = datetime.strptime(date, "%Y-%m-%d").strftime('%d/%m/%Y')
    return date

def convertDeadlinetoDate(text):
    text = text.split()
    today = date.today()
    jumlah = int(text[0])
    if text[1] == "minggu" or text[1] == "Minggu":
        endDate = today + timedelta(weeks=jumlah)
    elif text[1] == "bulan" or text[1] == "Bulan":
        endDate = today + timedelta(weeks=jumlah*4)
    elif text[1] == "hari" or text[1] == "Hari":
        endDate = today + timedelta(days=jumlah)
    endDate = endDate.strftime("%Y-%m-%d")
    return endDate

def inputValue(text, query):
    kmp = KMP()
    
    stemText = text[kmp.search(text, query)[0]:]
    kodeKuliah = getKodeKuliah(stemText).group()
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

def checkElmtList(list1, list2):
    return list(set(list1).intersection(list2))

def stemInput2(text):
    text = text.split()
    return text

def getFromDatabase(jenis, Id):
    global conn
    global cur
    cur.execute("SELECT "+jenis+" FROM data WHERE id_task = '"+Id+"';")
    for row in cur.fetchall():
        return row[0]

def cariDeadline(inpt):
    global conn
    global cur

    kodeKuliah = getKodeKuliah(inpt).group()
    cur.execute("SELECT tanggal FROM data WHERE kode_matkul = '"+kodeKuliah+"';")
    for row in cur.fetchall():
        return str(row[0]) 

def showDeadlineWithJenisTask(deadlinePerSatuanWaktu, task, listText):
    global conn
    global cur

    deadlineDateSql = convertDeadlinetoDate(deadlinePerSatuanWaktu.group())
    jenisTask = getJenisTask(task, listText)[0]
    upper_jenisTask = uppercaseTask(jenisTask)

    kodeMatkul= ""
    deskripsi =""
    jenisTask =""
    tanggal = ""
    output = ""
    cur.execute("SELECT * FROM data WHERE jenis_task = '"+upper_jenisTask+"' AND tanggal < '"+deadlineDateSql+"';")
    for row in cur.fetchall():
        (A,B,C,D, E) = row
        Id = A
        kodeMatkul = B
        deskripsi = C
        jenisTask = D
        tanggal = str(E)
        output += Id+" "+tanggal+" - "+ kodeMatkul+" - "+jenisTask+" - "+deskripsi+"<br>"

    if output == "":
        output = "Tidak ada"
        
    return output

def showDeadline(deadlinePerSatuanWaktu):
    global conn
    global cur

    deadlineDateSql = convertDeadlinetoDate(deadlinePerSatuanWaktu.group())

    kodeMatkul= ""
    deskripsi =""
    jenisTask =""
    tanggal = ""
    output = ""
    cur.execute("SELECT * FROM data WHERE tanggal <= '"+deadlineDateSql+"';")
    for row in cur.fetchall():
        (A,B,C,D, E) = row
        Id = A
        kodeMatkul = B
        deskripsi = C
        jenisTask = D
        tanggal = str(E)
        output += Id+" "+tanggal+" - "+ kodeMatkul+" - "+jenisTask+" - "+deskripsi+"<br>"

    if output == "":
        output = "Tidak ada"
        
    return output

def showDeadlineInterval(batasBawah, batasAtas):
    global conn
    global cur

    fromDate = changeDateToSqlFormat(batasBawah)
    dueDate = changeDateToSqlFormat(batasAtas)

    kodeMatkul= ""
    deskripsi =""
    jenisTask =""
    tanggal = ""
    output = ""
    cur.execute("SELECT * FROM data WHERE tanggal >= '"+fromDate+"' AND tanggal <= '"+dueDate+"';")
    for row in cur.fetchall():
        (A,B,C,D, E) = row
        Id = A
        kodeMatkul = B
        deskripsi = C
        jenisTask = D
        tanggal = str(E)
        output += Id+" "+tanggal+" - "+ kodeMatkul+" - "+jenisTask+" - "+deskripsi+"<br>"

    if output == "":
        output = "Tidak ada"
        
    return output

def showAllDeadline():
    global conn
    global cur

    kodeMatkul= ""
    deskripsi =""
    jenisTask =""
    tanggal = ""
    output = ""
    cur.execute("SELECT * FROM data;")
    for row in cur.fetchall():
        (A,B,C,D, E) = row
        Id = A
        kodeMatkul = B
        deskripsi = C
        jenisTask = D
        tanggal = str(E)
        output += Id+" "+tanggal+" - "+ kodeMatkul+" - "+jenisTask+" - "+deskripsi+"<br>"
        
    return output

def inputCommand(text):
    global conn
    global cur
    global turn

    task = ["kuis", "Kuis", "ujian", "Ujian", "Tubes", "tubes", "Tucil", "tucil", "praktikum", "Praktikum"]
    listText = stemInput2(text)
    output = ""
    # fungsionalitas update
    if "sudah" in listText and "mengerjakan" in listText or "sudah" in listText and "menyelesaikan" in listText or "udah" in listText and "ngerjain" in listText:
        output = fungsionalitasDeleteTask(text)

    # fungsionalitas help
    elif "help" in listText or "assistant" in listText or "bot" in listText:
        output = fitur()

    # fungsionalitas update task
    elif "diundur" in listText:
        output = fungsionalitasUpdateTask(text)

    # fungsioalitas deadline
    elif "deadline" in listText or "Deadline" in listText:
        output = fungsionalitasDeadline(text, task, listText)

    # fungsinonalitas tambah task
    elif len(checkElmtList(task, listText)) == 1:
        output = fungsionalitasInputTask(text, listText, task)
        turn += 1
        
    elif "exit" in listText:
        cur.execute("DELETE FROM data;")
        conn.commit()
        return 

    else:
        output = "Maaf, pesan tidak dikenali<br>"

    return output

def fungsionalitasDeadline(inpt, task, listText):
    kodeKuliah = getKodeKuliah(inpt)
    output = ""
    # Tampilkan deadline dari suatu task tertentu
    if kodeKuliah != None:
        output = cariDeadline(inpt)
    else:
        deadlinePerSatuanWaktu = getDeadline(inpt)
        if (deadlinePerSatuanWaktu != None):
            # Tampilkan deadline dari task tertentu dalam jangka waktu tertentu
            if (len(getJenisTask(task, listText)) == 1):
                output = showDeadlineWithJenisTask(deadlinePerSatuanWaktu, task, listText)

            # Tampilkan deadline dari semua task dalam jangka waktu tertentu
            else:
                output = showDeadline(deadlinePerSatuanWaktu)
        else:
            listDeadline = getDualDate(inpt)
            # Tampilkan deadline dalam interval waktu tertentu
            if (listDeadline != None):
                batasBawah = listDeadline[0]
                batasAtas = listDeadline[1]
                output = showDeadlineInterval(batasBawah, batasAtas)

            # Menampilkan semua deadline yang ada
            else:
                output = showAllDeadline()
    return output

def fungsionalitasInputTask(inpt, listText, task):
    global conn
    global cur
    
    global turn
    jenisTask = getJenisTask(task, listText)[0]
    (kodeKuliah, deskripsi, tanggal) = inputValue(inpt, jenisTask)
    upper_jenisTask = uppercaseTask(jenisTask)
    Id = "(ID: "+str(turn)+")"
    sqlDate = changeDateToSqlFormat(tanggal)

    # execute db
    cur.execute("INSERT INTO data VALUES (?, ?, ?, ?, ?);", (Id, kodeKuliah, deskripsi, upper_jenisTask, sqlDate))
    conn.commit()

    # Display
    output = ""
    output += "TASK BERHASIL DICATAT<br>"
    output += Id+" "+tanggal+ " - "+ kodeKuliah+" - "+ upper_jenisTask+ " - "+ deskripsi
    return output

def fungsionalitasDeleteTask(inpt):
    global conn
    global cur

    
    Id = "("+getId(inpt)+")"
    jenisTask = getFromDatabase("jenis_task", Id)
    kodeKuliah = getFromDatabase("kode_matkul", Id)
    deskripsi = getFromDatabase("deskripsi", Id)
    sqlDate = getFromDatabase("tanggal", Id)
    tanggal = changeDateFormat(str(sqlDate))

    # execute db
    cur.execute("DELETE FROM data WHERE id_task = '"+Id+"';")
    conn.commit()

    # Display
    output = ""
    output += Id+" "+tanggal+ " - "+ kodeKuliah+" - "+ jenisTask+ " - "+ deskripsi+"<br>"
    output += "BERHASIL DIHAPUS<br>"
    return output

def fungsionalitasUpdateTask(inpt):
    global conn
    global cur

    tanggal = getDate(inpt)
    Id = "("+getId(inpt)+")"
    sqlDate = changeDateToSqlFormat(tanggal)

    # execute db
    cur.execute("UPDATE data SET tanggal = '"+sqlDate+"' WHERE id_task = '"+Id+"';")
    jenisTask = getFromDatabase("jenis_task", Id)
    kodeKuliah = getFromDatabase("kode_matkul", Id)
    deskripsi = getFromDatabase("deskripsi", Id)
    conn.commit()

    # Display
    output =""
    output += "TASK BERHASIL DIUBAH<br>"
    output += Id+" "+tanggal+ " - "+ kodeKuliah+" - "+ jenisTask+ " - "+ deskripsi+"<br>"
    return output
    

def fitur():
    output = "[Fitur]<br>"
    output += " 1   Menambahkan task baru<br>"
    output += " 2   Melihat daftar task<br>"
    output += " 3   Mencari deadline pada rentang waktu tertentu<br>"
    output += " 4   Melihat deadline suatu task<br>"
    output += " 5   Memperbaharui task tertentu<br>"
    output += " 6   Menandai bahwa suatu task sudah selesai dikerjakan<br>"
    output += " 7   Menampilkan opsi help dan kata kunci yang difasilitasi oleh assistant<br>"
    output += " 8   Menampilkan pesan error jika assistant tidak dapat mengenali masukan user<br><br>"
    output += "[Daftar kata penting]<br>"
    output += " 1   Tubes<br>"
    output += " 2   Tucil<br>"
    output += " 3   Ujian<br>"
    output += " 4   Kuis<br>"
    output += " 5   Praktikum<br>"
    return output

conn = mariadb.connect(user="root", password="", host="localhost", database="stima2")
cur = conn.cursor()
turn = 1

loop = True
txtbotajg = ""
'''while loop:
    result = txt
    if result == "exit":
        cur.execute("DELETE FROM data;")
        conn.commit()
        loop = False
    else:
        inputCommand(result)
        turn += 1'''

#(minggu|bulan|Minggu|Bulan)|(?:([1-9]|[12][0-9]|3[01])
#b(?:IF1\d{3}|IF2\d{3}|IF3\d{3}|IF4\d{3})\b
# result = re.search(r'\b(?:\\(ID: \d{1})\\|\\(ID: \d{2})\\)\b' ,"gua sudah menyelesaikan kuis (ID: 1) kemaren")
# print(result.group()) 

# ======== test case ==========
# Fungsionalitas 1
# halo bot, tolong ingetin kalau ada Kuis IF3310 bab 2 sampai 3 pada 29 april 2021
# Praktikum IF3310 materi generic class tanggal 5 mei 2021
# oyy cokk ingetin gua lah ntar kuis IF2121 materi vektor tanggal 11/05/21
# Apa saja Deadline yang dimiliki sejauh ini
# Apa saja deadline antara 30/04/2021 hingga 11/05/2021
# Deadline 2 hari ke depan apa aja
# 3 minggu ke depan ada deadline kuis apa aja
# deadline kuis IF2121 itu kapan si
# oyy bot lu bisa ngapain aja sih
# gua sudah menyelesaikan kuis (ID: 1) kemaren
# deadline tubes (ID: 1) diundur jadi tanggal 12/07/2021
# oyy cok lu mau apa sih