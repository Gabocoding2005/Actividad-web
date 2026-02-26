# Finance & Habits Tracker - Alpha Version

Aplicación web simple para rastrear finanzas y hábitos diarios.

## 🚀 Tecnologías

- **Backend**: Python 3.x + Flask + SQLAlchemy ORM
- **Frontend**: HTML5 + JavaScript (Vanilla)
- **Base de Datos**: MySQL con SQLAlchemy
- **ORM**: SQLAlchemy 2.0 para manejo de base de datos
- **Conector**: PyMySQL para conexión a MySQL

## 📁 Estructura del Proyecto

```
Actividad Web/
├── backend/
│   ├── app.py          # Servidor Flask con API REST
│   ├── requirements.txt # Dependencias de Python
│   ├── .env            # Variables de entorno (MySQL credentials)
│   └── .env.example    # Plantilla de configuración
├── frontend/
│   ├── index.html      # Interfaz de usuario
│   └── app.js          # Lógica del frontend
└── README.md
```

## 🔧 Instalación y Ejecución

### Prerequisitos

1. **MySQL instalado y corriendo**
2. **Crear base de datos**:
```sql
CREATE DATABASE tracker_db;
```

### Backend

1. Navegar a la carpeta backend:
```bash
cd backend
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno** (Opción 1 - Recomendado):

Crear archivo `.env` en la carpeta backend:
```bash
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tracker_db
```

**O configurar variables de entorno** (Opción 2):
```bash
# Windows PowerShell
$env:DB_USER="root"
$env:DB_PASSWORD="tu_password"
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_NAME="tracker_db"

# Linux/Mac
export DB_USER=root
export DB_PASSWORD=tu_password
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=tracker_db
```

4. Ejecutar el servidor:
```bash
python app.py
```

El servidor estará disponible en `http://localhost:5000`

### Frontend

Abrir el archivo `frontend/index.html` en un navegador web.

## 📋 Funcionalidades

### Backend (API REST)
- **POST /api/transaction** - Registrar transacción financiera (ingreso/gasto)
- **POST /api/habit** - Registrar hábito completado
- **GET /api/summary** - Obtener resumen de finanzas y hábitos

### Frontend
- Formulario para agregar transacciones
- Formulario para registrar hábitos
- Visualización de resumen en tiempo real
- Lista de transacciones y hábitos recientes

## 💾 Base de Datos

La base de datos **MySQL** se gestiona con **SQLAlchemy ORM**. Las tablas se crean automáticamente al iniciar el servidor.

### Modelos SQLAlchemy:

**Transaction (Transacciones)**
- `id`: Integer (Primary Key)
- `type`: String(50) - 'income' o 'expense'
- `description`: String(200) - Descripción de la transacción
- `amount`: Float - Monto
- `date`: DateTime - Fecha y hora

**Habit (Hábitos)**
- `id`: Integer (Primary Key)
- `name`: String(200) - Nombre del hábito
- `date`: DateTime - Fecha y hora de registro

### Ventajas de SQLAlchemy + MySQL:
- ✅ ORM completo con modelos Python
- ✅ Manejo automático de sesiones
- ✅ Queries type-safe y más legibles
- ✅ Manejo de errores con rollback automático
- ✅ MySQL para producción con mejor rendimiento
- ✅ Soporte para múltiples usuarios concurrentes
- ✅ Pool de conexiones con `pool_pre_ping`

### Configuración de Conexión:
La aplicación usa variables de entorno para la configuración de MySQL:
- `DB_USER` - Usuario de MySQL (default: root)
- `DB_PASSWORD` - Contraseña de MySQL (default: vacío)
- `DB_HOST` - Host de MySQL (default: localhost)
- `DB_PORT` - Puerto de MySQL (default: 3306)
- `DB_NAME` - Nombre de la base de datos (default: tracker_db)

Los datos persisten en MySQL entre reinicios del servidor.

## 📝 Notas

- Versión alpha básica sin estilos CSS
- Sin autenticación de usuarios
- CORS configurado manualmente
- Interfaz minimalista funcional

## 🔮 Futuras Mejoras

- Autenticación de usuarios
- Interfaz visual mejorada
- Gráficos y estadísticas
- Filtros por fecha
- Categorías para transacciones
- Seguimiento de racha de hábitos
