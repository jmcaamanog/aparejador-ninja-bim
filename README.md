# Aparejador Ninja BIM - Extractor & Presupuestos 🥷🏗️

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-lightgrey.svg)
![IfcOpenShell](https://img.shields.io/badge/BIM-IfcOpenShell-success.svg)
![Trimesh](https://img.shields.io/badge/3D-Trimesh-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

(Arquitecto Técnico_JMC) Herramienta de escritorio irreverente y directa al grano para auditar modelos BIM en formato IFC. Diseñada para extraer mediciones rápidas, evaluar el comportamiento térmico básico de la fachada y generar presupuestos estimativos al vuelo[cite: 9].

## 🚀 Características Principales

*   **Radiografía BIM Automática:** Extrae y contabiliza elementos constructivos clave (muros, forjados, pilares, ventanas, etc.) sumando sus superficies útiles reales[cite: 9].
*   **Índice de "Ruina Térmica":** Calcula automáticamente el ratio de huecos (superficie de ventanas frente a muros) para advertir sobre posibles problemas de climatización[cite: 9].
*   **Generador GLB y Visor 3D:** Aísla las entidades `IfcSpace` (estancias), extrae su geometría tridimensional y las exporta a un archivo `.glb` universal, permitiendo además su visualización instantánea mediante Trimesh[cite: 9].
*   **Presupuestador al Vuelo ("La Dolorosa"):** A partir de un coste de construcción estimado (€/m²) y un porcentaje de honorarios, reparte el peso económico por partidas y exporta un archivo CSV listo para abrir en Excel[cite: 9].
*   **Consola de Log Integrada:** Registro de operaciones en tiempo real con mensajes directos e informativos sobre el estado del procesamiento[cite: 9].

## 🛠️ Stack Tecnológico

*   **Tkinter:** Interfaz gráfica nativa con sistema de pestañas (Calculadora y Visor)[cite: 9].
*   **IfcOpenShell:** Motor pesado para la lectura de datos, propiedades paramétricas y parseo geométrico del archivo IFC[cite: 9].
*   **Trimesh & NetworkX:** Librerías matemáticas encargadas de agrupar vértices y caras para la reconstrucción, renderizado 3D y exportación de la malla a formato GLB[cite: 9].

## ⚙️ Instalación y Uso

1. Clona este repositorio en tu equipo:
   ```bash
   git clone [https://github.com/TU_USUARIO/aparejador-ninja-bim.git](https://github.com/TU_USUARIO/aparejador-ninja-bim.git)

2. Instala las dependencias necesarias. Es crítico instalar una versión específica de pyglet para asegurar la compatibilidad del visor 3D[cite: 9]:
   ```bash
   pip install ifcopenshell trimesh "pyglet<2" networkx

3. Ejecuta la aplicación:
   ```bash
   python nombre_del_archivo.py

## 👨‍💻 Autor

Jose Manuel Caamaño González | Arquitecto Técnico & BIM Manager.
Digital Product Lead | ConTech & Digital Twin SaaS | BIM, Energy Modeling & Sustainability | Data Analytics (SQL, Power BI)

Hecho con código y café desde A Coruña. ☕

Jose Manuel Caamaño González | [LinkedIn](https://www.linkedin.com/in/jmcaamanog/)
