# Manual de Usuario: Uso de Acciones de Automatización en el Proyecto

Este manual está diseñado para guiar a los desarrolladores en el uso de las acciones de automatización configuradas en el proyecto.
Aquí se explica qué hacer para añadir funcionalidades al proyecto, gestionar nuevas librerías y activar los workflows correctamente.

---

## 1. Acciones Automatizadas en GitHub Actions

El proyecto cuenta con tres acciones automatizadas para garantizar la calidad, la documentación y el empaquetado del proyecto.
Estas acciones están explicadas más detalladamente en la sección "Acciones explicadas".

### **1.1 Python Package**
- **Propósito**: Instala dependencias, ejecuta análisis de calidad con flake8 y corre los tests.
- **Trigger**: Push a cualquier rama o creación de un Pull Request.

### **1.2 Generate and Publish Documentation**
- **Propósito**: Genera documentación actualizada combinando docstrings del código en `src/` con documentación manual en `docs/`.
- **Trigger**: Push a `main` o de forma manual.

### **1.3 Upload Python Package**
- **Propósito**: Crea un paquete Python y lo sube a Test PyPI con el nombre del release.
- **Trigger**: Publicación de un release en GitHub.

---

## 2. Pipeline de Trabajo para los Desarrolladores

### **Paso 1: Clonar el Repositorio**
1. Clona el repositorio en tu máquina local:

    ```bash
    git clone https://github.com/capo-urjc/python-tools.git
    ```

    Accede al directorio del proyecto:

    ```bash
    cd proyecto
    ```

### **Paso 2: Desarrollar la Funcionalidad**

1. Crea una nueva rama para trabajar en tu funcionalidad:

    ```bash
    git checkout -b feature/nueva-funcionalidad
    ```

2. Realiza las siguientes tareas:
    - **2.1 Incluir tu código**: Añade el código necesario en los archivos correspondientes del proyecto.
    - **2.2 Desarrollar los tests unitarios**: Escribe tests para validar la funcionalidad en la carpeta de tests.
    - **2.3 Documentar el código**: Añade docstrings en formato Google y, si es necesario, actualiza la documentación manual en la carpeta `docs/`. Debes añadir tus archivos en docs/api.md en este formato "::: src.capo_tools.ejemplo"

### **Paso 3: Verificar el Funcionamiento Correcto**

1. Si has añadido nuevas dependencias:
    - Instálalas y agrégalas de forma manual al archivo `pyproject.toml` en la sección [tool.pdm.dev-dependencies]:

      ```bash
      pip install nombre-libreria
      ```
 2. Asegúrate de que el código pasa las acciones:
    - Python package: Lo puedes activar haciendo push a tu rama de desarrollo o a cualquier rama. Revisa el feedback de flake8 para la calidad del código y el feedback de pytest con los tests unitarios. Modificar las restricciones de lint con flake8 si es necesario según tus requisitos, al igual que a la hora de pasar los tests con pypi.
    - Upload python package: Solo lo puedes activar publicando un realease, pero puedes hacer pruebas en tu rama. Revisa que el nombre de versión del tag del realease es correcto con el formato "vX.X.X". Verificar que el paquete se ha construido correctamente con twine. Por último, comprobar que se ha subido correctamente a TestPypi.
    - Generate and publish documentation: Lo puedes activar de forma manual es la pestaña actions de Github, importante activarla en tu rama de desarrollo. Se activa automaticamente cuando se hace push a main. Comprueba en https://capo-urjc.github.io/python-tools/ que se ha subido la documentación correctamente. La documentación del código está en el apartado API. Para ello tiene que estar en docs/api.md vuestros archivos añadidos.




### **Paso 4: Crear el Pull Request**

1. Sube tus cambios a tu rama remota:

    ```bash
    git push origin feature/nueva-funcionalidad
    ```

2. Abre un Pull Request en GitHub contra la rama `main`.

3. Verifica que las acciones automatizadas en GitHub Actions se ejecuten correctamente:
    - La acción **Python Package** debe pasar sin errores.
    - La acción **Generate and Publish Documentation** debe generar la documentación correctamente.

---

## 3. Consideraciones Adicionales

### **Errores en las Acciones**
- Si alguna acción falla, revisa los logs en la pestaña **Actions** de GitHub para identificar el problema.
- Soluciona los errores y haz un nuevo push.

### **Credenciales para Test PyPI**
- Asegúrate de que las credenciales están configuradas en los **secrets** del repositorio si necesitas publicar un paquete.

---

## Resumen del Pipeline con ejemplo

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/capo-urjc/python-tools.git
    cd proyecto
    ```

2. **Desarrollar la funcionalidad**:
    - Crear una rama:

      ```bash
      git checkout -b feature/nueva-funcionalidad
      ```

    - Incluir el código.
    - Añadir tests unitarios.
    - Documentar el código con docstrings y actualizar `docs/` si es necesario.

3. **Verificar el funcionamiento correcto**:
    - Si has añadido nuevas dependencias, instálalas y agrégalas en `pyproject.toml`
    - Asegúrate de que el código pasa las acciones


4. **Crear el Pull Request**:
    - Subir los cambios:

      ```bash
      git push origin feature/nueva-funcionalidad
      ```

    - Abrir un Pull Request en GitHub.

5. **Confirmar que las acciones de GitHub se ejecuten correctamente**:
    - Validar que todas las acciones pasan sin errores.
