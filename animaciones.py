"""Visualización de q(t): esfera rígida y blanco deformable.

El perfil espacial Hertz se adopta para reconstruir la superficie. No se
calculan daño, ondas ni deformación celular 3D. Las magnitudes son relativas.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Polygon
from matplotlib.animation import FuncAnimation,PillowWriter
from motor_contacto import perfil_blanco,RADIO_RELATIVO,cuadratura_contacto


def graficar_comparacion(numero,resultados,carpeta):
    """Grafica referencia, indentación, fuerza, histéresis y balance de energía."""
    fig,axs=plt.subplots(2,2,figsize=(10,7))
    for e,r in resultados.items():
        d=r['datos'];color={'A':'#c66a13','B':'#1672a0','C':'#397a42'}[e]
        axs[0,0].plot(d[:,0],d[:,1],color=color,label=f'{e} numérica')
        etiqueta='serie s≤0.12' if 'limite_serie' in r['referencia'] else 'referencia'
        axs[0,0].plot(d[:,0],d[:,7],ls='--',color=color,label=f'{e} {etiqueta}')
        axs[0,1].plot(d[:,0],d[:,3],color=color,label=e)
        axs[1,0].plot(d[:,1],d[:,3],color=color,label=e)
        axs[1,1].plot(d[:,0],d[:,6],color=color,label=f'{e} total')
    b=resultados.get('B',next(iter(resultados.values())))['datos']
    if 'limite_serie' in next(iter(resultados.values()))['referencia']:
        limite,_=cuadratura_contacto()
        axs[0,0].plot(limite[:,0],limite[:,1],':',color='#777777',label='Hertz sin disipación (límite)')
    for y,nombre in [(0.5*b[:,2]**2,'Cinética'),(b[:,4],'Elástica'),(b[:,5],'Disipada')]:
        axs[1,1].plot(b[:,0],y,':',label=f'{nombre} (B o único)')
    for ax,x,y in zip(axs.flat,['Tiempo s','Tiempo s','Indentación q','Tiempo s'],['Indentación q','Reacción F','Reacción F','Energía relativa']):
        ax.set(xlabel=x,ylabel=y);ax.grid(alpha=.2);ax.legend(fontsize=7)
    fig.suptitle(f'Alumno {numero} · impacto y deformación global del blanco')
    fig.text(.5,.015,'Referencia: cerrada, semianalítica o serie corta según la ficha. Magnitudes adimensionales.',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.04,1,.95));fig.savefig(carpeta/'comparacion.png',dpi=130);plt.close(fig)
    if 'e_serie_orden2' in next(iter(resultados.values()))['referencia']:
        fig,ax=plt.subplots(figsize=(7,4));valores=[r['parametros']['d'] for r in resultados.values()]
        for campo,estilo,label in [('e_serie_orden1','--','Serie orden 1'),('e_serie_orden2','-','Serie orden 2'),('e_criterio_antiguo_q0','o','Numérica: q=0')]:
            ax.plot(valores,[r['referencia'][campo] for r in resultados.values()],estilo,label=label)
        ax.plot(valores,[r['metricas']['restitucion'] for r in resultados.values()],'x',label='Numérica: F=0')
        ax.set(xlabel='Disipación χ',ylabel='Restitución');ax.legend(fontsize=8);ax.grid(alpha=.2)
        fig.tight_layout();fig.savefig(carpeta/'restitucion_analitica.png',dpi=130);plt.close(fig)


def preparar_serie(datos):
    """Cuadros del vuelo uniforme previo y del contacto, ralentizado para verlo."""
    tiempos=np.r_[np.linspace(-6,0,16,endpoint=False),np.linspace(0,datos[-1,0],104)]
    filas=[];valida=np.isfinite(datos[:,7])
    for t in tiempos:
        if t<0:filas.append([float(t),float(t),1.,0.,float(t)])
        else:
            q,v,f=[float(np.interp(t,datos[:,0],datos[:,i])) for i in (1,2,3)]
            ref=float(np.interp(t,datos[valida,0],datos[valida,7])) if t<=datos[valida,0][-1] else None
            filas.append([float(t),q,v,f,ref])
    return filas


def crear_paquete(numero,resultados,titulo=''):
    """Une cuadros, curvas y métricas A/B/C sin recalcular la dinámica."""
    escenarios={}
    for e,r in resultados.items():
        d=r['datos'];ids=np.linspace(0,len(d)-1,min(400,len(d))).astype(int)
        curva=[[float(f[0]),float(f[1]),float(f[7]) if np.isfinite(f[7]) else None] for f in d[ids]]
        escenarios[e]=dict(serie=preparar_serie(d),curva=curva,metricas=r['metricas'])
    return dict(numero=numero,titulo=titulo,radio=RADIO_RELATIVO,escenarios=escenarios)


HTML=r'''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Impacto y deformación del blanco</title><style>body{font:16px system-ui;margin:22px auto;max-width:1120px;padding:0 16px;background:#f2f6fa;color:#14304a}canvas{width:100%;background:white;border:1px solid #b2c5d0;border-radius:8px}button,select,input{font:inherit;padding:7px;margin:4px}#tiempo{width:45%}#metricas{display:flex;gap:8px;flex-wrap:wrap}.m{background:white;padding:10px;border-radius:6px}small{display:block;margin:15px 0;color:#465b6d}</style>
<h1>Impacto y deformación del blanco</h1><p>Esfera rígida · blanco deformable · comparación analítica–numérica · parámetros relativos docentes</p>
<label>Alumno <select id="alumno"></select></label><label>Escenario <select id="escenario"></select></label><button id="play">Pausar</button><button id="reiniciar">Reiniciar</button><label>Cuadro <input id="tiempo" type="range" min="0" max="119" value="0"></label>
<canvas id="lienzo" width="1080" height="540"></canvas><p id="referencia"></p><div id="metricas"></div>
<small>R/L=30. El contacto se ralentiza para verlo. La ampliación usa escalas horizontal y vertical distintas. El perfil superficial Hertz es una hipótesis común a partir de q(t), no una solución independiente del campo espacial de las leyes disipativas. El último cuadro finaliza el contacto: una indentación positiva al separarse no demuestra una huella permanente. No se calcula perforación, daño ni recuperación posterior libre.</small>
<script>const casos=__DATOS__;
const $=id=>document.getElementById(id),sel=$('alumno'),esc=$('escenario'),slider=$('tiempo'),cv=$('lienzo'),ctx=cv.getContext('2d');let indice=0,activo=true,prev=0;
for(const [n,c]of Object.entries(casos)){const o=document.createElement('option');o.value=n;o.textContent=n+' · '+c.titulo;sel.appendChild(o)}
function opciones(){esc.replaceChildren();for(const e of Object.keys(casos[sel.value].escenarios)){let o=document.createElement('option');o.value=e;o.textContent=e;esc.appendChild(o)}if([...esc.options].some(o=>o.value==='B'))esc.value='B';cargar()}
function cargar(){indice=0;slider.value=0;const d=casos[sel.value].escenarios[esc.value];$('referencia').textContent=d.metricas.referencia.tipo_referencia;$('metricas').replaceChildren();for(const k of ['indentacion_maxima_L','indentacion_maxima_sobre_R','fuerza_maxima','tiempo_contacto','restitucion','error_q_referencia']){let x=document.createElement('div');x.className='m';x.textContent=k.replaceAll('_',' ')+': '+d.metricas[k].toPrecision(5);$('metricas').appendChild(x)}dibujar()}
function texto(t,x,y,size=16,color='#14304a'){ctx.fillStyle=color;ctx.font=size+'px system-ui';ctx.fillText(t,x,y)}
function w(r,q,R){r=Math.abs(r);if(q<=0)return 0;const a=Math.sqrt(R*q);return r<=a?q-r*r/(2*R):((2*a*a-r*r)*Math.asin(a/r)+a*Math.sqrt(r*r-a*a))/(Math.PI*R)}
function perfil(x0,base,sx,sy,rmax,q,R){ctx.beginPath();for(let j=0;j<=160;j++){let r=-rmax+2*rmax*j/160,x=x0+r*sx,y=base+w(r,q,R)*sy;j?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.lineTo(x0+rmax*sx,base+165);ctx.lineTo(x0-rmax*sx,base+165);ctx.closePath();ctx.fillStyle='#c7e9e2';ctx.fill();ctx.strokeStyle='#247e72';ctx.lineWidth=2;ctx.beginPath();for(let j=0;j<=160;j++){let r=-rmax+2*rmax*j/160,x=x0+r*sx,y=base+w(r,q,R)*sy;j?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.stroke()}
function dibujar(){const c=casos[sel.value],d=c.escenarios[esc.value],f=d.serie[indice],t=f[0],q=f[1],R=c.radio;ctx.clearRect(0,0,1080,540);texto('Alumno '+sel.value+' · escenario '+esc.value,22,27,19);texto('s='+t.toFixed(3)+'   q='+Math.max(q,0).toFixed(3)+'   v='+f[2].toFixed(3)+'   F='+f[3].toFixed(3),22,55);texto(t<0?'Aproximación libre':indice===119?'Fin del contacto':'Contacto y deformación',22,84,16,'#8a4b10');
ctx.save();ctx.beginPath();ctx.rect(15,100,390,350);ctx.clip();const base=405,s=4.45;perfil(207,base,s,s,42,Math.max(q,0),R);ctx.fillStyle='#df8b30';ctx.beginPath();ctx.arc(207,base+(q-R)*s,R*s,0,2*Math.PI);ctx.fill();ctx.restore();texto('Esfera rígida · blanco deformable',30,475,15);texto('δ/R = '+(Math.max(q,0)/R).toFixed(5),30,503,16);
texto('Ampliación del contacto: superficie del blanco',450,92,16);ctx.save();ctx.beginPath();ctx.rect(445,105,600,170);ctx.clip();const bx=745,by=185,sx=27,sy=48;ctx.fillStyle='#df8b30';ctx.beginPath();ctx.moveTo(445,105);for(let j=0;j<=180;j++){let r=-11+22*j/180;ctx.lineTo(bx+r*sx,by+(q-r*r/(2*R))*sy)}ctx.lineTo(1045,105);ctx.closePath();ctx.fill();perfil(bx,by,sx,sy,11,Math.max(q,0),R);ctx.strokeStyle='#718390';ctx.setLineDash([5,4]);ctx.beginPath();ctx.moveTo(445,by);ctx.lineTo(1045,by);ctx.stroke();ctx.setLineDash([]);ctx.restore();texto('q(t) desplaza el centro de la superficie',450,299,14,'#3b625e');
const a=d.curva,tf=a.at(-1)[0],maxq=Math.max(...a.map(p=>p[1]),.01),gx=470,gy=480,gw=550,gh=150;ctx.strokeStyle='#738897';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(gx,gy-gh);ctx.lineTo(gx,gy);ctx.lineTo(gx+gw,gy);ctx.stroke();function linea(col,color,dash){ctx.strokeStyle=color;ctx.lineWidth=2;ctx.setLineDash(dash);ctx.beginPath();let inicio=true;for(const p of a){if(p[col]===null){inicio=true;continue}let x=gx+gw*p[0]/tf,y=gy-gh*p[col]/maxq;inicio?ctx.moveTo(x,y):ctx.lineTo(x,y);inicio=false}ctx.stroke();ctx.setLineDash([])}linea(1,'#d77820',[]);linea(2,'#176ca1',[5,3]);if(t>=0){ctx.fillStyle='#bd2945';ctx.beginPath();ctx.arc(gx+gw*t/tf,gy-gh*q/maxq,5,0,7);ctx.fill()}texto('Indentación: numérica (naranja), referencia (azul)',450,324,15);texto('Tiempo relativo s',670,510,14);
}
sel.onchange=opciones;esc.onchange=cargar;slider.oninput=()=>{indice=+slider.value;activo=false;$('play').textContent='Reproducir';dibujar()};$('play').onclick=()=>{activo=!activo;$('play').textContent=activo?'Pausar':'Reproducir'};$('reiniciar').onclick=()=>{indice=0;slider.value=0;dibujar()};function ciclo(ms){if(activo&&ms-prev>75){indice=(indice+1)%120;slider.value=indice;dibujar();prev=ms}requestAnimationFrame(ciclo)}opciones();requestAnimationFrame(ciclo);
</script></html>'''


def guardar_visor(paquetes,ruta):
    """Escribe HTML autónomo con datos finitos, controles y superficie del blanco."""
    Path(ruta).write_text(HTML.replace('__DATOS__',json.dumps(paquetes,ensure_ascii=False,allow_nan=False)),encoding='utf8')


def crear_gif(paquete,ruta):
    """Anima esfera, superficie deformada, ampliación y curva sincronizada."""
    e='B' if 'B' in paquete['escenarios'] else next(iter(paquete['escenarios']))
    r=paquete['escenarios'][e];serie=r['serie'];curva=np.array([[a,b,np.nan if c is None else c] for a,b,c in r['curva']])
    fig,axs=plt.subplots(1,3,figsize=(12,4.8),gridspec_kw={'width_ratios':[1,1,1.15]})
    escena,zoom,graf=axs;R=paquete['radio']
    escena.set(xlim=(-42,42),ylim=(8,-73),xlabel='x/L',ylabel='z/L',title='Esfera rígida y blanco');escena.set_aspect('equal',adjustable='box')
    zoom.set(xlim=(-10,10),ylim=(2.2,-2.4),xlabel='x/L',ylabel='z/L',title='Contacto ampliado')
    esfera=Circle((0,-R-6),R,color='#df8b30');escena.add_patch(esfera)
    rz=np.linspace(-10,10,241);rg=np.linspace(-42,42,301)
    superficie,=escena.plot(rg,np.zeros_like(rg),color='#247e72',lw=1.5)
    suelo=Polygon(np.column_stack((np.r_[rg,42,-42],np.r_[np.zeros_like(rg),8,8])),color='#c7e9e2',zorder=0);escena.add_patch(suelo)
    borde,=zoom.plot(rz,np.zeros_like(rz),color='#247e72',lw=2,zorder=4)
    blanco=Polygon(np.column_stack((np.r_[rz,10,-10],np.r_[np.zeros_like(rz),3,3])),color='#c7e9e2',zorder=1);zoom.add_patch(blanco)
    proyectil=Polygon(np.column_stack((np.r_[rz,10,-10],np.r_[-6-rz**2/(2*R),-4,-4])),color='#df8b30',zorder=2);zoom.add_patch(proyectil)
    zoom.axhline(0,color='#718390',ls='--',lw=.7,zorder=3)
    etiqueta='Serie s≤0.12' if 'limite_serie' in r['metricas']['referencia'] else 'Referencia'
    graf.plot(curva[:,0],curva[:,1],color='#d77820',label='Numérica');graf.plot(curva[:,0],curva[:,2],color='#176ca1',ls='--',label=etiqueta)
    punto,=graf.plot([],[],'o',color='#bd2945');graf.set(xlabel='Tiempo s',ylabel='Indentación q',title='Analítica frente a numérica');graf.legend(fontsize=8);graf.grid(alpha=.2)
    texto=fig.text(.05,.14,'',fontsize=10)
    fig.suptitle(f"Alumno {paquete['numero']} · escenario {e} · impacto y deformación del blanco")
    fig.text(.5,.06,'Perfil cuasiestático Hertz adoptado; ampliación con escalas distintas. Parámetros relativos docentes.',ha='center',fontsize=8)
    fig.text(.5,.025,'Solo contacto: no calcula perforación, daño celular ni recuperación posterior libre del blanco.',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.20,1,.92));ids=np.linspace(0,len(serie)-1,96).astype(int)
    def cuadro(j):
        t,q,v,f,_=serie[ids[j]];delta=max(q,0.);esfera.center=(0,q-R)
        wg=perfil_blanco(rg,delta);wz=perfil_blanco(rz,delta)
        superficie.set_data(rg,wg);suelo.set_xy(np.column_stack((np.r_[rg,42,-42],np.r_[wg,8,8])))
        borde.set_data(rz,wz);blanco.set_xy(np.column_stack((np.r_[rz,10,-10],np.r_[wz,3,3])))
        proyectil.set_xy(np.column_stack((np.r_[rz,10,-10],np.r_[q-rz**2/(2*R),-4,-4])))
        punto.set_data([t] if t>=0 else [],[q] if t>=0 else [])
        fase='Aproximación' if t<0 else ('Fin del contacto' if j==len(ids)-1 else 'Contacto')
        texto.set_text(f'{fase} · s={t:.3f}   δ/L={delta:.4f}   δ/R={delta/R:.5f}   v={v:.3f}   F={f:.3f}')
        return esfera,superficie,suelo,borde,blanco,proyectil,punto,texto
    anim=FuncAnimation(fig,cuadro,frames=len(ids),interval=80,blit=False)
    anim.save(ruta,writer=PillowWriter(fps=12),dpi=85);plt.close(fig)


def exportar_movimiento(numero,resultados,carpeta,animar=False):
    """Exporta visor de escenarios y GIF opcional; no altera la física calculada."""
    paquete=crear_paquete(numero,resultados);guardar_visor({numero:paquete},carpeta/'visor.html')
    if animar:crear_gif(paquete,carpeta/'animacion.gif')
