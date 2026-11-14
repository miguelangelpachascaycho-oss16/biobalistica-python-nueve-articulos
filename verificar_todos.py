"""Verificación del material AUXILIAR de contacto general, no de las nueve actividades actuales."""
from pathlib import Path
import sys,subprocess,json,time,platform,importlib.metadata
import numpy as np
from motor_contacto import perfil_blanco


def verificar_perfil():
    """Comprueba blanco plano, centro desplazado, continuidad y decaimiento."""
    x=np.linspace(0,200,2001)
    assert np.max(abs(perfil_blanco(x,0.)))==0
    for q in (.1,.5,1.):
        w=perfil_blanco(x,q)
        assert abs(w[0]-q)<1e-12 and w[-1]<.02*q
        assert np.min(w)>=0 and np.max(np.diff(w))<1e-10
        a=np.sqrt(30*q);c=perfil_blanco(np.array([a*(1-1e-7),a*(1+1e-7)]),q)
        assert abs(c[0]-c[1])<1e-6
    return 'Blanco plano en reposo; w(0)=q, perfil continuo y decae lejos del contacto'


def main():
    """Ejecuta 27 escenarios y registra evidencia matemática y salidas del software."""
    raiz=Path(__file__).resolve().parent
    fuentes=json.loads((raiz/'FUENTES_CONTACTO_AUXILIAR.json').read_text(encoding='utf8'))
    assert len(fuentes)==len({f['doi'].lower() for f in fuentes})==9
    assert len({f['title'].lower() for f in fuentes})==9
    perfil=verificar_perfil();registros=[]
    for fuente in fuentes:
        n=fuente['n'];inicio=time.perf_counter();salida=raiz/'resultados'/f'alumno_{n}'
        r=subprocess.run([sys.executable,str(raiz/f'simulacion_{n}.py'),'--verificar','--salida',str(salida)],cwd=raiz,text=True,encoding='utf8',capture_output=True,timeout=120)
        print(f"Alumno {n}: {'OK' if r.returncode==0 else 'ERROR'}",flush=True)
        if r.returncode:print(r.stdout,r.stderr)
        linea=next((s for s in r.stdout.splitlines() if s.startswith('{')),None)
        metricas=json.loads((salida/'metricas.json').read_text(encoding='utf8')) if r.returncode==0 else {}
        if r.returncode==0:
            assert set(metricas)==set('ABC')
            assert all(metricas[e]['indentacion_maxima_L']>0 for e in 'ABC')
            assert (salida/'visor.html').exists() and (salida/'comparacion.png').exists()
        registros.append(dict(alumno=n,doi=fuente['doi'],exit_code=r.returncode,
                              segundos=round(time.perf_counter()-inicio,2),
                              comprobacion=json.loads(linea) if linea else None,escenarios=metricas))
    informe=dict(python=platform.python_version(),dependencias={p:importlib.metadata.version(p) for p in ['numpy','scipy','matplotlib','Pillow']},
                 fecha_revision='2026-11-13',articulos_distintos=9,escenarios=27,
                 perfil_blanco=perfil,resultados=registros,
                 alcance='Verificación matemática y local; no validación de tejidos ni de campo 3D')
    (raiz/'VERIFICACION.json').write_text(json.dumps(informe,ensure_ascii=False,indent=2),encoding='utf8')
    assert all(r['exit_code']==0 for r in registros),'Hay comprobaciones fallidas'
    print('Nueve artículos, 27 escenarios y deformación del blanco verificados.')


if __name__=='__main__':main()
