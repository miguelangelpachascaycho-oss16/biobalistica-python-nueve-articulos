"""Visualización de estados ya calculados; no modifica las ecuaciones físicas.

Todas las coordenadas y métricas son adimensionales. Los contornos son esquemas.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.animation import FuncAnimation, PillowWriter


def preparar_serie(numero, datos, muestras=100):
    """Interpola estados al tiempo de reproducción; devuelve columnas para el visor.

    No altera la simulación ni extrapola fuera de su intervalo. El GIF ralentiza
    el fenómeno; las métricas se calculan desde los datos originales, sin remuestrear.
    """
    t=np.linspace(datos[0,0],datos[-1,0],muestras)
    d=np.column_stack([np.interp(t,datos[:,0],datos[:,i]) for i in range(datos.shape[1])])
    if numero=='06':
        x,y,v=d[:,1],d[:,2],np.hypot(d[:,3],d[:,4])
    elif numero=='09':
        x,y,v=d[:,1],np.zeros(len(t)),d[:,2]
    else:
        x,y,v=d[:,2],np.zeros(len(t)),d[:,1]
    fuerza=d[:,3] if numero=='09' else np.zeros(len(t))
    return np.column_stack((t,x,y,v,fuerza)).tolist()


def resumir_metricas(numero, datos):
    """Extrae magnitudes del modelo sin confundir penetración y deformación."""
    if numero=='09':
        return dict(indentacion_maxima=float(datos[:,1].max()),
                    fuerza_maxima=float(datos[:,3].max()),
                    tiempo_contacto=float(datos[-1,0]),
                    restitucion=float(abs(datos[-1,2])/abs(datos[0,2])),
                    error_energia=float(np.max(abs(datos[:,4]-datos[0,4]))))
    if numero=='06':
        return dict(posicion_final_x=float(datos[-1,1]),posicion_final_y=float(datos[-1,2]),
                    velocidad_final=float(np.hypot(*datos[-1,3:5])),tiempo_final=float(datos[-1,0]))
    salida=dict(desplazamiento_final=float(datos[-1,2]),velocidad_final=float(datos[-1,1]),tiempo_final=float(datos[-1,0]))
    if numero in ('02','03','05','07','08'):
        salida['penetracion_maxima']=float(datos[:,2].max())
        salida['tiempo_parada']=float(datos[-1,0])
    return salida


def crear_paquete(numero, resultados):
    """Une trayectorias de reproducción, métricas y límites para A/B/C."""
    modo='contacto' if numero=='09' else ('fluido' if numero in ('01','04','06') else 'penetracion')
    limites={'contacto':'Indentación global elástica; contorno esquemático. No calcula deformación local.',
             'fluido':'Movimiento en fluido; la interacción con el blanco no está resuelta.',
             'penetracion':'Profundidad de penetración; no calcula el campo de deformaciones del blanco.'}
    return dict(numero=numero,modo=modo,limite=limites[modo],
                escenarios={k:dict(serie=preparar_serie(numero,d),metricas=resumir_metricas(numero,d)) for k,d in resultados.items()})


HTML=r'''<!doctype html><html lang="es"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Movimiento de microesferas</title>
<style>body{font:16px system-ui;margin:24px auto;max-width:1080px;padding:0 16px;background:#f3f6fa;color:#142a43}canvas{background:white;width:100%;border:1px solid #bbc9d5;border-radius:8px}button,select,input{font:inherit;padding:7px;margin:5px}#tiempo{width:48%}#metricas{display:flex;flex-wrap:wrap;gap:10px}.metrica{background:white;padding:12px;border-radius:6px}small{display:block;margin:12px 0;color:#435469}</style>
<h1>Movimiento e impacto de microesferas</h1><p>Resultados numéricos educativos · coordenadas adimensionales · reproducción ralentizada</p>
<label>Alumno <select id="alumno"></select></label><label>Escenario <select id="escenario"></select></label>
<button id="play">Pausar</button><button id="reiniciar">Reiniciar</button>
<label>Tiempo <input id="tiempo" type="range" min="0" max="99" value="0"></label>
<canvas id="lienzo" width="1000" height="490"></canvas><p id="limite"></p><div id="metricas"></div>
<small>El radio se amplifica para ver la esfera. La superficie y el contorno son esquemas: no son imágenes de células ni resultados de elementos finitos. Los gráficos y las posiciones se leen del mismo estado calculado en Python. En los casos de penetración, s=0 es el contacto inicial. En contacto elástico, la superposición representa la indentación global, no interpenetración física.</small>
<script>const casos=__DATOS__;
const $=id=>document.getElementById(id),sel=$('alumno'),esc=$('escenario'),slider=$('tiempo'),cv=$('lienzo'),ctx=cv.getContext('2d');let indice=0,activo=true,prev=0;
for(const n of Object.keys(casos)){const o=document.createElement('option');o.value=n;o.textContent=n+' · '+(casos[n].titulo||casos[n].modo);sel.appendChild(o)}
function cargarEscenarios(){esc.innerHTML='';for(const e of Object.keys(casos[sel.value].escenarios)){const o=document.createElement('option');o.value=e;o.textContent=e;esc.appendChild(o)}if([...esc.options].some(o=>o.value==='B'))esc.value='B';cargar()}
function cargar(){indice=0;slider.value=0;const c=casos[sel.value],d=c.escenarios[esc.value];$('limite').textContent=c.limite;$('metricas').replaceChildren();for(const [k,v]of Object.entries(d.metricas)){const el=document.createElement('div');el.className='metrica';el.textContent=k.replaceAll('_',' ')+': '+v.toPrecision(5);$('metricas').appendChild(el)}dibujar()}
function texto(s,x,y,color='#142a43',tam=17){ctx.fillStyle=color;ctx.font=tam+'px system-ui';ctx.fillText(s,x,y)}
function dibujar(){const c=casos[sel.value],d=c.escenarios[esc.value],a=d.serie,i=Math.min(indice,a.length-1),r=a[i];ctx.clearRect(0,0,1000,490);texto('Alumno '+sel.value+' · Escenario '+esc.value,25,28);texto('s = '+r[0].toFixed(3)+'   v = '+r[3].toFixed(3),25,57);
const xmax=Math.max(...a.map(p=>p[1]),.01),ymax=Math.max(...a.map(p=>Math.abs(p[2])),.15),contacto=c.modo==='contacto',fluido=c.modo==='fluido';
const origen=contacto?330:110,escala=(contacto?50:420)/xmax,radio=contacto?85:16;
ctx.fillStyle='#d9f2ee';ctx.fillRect(fluido?35:origen,85,fluido?520:570-origen,245);ctx.strokeStyle='#418e86';ctx.setLineDash([6,5]);ctx.beginPath();ctx.moveTo(origen,85);ctx.lineTo(origen,330);ctx.stroke();ctx.setLineDash([]);texto(fluido?'Medio fluido':contacto?'Pared rígida':'Blanco homogéneo',origen+8,112,'#286a63',15);
const px=origen+r[1]*escala-(fluido?0:radio),py=220-r[2]*80/ymax;
ctx.strokeStyle='#e89634';ctx.lineWidth=2;ctx.beginPath();a.slice(0,i+1).forEach((p,j)=>{const x=origen+p[1]*escala-(fluido?0:radio),y=220-p[2]*80/ymax;j?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke();
ctx.save();ctx.beginPath();ctx.rect(35,115,535,210);ctx.clip();ctx.fillStyle='#e7892f';ctx.beginPath();ctx.arc(px,py,radio,0,Math.PI*2);ctx.fill();if(contacto){ctx.clearRect(origen,115,310,210);ctx.fillStyle='#d9f2ee';ctx.fillRect(origen,115,310,210);ctx.strokeStyle='#418e86';ctx.beginPath();ctx.moveTo(origen,115);ctx.lineTo(origen,325);ctx.stroke()}ctx.restore();
texto(contacto?'q = '+r[1].toFixed(4)+' · F = '+r[4].toFixed(4):'x = '+r[1].toFixed(4)+' · y = '+r[2].toFixed(4),30,361);
texto(contacto?'Indentación global; perfil esquemático':fluido?'Trayectoria calculada; impacto fuera del modelo':'Trayectoria dentro del blanco; no es una cavidad',30,389,'#435469',15);
const gx=640,gy=310,gw=320,gh=180;let valores=a.map(p=>contacto?p[1]:p[3]),lo=Math.min(0,...valores),hi=Math.max(.01,...valores),tmax=a.at(-1)[0];ctx.strokeStyle='#71869c';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(gx,gy-gh);ctx.lineTo(gx,gy);ctx.lineTo(gx+gw,gy);ctx.stroke();ctx.strokeStyle='#1d669f';ctx.lineWidth=2;ctx.beginPath();a.forEach((p,j)=>{let x=gx+gw*p[0]/tmax,y=gy-gh*(valores[j]-lo)/(hi-lo);j?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke();ctx.fillStyle='#d6424b';ctx.beginPath();ctx.arc(gx+gw*r[0]/tmax,gy-gh*(valores[i]-lo)/(hi-lo),6,0,7);ctx.fill();texto(contacto?'Indentación q(s)':'Velocidad v(s)',gx,95);texto('Tiempo relativo s',gx+80,344);texto('Máximo '+hi.toFixed(3),gx,371,'#435469',15);texto('El punto rojo sigue el mismo tiempo',gx,398,'#435469',15);
}
sel.onchange=cargarEscenarios;esc.onchange=cargar;slider.oninput=()=>{indice=+slider.value;activo=false;$('play').textContent='Reproducir';dibujar()};$('play').onclick=()=>{activo=!activo;$('play').textContent=activo?'Pausar':'Reproducir'};$('reiniciar').onclick=()=>{indice=0;slider.value=0;dibujar()};
function ciclo(ms){if(activo&&ms-prev>90){indice=(indice+1)%100;slider.value=indice;dibujar();prev=ms}requestAnimationFrame(ciclo)}cargarEscenarios();requestAnimationFrame(ciclo);
</script></html>'''


def guardar_visor(paquetes, ruta):
    """Escribe HTML autónomo: sus controles no necesitan servidor ni Internet."""
    Path(ruta).write_text(HTML.replace('__DATOS__',json.dumps(paquetes,ensure_ascii=False)),encoding='utf8')


def crear_gif(paquete, ruta):
    """Dibuja 60 cuadros sincronizados con la trayectoria del escenario B o el único."""
    e='B' if 'B' in paquete['escenarios'] else next(iter(paquete['escenarios']))
    serie=np.array(paquete['escenarios'][e]['serie']);modo=paquete['modo']
    t,x,y,v,f=serie.T;xmax=max(float(x.max()),.01)
    contacto=modo=='contacto';fluido=modo=='fluido'
    radio=(2*xmax if contacto else .035*xmax)
    fig,(ax,curva)=plt.subplots(1,2,figsize=(8,4),gridspec_kw={'width_ratios':[1.3,1]})
    fig.suptitle(f"Alumno {paquete['numero']} · escenario {e}")
    xmin=-2.2*radio if contacto else -.15*xmax
    alto=2.3*xmax if contacto else .65*xmax
    ax.set(xlim=(xmin,1.15*xmax),ylim=(-alto,alto),xlabel='Posición relativa',yticks=[])
    ax.set_aspect('equal',adjustable='box')
    ax.axvspan(xmin if fluido else 0,1.15*xmax,color='#d9f2ee')
    ax.axvline(0,color='#418e86',ls='--',lw=1)
    ax.set_title('Fluido' if fluido else ('Contacto elástico' if contacto else 'Impacto y penetración'),fontsize=11)
    esfera=Circle((0,0),radio,color='#e7892f');ax.add_patch(esfera)
    if contacto:
        pared=Rectangle((0,-2*xmax),3*xmax,4*xmax,color='#d9f2ee',zorder=3);ax.add_patch(pared)
        ax.axvline(0,color='#418e86',lw=1,zorder=4)
    traza,=ax.plot([],[],color='#e89634',lw=1)
    valores=x if contacto else v
    curva.plot(t,valores,color='#1d669f');punto,=curva.plot([],[],'o',color='#d6424b')
    curva.set(xlabel='Tiempo relativo s',ylabel='Indentación q' if contacto else 'Velocidad relativa');curva.grid(alpha=.2)
    texto=fig.text(.06,.13,'',fontsize=9)
    nota='Contorno esquemático; no calcula deformaciones locales.' if not fluido else 'Trayectoria en fluido; impacto fuera del submodelo.'
    fig.text(.5,.025,nota+' Valores adimensionales.',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.17,1,.91))
    indices=np.linspace(0,len(t)-1,60).astype(int)
    def cuadro(j):
        i=indices[j];xc=x[i]-(0 if fluido else radio)
        esfera.center=(xc,y[i]);traza.set_data(x[:i+1]-(0 if fluido else radio),y[:i+1]);punto.set_data([t[i]],[valores[i]])
        texto.set_text(f's={t[i]:.3f}   x={x[i]:.3f}   v={v[i]:.3f}'+(f'   F={f[i]:.3f}' if contacto else ''))
        return esfera,traza,punto,texto
    anim=FuncAnimation(fig,cuadro,frames=len(indices),interval=100,blit=False)
    anim.save(ruta,writer=PillowWriter(fps=10),dpi=85)
    plt.close(fig)


def exportar_movimiento(numero, resultados, carpeta, animar=False):
    """Exporta métricas y visor de todos los escenarios; GIF opcional."""
    paquete=crear_paquete(numero,resultados)
    (carpeta/'metricas.json').write_text(json.dumps({k:v['metricas'] for k,v in paquete['escenarios'].items()},indent=2,ensure_ascii=False),encoding='utf8')
    guardar_visor({numero:paquete},carpeta/'visor.html')
    if animar: crear_gif(paquete,carpeta/'animacion.gif')
