"""Comprueba referencias y ejecuta secuencialmente los nueve ejemplos."""
from pathlib import Path
import sys,subprocess,json,time,platform,importlib.metadata


def main():
    raiz=Path(__file__).resolve().parent
    fuentes=json.loads((raiz/"FUENTES.json").read_text(encoding="utf8"))
    assert len(fuentes)==9 and len({f["doi"].lower() for f in fuentes})==9,"Hay artículos repetidos"
    assert len({f["title"].lower() for f in fuentes})==9,"Hay títulos repetidos"
    registros=[]
    for fuente in fuentes:
        n=fuente["n"];inicio=time.perf_counter()
        r=subprocess.run([sys.executable,str(raiz/f"simulacion_{n}.py"),"--verificar","--salida",str(raiz/"resultados"/f"alumno_{n}")],cwd=raiz,text=True,encoding="utf8",capture_output=True,timeout=90)
        print(f"Alumno {n}: {'OK' if r.returncode==0 else 'ERROR'}",flush=True)
        if r.returncode:print(r.stdout,r.stderr)
        linea=next((s for s in r.stdout.splitlines() if s.startswith('{')),None)
        registros.append({"alumno":n,"doi":fuente['doi'],"exit_code":r.returncode,"segundos":round(time.perf_counter()-inicio,2),"comprobacion":json.loads(linea) if linea else None})
    informe={"dependencias":{n:importlib.metadata.version(n) for n in ["numpy","matplotlib"]},"python":platform.python_version(),"articulos_distintos":9,"fecha_revision":"2026-11-13","resultados":registros,"alcance":"Comprobaciones matemáticas y ejecución local; no validación biológica"}
    (raiz/"VERIFICACION.json").write_text(json.dumps(informe,ensure_ascii=False,indent=2),encoding="utf8")
    assert all(r['exit_code']==0 for r in registros),"Hay comprobaciones fallidas"
    print("Nueve artículos distintos y nueve programas verificados.")


if __name__=="__main__":main()
