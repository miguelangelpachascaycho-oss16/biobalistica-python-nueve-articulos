"""Migración acotada de la entrega docente; conserva íntegros los GIF calculados."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import os
import re
import subprocess

CARPETAS = ['01_celula_individual', '02_celula_multiples', '03_bicapa_dem',
            '04_piel_ogden', '05_vesicula_dpd', '06_membrana_plana',
            '07_membrana_dipolar', '08_bicapa_cooperativa', '09_bicapa_tetraedro']
NOTAS = [
    'Contacto lateral y deformación pequeña de la célula idealizada. El color y la curva permiten apreciar cambios difíciles de ver a escala global.',
    'Varios proyectiles, cambio de forma y rotura de enlaces del modelo DEM. La rotura de un enlace numérico no demuestra daño en una célula real.',
    'Vista 3D y proyección lateral de la bicapa: se aprecia la depresión local producida por las partículas.',
    'Fase temprana del impacto en piel: la indentación es pequeña en esta ventana y se aprecia mejor en la curva. No se simula perforación.',
    'Colisión con una vesícula idealizada y comparación con velocidad inicial cero. La deformación se analiza mediante el cambio de forma global.',
    'Empuje activo contra una hoja elástica artificial. El eje de deformación está ampliado; no corresponde a un disparo balístico.',
    'Empuje activo contra una cadena dipolar artificial y comparación con el perfil analítico. No es una célula ni una bicapa molecular.',
    'Dos nanopartículas guiadas por resortes móviles contactan la bicapa. La curva incluye fluctuación térmica y se compara con el control.',
    'Contacto temprano de un tetraedro con una bicapa DOPC, con traslación y rotación. La rugosidad se compara con el control; no es un cañón de genes.'
]


def construir(archivos):
    """Produce un árbol nuevo desde la versión plana, sin recalcular física."""
    def leer(nombre):
        return archivos[nombre].decode('utf-8').replace('\r\n', '\n')
    actividades = json.loads(leer('ACTIVIDADES.json'))
    mapa = {'LICENSE': 'LICENSE', 'requirements.txt': 'requirements.txt',
            'GUIA_DOCENTE.md': 'docs/GUIA_DOCENTE.md',
            'GUIA_COPILOT.md': 'docs/GUIA_COPILOT.md',
            'APRENDE_A_CONSTRUIR.md': 'docs/APRENDE_A_CONSTRUIR.md',
            'EXPLICACION_FUNCIONES.md': 'docs/EXPLICACION_FUNCIONES.md',
            'SOLUCIONES_ANALITICAS.md': 'docs/SOLUCIONES_ANALITICAS.md',
            'REVISION_BIOBALISTICA.md': 'docs/FUENTES_Y_ALCANCE.md',
            'ACTIVIDADES.json': 'docs/ACTIVIDADES.json',
            'README.md': 'README.md',
            'OBSERVACION_VESICULA.json': 'pruebas/evidencia/OBSERVACION_VESICULA.json',
            'EJECUCIONES_NUEVAS.json': 'pruebas/evidencia/EJECUCIONES_NUEVAS.json'}
    guias = {'CASOS_CELULARES.md', 'PILOTO_MEMBRANA.md', 'PIEL_OGDEN.md',
             'VESICULA_DPD.md', 'CASO_06.md', 'CASO_07.md', 'CASO_08.md', 'CASO_09.md'}
    for nombre in guias:
        mapa[nombre] = 'docs/modelos/' + nombre
    programas = {a['programa'] for a in actividades} | {
        'celula_dem.py', 'penetracion_activa.py', 'bicapa_dpd.py'}
    for nombre in programas:
        mapa[nombre] = 'src/' + nombre
    verificadores = {a['verificador'] for a in actividades}
    for nombre in verificadores:
        mapa[nombre] = 'pruebas/' + nombre
    for nombre in ['VERIFICACION_CELULAS.json', 'VERIFICACION_PILOTO.json',
                   'VERIFICACION_PIEL.json', 'VERIFICACION_VESICULA.json', 'VERIFICACION_NUEVOS.json']:
        mapa[nombre] = 'pruebas/evidencia/' + nombre
    prefijos = ['CELULA_01', 'CELULA_02', 'PILOTO', 'PIEL', 'VESICULA',
                'CASO_06', 'CASO_07', 'CASO_08', 'CASO_09']
    for a, carpeta, prefijo in zip(actividades, CARPETAS, prefijos):
        ruta = 'casos/' + carpeta
        mapa[f"ALUMNO_{a['alumno']:02d}.md"] = ruta + '/README.md'
        mapa[a['preview'] + '.gif'] = ruta + '/animacion.gif'
        mapa[a['preview'] + '.png'] = ruta + '/figura.png'
        for nombre in archivos:
            if nombre.startswith(prefijo + '_') and nombre.endswith(('.csv', '.json')):
                resto = nombre[len(prefijo) + 1:].lower()
                mapa[nombre] = ruta + '/ejemplo/' + resto
    # Los vínculos Markdown se resuelven desde su nueva carpeta.
    def transformar_md(texto, destino):
        def vinculo(m):
            enlace = m.group(1)
            if re.match(r'\w+://', enlace) or enlace.startswith('#'):
                return m.group(0)
            nombre, sep, ancla = enlace.partition('#')
            if nombre not in mapa:
                return m.group(0)
            relativo = os.path.relpath(mapa[nombre], str(Path(destino).parent)).replace('\\', '/')
            return '](' + relativo + (sep + ancla if sep else '') + ')'
        texto = re.sub(r'\]\(([^)]+)\)', vinculo, texto)
        # Rutas de comandos y nombres de archivos en prosa: siempre desde raíz.
        for antiguo in sorted(mapa, key=len, reverse=True):
            nuevo = mapa[antiguo]
            texto = texto.replace('`' + antiguo + '`', '`' + nuevo + '`')
            if antiguo.endswith('.py'):
                texto = re.sub(r'(?<![\w/])' + re.escape(antiguo) + r'(?=\s|`|$)', nuevo, texto)
        return texto
    nuevo = {}
    for origen, destino in mapa.items():
        contenido = archivos[origen]
        if origen.endswith('.md'):
            texto = leer(origen)
            if origen == 'REVISION_BIOBALISTICA.md':
                texto = texto.split('## Candidatos')[0]
                texto = re.sub(r'^.*BUSQUEDA_FALTANTES\.md.*\n?', '', texto, flags=re.M)
            contenido = transformar_md(texto, destino).encode('utf-8')
        if origen in verificadores:
            texto = leer(origen)
            pos = texto.index('\n', texto.index('"""', 3) + 3) + 1
            arranque = ('import sys\nfrom pathlib import Path as _Path\n'
                        'sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "src"))\n'
                        '_evidencia = _Path(__file__).resolve().parent / "resultados"\n'
                        '_evidencia.mkdir(exist_ok=True)\n')
            texto = texto[:pos] + arranque + texto[pos:]
            texto = re.sub(r'Path\(([\'\"])(VERIFICACION_[A-Z]+\.json)\1\)',
                           r'(_evidencia / "\2")', texto)
            contenido = texto.encode('utf-8')
        nuevo[destino] = contenido
    for a, carpeta in zip(actividades, CARPETAS):
        i = a['alumno']
        a['programa'] = mapa[a['programa']]
        a['guia'] = mapa[a['guia']]
        a['verificador'] = mapa[a['verificador']]
        a['ficha'] = f'casos/{carpeta}/README.md'
        a['preview'] = f'casos/{carpeta}/animacion'
        a['figura'] = f'casos/{carpeta}/figura.png'
        a['ejemplo'] = f'casos/{carpeta}/ejemplo'
        a['nota_visual'] = NOTAS[i-1]
        texto = nuevo[a['ficha']].decode('utf-8')
        texto += '\n## Qué observar en la animación\n\n' + NOTAS[i-1] + '\n\n![Animación calculada](animacion.gif)\n'
        nuevo[a['ficha']] = texto.encode('utf-8')
    nuevo['docs/ACTIVIDADES.json'] = json.dumps(actividades, ensure_ascii=False, indent=2).encode('utf-8')
    lanzador = leer('ejecutar_caso.py').replace("raiz/'ACTIVIDADES.json'", "raiz/'docs'/'ACTIVIDADES.json'")
    nuevo['ejecutar_caso.py'] = lanzador.encode('utf-8')
    nuevo['.gitignore'] = b'__pycache__/\n*.pyc\n.venv/\nresultados/\npruebas/resultados/\n'
    filas = []
    for a in actividades:
        filas.append(f"| [{a['alumno']:02d}]({a['ficha']}) | {a['autor']} ({a['year']}) | {a['blanco']} | [GIF]({a['preview']}.gif) |")
    readme = '''# Biobalística y penetración mecánica en Python

Nueve actividades docentes con **nueve artículos distintos**. Cada caso tiene su ficha, animación, figura y resultados de ejemplo en una carpeta propia.

**[Ver las nueve animaciones](GALERIA.md)** · [Guía del docente](docs/GUIA_DOCENTE.md) · [Funciones](docs/EXPLICACION_FUNCIONES.md) · [Trabajo analítico](docs/SOLUCIONES_ANALITICAS.md)

## Elige tu caso

| Alumno | Artículo | Blanco del modelo | Animación |
|---|---|---|---|
''' + '\n'.join(filas) + '''

## Ejecutar en Visual Studio Code

Descarga **Code → Download ZIP**, extrae el archivo y abre la carpeta completa en VS Code. Desde **Terminal → New Terminal**, ejecuta en la raíz:

```powershell
py -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.\\.venv\\Scripts\\python.exe ejecutar_caso.py --listar
.\\.venv\\Scripts\\python.exe ejecutar_caso.py 1 --animar
```

Cambia `1` por tu número del 1 al 9 y selecciona `.venv` como intérprete. Si `py` no está disponible, utiliza `python -m venv .venv`. Ejecuta un caso cada vez. Tu ficha indica la salida en `resultados/`, el verificador, los controles y las tareas analíticas. La instalación de dependencias requiere Internet; el cálculo se ejecuta sin Copilot ni claves de IA.

## Cómo está organizado

```text
casos/       Una carpeta por alumno: README, GIF, figura y ejemplo/
src/         Programas de simulación y motores físicos compartidos
docs/        Guías, funciones, referencias analíticas y fuentes
pruebas/     Verificadores matemáticos y evidencia de las ejecuciones
resultados/  Tus propias salidas al ejecutar; no se suben al repositorio
```

En [cada ficha](casos/) se explica qué programa de `src/` estudiar y qué realiza cada función. [Copilot como tutor](docs/GUIA_COPILOT.md) y [cómo construir el modelo](docs/APRENDE_A_CONSTRUIR.md) acompañan la práctica. Las pruebas se ejecutan con los comandos de [pruebas/README.md](pruebas/README.md).

## Alcance científico

01–04: biobalística en células, bicapa o tejido idealizados. 05: colisión con una vesícula. 06–07: penetración activa en membranas artificiales mínimas; no son células ni bicapas moleculares. 08–09: interacción mecánica de nanopartículas con bicapas; no son disparos de un cañón de genes.

**Son implementaciones docentes reducidas**, con supuestos y elecciones complementarias declarados en cada guía. No constituyen nueve reproducciones cuantitativas completas ni predicciones biológicas validadas. El caso 04 muestra únicamente el impacto temprano; en 06–07 hay empuje activo, y en 08 el movimiento es guiado. Los GIF conservan las coordenadas y escalas calculadas. Consulta [fuentes, acceso y límites](docs/FUENTES_Y_ALCANCE.md): hay artículos CC BY y copias públicas de autor; la licencia de reutilización de las tres copias de Campello no está confirmada.

Los anteriores ejercicios genéricos de contacto y los documentos de búsqueda históricos se retiraron de la versión para alumnos. El historial de Git conserva la versión previa. El PDF original del docente se mantiene intacto.
'''
    nuevo['README.md'] = readme.encode('utf-8')
    galeria = ['# Las nueve animaciones', '', '[Volver al inicio](README.md)', '',
               'Vistas pregeneradas de las implementaciones docentes. Se muestra el resultado calculado, sin ampliar artificialmente la deformación; las escalas y ampliaciones indicadas en cada figura deben respetarse. Los controles de los casos 05–09 ayudan a distinguir deformación por contacto y evolución sin excitación.', '']
    for a in actividades:
        galeria += [f"## {a['alumno']:02d} · {a['blanco']}", '',
                    f"{a['autor']} ({a['year']}) · [Artículo](https://doi.org/{a['doi']}) · [Ficha y paso a paso]({a['ficha']})", '',
                    a['nota_visual'], '', f"![Caso {a['alumno']:02d}: movimiento y deformación]({a['preview']}.gif)", '']
    nuevo['GALERIA.md'] = '\n'.join(galeria).encode('utf-8')
    texto_pruebas = '''# Verificación matemática

Ejecuta desde la raíz del repositorio, con las dependencias instaladas:

```powershell
.\\.venv\\Scripts\\python.exe pruebas/verificar_celulas.py
.\\.venv\\Scripts\\python.exe pruebas/verificar_piloto.py
.\\.venv\\Scripts\\python.exe pruebas/verificar_piel.py
.\\.venv\\Scripts\\python.exe pruebas/verificar_vesicula.py
.\\.venv\\Scripts\\python.exe pruebas/verificar_nuevos.py
```

Las nuevas comprobaciones se guardan en `pruebas/resultados/`. `evidencia/` conserva las comprobaciones de las simulaciones que generaron los GIF de ejemplo. Estas pruebas comprueban fuerzas, energía, integración y límites analíticos; no constituyen validación experimental ni reproducción completa de los artículos.
'''
    nuevo['pruebas/README.md'] = texto_pruebas.encode('utf-8')
    for nombre, contenido in nuevo.items():
        if nombre.endswith('.py'):
            ast.parse(contenido.decode('utf-8'), filename=nombre)
        if nombre.endswith('.md'):
            for enlace in re.findall(r'\]\(([^)]+)\)', contenido.decode('utf-8')):
                if re.match(r'\w+://', enlace.strip('<>')) or enlace.startswith('#'):
                    continue
                limpio = enlace.split('#')[0].strip('<>')
                ruta = os.path.normpath(str(Path(nombre).parent / limpio)).replace('\\', '/')
                if ruta not in nuevo and not any(f.startswith(ruta.rstrip('/') + '/') for f in nuevo):
                    raise ValueError(f'Enlace local sin destino: {nombre}: {enlace}')
    return nuevo, mapa


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--origen', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--salida', type=Path)
    parser.add_argument('--aplicar', action='store_true')
    args = parser.parse_args()
    raiz = args.origen.resolve()
    base = json.loads(BASE_JSON)
    archivos = {}
    for nombre, esperado in base.items():
        ruta = (raiz / nombre).resolve()
        assert ruta.is_relative_to(raiz) and ruta.is_file(), nombre
        contenido = ruta.read_bytes()
        assert hashlib.sha256(contenido).hexdigest() == esperado, f'Archivo cambió: {nombre}'
        archivos[nombre] = contenido
    nuevo, mapa = construir(archivos)
    destino = raiz if args.aplicar else args.salida.resolve()
    if not args.aplicar:
        assert destino != raiz and not destino.exists(), str(destino)
    else:
        assert (raiz / '.git').exists(), 'Aplicación solo en checkout Git'
        rastreados = set(subprocess.check_output(['git', 'ls-files'], cwd=raiz, text=True).splitlines())
        assert rastreados <= set(base) | {'organizar_entrega.py', '.github/workflows/organizar.yml'}, 'Cambios ajenos detectados'
        # Solo archivos exactos previamente cotejados; el historial Git conserva la versión anterior.
        for nombre in base:
            ruta = (raiz / nombre).resolve()
            assert ruta.is_relative_to(raiz)
            ruta.unlink()
        propio = raiz / 'organizar_entrega.py'
        if propio.exists():
            propio.unlink()
    for nombre, contenido in nuevo.items():
        ruta = (destino / nombre).resolve()
        assert ruta.is_relative_to(destino)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_bytes(contenido)
    print(json.dumps({'archivos_finales': len(nuevo), 'retirados_de_version_plana': len(set(base)-set(mapa)), 'gif_conservados': 9}))


BASE_JSON = '{".gitignore": "4d8b8bfdd68dc332301d3ac3cd1d67d1e4feef9607266e4bc743d87bb8ffcafd", "ACCESO_FUENTES.md": "1e2871dacde84509ed2e75ee85cd2e87a8f952e9d428a9e11bc8abf7685fb418", "ACTIVIDADES.json": "aafedfafc85a7a8379bbafa3e7fa53632237c0576f4397867c971961dfc0718b", "ALUMNO_01.md": "f9b11c65752d72ce1bd24238c76fd0d6fd644404e150fad6a5da8a2e3edad206", "ALUMNO_02.md": "e63949cef58a30b65effff9907b4d032e5ea45022e581f532382c07747ea3bdf", "ALUMNO_03.md": "d0f75178a2f7fd8992e2ec2a5adb86ff97404a0769e43930017746fcf0f16987", "ALUMNO_04.md": "71ce4abb3936977062bea67b546d861529ffeb0a634fd9201ce2a9708dbe670f", "ALUMNO_05.md": "3768f0154a9f27674db4bf22b41e577a2c2d71f817e27656ed88e6654527dec1", "ALUMNO_06.md": "e0c2ab6bfb4399ec942b92d7556004c5349af02e0736c0d90c8e40afd86c9170", "ALUMNO_07.md": "6f77a7e0cf22725a21ea1e611c207474c963fa265d10e9ea0cfdb14571a044db", "ALUMNO_08.md": "83140694f06f10f43e70dd4ecdb2578ba89acc47a0b8511b1ea8462dd1df8ad4", "ALUMNO_09.md": "4f8aaba150702140401b1748f49f14f988ce5b845d32f9350cc26fd4589e9d8a", "APRENDE_A_CONSTRUIR.md": "a00976e9d7f95fe4be2ea50b461a789ed7623a6e9b3b56e00df45474640e3e46", "APRENDE_CONTACTO_AUXILIAR.md": "3f81ecfc3cb66669e458039eff194ab6456f41305ccbdf195601a143504f1f14", "BUSQUEDA_FALTANTES.md": "4bb3d6858e624c2f3ffef55137914aea1bc9cca08388abcbb92fa1b61b8ed75e", "CASOS_CELULARES.md": "62d653af3ddc7595ebbb5e741a6c08a0b55518f44381df6747f60af28205d9fa", "CASO_06.md": "77243038e3a1f4bda7976e1c637cd103bff2c04539d2b5c5ddafd0ed0f1dfdc6", "CASO_06_METRICAS.csv": "3c60dee9ee46310038d8ff2a53d4cc5a195d49f0fa977f4bb6c67452a130d064", "CASO_06_PARAMETROS.json": "04b171495f5aff6eb2e6c6d64a190142e09961207ad492b8d4e492a8127faacd", "CASO_06_REFERENCIA.csv": "cfa7e9d15fcfe6e3055b2e4a6d7c367ec6068fcb6a1b0d68f5bab12328adcec8", "CASO_06_RESUMEN.json": "1778971e03f298d7da8c350e4a65dffbb3419dd779705e6cb856740c193727b5", "CASO_07.md": "fe44e03d4eeec48e64dc19723cae49957ff934617c3f6c94d2c0f494536f6825", "CASO_07_METRICAS.csv": "3eb9019e2db3f2d431918613535fef2b3f185fed48b516ada7c11a2074a81d10", "CASO_07_PARAMETROS.json": "454ebcc93467125f00ecb5a4e16f14f03b67a7e75aef2a7588c4ad71393af428", "CASO_07_REFERENCIA.csv": "832cd0518ed9e098541414e1cdd939af9270895218c8132447fbcff6514d297a", "CASO_07_RESUMEN.json": "4b4f150c8658b64121404d3bd7d59d70cad60786541166f8578e54ccf29fa7e7", "CASO_08.md": "1b733c70f0ff17292db8c67635812528bf8f68043e709b6857a93b0d1002d036", "CASO_08_METRICAS.csv": "53f4cc413fa0e8907656032252c64ecd9a5496df01b2b15a2470f6c8c0fa998c", "CASO_08_PARAMETROS.json": "411117da61b1048909d24e19ae99a3aacda234b0802dc00895300ce0a5dd040b", "CASO_08_RESUMEN.json": "d8f0bfde2b49ea36c86bb5e45d05474de5d88169c7b5163546ae71262c0cda46", "CASO_09.md": "5e160b304b88ed1d01c0a498361b7fb90bb9879a7d6a30a79f18f9ca5160407a", "CASO_09_METRICAS.csv": "d46eb1da913c604a02549f0c2974eda277eaf977953b09740d0cfbc34636f192", "CASO_09_PARAMETROS.json": "9a85e1ff119ba92968f4db9d988f0f4b7b2a32fbb9555adadf807e55cbc78615", "CASO_09_RESUMEN.json": "e5b1cf54cae3019355aff69bf5dea4a8fb94d970df24d1a220efec1abddbc6f4", "CELULA_01_METRICAS.csv": "29a413c151c98a9ce14d6884dfa305979426683800a10bdff5b398cf85a89c6a", "CELULA_01_PARAMETROS.json": "2aa223ddc2cafe75f61f6d549e0157651ef36833a97e7493cfe1a6bfa0979cc5", "CELULA_02_METRICAS.csv": "ea61ae5d6ec72b5378882732f8124da03aebee467b422717f8e7ea8c2debd426", "CELULA_02_MUESTRAS.csv": "41c45b27ae0f6c8072171d65a62e43f72cb3c0729d810ddcda28a18275addf36", "CELULA_02_PARAMETROS.json": "48eaf0fbaf17354ac0f9b4fa0b19885ed98aa637b235a902d4baa616e9893ef7", "CONTACTO_AUX_01.md": "fd795e8b0a1a1309fd1738db4071b79f66190f88ac8b34a1d294a0bd5136a7f1", "CONTACTO_AUX_02.md": "1be2a8996202e9f5b2d257d5a2830df425e361f2f4b9d7aa7a4e21c36632ebd9", "CONTACTO_AUX_03.md": "6b90fcaa86b415b4f44ba4a56a0f52e9f62b0630df52cda2b29573da981d9428", "CONTACTO_AUX_04.md": "e408b5e208f01500024086524b37a92b4857599b2d0f7d0b14416e42c3337fcc", "CONTACTO_AUX_05.md": "1b5c7a2ad46a1ab4cea6f69b8c7bae23703c2d40a7214cdf255905886fdc0d09", "CONTACTO_AUX_06.md": "a85218e51f5ec394b2503dab6b29016b586ed37d80032a08b3ac98995c436f61", "CONTACTO_AUX_07.md": "aab0159f4829f6f81d92a6b05ae2b220d12951038d7eebcce0a697455364e256", "CONTACTO_AUX_08.md": "69ef695d7c382a3b79f2f064f9cf5166c32a5d2697c2614656a481ebe57959e2", "CONTACTO_AUX_09.md": "b268e309c8cfd7791bb3634ad21bdca08e76a71b63cda55a083d47b4fa164895", "EJECUCIONES_NUEVAS.json": "cbd4fcfac57de5056bea034ad3d69910124ba942fa0ddd7a5a6fa6564b61d6e6", "EXPLICACION_FUNCIONES.md": "6ee90f4a3ded5307efb17eadd9841db01706eb97a63237c2fa1225aadb2af197", "FUENTES.json": "aafedfafc85a7a8379bbafa3e7fa53632237c0576f4397867c971961dfc0718b", "FUENTES_CONTACTO_AUXILIAR.json": "8f54dbdf7b6f8b5cd0d573c51d5831632531f75db297ade5632d386ab59cda80", "FUNCIONES_CONTACTO_AUXILIAR.md": "dcfb01db21c6ce84faa51f1fe66caf9153bb7b32a308fcdefcc238b768d02a63", "FUNDAMENTOS_CONTACTO.md": "a15e68517ed07ed9941d5821d591bd468ca436bb0910f13c378b68f20727cfbb", "GUIA_COPILOT.md": "d79790db6e47f96b287e7344d575e14ec24f84e16f3d93931eb50a20aebcc9b8", "GUIA_DOCENTE.md": "461ff2e62015d36f613312116d5a8984513abf9c518ecd4714063b463cd7144d", "LICENSE": "d4bee084d61f3a00296f0800922278010e871edd15a481975c42ec68a6127c8a", "MODELO_DEFORMACION_BLANCO.md": "637360afc6445304b5753c055eab479b3caffef9ca80bd8cfc113645931fd831", "OBSERVACION_VESICULA.json": "7cac445e7dfb51cc67eb5a6e8bac0b6407e112057a709fba62baa589b2d70ece", "PIEL_METRICAS.csv": "d6bbc0cf31cdee9d860f1547a4c9af110b77b4094aae886103d91dcc4a258eba", "PIEL_OGDEN.md": "15a0096719d38470feb3d607a22db6b12ab18e3f1a2df00e91d20dc99f14ced7", "PIEL_PARAMETROS.json": "8a9995bad54d79544b33bf65ac2af1ffcf65ec6a86ab76a20b9f3fbebd852375", "PILOTO_ESTADOS.npz": "ca283d1d47b5ed6db3a2a6bc0b09883eaf860fc17ce223436e204bd066c34c9f", "PILOTO_MEMBRANA.md": "ed0b9601cdc510f8f4b3c95f1d9ec30d6481711d2c5ce66a1bf1aba9fb36bf5b", "PILOTO_METRICAS.csv": "e377865be25f4a3d922fbcfeac5f981cca4a98b7404a83f01bc75412cfd77907", "PILOTO_PARAMETROS.json": "0deff31348a9dd3922930d67c379be0b0c4a6ed5b3410318d2a3ba30a5932d97", "README.md": "12ae6b15fc024c0787c83499c1042d3b2cbd691d3fbf321312659d1cecb642c0", "REVISION_BIOBALISTICA.md": "8ad7e4de82114247971bd6ca9f3528a4e4a3594d5d74dc4d4ce7f89f4454dc42", "SELECCION_BIOBALISTICA.json": "9a3454b47f65a3540f504b3bcf483fafee1990f641c4e78491dc0bafb652b886", "SOLUCIONES_ANALITICAS.md": "da84400a33662c4567cc46fa17ef6973728abccc280a3cf1ec9d72dfd1e8bb28", "SOLUCIONES_CONTACTO_AUXILIAR.md": "bc7ee2822dd0aee0fe463ebeead56419413cac318dc669315e05119369d9748a", "VERIFICACION.json": "fd175b693d24f863b041a2e37c4f55cfa76277efd40a6da21b27d078ad33d877", "VERIFICACION_CELULAS.json": "67975e4993d3dcf2c34d60fc1fd6b1ed4df34ac6bef7ca1bc36f2ecaa74e48f3", "VERIFICACION_ENTREGA.json": "bda9bf1e97acf58a4bb3b791f40dd990a9fbaba3e6376a07aadbefc81ded0f01", "VERIFICACION_NUEVOS.json": "058a1effbbad454b24a2ffd0e8a8e31214a91d1416b4b3b6101db1f7045ff07e", "VERIFICACION_PIEL.json": "351139f4d61ed42874d936544d76b3e4b2593b3089592d36064a7577ed71dd6f", "VERIFICACION_PILOTO.json": "0e614cba6b43722120650bf9570035ef76dcdd76f9e636bc2742db32de75d048", "VERIFICACION_VESICULA.json": "8715a9826061d192832d6e416b78879943824ad803974f90b80f888ec632c81d", "VESICULA_DPD.md": "1ac9148a8ad94cacc3d559c18cec5b458245c7b48594cfd02d17b4a02f34e498", "VESICULA_METRICAS.csv": "6902d068278692ab4a6197ebfe4fff876a2f07a6b717d7fe7e73bb80efcbed5c", "VESICULA_PARAMETROS.json": "dbcb10015866984add01a8e7f9e928b9b9fa666da803303edfeb21f94f2cbe59", "animacion_01.gif": "678386f2d68b917787c19bbff318de9926abd339689f0e1fb5a10b9c068265b5", "animacion_02.gif": "685e4cb6cae3f7eddd98a1e06390c2c8f3ace6b40127b8003a9d473848a8ec10", "animacion_03.gif": "b8cb9843b130adaa7e1f8125ee3fe81ae30136c9af98e240f94bcc1482332fdc", "animacion_04.gif": "15818286e697b795df420db4847406dc6c4c11ba2e067e9ed70d55b749b4a87d", "animacion_05.gif": "23045e6aef711d292167028d774d706907b08a048040a86a9cfca97e77a9b083", "animacion_06.gif": "cc81da7c5c08adc7bba12d6a2357d6093e1712a60f84f99570848ae8daa21a9e", "animacion_07.gif": "914ec798f6aed1ed2c2c6438d2591c625a393373e15916735070693193c3f161", "animacion_08.gif": "cb5f6c7b33897a25fd4a9a1728a3ceec59357536a1f4c9fb647df973ec495370", "animacion_09.gif": "2fabf7b5685f49bf3be30344fe192af1cab6b0a8379999222943d8c024a2f665", "animaciones.py": "5ba40b3a39f724dce25d97b7f93a156651a2c8231ed2cc0512b4da852b6fff6f", "bicapa_dpd.py": "1ba5c9b6039ffbc771310379a95305f2e65815f97f97e72dfaad4ec9da0a9179", "caso_06.gif": "9ec439c2669384b858f11754f5afcf0c122a8d9de1a984b475587acbbec9d2a6", "caso_06.png": "893d8a67aea3d5410e2f10eb4e2c682236eda02000e7b0f189279d75cfe8a38f", "caso_06_plana.py": "c5e5e5d5f1e95f84d825322436cb643617bf610d80fa8aa44e25085d027f338e", "caso_07.gif": "6072e8dec962b91c6dd88ed5aab735778c05ae2929bc226dcd3b257570019ab6", "caso_07.png": "9f6245aed5d35803e2f1e03473d3d0644163be3002c3736d3d453205b7eb7a6e", "caso_07_dipolar.py": "463d097f0d68c52b9bebb5191658f75de37ec57830503b6ed28c09135122876a", "caso_08.gif": "b2783acd4464cdeb6fbdb46e20dfee4d3513e9ea0850abb5f2271ad7319e67b1", "caso_08.png": "5f15c89d5070cd9f48593fa858e6b9456b14da0c0d62b95fa4bab13a858abc1d", "caso_08_cooperativa.py": "9e353a2637dcf62ea3b1779e9931b62818f7b2c037e0db6931f7b69b39074090", "caso_09.gif": "3561864aed6e4fe51287069faeee9f3a2fc2d869e98c091cfd003f152416f9dd", "caso_09.png": "99ef192a6f7d3b0596af0ce8e0b396a2d0339ddf0c0ed8c6bcf183f635d15ff7", "caso_09_tetraedro.py": "7708b759186085992e07fd89ede0ce20c4378aea1f74e56b97d5f0fbd8b5e9e4", "caso_celular_01.py": "768d77730ea6696bd9b5411fddb8a0b3fdfa3d0afea195b73d9719a08eef2676", "caso_celular_02.py": "771d6a53d4ed3d93807a666f25b02202b442b779b3fb154f43dbe7db69943963", "celula_01.gif": "02726c9c0a3f386db85a820870fdaa0bfaf8eb3d11f2bbfe1a4769365dc481d2", "celula_01.png": "761e5dd1b53d7bb4d6ba634fe9fb9e5473b0eafe6c49afeaaf2278ba562e8916", "celula_02.gif": "0828e6c1f1d4ebc5bf5f49b1ecd582e292c7a2ad13ece9f91456e33a4fa7a6e2", "celula_02.png": "ace4b5bc41e6eab04d41ce2abaf37b8ad488130f2aacc2dc5bcb002078d0176e", "celula_dem.py": "dd0e4494c426604551064e3905f15772a047885e5a1cf46d7d6ca9c94937aaa0", "ejecutar_caso.py": "3964794139434a4cc9effe54c319ddb6b47d184b49e144fe3a2d26ccb3febaa2", "motor_contacto.py": "2984e88ca2acb10fbaf78b2f0fdefa0c251554270a8c0804012c022eca639600", "penetracion_activa.py": "3e8cecd11a61cd18dfd41ee175cbffa0d8df0546463cc8642233d14c30c4ab7b", "piel_ogden.gif": "667c2917457db5eea12c0cb6784ba22a3bec78483ac3cc504664cd02c8704100", "piel_ogden.png": "c7b882e4a5cd1961b4915d2bf49fa76b879016acd75644a97d54947b96573e89", "piel_ogden.py": "88a3058130c0fcf815e4080473e62099db2df043fe9125f4d5677c0885f11d95", "piloto_membrana.gif": "9e115009d46daf9821ed361b6fd4bf7f9a0d91bf6a9d83cd3f7ffd605fbdef52", "piloto_membrana.png": "05cdd0ccc4c9bb2259b5276dfc838e0f66a1ddf7b7ca778ed5d4c367fa58d590", "piloto_membrana.py": "78f6147f40af7f268b13c6c9b2923a4c2141184d3d17a736689d71e99ea969ec", "requirements.txt": "2c7bd7495acb81ede194727b17be90ba52bfaa3937f2efe4a5e37f213e93f8d7", "simulacion_01.py": "02beb756f39f4d11eb83b0499360eeeb21b4b6f9a0c7b2f04574a40cebe9e817", "simulacion_02.py": "fe254d419f973a8ddd1193e167c867577afe48a751307c107d6b2776197e6f00", "simulacion_03.py": "c2c28d9a0a0506c899dc63a37810039f2b7203126b765627f20fdbe74075b47a", "simulacion_04.py": "937e78e3cbd1b7fa812f9ff0e5955861c7ec450ea07d5f7936d0fa2c07c0b0d1", "simulacion_05.py": "40b77a47e03a415caae4c7330004dce75e4fa3497e5933bc69574363ee61babb", "simulacion_06.py": "d24d50a828c68dab3ca00fa1eaf0eeb0074e3a6415f8fb49268b2e3a32f2a9d6", "simulacion_07.py": "a325c9cc1c3e80fc5ff17c5dc128b32fc8be934931c336f6d37328d6e834e24c", "simulacion_08.py": "83e533cf8d07800593a6a3c6e24b3cd00845273250d316719072f05ef37bf013", "simulacion_09.py": "c56af58ac880b6661ce073dab80d98b517c4c78b5dfdcb235bbdf39374845efe", "verificar_celulas.py": "ebd01f34ef943bacd7a021bf576fd28433760b05a24a7a04058658952aac25bc", "verificar_nuevos.py": "54d54f6f4affec322fe1a833234a885538222dbdf0bf709f51b9ae9ab46bb57d", "verificar_piel.py": "e0399468700f9476d5d37a66c5cd31dd7fe249a714fff7d8fbd47b6f432e132b", "verificar_piloto.py": "c6bb2c08410ce98e563bab9371785d41c78be19747205f97a11f65f3fbd653e4", "verificar_todos.py": "848d1b3f361ce65c7bfad2e4dcadaa5fd575eab5044407639dbf2487185bf2b1", "verificar_vesicula.py": "9ee99bb0ebbe6d77783ada84c81436c857dbccdf50e7c4bca272c313ff346dce", "vesicula_dpd.gif": "f536fc67200e2f5f60e55d2aa6478a4ed890c3343542dc808ca2d3570df861b5", "vesicula_dpd.png": "597524996ca1e2e11186285ecbcbd567d7b1fa529ec9b0cc3dfc7a4006bd632e", "vesicula_dpd.py": "6ab564a5f3d2b48a0d3cd25f81405ed6fe64fc7e36e192640848328190f04db6", "visor_simulaciones.html": "bfee8c7c18a89924f6efff5bfd96c934e7d619c6f467eeb0f0d20beecdbee812"}'

if __name__ == '__main__':
    main()
