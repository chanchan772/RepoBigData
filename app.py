from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from pymongo.errors import PyMongoError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import zipfile
import os
import shutil
from datetime import datetime
import json
import re
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.secret_key = 'Sebas2025/*'  # Puedes cambiar esto por una clave secreta más segura

# Agregar la función now al contexto de la plantilla
@app.context_processor
def inject_now():
    return {'now': datetime.now}

# Versión de la aplicación
VERSION_APP = "Versión 1 de 2025"
CREATOR_APP = "Sebastian Mateus Villegas"

# Obtener MONGO_URI desde variable de entorno; si no existe, usar valor por defecto.
# IMPORTANTE: reemplaza "<your-cluster-host>" con el host real de tu clúster Atlas.
mongo_uri = os.environ.get("MONGO_URI")
if not mongo_uri:
    mongo_uri = "mongodb+srv://sebastian:Sebas2025@bigdata.fcwb2ux.mongodb.net/?retryWrites=true&w=majority&appName=BigData"

# Función para conectar a MongoDB
def connect_mongo():
    try:
        client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("Conexión exitosa a MongoDB Atlas!")
        return client
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        return None

# Configuración de Elasticsearch
# (Reemplaza "<your-elastic-url>" y "<your-elastic-api-key>" con tus valores reales)
ELASTIC_URL = os.environ.get("ELASTIC_URL", "https://my-elasticsearch-project-f86acf.es.us-east-1.aws.elastic.cloud:443")
ELASTIC_API_KEY = os.environ.get("ELASTIC_API_KEY", "NWN1VVFaY0I2cjBzUkx3RWRWV2Q6OGNXdnlvbURxdElXa0ljcGpRakJydw==")

client_es = Elasticsearch(
    ELASTIC_URL,
    api_key=ELASTIC_API_KEY
)
INDEX_NAME = "libros-deployment"


@app.route('/')
def index():
    return render_template('index.html', version=VERSION_APP, creador=CREATOR_APP)


@app.route('/about')
def about():
    return render_template('about.html', version=VERSION_APP, creador=CREATOR_APP)


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')

        client = connect_mongo()
        if client:
            db = client['administracion']
            contactos_collection = db['contactos']
            contactos_collection.insert_one({
                'nombre': nombre,
                'email': email,
                'asunto': asunto,
                'mensaje': mensaje,
                'fecha': datetime.now()
            })
            client.close()

        return redirect(url_for('contacto'))

    return render_template('contacto.html', version=VERSION_APP, creador=CREATOR_APP)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        client = connect_mongo()
        if not client:
            return render_template(
                'login.html',
                error_message='Error de conexión con la base de datos. Por favor, intente más tarde.',
                version=VERSION_APP,
                creador=CREATOR_APP
            )

        try:
            db = client['administracion']
            security_collection = db['seguridad']
            usuario = request.form['usuario']
            password = request.form['password']

            user = security_collection.find_one({
                'usuario': usuario,
                'password': password
            })

            if user:
                session['usuario'] = usuario
                return redirect(url_for('gestion_proyecto'))
            else:
                return render_template(
                    'login.html',
                    error_message='Usuario o contraseña incorrectos',
                    version=VERSION_APP,
                    creador=CREATOR_APP
                )

        except Exception as e:
            return render_template(
                'login.html',
                error_message=f'Error al validar credenciales: {str(e)}',
                version=VERSION_APP,
                creador=CREATOR_APP
            )
        finally:
            client.close()

    return render_template('login.html', version=VERSION_APP, creador=CREATOR_APP)


@app.route('/listar-usuarios')
def listar_usuarios():
    try:
        client = connect_mongo()
        if not client:
            return jsonify({'error': 'Error de conexión con la base de datos'}), 500

        db = client['administracion']
        security_collection = db['seguridad']
        usuarios = list(security_collection.find({}, {'password': 0}))

        for usr in usuarios:
            usr['_id'] = str(usr['_id'])

        return jsonify(usuarios)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if 'client' in locals():
            client.close()


@app.route('/gestion_proyecto', methods=['GET', 'POST'])
def gestion_proyecto():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    client = connect_mongo()
    if not client:
        # Si la conexión a MongoDB falló, devolvemos un template con el error
        return render_template('gestion/index.html',
                            error_message='Error al conectar con MongoDB. Por favor, verifica tus credenciales.',
                            version=VERSION_APP,
                            creador=CREATOR_APP,
                            usuario=session['usuario'])

    try:
        # 1) Listamos todas las bases de datos
        databases = client.list_database_names()

        # 2) Quitamos las bases de sistema que no queremos mostrar
        system_dbs = ['admin', 'local', 'config', 'administracion']
        databases = [db for db in databases if db not in system_dbs]

        # 3) Obtenemos el valor de selected_db sin el typo “=-”
        if request.method == 'POST':
            selected_db = request.form.get('database')
        else:
            selected_db = request.args.get('database')

        collections_data = []

        # 4) Si el usuario ya escogió una base de datos
        if selected_db:
            # Cambiamos al contexto de esa base
            db = client[selected_db]
            # Listamos las colecciones
            collections = db.list_collection_names()
            for idx, coll_name in enumerate(collections, 1):
                coll = db[coll_name]
                count = coll.count_documents({})
                collections_data.append({
                    'index': idx,
                    'name': coll_name,
                    'count': count
                })

        # 5) Renderizamos la plantilla, pasándole las bases encontradas y el selected_db
        return render_template('gestion/index.html',
                            databases=databases,
                            selected_db=selected_db,
                            collections_data=collections_data,
                            version=VERSION_APP,
                            creador=CREATOR_APP,
                            usuario=session['usuario'])
    except Exception as e:  
        # Cualquier otro error al listar bases o colecciones
        return render_template('gestion/index.html',
                            error_message=f'Error interno: {str(e)}',
                            version=VERSION_APP,
                            creador=CREATOR_APP,
                            usuario=session['usuario'])
    finally:
        client.close()



@app.route('/crear-coleccion-form/<database>')
def crear_coleccion_form(database):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template(
        'gestion/crear_coleccion.html',
        database=database,
        usuario=session['usuario'],
        version=VERSION_APP,
        creador=CREATOR_APP
    )


@app.route('/crear-coleccion', methods=['POST'])
def crear_coleccion():
    if 'usuario' not in session:
        flash('Debes iniciar sesión para crear colecciones.', 'warning')
        return redirect(url_for('login'))

    client_mongo = None
    temp_dir = None

    try:
        database = request.form.get('database')
        collection_name = request.form.get('collection_name')
        zip_file = request.files.get('zip_file')

        if not all([database, collection_name, zip_file]):
            flash('Todos los campos (Base de datos, Nombre de colección, Archivo ZIP) son requeridos.', 'error')
            return render_template(
                'gestion/crear_coleccion.html',
                database=database,
                usuario=session['usuario'],
                version=VERSION_APP,
                creador=CREATOR_APP
            )

        client_mongo = connect_mongo()
        if not client_mongo:
            flash('Error de conexión con MongoDB. No se pudo crear la colección.', 'error')
            return render_template(
                'gestion/crear_coleccion.html',
                database=database,
                usuario=session['usuario'],
                version=VERSION_APP,
                creador=CREATOR_APP
            )

        db = client_mongo[database]
        collection = db[collection_name]

        # Crear directorio temporal único
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp_uploads', str(datetime.now().timestamp()))
        os.makedirs(temp_dir, exist_ok=True)

        zip_path = os.path.join(temp_dir, zip_file.filename)
        zip_file.save(zip_path)

        inserted_count = 0

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_in_zip in zip_ref.namelist():
                if file_in_zip.endswith('.json') and not file_in_zip.endswith('/'):
                    try:
                        with zip_ref.open(file_in_zip) as f:
                            json_data = json.load(f)
                            if isinstance(json_data, list):
                                batch_size = 1000
                                batch = []
                                for doc in json_data:
                                    batch.append(doc)
                                    if len(batch) >= batch_size:
                                        collection.insert_many(batch)
                                        inserted_count += len(batch)
                                        batch = []
                                if batch:
                                    collection.insert_many(batch)
                                    inserted_count += len(batch)
                            else:
                                collection.insert_one(json_data)
                                inserted_count += 1

                    except json.JSONDecodeError:
                        print(f"Error: JSON inválido en {file_in_zip}")
                        flash(f'Advertencia: "{file_in_zip}" no es un JSON válido y fue ignorado.', 'warning')
                    except Exception as e:
                        print(f"Error al procesar {file_in_zip}: {str(e)}")
                        flash(f'Advertencia: Error con "{file_in_zip}": {str(e)}.', 'warning')

        flash(
            f'Colección "{collection_name}" creada y {inserted_count} documentos insertados en "{database}".',
            'success'
        )
        return redirect(url_for('gestion_proyecto', database=database))

    except PyMongoError as e:
        flash(f'Error de base de datos al crear la colección: {str(e)}', 'error')
        print(f"Error de PyMongo en crear_coleccion: {e}")
        return render_template(
            'gestion/crear_coleccion.html',
            database=database,
            usuario=session['usuario'],
            version=VERSION_APP,
            creador=CREATOR_APP
        )

    except Exception as e:
        flash(f'Error inesperado al crear la colección: {str(e)}', 'error')
        print(f"Error inesperado en crear_coleccion: {e}")
        return render_template(
            'gestion/crear_coleccion.html',
            database=database,
            usuario=session['usuario'],
            version=VERSION_APP,
            creador=CREATOR_APP
        )

    finally:
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print(f"Directorio temporal '{temp_dir}' limpiado.")
            except Exception as e:
                print(f"Error al limpiar '{temp_dir}': {str(e)}")
        if client_mongo:
            client_mongo.close()
            print("Conexión a MongoDB cerrada.")


@app.route('/ver-registros/<database>/<collection>')
def ver_registros(database, collection):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    try:
        client = connect_mongo()
        if not client:
            return render_template(
                'gestion/index.html',
                error_message='Error de conexión con MongoDB',
                version=VERSION_APP,
                creador=CREATOR_APP,
                usuario=session.get('usuario')
            )

        db = client[database]
        coll = db[collection]
        records = list(coll.find().limit(100))
        for rec in records:
            rec['_id'] = str(rec['_id'])

        return render_template(
            'gestion/ver_registros.html',
            database=database,
            collection_name=collection,
            records=records,
            version=VERSION_APP,
            creador=CREATOR_APP,
            usuario=session['usuario']
        )

    except Exception as e:
        return render_template(
            'gestion/index.html',
            error_message=f'Error al obtener registros: {str(e)}',
            version=VERSION_APP,
            creador=CREATOR_APP,
            usuario=session.get('usuario')
        )

    finally:
        if 'client' in locals():
            client.close()


@app.route('/obtener-registros', methods=['POST'])
def obtener_registros():
    if 'usuario' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    try:
        database = request.form.get('database')
        collection = request.form.get('collection')
        limit = int(request.form.get('limit', 100))

        client = connect_mongo()
        if not client:
            return jsonify({'error': 'Error de conexión con MongoDB'}), 500

        db = client[database]
        coll = db[collection]
        records = list(coll.find().limit(limit))
        for rec in records:
            rec['_id'] = str(rec['_id'])

        return jsonify({'records': records})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if 'client' in locals():
            client.close()


@app.route('/crear-base-datos-form')
def crear_base_datos_form():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template(
        'gestion/crear_base_datos.html',
        version=VERSION_APP,
        creador=CREATOR_APP,
        usuario=session['usuario']
    )


@app.route('/crear-base-datos', methods=['POST'])
def crear_base_datos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    try:
        database_name = request.form.get('database_name')
        collection_name = request.form.get('collection_name')

        valid_pattern = re.compile(r'^[a-zA-Z0-9_]+$')
        if not valid_pattern.match(database_name) or not valid_pattern.match(collection_name):
            return render_template(
                'gestion/crear_base_datos.html',
                error_message='Los nombres no pueden contener caracteres especiales',
                version=VERSION_APP,
                creador=CREATOR_APP,
                usuario=session['usuario']
            )

        client = connect_mongo()
        if not client:
            return render_template(
                'gestion/crear_base_datos.html',
                error_message='Error de conexión con MongoDB',
                version=VERSION_APP,
                creador=CREATOR_APP,
                usuario=session['usuario']
            )

        db = client[database_name]
        coll = db[collection_name]
        coll.insert_one({})    # Crea la colección al insertar
        coll.delete_one({})    # Elimina el documento vacío

        return redirect(url_for('gestion_proyecto', database=database_name))

    except Exception as e:
        return render_template(
            'gestion/crear_base_datos.html',
            error_message=f'Error al crear la base de datos: {str(e)}',
            version=VERSION_APP,
            creador=CREATOR_APP,
            usuario=session.get('usuario')
        )

    finally:
        if 'client' in locals():
            client.close()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/elasticAdmin')
def elasticAdmin():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    try:
        index_info = client_es.indices.get(index=INDEX_NAME)
        doc_count = client_es.count(index=INDEX_NAME)['count']

        return render_template(
            'gestion/ver_elasticAdmin.html',
            index_name=INDEX_NAME,
            doc_count=doc_count,
            version=VERSION_APP,
            creador=CREATOR_APP,
            usuario=session['usuario']
        )

    except Exception as e:
        return render_template(
            'gestion/ver_elasticAdmin.html',
            error_message=f'Error al conectar con Elasticsearch: {str(e)}',
            version=VERSION_APP,
            creador=CREATOR_APP,
            usuario=session.get('usuario')
        )


@app.route('/elastic-agregar-documentos', methods=['GET', 'POST'])
def elastic_agregar_documentos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            if 'zipFile' not in request.files:
                return render_template(
                    'gestion/elastic_agregar_documentos.html',
                    error_message='No se ha seleccionado ningún archivo',
                    index_name=INDEX_NAME,
                    version=VERSION_APP,
                    creador=CREATOR_APP,
                    usuario=session['usuario']
                )

            zip_file = request.files['zipFile']
            if zip_file.filename == '':
                return render_template(
                    'gestion/elastic_agregar_documentos.html',
                    error_message='No se ha seleccionado ningún archivo',
                    index_name=INDEX_NAME,
                    version=VERSION_APP,
                    creador=CREATOR_APP,
                    usuario=session['usuario']
                )

            temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
            os.makedirs(temp_dir, exist_ok=True)

            zip_path = os.path.join(temp_dir, zip_file.filename)
            zip_file.save(zip_path)

            with zipfile.ZipFile(zip_path) as zip_ref:
                zip_ref.extractall(temp_dir)

            success_count = 0
            error_count = 0

            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                json_data = json.load(f)
                                if isinstance(json_data, list):
                                    for doc in json_data:
                                        client_es.index(index=INDEX_NAME, document=doc)
                                        success_count += 1
                                else:
                                    client_es.index(index=INDEX_NAME, document=json_data)
                                    success_count += 1
                        except Exception as e:
                            error_count += 1
                            print(f"Error procesando {file}: {str(e)}")

            # Limpiar temporales
            for root, dirs, files in os.walk(temp_dir, topdown=False):
                for f in files:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(temp_dir)

            return render_template(
                'gestion/elastic_agregar_documentos.html',
                success_message=f'Se indexaron {success_count} documentos exitosamente. Errores: {error_count}',
                index_name=INDEX_NAME,
                version=VERSION_APP,
                creador=CREATOR_APP,
                usuario=session['usuario']
            )

        except Exception as e:
            return render_template(
                'gestion/elastic_agregar_documentos.html',
                error_message=f'Error al procesar el archivo: {str(e)}',
                index_name=INDEX_NAME,
                version=VERSION_APP,
                creador=CREATOR_APP,
                usuario=session.get('usuario')
            )

    return render_template(
        'gestion/elastic_agregar_documentos.html',
        index_name=INDEX_NAME,
        version=VERSION_APP,
        creador=CREATOR_APP,
        usuario=session.get('usuario')
    )


@app.route('/elastic-listar-documentos')
def elastic_listar_documentos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    try:
        response = client_es.search(
            index=INDEX_NAME,
            body={
                "query": {"match_all": {}},
                "size": 100
            }
        )
        documents = response['hits']['hits']

        return render_template(
            'gestion/elastic_listar_documentos.html',
            index_name=INDEX_NAME,
            documents=documents,
            version=VERSION_APP,
            creador=CREATOR_APP,
            usuario=session['usuario']
        )
    except Exception as e:
        return render_template(
            'gestion/elastic_listar_documentos.html',
            error_message=f'Error al obtener documentos: {str(e)}',
            index_name=INDEX_NAME,
            version=VERSION_APP,
            creador=CREATOR_APP,
            usuario=session.get('usuario')
        )


@app.route('/elastic-eliminar-documento', methods=['POST'])
def elastic_eliminar_documento():
    if 'usuario' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    try:
        doc_id = request.form.get('doc_id')
        if not doc_id:
            return jsonify({'error': 'ID de documento no proporcionado'}), 400

        response = client_es.delete(index=INDEX_NAME, id=doc_id)
        if response.get('result') == 'deleted':
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Error al eliminar el documento'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/buscador', methods=['GET', 'POST'])
def buscador():
    if request.method == 'POST':
        try:
            search_type = request.form.get('search_type')
            search_text = request.form.get('search_text')
            fecha_desde = request.form.get('fecha_desde')
            fecha_hasta = request.form.get('fecha_hasta')

            if not fecha_desde:
                fecha_desde = "1500-01-01"
            if not fecha_hasta:
                fecha_hasta = datetime.now().strftime("%Y-%m-%d")

            query = {
                "query": {
                    "bool": {
                        "must": []
                    }
                },
                "aggs": {
                    "categoria": {
                        "terms": {
                            "field": "categoria",
                            "size": 10,
                            "order": {"_key": "asc"}
                        }
                    },
                    "clasificacion": {
                        "terms": {
                            "field": "clasificacion",
                            "size": 10,
                            "order": {"_key": "asc"}
                        }
                    },
                    "Fecha": {
                        "date_histogram": {
                            "field": "fecha",
                            "calendar_interval": "year",
                            "format": "yyyy"
                        }
                    }
                }
            }

            if search_type == 'texto':
                query["query"]["bool"]["must"].append({
                    "match_phrase": {
                        "texto": {
                            "query": search_text,
                            "slop": 1
                        }
                    }
                })
            else:
                search_text = '*' + search_text + '*'
                query["query"]["bool"]["must"].append({
                    "match": {search_type: search_text}
                })

            range_query = {
                "range": {
                    "fecha": {
                        "format": "yyyy-MM-dd",
                        "gte": fecha_desde,
                        "lte": fecha_hasta
                    }
                }
            }
            query["query"]["bool"]["must"].append(range_query)

            response = client_es.search(index=INDEX_NAME, body=query)
            hits = response['hits']['hits']
            aggregations = response.get('aggregations', {})

            return render_template(
                'buscador.html',
                version=VERSION_APP,
                creador=CREATOR_APP,
                hits=hits,
                aggregations=aggregations,
                search_type=search_type,
                search_text=search_text,
                fecha_desde=fecha_desde,
                fecha_hasta=fecha_hasta,
                query=query
            )

        except Exception as e:
            return render_template(
                'buscador.html',
                version=VERSION_APP,
                creador=CREATOR_APP,
                error_message=f'Error en la búsqueda: {str(e)}'
            )

    return render_template('buscador.html', version=VERSION_APP, creador=CREATOR_APP)


@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        index_name = data.get('index', INDEX_NAME)
        query = data.get('query')

        response = client_es.search(index=index_name, body=query)
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
