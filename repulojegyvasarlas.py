from abc import ABC, abstractmethod
from datetime import datetime
import uuid

# === Absztrakt Járat osztály ===
class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar

    @abstractmethod
    def info(self):
        pass


# === Belföldi járat ===
class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegyar):
        super().__init__(jaratszam, celallomas, jegyar)

    def info(self):
        return f"[Belföldi] {self.jaratszam} -> {self.celallomas} | Ár: {self.jegyar} Ft"


# === Nemzetközi járat ===
class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegyar):
        super().__init__(jaratszam, celallomas, jegyar)

    def info(self):
        return f"[Nemzetközi] {self.jaratszam} -> {self.celallomas} | Ár: {self.jegyar} Ft"


# === JegyFoglalás osztály ===
class JegyFoglalas:
    def __init__(self, felhasznalo, jarat, datum):
        self.foglalas_id = str(uuid.uuid4())
        self.felhasznalo = felhasznalo
        self.jarat = jarat
        self.datum = datum

    def __str__(self):
        return f"{self.foglalas_id[:8]} | {self.felhasznalo} | {self.jarat.jaratszam} -> {self.jarat.celallomas} | {self.datum.strftime('%Y-%m-%d')} | {self.jarat.jegyar} Ft"


# === Légitársaság osztály ===
class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []
        self.foglalasok = []

    def hozzaad_jarat(self, jarat):
        self.jaratok.append(jarat)

    def listaz_jaratok(self):
        for i, j in enumerate(self.jaratok, 1):
            print(f"{i}. {j.info()}")

    def jegy_foglalasa(self, felhasznalo, jarat_index, datum_str):
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
            if datum < datetime.now():
                print("Nem lehet múltbeli dátumra foglalni.")
                return

            if jarat_index < 1 or jarat_index > len(self.jaratok):
                print("Érvénytelen a járat indexe.")
                return

            jarat = self.jaratok[jarat_index - 1]
            foglalas = JegyFoglalas(felhasznalo, jarat, datum)
            self.foglalasok.append(foglalas)
            print(f"A foglalás sikeres! Foglalás ID: {foglalas.foglalas_id[:8]} | Ár: {jarat.jegyar} Ft")
        except ValueError:
            print("Hibás dátum.")

    def listaz_foglalasok(self):
        if not self.foglalasok:
            print("Még nincsenek foglalások.")
            return
        for f in self.foglalasok:
            print(f)

    def lemond_foglalas(self, foglalas_id):
        for f in self.foglalasok:
            if f.foglalas_id.startswith(foglalas_id):
                self.foglalasok.remove(f)
                print("A foglalásod sikeresen lemondva.")
                return
        print("Nincs ilyen azonosítójú foglalás.")


# === Alkalmazás inicializálása ===
def inicializal_rendszer():
    legitarsasag = LegiTarsasag("FlyHigh Hungary")

    # Járatok
    legitarsasag.hozzaad_jarat(BelfoldiJarat("HUN101", "Budapest", 18000))
    legitarsasag.hozzaad_jarat(BelfoldiJarat("HUN202", "Debrecen", 12000))
    legitarsasag.hozzaad_jarat(NemzetkoziJarat("INT303", "London", 45000))

    # Foglalások (6 előre definiált)
    legitarsasag.jegy_foglalasa("user1", 1, "2025-06-01")
    legitarsasag.jegy_foglalasa("user1", 2, "2025-07-03")
    legitarsasag.jegy_foglalasa("user2", 3, "2025-04-05")
    legitarsasag.jegy_foglalasa("user3", 1, "2025-12-10")
    legitarsasag.jegy_foglalasa("user4", 2, "2025-02-07")
    legitarsasag.jegy_foglalasa("user5", 3, "2025-01-15")

    return legitarsasag


# Menü 
def menu(legitarsasag):
    while True:
        print("\n==== LÉGIJÁRAT FOGLALÓ RENDSZER ====")
        print("1. Járatok listázása")
        print("2. Jegy foglalása")
        print("3. Foglalás lemondása")
        print("4. Foglalások listázása")
        print("5. Kilépés")

        valasz = input("Válassz műveletet (1-5): ")

        if valasz == "1":
            legitarsasag.listaz_jaratok()

        elif valasz == "2":
            felhasznalo = input("Felhasználónév: ")
            legitarsasag.listaz_jaratok()
            try:
                jarat_index = int(input("Járat sorszáma: "))
                datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
                legitarsasag.jegy_foglalasa(felhasznalo, jarat_index, datum)
            except ValueError:
                print("Hibás bevitel.")

        elif valasz == "3":
            foglalas_id = input("Add meg a lemondandó foglalás azonosítóját (ID eleje): ")
            legitarsasag.lemond_foglalas(foglalas_id)

        elif valasz == "4":
            legitarsasag.listaz_foglalasok()

        elif valasz == "5":
            print("Viszlát!")
            break

        else:
            print("Érvénytelen bevitel.")


# Main 
if __name__ == "__main__":
    legitarsasag = inicializal_rendszer()
    menu(legitarsasag)
