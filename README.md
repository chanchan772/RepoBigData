# 📚🔍 BigData-MiProyecto

---

## 🚀 Descripción General

**BigData-MiProyecto** es una **aplicación web** desarrollada en **Python/Flask** para la **gestión** y **búsqueda** de datos usando **MongoDB Atlas** y **Elasticsearch**. Con ella podrás:

- 🔒 **Autenticación de usuarios** (login/logout).
- 🗃️ **Explorar bases de datos y colecciones** alojadas en MongoDB Atlas.
- 🛠️ **Crear nuevas bases de datos** y colecciones desde la interfaz.
- 📨 **Enviar mensajes de contacto** que se almacenan en MongoDB.
- 🔍 **Buscar libros** en un índice de Elasticsearch con filtros por título, autor, categoría y fecha.
- 📊 **Visualizar resultados** en tablas dinámicas con DataTables.

---

## 📦 Estructura del Proyecto

```
ProyectoFinalBigData/
├── .env
├── app.py
├── requirements.txt
├── README.md
├── static/
│   ├── css/
│   │   ├── landingPage.css
│   │   └── gestor.css
│   ├── images/
│   │   ├── creador.png
│   │   └── loading.gif
│   └── ...
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── contacto.html
│   ├── login.html
│   ├── buscador.html
│   └── gestion/
│       ├── index.html
│       ├── crear_base_datos.html
│       ├── crear_coleccion.html
│       ├── ver_registros.html
│       ├── elastic_agregar_documentos.html
│       └── elastic_listar_documentos.html
└── docs/
    └── ejemplos/
```

- **`app.py`**: Archivo principal con todas las rutas de Flask.  
- **`static/`**: Contiene CSS, imágenes y JavaScript (assets estáticos).  
- **`templates/`**: Plantillas HTML de Jinja2 para cada vista.  
- **`.env`**: Variables de entorno con credenciales 🔑 (no subir a GitHub).  
- **`requirements.txt`**: Dependencias de Python.  
- **`docs/`**: Carpeta para documentación adicional y ejemplos.

---

## ⚙️ Tecnologías Utilizadas

- **Python 3.9+** 🐍  
- **Flask** como framework web.  
- **Jinja2** para plantillas HTML.  
- **MongoDB Atlas** (MongoDB Cloud) para la base de datos de usuarios, contactos y gestión.  
- **PyMongo** para la conexión a MongoDB.  
- **Elasticsearch 8.x** + **elasticsearch-py** para búsquedas avanzadas.  
- **Bootstrap 5** para estilos y layout responsive.  
- **DataTables** para tablas interactivas.  
- **FontAwesome** / Emojis para íconos y mejoras visuales.

---

## 🔧 Requisitos Previos

Antes de comenzar, asegúrate de tener:

1. **Python 3.9 o superior**  
   - [Descarga e instalación](https://www.python.org/downloads/)  
2. **Git** (opcional, para clonar el repositorio)  
   - [Descarga](https://git-scm.com/downloads)  
3. **Cuenta en MongoDB Atlas** (gratuita)  
   - [MongoDB Atlas](https://cloud.mongodb.com/)  
   - Configura un cluster (Basic Free) y crea un usuario con permisos de lectura/escritura **y** `listDatabases`.  
4. **Deployment de Elasticsearch en Elastic Cloud** (Basic Free)  
   - [Elastic Cloud](https://cloud.elastic.co/)  
   - Genera un **API Key** con permisos de lectura/escritura.

---

## 📝 Guía de Instalación Paso a Paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/ProyectoFinalBigData.git
cd ProyectoFinalBigData
```

### 2. Crear y activar entorno virtual

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows (CMD)
python -m venv venv
.\venv\Scripts\activate.bat

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Verás el prompt del terminal cambió a `(venv)`.

### 3. Instalar dependencias 📦

```bash
pip install -r requirements.txt
```

El `requirements.txt` incluye:
```
Flask
pymongo[srv]
elasticsearch
python-dotenv
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# ===========================
#   VARIABLES DE ENTORNO
# ===========================

# Flask secret key (puede ser cualquier cadena aleatoria)
SECRET_KEY=MiClaveSuperSecreta123!

# MongoDB Atlas connection string 🔑
MONGO_URI=mongodb+srv://sebastian:Sebas2025@bigdata.fcwb2ux.mongodb.net/administracion?retryWrites=true&w=majority&appName=BigData

# Elasticsearch endpoint y API Key 🗝️
ELASTIC_URL=https://abcd1234.us-east-1.aws.found.io:9243
ELASTIC_API_KEY=AbCdEfGh1234567890:ZyXwVuTs987654321

# Nombre del índice Elasticsearch para libros
INDEX_NAME=libros
```

- **`SECRET_KEY`**: usada por Flask para sesiones seguras.  
- **`MONGO_URI`**:  
  - Cambia `sebastian:Sebas2025` por tu usuario/contraseña reales.  
  - `bigdata.fcwb2ux.mongodb.net` es el host.  
  - `/administracion` es la base de datos donde está la colección `seguridad`.  
- **`ELASTIC_URL`**: URL de tu cluster Elasticsearch (obtenido en Elastic Cloud).  
- **`ELASTIC_API_KEY`**: generado en Elastic Cloud → Security → API Keys.  
- **`INDEX_NAME`**: nombre del índice donde indexarás libros (puedes cambiarlo si quieres).

⚠️ **No compartas** este archivo públicamente ni lo subas a GitHub (añádelo a `.gitignore`).

### 5. Crear la colección `seguridad` en MongoDB Atlas

1. En MongoDB Atlas → tu proyecto → **Clusters** → **Collections**.  
2. Selecciona la base de datos **administracion** y añade la colección **seguridad**.  
3. Dentro de `seguridad`, pulsa **“Insert Document”** y elige la pestaña **Raw JSON**.  
4. Pega este JSON de ejemplo para crear un usuario inicial:

   ```json
   {
     "usuario": "juanperez",
     "password": "Perez2025!",
     "rol": "Administrador",
     "fechaCreacion": { "$date": "2025-06-07T12:00:00.000Z" }
   }
   ```

5. Haz clic en **Insert**. Ahora verás “TOTAL DOCUMENTS: 1” y el documento listado.

📝 **Nota:** Agrega más usuarios si deseas probar distintas cuentas.

---

## ⚡️ Configurar el índice `libros` en Elasticsearch

Para la funcionalidad de **Buscador de Libros**, crearemos un índice `libros` con el mapping adecuado.

### 6.1. Conectar a Kibana Dev Tools

1. Abre la URL de **Kibana** de tu deployment (algo como `https://abcd1234.us-east-1.aws.found.io:9243/app/kibana`).  
2. Inicia sesión con tu usuario `elastic` y la contraseña generada o con un **API Key** con rol `kibana_user` mínimo.

### 6.2. Crear el índice `libros` con mapping

En **Dev Tools**, ejecuta (▶️) el siguiente comando:

```json
PUT /libros
{
  "mappings": {
    "properties": {
      "titulo": {
        "type": "text",
        "analyzer": "spanish"
      },
      "autor": {
        "type": "text",
        "analyzer": "spanish"
      },
      "categoria": {
        "type": "keyword"
      },
      "fecha": {
        "type": "date",
        "format": "yyyy-MM-dd"
      },
      "descripcion": {
        "type": "text",
        "analyzer": "spanish"
      }
    }
  }
}
```

- **`titulo`, `autor`, `descripcion`**: `analyzer: "spanish"` para búsquedas en español.  
- **`categoria`**: `keyword` (valores exactos).  
- **`fecha`**: tipo `date` con formato `yyyy-MM-dd`.

✅ Si todo va bien, verás:
```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "libros"
}
```

---

## 7. Indexar Libros de Ejemplo

En **Kibana Dev Tools**, inserta algunos libros de muestra:

```json
POST /libros/_doc/1
{
  "titulo": "Cien años de soledad",
  "autor": "Gabriel García Márquez",
  "categoria": "Novela",
  "fecha": "1967-05-30",
  "descripcion": "Historia épica de la familia Buendía en el pueblo ficticio de Macondo."
}

POST /libros/_doc/2
{
  "titulo": "Don Quijote de la Mancha",
  "autor": "Miguel de Cervantes",
  "categoria": "Clásico",
  "fecha": "1605-01-16",
  "descripcion": "Relato de las aventuras del ingenioso hidalgo Don Quijote y su fiel escudero Sancho Panza."
}

POST /libros/_doc/3
{
  "titulo": "El nombre del viento",
  "autor": "Patrick Rothfuss",
  "categoria": "Fantasía",
  "fecha": "2007-03-27",
  "descripcion": "Primera parte de la saga de Kvothe: un músico y aventurero extraordinario."
}

POST /libros/_doc/4
{
  "titulo": "La sombra del viento",
  "autor": "Carlos Ruiz Zafón",
  "categoria": "Misterio",
  "fecha": "2001-05-14",
  "descripcion": "Thriller ambientado en la Barcelona de posguerra, lleno de libros y secretos."
}
```

Luego, verifica con:
```json
GET /libros/_search
{
  "query": { "match_all": {} }
}
```
Verás tus 4 documentos.

---

## 📝 Detalle del Código Fuente

### 8. Conexión a MongoDB (`connect_mongo()`)

```python
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

mongo_uri = os.environ.get("MONGO_URI")

def connect_mongo():
    if not mongo_uri:
        print("❌ Error: MONGO_URI no está definido.")
        return None

    try:
        client = MongoClient(mongo_uri, server_api=ServerApi("1"))
        client.admin.command("ping")
        print("✅ Conexión exitosa a MongoDB!")
        return client
    except Exception as e:
        print(f"❌ Error al conectar a MongoDB: {e}")
        return None
```

- Lee `MONGO_URI` de las variables de entorno.  
- Intenta un `ping` para verificar la conexión.  
- Retorna el `client` si tuvo éxito, o `None` si falló.

---

### 9. Ruta de Login `/login`

```python
from flask import Flask, render_template, request, redirect, url_for, session

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        client = connect_mongo()
        if not client:
            return render_template('login.html',
                                   error_message='🚫 Error de conexión con la base de datos.',
                                   version=VERSION_APP,
                                   creador=CREATOR_APP)

        try:
            db = client['administracion']
            security_collection = db['seguridad']
            usuario = request.form.get('usuario')
            password = request.form.get('password')

            # Validar credenciales
            user = security_collection.find_one({
                'usuario': usuario,
                'password': password
            })

            if user:
                session['usuario'] = usuario
                return redirect(url_for('gestion_proyecto'))
            else:
                return render_template('login.html',
                                       error_message='❌ Usuario o contraseña incorrectos.',
                                       version=VERSION_APP,
                                       creador=CREATOR_APP)
        except Exception as e:
            return render_template('login.html',
                                   error_message=f'⚠️ Error al validar credenciales: {e}',
                                   version=VERSION_APP,
                                   creador=CREATOR_APP)
        finally:
            client.close()

    return render_template('login.html',
                           version=VERSION_APP,
                           creador=CREATOR_APP)
```

- **Si POST**: intenta conectar a MongoDB Atlas y verifica las credenciales en la colección `seguridad`.  
- **Si GET**: muestra el formulario de login.  
- **Sesión**: guarda `session['usuario']` para proteger rutas.

---

### 10. Plantilla de Login (`templates/login.html`)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Ingresar – BigData-MiProyecto</title>
    <!-- Bootstrap 5 -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      crossorigin="anonymous"
    />
    <!-- CSS propio -->
    <link href="{{ url_for('static', filename='css/landingPage.css') }}" rel="stylesheet" />
</head>
<body>
  <!-- HEADER -->
  <header class="header">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center">
        <h1 class="h3 mb-0">BigData-MiProyecto</h1>
        <nav>
          <ul class="nav">
            <li class="nav-item"><a class="nav-link" href="/">Inicio</a></li>
            <li class="nav-item"><a class="nav-link" href="/about">Acerca de</a></li>
            <li class="nav-item"><a class="nav-link" href="/buscador">Buscador</a></li>
            <li class="nav-item"><a class="nav-link active" href="/login"><b>Ingresar</b></a></li>
            <li class="nav-item"><a class="nav-link" href="/contacto">Contacto</a></li>
          </ul>
        </nav>
      </div>
    </div>
  </header>

  <!-- Cuerpo Principal -->
  <div class="container py-5">
    <div class="login-form mx-auto" style="max-width:400px;">
      <h1 class="text-center mb-4">🔐 Iniciar Sesión</h1>

      {% if error_message %}
      <div class="alert alert-danger" role="alert">
        {{ error_message }}
      </div>
      {% endif %}

      <form method="POST" action="/login" id="loginForm" onsubmit="mostrarCargando()">
        <div class="mb-3">
          <label for="usuario" class="form-label">👤 Usuario</label>
          <input type="text" class="form-control" id="usuario" name="usuario" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">🔒 Contraseña</label>
          <input type="password" class="form-control" id="password" name="password" required>
        </div>
        <div class="d-flex justify-content-between">
          <button type="submit" class="btn btn-primary">Ingresar</button>
          <button type="button" class="btn btn-info" onclick="listarUsuarios()">Listar usuarios</button>
        </div>
      </form>

      <!-- Tabla de Usuarios (inicialmente oculta) -->
      <div id="ListadoUsuarios" class="mt-4" style="display:none;">
        <h3 class="text-center mb-3">📋 Listado de Usuarios</h3>
        <div class="table-responsive">
          <table class="table table-striped table-bordered">
            <thead class="table-dark">
              <tr>
                <th>Usuario</th>
                <th>Password</th>
                <th>Rol</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody id="tablaUsuarios"></tbody>
          </table>
        </div>
      </div>

      <!-- Spinner de carga (oculto) -->
      <div id="div_cargando" class="text-center mt-4" style="display:none;">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
        <p class="mt-2">⏳ Procesando tu solicitud…</p>
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer class="text-center py-3">
    <p class="mb-0">👨‍💻 Creado por {{ creador }}</p>
    <p class="mb-0" id="current-year"></p>
    <p class="mb-0" id="version_app">{{ version }}</p>
  </footer>

  <!-- Scripts -->
  <script
    src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
    crossorigin="anonymous"
  ></script>
  <script>
    // Mostrar año actual en el footer
    document.getElementById("current-year").textContent = new Date().getFullYear();

    // Mostrar spinner mientras se envía el formulario
    function mostrarCargando() {
      document.getElementById("div_cargando").style.display = "block";
      document.querySelector('button[type="submit"]').disabled = true;
    }

    // Llamar a la ruta /listar-usuarios para poblar la tabla
    function listarUsuarios() {
      document.getElementById("div_cargando").style.display = "block";
      fetch("/listar-usuarios")
        .then((res) => res.json())
        .then((data) => {
          const tabla = document.getElementById("tablaUsuarios");
          tabla.innerHTML = "";
          data.forEach((u) => {
            const row = document.createElement("tr");
            row.innerHTML = `
              <td>${u.usuario}</td>
              <td>${u.password}</td>
              <td>${u.rol || "Usuario"}</td>
              <td>${new Date(u.fechaCreacion).toLocaleString()}</td>
            `;
            tabla.appendChild(row);
          });
          document.getElementById("div_cargando").style.display = "none";
          document.getElementById("ListadoUsuarios").style.display = "block";
        })
        .catch((err) => {
          console.error("Error:", err);
          alert("❌ Error al obtener la lista de usuarios");
          document.getElementById("div_cargando").style.display = "none";
        });
    }
  </script>
</body>
</html>
```

---

## 🔄 Corrección de la Ruta `/gestion_proyecto`

```python
@app.route('/gestion_proyecto', methods=['GET', 'POST'])
def gestion_proyecto():
    # 1️⃣ Proteger ruta: sólo usuarios con sesión activa
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # 2️⃣ Intentar conectar a MongoDB
    client = connect_mongo()
    if not client:
        return render_template('gestion/index.html',
                               error_message='🚫 Error al conectar con MongoDB.',
                               version=VERSION_APP,
                               creador=CREATOR_APP,
                               usuario=session['usuario'])

    try:
        # 3️⃣ Listar nombres de bases de datos
        databases = client.list_database_names()

        # 4️⃣ Filtrar bases de sistema
        system_dbs = ['admin', 'local', 'config', 'administracion']
        databases = [db for db in databases if db not in system_dbs]

        # 5️⃣ Obtener base seleccionada (sin typo “=-”)
        selected_db = request.form.get('database') if request.method == 'POST' else request.args.get('database')

        collections_data = []

        if selected_db:
            # 6️⃣ Cambiar contexto a la base elegida
            db = client[selected_db]
            collections = db.list_collection_names()
            for idx, coll_name in enumerate(collections, 1):
                coll = db[coll_name]
                count = coll.count_documents({})
                collections_data.append({
                    'index': idx,
                    'name': coll_name,
                    'count': count
                })

        # 7️⃣ Renderizar plantilla con datos
        return render_template('gestion/index.html',
                               databases=databases,
                               selected_db=selected_db,
                               collections_data=collections_data,
                               version=VERSION_APP,
                               creador=CREATOR_APP,
                               usuario=session['usuario'])
    except Exception as e:
        return render_template('gestion/index.html',
                               error_message=f"⚠️ Error interno: {e}",
                               version=VERSION_APP,
                               creador=CREATOR_APP,
                               usuario=session['usuario'])
    finally:
        client.close()
```

- **IMPORTANTE**: Asegúrate que el **usuario Atlas** (`sebastian`) tenga el rol `readAnyDatabase` (o `readWriteAnyDatabase`) para que `list_database_names()` devuelva resultados.

---

## 🌟 Características Principales

1. **🔒 Autenticación con MongoDB Atlas**  
   - Usuarios y contraseñas almacenadas en la colección `administracion.seguridad`.  
   - El login compara en texto plano (podrías encriptar en próximas versiones).

2. **🗃️ Gestión de Bases y Colecciones**  
   - 📜 Listar todas las bases de datos (excluyendo `admin`, `local`, `config`, `administracion`).  
   - 📂 Al seleccionar una base, muestra sus colecciones con conteo de documentos.  
   - ➕ Botones para **Crear Base de Datos** y **Crear Colección** con carga de archivos ZIP con JSON.

3. **✉️ Formulario de Contacto**  
   - Ruta `/contacto`: permite enviar nombre, email, asunto y mensaje.  
   - Los datos se guardan en `administracion.contactos`.

4. **🔍 Buscador de Libros con Elasticsearch**  
   - Permite buscar por:
     - **Texto libre** (título, autor, descripción).  
     - **Título** (match_phrase).  
     - **Autor** (match).  
     - **Categoría** (term).  
   - Filtros laterales (aggregations) por **Categoría**, **Autor** y **Año** (date_histogram por `fecha`).  
   - Tabla interactiva con DataTables: paginación, ordenamiento y búsqueda en vivo.

5. **📈 Administración de Elasticsearch**  
   - Ruta `/elasticAdmin`: muestra información del índice (`doc_count`, settings).  
   - Subir documentos JSON en lote desde ZIP.  
   - Listar y eliminar documentos desde la UI.

---

## 🔄 Flujo de Trabajo

1. **Inicio** (`/` redirige a `/login`).  
2. **Login** (`/login`):  
   - Usuario/Contraseña → validación contra `administracion.seguridad`.  
   - Si correcto → redirige a `/gestion_proyecto`.  
   - Botón “Listar usuarios” → GET `/listar-usuarios` → JSON con todos los usuarios.  
3. **Gestión de Proyecto** (`/gestion_proyecto`):  
   - Dropdown con bases de MongoDB Atlas.  
   - Al elegir una base y enviar (`POST`), muestra colecciones y conteo de documentos.  
   - Botones:
     - **“Crear base de datos”** → `/crear-base-datos-form`  
     - **“Crear colección”** → `/crear-coleccion-form/<database>`  
4. **Crear Base de Datos** (`/crear-base-datos-form` & `/crear-base-datos`):  
   - Formulario para nombre de base y colección inicial.  
   - Valida caracteres y crea la base con un documento vacío.  
5. **Crear Colección** (`/crear-coleccion-form/<database>` & `/crear-coleccion`):  
   - Permite subir un ZIP con archivos JSON para poblar la colección en lote.  
   - Inserción en batch para mejor rendimiento.  
   - Limpia directorio temporal tras importación.  
6. **Ver Registros** (`/ver-registros/<database>/<collection>`):  
   - Muestra primeros 100 documentos de la colección (con `_id` convertido a string).  
7. **Elasticsearch Admin** (`/elasticAdmin`):  
   - Muestra estadísticas del índice `libros`.  
8. **Añadir Documentos a Elasticsearch** (`/elastic-agregar-documentos`):  
   - Cargar ZIP con JSON para indexar en `libros`.  
   - Reporta conteo exitosos/errores.  
9. **Listar Documentos de Elasticsearch** (`/elastic-listar-documentos`):  
   - Muestra primeros 100 documentos indexados (con `_source`).  
   - Permite eliminar documentos vía POST AJAX (`/elastic-eliminar-documento`).  
10. **Buscador de Libros** (`/buscador`):  
    - Formulario para seleccionar tipo de búsqueda (texto, título, autor, categoría) y rango de fechas.  
    - Muestra resultados en tabla paginada con DataTables.  
    - Filtros laterales con aggregations (categoría, autor, año).  
11. **Logout** (`/logout`):  
    - Limpia sesión y redirige a `/`.

---

## 🛠️ Cómo Probar Localmente

1. ✅ Configura correctamente las variables en `.env`.  
2. ✅ Verifica que el usuario Atlas (`sebastian`) tenga el rol `readAnyDatabase` o `readWriteAnyDatabase`.  
3. ✅ En MongoDB Atlas, crea la colección `administracion.seguridad` y añade al menos un usuario de prueba.  
4. ✅ En Kibana, crea el índice `libros` con mapping y indexa algunos ejemplares.  
5. En tu terminal (venv activo), ejecuta:

   ```bash
   python app.py
   ```
6. Abre tu navegador en:
   ```
   http://127.0.0.1:5000/
   ```
7. **Login** con:
   - Usuario: `juanperez`  
   - Contraseña: `Perez2025!`  
8. Explora:
   - **🔧 Gestión Proyecto**: bases, colecciones, creación.  
   - **🔍 Buscador**: búsqueda de libros en Elasticsearch.  
   - **📊 Elasticsearch Admin**: indexar/listar/eliminar documentos.  
   - **✉️ Contacto**: enviar mensaje y guardarlo en MongoDB.

---

## ✅ Checklist de Verificación

- [ ] Creaste un usuario en MongoDB Atlas (`administracion.seguridad`).  
- [ ] Usuario Atlas tiene permisos `listDatabases`.  
- [ ] Configuraste `.env` con **MONGO_URI**, **ELASTIC_URL**, **ELASTIC_API_KEY**, **SECRET_KEY**.  
- [ ] Ejecutaste `pip install -r requirements.txt` sin errores.  
- [ ] Creaste el índice `libros` en Kibana Dev Tools.  
- [ ] Indexaste documentos de ejemplo en `libros`.  
- [ ] Al correr `python app.py`, no aparece error de conexión a MongoDB ni Elasticsearch.  
- [ ] El dropdown de bases de datos en `/gestion_proyecto` se pobla correctamente.  
- [ ] El login funciona y redirige a la página de gestión.  
- [ ] Formularios de creación de BD/colección crean datos en MongoDB Atlas.  
- [ ] El buscador devuelve los resultados esperados de libros.

---

## 📚 Recursos Adicionales

- **MongoDB Atlas → Quickstart**:  
  https://docs.atlas.mongodb.com/getting-started/  
- **PyMongo Documentation**:  
  https://pymongo.readthedocs.io/  
- **Elasticsearch Python Client**:  
  https://elasticsearch-py.readthedocs.io/  
- **Flask Official Docs**:  
  https://flask.palletsprojects.com/  
- **Bootstrap 5**:  
  https://getbootstrap.com/docs/5.3/getting-started/introduction/  

---

## 🤝 Contribuciones

¡Bienvenido a contribuir! Si encuentras errores, mejoras de estilo o nuevas funcionalidades:

1. Haz **fork** de este repositorio.  
2. Crea una **rama** (`git checkout -b mejora/tu-mejora`).  
3. Realiza tus cambios y haz **commit** (`git commit -m "✔️ Corrige X y añade Y"`).  
4. Sube tu rama (`git push origin mejora/tu-mejora`).  
5. Abre un **Pull Request** detallando tus cambios.

---

## 📝 Licencia

Este proyecto está bajo la licencia **MIT**. Véase el archivo [LICENSE](LICENSE.md) para más detalles.

---

¡Gracias por usar **BigData-MiProyecto**!  
🎉 **Disfruta explorando datos y creando tus propias soluciones de Big Data** 🎉
