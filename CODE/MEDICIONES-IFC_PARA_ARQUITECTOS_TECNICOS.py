"""
      ██╗███╗   ███╗ ██████╗
      ██║████╗ ████║██╔════╝
      ██║██╔████╔██║██║
 ██   ██║██║╚██╔╝██║██║    
 ╚█████╔╝██║ ╚═╝ ██║╚██████╗
  ╚════╝ ╚═╝     ╚═╝ ╚═════╝
 """

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import re
import csv
import threading
import webbrowser # <--- Añadido para que el enlace a tu LinkedIn funcione

# Si te da error de importación, necesitas instalar estas librerías:
# pip install ifcopenshell trimesh "pyglet<2" networkx
try:
    import ifcopenshell
    import ifcopenshell.geom
    import ifcopenshell.util.element
    import trimesh
    import networkx  # <--- El cerebro matemático para que el visor 3D no reviente
except ImportError:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("¡Freno, Jose!", "Te faltan librerías.\nAbre la terminal y tira un:\npip install ifcopenshell trimesh \"pyglet<2\" networkx")
    exit()

# ==========================================
# FUNCIONES SABUESO (Mantenemos la magia)
# ==========================================
def extraer_numero(valor):
    if isinstance(valor, (int, float)):
        return float(valor)
    if isinstance(valor, str):
        try:
            numero_limpio = re.sub(r'[^\d.,-]', '', valor)
            if not numero_limpio: return None
            return float(numero_limpio.replace(',', '.'))
        except: pass
    return None

def obtener_area(elemento):
    try:
        psets = ifcopenshell.util.element.get_psets(elemento)
        nombres_area = ['netarea', 'grossarea', 'area', 'área', 'superficie', 'net_area', 'gross_area']
        dim_base = dim_alto = 0.0
        
        for pset_name, pset_data in psets.items():
            if not isinstance(pset_data, dict): continue
            for prop_name, prop_value in pset_data.items():
                val = extraer_numero(prop_value)
                if val is None: continue
                prop_low = prop_name.lower().strip()
                if prop_low in nombres_area: return val
                if prop_low in ['length', 'longitud', 'longitud de corte']: dim_base = max(dim_base, val)
                elif prop_low in ['width', 'anchura', 'ancho']:
                    if dim_base == 0: dim_base = val
                elif prop_low in ['height', 'altura', 'unconnected height', 'altura desconectada']: dim_alto = max(dim_alto, val)
                    
        if dim_base > 0 and dim_alto > 0: return dim_base * dim_alto
    except: pass
    return 0.0

def obtener_nombre_tipo(elemento):
    try:
        tipo = ifcopenshell.util.element.get_type(elemento)
        if tipo and hasattr(tipo, 'Name') and tipo.Name: return tipo.Name
        if hasattr(elemento, 'ObjectType') and elemento.ObjectType: return elemento.ObjectType
        if hasattr(elemento, 'Name') and elemento.Name: return elemento.Name
    except: pass
    return "Tipo Desconocido"

# ==========================================
# INTERFAZ GRÁFICA (La App de Windows)
# ==========================================
class AppAparejadorBIM:
    def __init__(self, root):
        self.root = root
        self.root.title("Aparejador Ninja BIM - Extractor & Presupuestos")
        self.root.geometry("850x700")
        self.root.configure(padx=10, pady=10)
        
        # Variables
        self.ruta_archivo = tk.StringVar()
        self.coste_m2 = tk.StringVar(value="1500")
        self.porcentaje_hon = tk.StringVar(value="8.5")
        self.escena_3d = None  # Aquí guardaremos la geometría para el visor
        
        self.crear_interfaz()

    def crear_interfaz(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('TLabel', font=('Segoe UI', 10))
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[15, 5])

        # --- SISTEMA DE PESTAÑAS ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Creamos los frames para cada pestaña
        self.tab_calc = ttk.Frame(self.notebook, padding=10)
        self.tab_visor = ttk.Frame(self.notebook, padding=10)
        self.tab_acerca = ttk.Frame(self.notebook, padding=10) # <--- Nueva pestaña

        self.notebook.add(self.tab_calc, text=" 📊 Calculadora y Extractor ")
        self.notebook.add(self.tab_visor, text=" 👁️ Visor 3D Rápido ")
        self.notebook.add(self.tab_acerca, text=" ℹ️ Acerca de... ")

        self.construir_pestaña_calculadora()
        self.construir_pestaña_visor()
        self.construir_pestaña_acerca() # <--- Construir contenido

    def construir_pestaña_calculadora(self):
        # --- PANEL SUPERIOR: Archivo ---
        frame_archivo = ttk.LabelFrame(self.tab_calc, text=" 1. El IFC de la discordia ", padding=10)
        frame_archivo.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(frame_archivo, text="Buscar IFC...", command=self.seleccionar_archivo).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(frame_archivo, textvariable=self.ruta_archivo, foreground='gray').pack(side=tk.LEFT, fill=tk.X, expand=True)

        # --- PANEL MEDIO: La Pasta ---
        frame_pasta = ttk.LabelFrame(self.tab_calc, text=" 2. Los números que duelen ", padding=10)
        frame_pasta.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame_pasta, text="Coste Construcción (€/m²):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame_pasta, textvariable=self.coste_m2, width=15).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame_pasta, text="(Baja: 1000-1400 | Media: 1450-1800 | Alta: 2000-2500)", font=('Segoe UI', 8), foreground='gray').grid(row=0, column=2, sticky=tk.W)

        ttk.Label(frame_pasta, text="Tus Honorarios (%):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame_pasta, textvariable=self.porcentaje_hon, width=15).grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(frame_pasta, text="(Pa' que el Colegio te cobre el visado con una sonrisa)", font=('Segoe UI', 8), foreground='gray').grid(row=1, column=2, sticky=tk.W)

        # --- BOTÓN DE PÁNICO ---
        self.btn_procesar = ttk.Button(self.tab_calc, text="¡EXTRAER GLB Y CALCULAR LA RUINA!", command=self.iniciar_proceso)
        self.btn_procesar.pack(fill=tk.X, pady=(0, 10), ipady=10)

        # --- CONSOLA DE SALIDA ---
        ttk.Label(self.tab_calc, text="Diario de Obra (Log):", style='TLabel').pack(anchor=tk.W)
        self.consola = scrolledtext.ScrolledText(self.tab_calc, height=12, bg='#1e1e1e', fg='#00ff00', font=('Consolas', 10))
        self.consola.pack(fill=tk.BOTH, expand=True)
        
        self.log("¡Bienvenido, Jose! Carga un IFC y dale al botón gordo.\nYo me encargo de pelearme con el BIM.")

    def construir_pestaña_visor(self):
        # Contenido de la pestaña del visor 3D
        ttk.Label(self.tab_visor, text="MODO POSTUREO BIM", font=('Segoe UI', 16, 'bold')).pack(pady=(40, 10))
        
        self.lbl_estado_visor = ttk.Label(self.tab_visor, text="Primero tienes que extraer un archivo IFC en la otra pestaña.", foreground="gray", font=('Segoe UI', 11))
        self.lbl_estado_visor.pack(pady=10)

        self.btn_abrir_visor = ttk.Button(self.tab_visor, text="👁️ ABRIR VISOR 3D 👁️", command=self.lanzar_visor, state=tk.DISABLED)
        self.btn_abrir_visor.pack(pady=20, ipady=15, ipadx=30)
        
        ttk.Label(self.tab_visor, text="💡 Un consejo: Al abrir el visor, usa el ratón para rotar y la rueda para el zoom.\nCierra la ventana del 3D cuando termines para volver aquí.", justify=tk.CENTER, foreground="gray").pack(pady=30)

    def construir_pestaña_acerca(self):
        # --- PESTAÑA DEL AUTOR ---
        frame_centro = ttk.Frame(self.tab_acerca)
        frame_centro.pack(expand=True)

        ttk.Label(frame_centro, text="👨‍💻 Autor", font=('Segoe UI', 18, 'bold')).pack(pady=(0, 20))
        
        ttk.Label(frame_centro, text="Jose Manuel Caamaño González", font=('Segoe UI', 14, 'bold')).pack(pady=2)
        ttk.Label(frame_centro, text="Arquitecto Técnico & BIM Manager", font=('Segoe UI', 12), foreground="#444444").pack(pady=(0, 15))
        
        desc = "Digital Product Lead | ConTech & Digital Twin SaaS\nBIM, Energy Modeling & Sustainability | Data Analytics (SQL, Power BI)"
        ttk.Label(frame_centro, text=desc, font=('Segoe UI', 10), justify=tk.CENTER).pack(pady=10)
        
        ttk.Label(frame_centro, text="Hecho con código y café desde A Coruña. ☕", font=('Segoe UI', 11, 'italic'), foreground='gray').pack(pady=25)

        # Enlace a LinkedIn
        lbl_linkedin = ttk.Label(frame_centro, text="🔗 Conectar en LinkedIn", font=('Segoe UI', 11, 'underline'), foreground="#0077b5", cursor="hand2")
        lbl_linkedin.pack(pady=10)
        lbl_linkedin.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.linkedin.com/in/jmcaamanog/"))

    def seleccionar_archivo(self):
        ruta = filedialog.askopenfilename(title="Jose, elige el archivo IFC", filetypes=[("Archivos IFC", "*.ifc"), ("Todos los archivos", "*.*")])
        if ruta:
            self.ruta_archivo.set(ruta)
            self.log(f"Archivo cargado: {os.path.basename(ruta)}")

    def log(self, mensaje):
        self.root.after(0, self._insertar_log, str(mensaje))

    def _insertar_log(self, mensaje):
        self.consola.insert(tk.END, mensaje + "\n")
        self.consola.see(tk.END)

    def lanzar_visor(self):
        if self.escena_3d:
            # Lo lanzamos; esto pausará un poco la ventana principal hasta que cierres el 3D, 
            # que es lo más seguro para que OpenGL y Tkinter no se peleen.
            self.log("\n🚀 Lanzando visor 3D... Cierra la ventana del modelo cuando termines.")
            try:
                self.escena_3d.show(viewer='gl')
            except Exception as e:
                # Cazamos el error de la versión de pyglet para que no reviente la app entera
                if "pyglet<2" in str(e):
                    msg = "¡Choque de versiones!\n\nTrimesh necesita una versión antigua de pyglet para funcionar.\nAbre tu terminal de Windows y ejecuta literalmente esto:\n\npip install \"pyglet<2\""
                    messagebox.showerror("Pyglet muy moderno", msg)
                    self.log("❌ Error: Pyglet versión 2.x detectado. Trimesh necesita la versión 1.x.")
                else:
                    messagebox.showerror("Error del visor", f"El visor ha reventado por otro motivo:\n{e}")
                    self.log(f"❌ Error al abrir visor 3D: {e}")

    def iniciar_proceso(self):
        ruta = self.ruta_archivo.get()
        if not ruta or not os.path.exists(ruta):
            messagebox.showwarning("Falta el archivo", "¡Ponme un archivo IFC primero, fiera!")
            return
            
        try:
            coste = float(self.coste_m2.get().replace(',', '.'))
            hono = float(self.porcentaje_hon.get().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Error de números", "Mete números normales en los costes y honorarios, por favor.")
            return

        self.btn_procesar.state(['disabled'])
        self.btn_abrir_visor.state(['disabled'])
        self.escena_3d = None
        self.consola.delete('1.0', tk.END)
        
        hilo = threading.Thread(target=self.procesar_ifc, args=(ruta, coste, hono))
        hilo.daemon = True
        hilo.start()

    def procesar_ifc(self, ruta_ifc, coste_m2, porcentaje):
        self.log(f"Abriendo el bicho: {os.path.basename(ruta_ifc)}\nTen paciencia, leer IFCs a veces es como leer el Quijote...")
        try:
            modelo = ifcopenshell.open(ruta_ifc)
        except Exception as e:
            self.log(f"❌ Error al abrir el IFC. ¿Seguro que no está corrupto?\nDetalle: {e}")
            self.root.after(0, lambda: self.btn_procesar.state(['!disabled']))
            return

        # --- RADIOGRAFÍA ---
        self.log("\n=== RADIOGRAFÍA DETALLADA DEL MODELO ===")
        resumen_categorias = {}
        tipos_elementos = {
            "Muros": ["IfcWall", "IfcWallStandardCase"], "Puertas": ["IfcDoor"], "Ventanas": ["IfcWindow"],
            "Forjados/Suelos": ["IfcSlab"], "Pilares": ["IfcColumn"], "Vigas": ["IfcBeam"],
            "Cubiertas": ["IfcRoof"], "Escaleras": ["IfcStair"]
        }
        
        for nombre_comun, clases_ifc in tipos_elementos.items():
            elementos_totales = []
            for clase in clases_ifc: elementos_totales.extend(modelo.by_type(clase))
            if not elementos_totales: continue
            
            self.log(f"\n> {nombre_comun} (Total: {len(elementos_totales)} Ud.)")
            tipos_dict = {}
            area_total_categoria = 0.0
            
            for elem in elementos_totales:
                nombre_tipo = obtener_nombre_tipo(elem)
                area = obtener_area(elem)
                if nombre_tipo not in tipos_dict: tipos_dict[nombre_tipo] = {"count": 0, "area": 0.0}
                tipos_dict[nombre_tipo]["count"] += 1
                tipos_dict[nombre_tipo]["area"] += area
                area_total_categoria += area
                
            for tipo, datos in tipos_dict.items():
                area_str = f" | Superficie: {datos['area']:.2f} m²" if datos['area'] > 0 else " | (Sin datos de superficie)"
                self.log(f"  - {tipo}: {datos['count']} Ud.{area_str}")
                
            if area_total_categoria > 0: self.log(f"  * SUPERFICIE TOTAL DE {nombre_comun.upper()}: {area_total_categoria:.2f} m²")
            resumen_categorias[nombre_comun] = {"count": len(elementos_totales), "area": area_total_categoria}

        # --- RUINA TÉRMICA ---
        area_muros = resumen_categorias.get("Muros", {}).get("area", 0)
        area_ventanas = resumen_categorias.get("Ventanas", {}).get("area", 0)
        if area_muros > 0 and area_ventanas > 0:
            ratio_huecos = (area_ventanas / area_muros) * 100
            self.log("\n=== 🌡️ ÍNDICE DE LA RUINA TÉRMICA 🌡️ ===")
            self.log(f"Ratio Ventanas / Muros: {ratio_huecos:.1f}%")
            if ratio_huecos > 30: self.log("🚨 OJO: Tienes más cristal que la fachada del Apple Store. Prepara el clima.")
            elif ratio_huecos > 15: self.log("👍 Ratio razonable. Ni pecera ni cueva.")
            else: self.log("🦇 Oye, esto es un búnker. Pon alguna ventana más que parecéis vampiros.")

        # --- EXTRACCIÓN GLB Y VISOR ---
        estancias = modelo.by_type("IfcSpace")
        area_total_estancias = 0.0
        
        if not estancias:
            self.log("\n¡Ojo! Este IFC no tiene entidades 'IfcSpace'. No hay estancias que sacar.")
        else:
            self.log(f"\nProcesando geometría de {len(estancias)} estancias para el GLB y el Visor...")
            settings = ifcopenshell.geom.settings()
            mallas = []
            
            for estancia in estancias:
                area_total_estancias += obtener_area(estancia)
                try:
                    forma = ifcopenshell.geom.create_shape(settings, estancia)
                    verts = forma.geometry.verts
                    caras = forma.geometry.faces
                    verts_agrupados = [verts[i:i+3] for i in range(0, len(verts), 3)]
                    caras_agrupadas = [caras[i:i+3] for i in range(0, len(caras), 3)]
                    mallas.append(trimesh.Trimesh(vertices=verts_agrupados, faces=caras_agrupadas))
                except: pass

            if mallas:
                self.escena_3d = trimesh.Scene(mallas)
                ruta_base = os.path.splitext(ruta_ifc)[0]
                ruta_glb = f"{ruta_base}.glb"
                self.escena_3d.export(ruta_glb)
                self.log(f"✅ ¡GLB Generado con éxito!\nRuta: {ruta_glb}")
                
                # Activamos el botón del visor en la interfaz gráfica
                self.root.after(0, lambda: self.btn_abrir_visor.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.lbl_estado_visor.config(text="¡Modelo cargado en memoria! Ya puedes verlo.", foreground="green"))
            else:
                self.log("⚠️ Ninguna estancia tenía volumen 3D exportado.")

        # --- FACTURACIÓN Y CSV ---
        if area_total_estancias > 0:
            coste_total = area_total_estancias * coste_m2
            self.log("\n" + "="*50 + f"\n{'🧾 LA DOLOROSA':^50}\n" + "="*50)
            
            pesos = {"Muros": 0.28, "Forjados/Suelos": 0.22, "Cubiertas": 0.12, "Pilares": 0.08, "Vigas": 0.08, "Ventanas": 0.10, "Puertas": 0.07, "Escaleras": 0.05}
            peso_total_real = sum(pesos.get(k, 0) for k in resumen_categorias.keys()) or 1
            datos_csv = [["PARTIDA", "UNIDADES", "SUPERFICIE (m2)", "COSTE APROX (EUR)"]]
            
            for categoria, datos in resumen_categorias.items():
                if datos['count'] == 0: continue
                coste_partida = coste_total * (pesos.get(categoria, 0) / peso_total_real)
                self.log(f"{categoria:<18} | {datos['count']:>3} Ud | {coste_partida:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
                datos_csv.append([categoria, datos['count'], round(datos['area'], 2), round(coste_partida, 2)])
            
            self.log("-" * 50)
            str_total = f"{coste_total:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
            self.log(f"TOTAL EJECUCIÓN MATERIAL: {str_total}")
            honorarios = coste_total * (porcentaje / 100)
            hon_formateado = f"{honorarios:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
            self.log(f"\n🤑 Tus honorarios ({porcentaje}%): {hon_formateado}")

            datos_csv.extend([["", "", "", ""], ["TOTAL EJECUCION MATERIAL", "", "", round(coste_total, 2)], ["HONORARIOS", f"{porcentaje}%", "", round(honorarios, 2)]])
            try:
                ruta_csv = f"{os.path.splitext(ruta_ifc)[0]}_presupuesto.csv"
                with open(ruta_csv, mode='w', newline='', encoding='utf-8-sig') as f:
                    csv.writer(f, delimiter=';').writerows(datos_csv)
                self.log(f"📄 Excel listo en: {ruta_csv}")
            except Exception as e: self.log(f"⚠️ Cierra el Excel, fiera. No he podido sobreescribir el CSV.")

        self.log("\n--- FIN DEL PROCESO ---")
        self.root.after(0, lambda: self.btn_procesar.state(['!disabled']))

if __name__ == "__main__":
    ventana = tk.Tk()
    app = AppAparejadorBIM(ventana)
    ventana.mainloop()