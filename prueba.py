import tkinter as tk
from tkinter import filedialog

def abrir_archivo():
    # Abre el cuadro de diálogo para seleccionar un archivo
    archivo_path = filedialog.askopenfilename()

    # Verifica si se seleccionó un archivo
    if archivo_path:
        # Abre el archivo y lee su contenido
        with open(archivo_path, 'r') as archivo:
            contenido_original = archivo.read()

        # Muestra el contenido original en el lado izquierdo
        texto_original.delete(1.0, tk.END)  # Borra el contenido anterior
        texto_original.insert(tk.END, contenido_original)

def realizar_conversion():
    # Obtiene el contenido original
    contenido_original = texto_original.get(1.0, tk.END)

    # Realiza la conversión (puedes personalizar esto según tus necesidades)
    contenido_convertido = contenido_original.upper()  # Convertir a mayúsculas (ejemplo)

    # Muestra el contenido convertido en el lado derecho
    texto_convertido.delete(1.0, tk.END)  # Borra el contenido anterior
    texto_convertido.insert(tk.END, contenido_convertido)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Conversión de Archivos")

# Crear un botón para abrir el archivo
boton_abrir = tk.Button(ventana, text="Abrir Archivo", command=abrir_archivo)
boton_abrir.pack(pady=10)

# Crear un widget de texto para mostrar el contenido original del archivo
texto_original = tk.Text(ventana, wrap=tk.WORD, width=40, height=10)
texto_original.pack(side=tk.LEFT, padx=10, pady=10)

# Crear un botón para realizar la conversión
boton_convertir = tk.Button(ventana, text="Realizar Conversión", command=realizar_conversion)
boton_convertir.pack(pady=10)

# Crear un widget de texto para mostrar el contenido convertido
texto_convertido = tk.Text(ventana, wrap=tk.WORD, width=40, height=10)
texto_convertido.pack(side=tk.RIGHT, padx=10, pady=10)

# Iniciar el bucle principal
ventana.mainloop()
