#!/usr/bin/env python3
"""Actualizador seguro: importa datos estructurados autorizados, sin inventar precios."""
import csv,json,os,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"datos"/"precios-derco.csv"
OUT=ROOT/"datos"/"catalogo.json"
BRANDS={"Suzuki","Mazda","Changan","GWM","Haval","Deepal","DFSK"}
def money(s):
    s=str(s).strip().replace("$","").replace(".","").replace(" ","")
    if not s.isdigit(): raise ValueError("Precio no numérico")
    n=int(s)
    if n<=0: raise ValueError("Precio no positivo")
    return n
def main():
    if not SOURCE.exists():
        print("Sin archivo de fuente verificada: se conserva el catálogo anterior.")
        return
    groups={}
    with SOURCE.open(encoding="utf-8-sig",newline="") as f:
        for row in csv.DictReader(f):
            brand=row["marca"].strip()
            model=row["modelo"].strip()
            version=row["version"].strip()
            url=row["fuente_url"].strip()
            if brand not in BRANDS or not model or not version or not url.startswith("https://"):
                raise ValueError("Registro incompleto o fuente inválida")
            price=money(row["precio"])
            kind=row["tipo_precio"].strip()
            if kind not in ("lista","contado","financiamiento"): raise ValueError("Tipo de precio inválido")
            key=(brand,model)
            groups.setdefault(key,[]).append({"version":version,"precio":price,"tipo_precio":kind,"fuente_url":url})
    if not groups:
        print("Fuente vacía: se conserva el catálogo anterior.")
        return
    data={"actualizado_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"origen":"Datos verificados de Derco.cl","modelos":[]}
    for (brand,model),versions in sorted(groups.items()):
        data["modelos"].append({"marca":brand,"modelo":model,"desde":min(v["precio"] for v in versions),"hasta":max(v["precio"] for v in versions),"versiones":versions})
    OUT.parent.mkdir(exist_ok=True)
    tmp=OUT.with_suffix(".tmp")
    tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    tmp.replace(OUT)
    print(f"Catálogo generado: {len(groups)} modelos")
if __name__=="__main__": main()
