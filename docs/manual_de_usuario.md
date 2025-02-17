# Manual de usuario: Como colaborar en el proyecto

Este manual está diseñado para guiar a los colaboradores en el flujo de trabajo del proyecto.
Aquí se explica qué hacer para añadir funcionalidades al proyecto, gestionar nuevas librerías y activar los workflows correctamente.

---
## Resumen del Pipeline con ejemplo

1. **Clonar el repositorio y preparar el proyecto**:
    ```bash
    git clone https://github.com/capo-urjc/python-tools.git
    ```
    ```bash
    cd python-tools
   ```
   ```bash
    python -m venv venv
   ```
   ```bash
    source venv/bin/activate  # En Linux/macOS
   ```
   ```bash
    venv\Scripts\activate    # En Windows
   ```
   ```bash
    pip install pdm
   ```
   ```bash
    pdm install
    ```

3. **Desarrollar la funcionalidad**:
    - Crear una rama:

      ```bash
      git checkout -b feature/nueva-funcionalidad
      ```

    - Incluir el código.
    - Añadir tests unitarios.
    - Documentar el código con docstrings y actualizar `docs/` si es necesario.

4. **Verificar el funcionamiento correcto**:
    ```bash
    pdm add <dependencia>
    ```
    ```bash
    pdm run pytest
    ```
    ```bash
    mkdocs build
    ```

6. **Crear el Pull Request**:
    - Subir los cambios:

      ```bash
      git push origin feature/nueva-funcionalidad
      ```

    - Abrir un Pull Request en GitHub.

7. **Confirmar que las acciones de GitHub se ejecuten correctamente**:
    - Validar que todas las acciones pasan sin errores.
  
---

## Pipeline de trabajo para los colaboradores

### **Paso 1: Clonar el repositorio y preparar el proyecto**
1. Clonar el repositorio
    ```bash
    git clone https://github.com/capo-urjc/python-tools.git
    ```
    ```bash
    cd python-tools
    ```

2. Crear un entorno virtual Python
    Usando virtualenv:
    ```bash
    python -m venv venv
    ```
    ```bash
    source venv/bin/activate  # En Linux/macOS
    ```
    ```bash
    venv\Scripts\activate    # En Windows
    ```

    Usando Conda:
    ```bash
    conda create --name <nombre_del_entorno> python=3.10 -y
    ```
    ```bash
    conda activate <nombre_del_entorno>
    ```

3. Instalar PDM
    ```bash
    pip install pdm
    ```

4. Instalar las dependencias del proyecto
    ```bash
    pdm install
    ```

### **Paso 2: Desarrollar la funcionalidad**

1. Crea una nueva rama para trabajar en tu funcionalidad:

    ```bash
    git checkout -b feature/nueva-funcionalidad
    ```

2. Realiza las siguientes tareas:
    - **2.1 Incluir tu código**: Todo el código debe añadirse dentro del directorio `src/capo_tools`. Es importante organizar bien los archivos y módulos para mantener la estructura del proyecto clara y mantenible. Buenas prácticas:
          **Organiza bien el código**: Ubica cada archivo en la carpeta adecuada según su funcionalidad.
          **Sigue las convenciones del proyecto**: Respeta los estándares definidos en el repositorio.
          **Consulta en caso de duda**: Si no estás seguro de dónde colocar el código, pregunta a los administradores del proyecto antes de proceder.
    - **2.2 Desarrollar los tests unitarios**: Escribe tests para validar la funcionalidad en la carpeta de tests.
    - **2.3 Documentar el código**: Añade docstrings en formato Google y, si es necesario, actualiza la documentación manual en la carpeta `docs/`. Debes añadir tus archivos en docs/api.md en este formato "::: src.capo_tools.ejemplo"

### **Paso 3: Verificar el funcionamiento correcto**

1. Dependencias:
    Las dependencias se gestionan con `pdm` y se añaden de la siguiente manera:
    
    - Para añadir una dependencia general:
      ```bash
      pdm add <dependencia>
      ```
      Esto actualizará automáticamente el archivo `pyproject.toml`.
    
    - Para añadir una dependencia solo para desarrollo:
      ```bash
      pdm add --dev <dependencia>
      ```

    Es importante asegurarse de que las dependencias se añaden correctamente y en la categoría adecuada. Si no estás seguro, consulta con los administradores del proyecto.

      
      
2. Comprobaciones:
    **Tests**
        Los tests se ejecutan con:
        ```bash
        pdm run pytest
        ```
        Desde la carpeta `tests/` o mediante una herramienta de desarrollo como PyCharm. Se debe verificar que todas las pruebas pasan y corregir cualquier error detectado.

    **Documentación**
        La documentación se compila y se prueba de la siguiente manera:

        - Para compilar la documentación:
   
          ```bash
          mkdocs build
          ```
   
        - Para visualizarla localmente:
   
          ```bash
          mkdocs serve
          ```
       Luego, accede a la página web que arranca para verificar que todo está correcto. Si hay errores, corrígelos antes de continuar.

    Siguiendo estos pasos y recomendaciones, ayudarás a mantener un código limpio y ordenado dentro del proyecto.

### **Paso 4: Crear el Pull Request**

1. Sube tus cambios a tu rama remota:

    ```bash
    git push origin feature/nueva-funcionalidad
    ```

2. Abre un Pull Request en GitHub contra la rama `main`.

3. Verifica que las acciones automatizadas en GitHub Actions se ejecuten correctamente:
    - La acción **Python Package** debe pasar sin errores.
    - La acción **Generate and Publish Documentation** debe generar la documentación correctamente.
   Si alguna de las acciones da error, hay que detectar que problema hay, corregir y subir un nuevo commit a la misma rama.

---

## Consideraciones adicionales

### **Errores en las acciones**
- Si alguna acción falla, revisa los logs en la pestaña **Actions** de GitHub para identificar el problema.
- Soluciona los errores y haz un nuevo push.




