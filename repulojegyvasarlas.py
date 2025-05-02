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
