# Aparejador Ninja BIM - Extractor & Presupuestos 🥷🏗️

![Profesión](https://img.shields.io/badge/Profesi%C3%B3n-Arquitectos%20T%C3%A9cnicos-2e7d32?logo=micro%3Abit&logoColor=white&style=flat-square)
![Role](https://img.shields.io/badge/Role-BIM%20%26%20ConTech-007ACC?logo=bim360&style=flat-square)
![Location](https://img.shields.io/badge/Location-A%20Coru%C3%B1a%20%F0%9F%8C%8A-005B94?logo=lighthouse&logoColor=white&style=flat-square)
![Sector](https://img.shields.io/badge/Sector-ConTech%20%7C%20AECO-E65100?logo=construct3&style=flat-square)
![BIM](https://img.shields.io/badge/BIM-IFC%20%2F%20openBIM-009688?style=flat-square)
![Maker](https://img.shields.io/badge/Maker-Software-red?logo=makerbot&style=flat-square)
![Hardware](https://img.shields.io/badge/Hardware---grey?style=flat-square)
![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&style=flat-square)
![Language](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white&style=flat-square)
![Stars](https://img.shields.io/github/stars/jmcaamanog/aparejador-ninja-bim?style=flat-square&color=yellow&logo=github)
![License](https://img.shields.io/github/license/jmcaamanog/aparejador-ninja-bim?style=flat-square&color=green)

(Arquitecto Técnico_JMC) Herramienta de escritorio irreverente y directa al grano para auditar modelos BIM en formato IFC. Diseñada para extraer mediciones rápidas, evaluar el comportamiento térmico básico de la fachada y generar presupuestos estimativos al vuelo

Echa un vistazo a las capturas en la carpeta **CAPTURAS**.

## 🚀 Características Principales

*   **Radiografía BIM Automática:** Extrae y contabiliza elementos constructivos clave (muros, forjados, pilares, ventanas, etc.) sumando sus superficies útiles reales.
*   **Índice de "Ruina Térmica":** Calcula automáticamente el ratio de huecos (superficie de ventanas frente a muros) para advertir sobre posibles problemas de climatización.
*   **Generador GLB y Visor 3D:** Aísla las entidades `IfcSpace` (estancias), extrae su geometría tridimensional y las exporta a un archivo `.glb` universal, permitiendo además su visualización instantánea mediante Trimesh.
*   **Presupuestador al Vuelo ("La Dolorosa"):** A partir de un coste de construcción estimado (€/m²) y un porcentaje de honorarios, reparte el peso económico por partidas y exporta un archivo CSV listo para abrir en Excel.
*   **Consola de Log Integrada:** Registro de operaciones en tiempo real con mensajes directos e informativos sobre el estado del procesamiento.

## 🛠️ Stack Tecnológico

*   **Tkinter:** Interfaz gráfica nativa con sistema de pestañas (Calculadora y Visor).
*   **IfcOpenShell:** Motor pesado para la lectura de datos, propiedades paramétricas y parseo geométrico del archivo IFC.
*   **Trimesh & NetworkX:** Librerías matemáticas encargadas de agrupar vértices y caras para la reconstrucción, renderizado 3D y exportación de la malla a formato GLB.

## ⚙️ Instalación y Uso

1. Clona este repositorio en tu equipo:
   ```bash
   git clone [https://github.com/jmcaamanog/aparejador-ninja-bim.git](https://github.com/TU_USUARIO/aparejador-ninja-bim.git)
2. Instala las dependencias necesarias. Es crítico instalar una versión específica de pyglet para asegurar la compatibilidad del visor 3D:
   ```bash
   pip install ifcopenshell trimesh "pyglet<2" networkx
3. Ejecuta la aplicación:
   ```bash
   python nombre_del_archivo.py
## 📦 Compilar a Ejecutable (.exe) para Windows

Si quieres distribuir la aplicación sin que los usuarios tengan que lidiar con Python o la terminal, puedes empaquetar el código en un único ejecutable.

1. Instala PyInstaller en tu entorno:

   ```bash
   pip install pyinstaller
2. Sitúate en la carpeta del proyecto donde están el script y el archivo app_icon.ico, y ejecuta::

   ```bash
   pyinstaller --noconsole --onefile --icon=app_icon.ico MEDICIONES-IFC_PARA_ARQUITECTOS_TECNICOS.py
El archivo `.exe` final se generará automáticamente dentro de la carpeta dist. Ya estará listo para compartir y hacer doble clic.

Debido al limite de almacenanmiento de GITHUB no puedo subir el ejecutable, pero siguiendo las instrucciones, lo teneis en unos min. XD

## 👨‍💻 Autor

Jose Manuel Caamaño González | Arquitecto Técnico & BIM Manager.
Digital Product Lead | ConTech & Digital Twin SaaS | BIM, Energy Modeling & Sustainability | Data Analytics (SQL, Power BI)

Hecho con código y café desde A Coruña. ☕

Jose Manuel Caamaño González | [LinkedIn](https://www.linkedin.com/in/jmcaamanog/)
