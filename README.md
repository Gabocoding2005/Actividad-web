# Finance & Habits Tracker - Alpha Version

Aplicación web simple para rastrear finanzas y hábitos diarios.

## 🚀 Tecnologías

- **Backend**: Python 3.x + Flask
- **Frontend**: HTML5 + JavaScript (Vanilla)
- **Base de Datos**: SQLite3
- **Sin librerías externas**: Solo Flask

## 📁 Estructura del Proyecto

```
Actividad Web/
├── backend/
│   ├── app.py          # Servidor Flask con API REST
│   ├── requirements.txt # Dependencias de Python
│   └── tracker.db      # Base de datos SQLite (se crea automáticamente)
├── frontend/
│   ├── index.html      # Interfaz de usuario
│   └── app.js          # Lógica del frontend
└── README.md
```

## 🔧 Instalación y Ejecución

### Backend

1. Navegar a la carpeta backend:
```bash
cd backend
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar el servidor:
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

La base de datos SQLite se crea automáticamente al iniciar el servidor con dos tablas:

- **transactions**: id, type, description, amount, date
- **habits**: id, name, date

Los datos persisten entre reinicios del servidor.

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
