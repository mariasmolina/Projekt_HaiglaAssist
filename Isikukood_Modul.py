from datetime import *

def kontrolli_ikood(ikood:str):
    if not ikood.isdigit():  # Kontrollime, kas sisaldab ainult numbreid
        return "Isikukood tohib sisaldada ainult numbreid!"

    if not kontroll_pikkus(ikood):  # Pikkuse kontroll
         return "Isikukood peab olema 11 numbrit pikk!"

    if not kontroll_esimene_arv(ikood):  # Esimese sümboli kontroll
         return "Isikukood peab algama numbriga 1-6!"

    synniaeg = leia_synniaeg(ikood)  # Sünnikuupäeva kontroll
    if not kontroll_synniaeg(synniaeg.year, synniaeg.month, synniaeg.day):  # Kontroll, kas inimene ei ole sündinud tulevikus
         return "Vigane sünnikuupäev isikukoodis!"

    kontrollnr = leia_kontroll_nr(ikood)  # Kontrollnumbri kontroll
    if int(ikood[10]) != kontrollnr:
        return "Vale kontrollnumber isikukoodis!"

    # Kui kõik kontrollid on edukalt läbitud
    return True


# Sümbolite arvu kontroll
def kontroll_pikkus(ikood: str) -> bool:
    """Kontrollib isikukoodi pikkust ja sisaldust
    :param str ikood: Isikukood
    :rtype: bool
    """
    return len(ikood) == 11 and ikood.isdigit()


# Esimese märgi kontroll
def kontroll_esimene_arv(ikood:str)->bool:
    """Kontrollib isikukoodi esimese numbri
    :param str ikood: Isikukood
    :rtype: bool
    """
    esimene_arv=int(ikood[0])

    return esimene_arv in {1,2,3,4,5,6}


# Sünnikuupäeva leidmine
def leia_synniaeg(ikood: str)->any:
    """Leiab sünniaja isikukoodist
    :param str ikood: Isikukood
    :rtype: any
    """
    esimene_arv=int(ikood[0])
# Täpset sünniaastat leitakse isikukoodi esimese numbri põhjal (1,2 - 1800; 3,4 - 1900; 5,6 - 2000)
    aasta=int(ikood[1:3])+(1800 if esimene_arv in {1,2} else 1900 if esimene_arv in {3,4} else 2000)
    kuu=int(ikood[3:5])
    paev=int(ikood[5:7])

    return datetime(aasta, kuu, paev)


# Kontroll – kas inimene ei ole sündinud tulevikus (kasutades funktsiooni datetime.now)
def kontroll_synniaeg(aasta:int,kuu:int,paev:int)->bool:
    """Kontrollib, kas sünniaeg on kehtiv ja mitte tulevikus
    :param int aasta: Aasta
    :param int kuu: Kuu
    :param int paev: Päev
    :rtype: bool
    """
    try:
        synniaeg=datetime(aasta,kuu,paev)
        return synniaeg<=datetime.now()
    except:
        return False


# Kontrollnumbri arvutamine
def leia_kontroll_nr(ikood:str)->int:
    """Kontrollib isikukoodi kontrollnumbri
    :param str ikood: Isikukood
    :rtype: int    
    """
    astme_kaal_1=[1,2,3,4,5,6,7,8,9,1]
    astme_kaal_2=[3,4,5,6,7,8,9,1,2,3]

# summa = ikoodi esimene number * astme_kaalu esimene number + → ja edasi tsüklis
    astme_summa_1=sum(int(ikood[i])*astme_kaal_1[i] for i in range (10))
    jaak=astme_summa_1%11  # jääk = summa jagatakse 11-ga → jääk = kontrollnumber

    if jaak==10:  # в случае если остаток равен 10, то -->
        astme_summa_2=sum(int(ikood[i])*astme_kaal_2[i] for i in range (10)) # такой же цикл, как и с astme_summa_1
        jaak=astme_summa_2%11    
        if jaak==10: 
            jaak=0    # tingimuse järgi, kui jääk on 10, siis kontrollnumber on 0

    return jaak


# Sünnikoha määramine (tehakse nimekiri, mis sisaldab alamnimekirju)
def leia_sunnikoht(sunnikoht_num:int)->str:
    """Määrab sünnikoha isikukoodi järgi
    :param int sunnikoht_num: Isikukoodi sünnikoha osa
    :rtype: str    
    """
    haiglad=[
            [1,10,"Kuressaare Haigla"],
            [11,19,"Tartu Ülikooli Naistekliinik, Tartumaa, Tartu"],
            [21,220,"Ida-Tallinna Keskhaigla, Pelgulinna sünnitusmaja, Hiiumaa, Keila, Rapla haigla, Loksa haigla"],
            [221,270,"Ida-Viru Keskhaigla (Kohtla-Järve, endine Jõhvi)"],
            [271,370,"Maarjamõisa Kliinikum (Tartu), Jõgeva Haigla"],
            [371,420,"Narva Haigla"],
            [421,470,"Pärnu Haigla"],
            [471,490,"Pelgulinna Sünнitusmaja (Tallinn), Haapsalu haigla"],
            [491,520,"Järvamaa Haigla (Paide)"],
            [521,570,"Rakvere, Tapa haigla"],
            [571,600,"Valga Haigla"],
            [601,650,"Viljandi Haigla"],
            [651,700,"Lõuna-Eesti Haigla (Võru), Põlva Haigla"]
    ]
    for alg,lopp,koht in haiglad:
        if alg<=sunnikoht_num<=lopp:
            return koht
    return "Tundmatu sünnikoht"


# Soo määramine (1, 3, 5 – mees; 2, 4, 6 – naine)
def leia_sugu(ikood:int)->str:
    """Määrab isiku soo
    :param int esimene_arv: Isikukoodi esimene number
    :rtype: str
    """
    esimene_arv=int(ikood[0])
    if esimene_arv in {1,3,5}:
        sugu="mees"
    else:
        sugu="naine"

    return sugu

