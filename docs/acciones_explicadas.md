# Acciones explicadas

Este manual describe el funcionamiento de las tres acciones automatizadas disponibles en este proyecto.
Cada acción está diseñada para facilitar tareas clave como la gestión de dependencias, generación de documentación y despliegue de paquetes.

---

Python package
## 1. **Instalar dependencias, ejecutar linting y tests**

### Descripción
Esta acción instala las dependencias del proyecto, ejecuta análisis de código con `flake8` y realiza los tests definidos en el proyecto.
Se activa en los siguientes casos:
- Cuando se hace un **push** a la rama `main`.
- Cuando se crea un **pull request**.

### Proceso
1. Instala todas las dependencias necesarias definidas en los archivos del proyecto.
2. Ejecuta `flake8` para asegurarse de que el código cumple con las normas de estilo y calidad.
3. Corre los tests definidos, asegurándose de que el proyecto es funcional y no contiene errores.

### Activación
- **Trigger:** Push a `main` o Pull Request.

---

Generate and Publish Documentation
## 2. **Generar documentación automáticamente**

### Descripción
Esta acción genera la documentación del proyecto combinando:
- Los **docstrings** de los archivos ubicados en `src/`.
- Cualquier documentación adicional definida manualmente en los archivos de la carpeta `docs/`.

El resultado es un sitio de documentación actualizado automáticamente.

### Proceso
1. Escanea los archivos en `src/` y procesa los **docstrings**.
2. Incluye la documentación manual definida en `docs/`.
3. Genera un sitio estático que puede ser desplegado para consulta.

### Activación
- **Trigger:** Push a `main`.

---

Upload Python Package
## 3. **Crear y publicar paquete en Test PyPI**

### Descripción
Esta acción automatiza la creación y despliegue de un paquete Python en **Test PyPI**. El paquete incluye la etiqueta asociada al nombre del release publicado.

### Proceso
1. Instala las dependencias necesarias para empaquetar el proyecto.
2. Crea el paquete del proyecto usando herramientas como `setuptools` o `pdm`.
3. Publica el paquete en **Test PyPI** con el nombre y la versión obtenidos del release.

### Activación
- **Trigger:** Publicación de un release.

### Notas
- El nombre del release se utiliza como etiqueta del paquete en Test PyPI.
- Asegúrate de que las credenciales para Test PyPI están configuradas en los **secrets** del repositorio.

---

## Preguntas Frecuentes (FAQ)

### ¿Qué sucede si una acción falla?
Si alguna acción falla, revisa los logs generados en GitHub Actions para identificar el problema. Los errores comunes incluyen:
- Dependencias faltantes.
- Estilo de código incorrecto (flake8).
- Tests fallidos.

### ¿Cómo puedo personalizar estas acciones?
Edita el archivo `workflow.yml` correspondiente en el directorio `.github/workflows/`. Asegúrate de seguir las normas de sintaxis de YAML.

### ¿Dónde puedo ver la documentación generada?
La documentación generada se encuentra en la carpeta `site/`, que puede ser desplegada en GitHub Pages o cualquier servidor estático.

---

¡Gracias por usar estas acciones automatizadas! Si necesitas más ayuda, no dudes en consultar con el equipo o revisar la configuración de los workflows.

