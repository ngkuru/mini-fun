import random

bilginotu = '''
Bunlar yardimci olmasi icin:
    
7 + 8 = 15
7 - (-8) = 15

7 - 8 = -1
7 - (+8) = -1
7 + (-8) = -1
'''


sayilar = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

m = random.randint(0, 9)
n = random.randint(0, 9)

sol_pozitif = {x:[f"{x}", f"+{x}", f"(+{x})", f"+({x})", f"+(+{x})"] for x in (m, n)}
sag_pozitif = {x:[f"{x}", f"(+{x})"] for x in (m, n)}

sol_negatif = {x:[f"-{x}", f"(-{x})", f"-({x})", f"+(-{x})", f"-(+{x})"] for x in (m, n)}
sag_negatif = {x:[f"(-{x})"] for x in (m, n)}

islem = ["+", "-"]

islemler = []
for (a, b) in ((m, n), (n, m)):
    for sol in sol_pozitif[a]:
        for sag in sag_pozitif[b]:
            yazi = sol + ' + ' + sag
            cevap = a + b
            yardim = f"Bunun cevabi {a} + {b} ile ayni."
            
            islemler.append((yazi, cevap, yardim))
            
            yazi = sol + ' - ' + sag
            cevap = a - b
            yardim = f"Bunun cevabi {a} - {b} ile ayni."
            
            islemler.append((yazi, cevap, yardim))
            
    for sol in sol_pozitif[a]:
        for sag in sag_negatif[b]:
            yazi = sol + ' + ' + sag
            cevap = a - b
            yardim = f"Bunun cevabi {a} - {b} ile ayni."
            
            islemler.append((yazi, cevap, yardim))
            
            yazi = sol + ' - ' + sag
            cevap = a + b
            yardim = f"Bunun cevabi {a} + {b} ile ayni."
            
            islemler.append((yazi, cevap, yardim))
    
    for sol in sol_negatif[a]:
        for sag in sag_pozitif[b]:
            yazi = sol + ' + ' + sag
            cevap = - a + b
            yardim = f"Bunun cevabi - {a} + {b} ile ayni."
            
            islemler.append((yazi, cevap, yardim))
            
            yazi = sol + ' - ' + sag
            cevap = - a - b
            yardim = f"Bunun cevabi - {a} - {b} ile ayni."
            
            islemler.append((yazi, cevap, yardim))
            
    for sol in sol_negatif[a]:
        for sag in sag_negatif[b]:
            yazi = sol + ' + ' + sag
            cevap = - a - b
            yardim = f"Bunun cevabi - {a} - {b} ile ayni."
            
            islemler.append((yazi, cevap, yardim))
            
            yazi = sol + ' - ' + sag
            cevap = - a + b
            yardim = f"Bunun cevabi - {a} + {b} ile ayni."
            
            islemler.append((yazi, cevap, yardim))
            
random.shuffle(islemler)
puan = 0

print()
for yazi, cevap, yardim in islemler:
    for deneme in range(3):
        tahmin = input(f"{yazi} = ")
        try:
            if int(tahmin) == cevap:
                puan += 30 - deneme * 10
                print(f"Tebrikler, dogru bildin, {puan} puan oldu\n")
                break
            elif deneme == 0:
                print("Bilemedin, tekrar dene")
            elif deneme == 1:
                print(f"Bilemedin, ipucu: {yardim}")
            elif deneme == 2:
                print(f"Dogru cevap {cevap} olacakti")
        except:
            print("Cevaba sayidan baska bir sey yazmak yok")
        print()

