from PyQt5.QtWidgets import QListWidget, QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
import sqlite3 as sql
import csv
from re import split

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("agenda.ui", self)
        self.key = ''
        self.cargadelista()
     
        # botones con la funcion apago(para prender en cada opcion que se requiera)
        self.eliminar.setEnabled(False)
        self.editar.setEnabled(False)
        self.aceptar.setEnabled(False)
        self.cancelar.setEnabled(False)
        
    
        #conecto los botones y la lista para seleccionar si es necesiario
        self.lista.itemSelectionChanged.connect(self.on_seleccionlista)
        self.nuevo.clicked.connect(self.on_nuevo)
        self.editar.clicked.connect(self.on_editar)
        self.eliminar.clicked.connect(self.on_eliminar)
        self.aceptar.clicked.connect(self.on_aceptar)
        self.cancelar.clicked.connect(self.on_cancelar)
    
    #defino la opcion nuevo donde puedo agregar un contacto a la base y habilito acpetar y cancelar
    def on_nuevo(self):
        self.nombre.text()
        self.apellido.text()
        self.email.text()
        self.telefono.text()
        self.direccion.text()
        self.fechnac.text()
        self.alt.text()
        self.peso.text()
        self.nuevo.setEnabled(False)
        self.aceptar.setEnabled(True)
        self.cancelar.setEnabled(True)
        self.lista.currentItem().setSelected(False)
        self.nombre.setFocus()
        self.key = 1
        
       #se habilita aceptar
    def on_aceptar(self):
        
        if self.key == 1:

          nombre2 = self.nombre.text()
          apellido2 = self.apellido.text()
          email2=self.email.text()
          telefono2=self.telefono.text()
          direccion2=self.direccion.text()
          fech2=self.fechnac.text()
          altura2=self.alt.text()
          peso2=self.peso.text()
    
          conn = sql.connect('agendanew.db')
          cursor = conn.cursor()
          instruccion = f"INSERT INTO contactos VALUES(NULL, '{nombre2}', '{apellido2}', '{email2}', '{telefono2}', '{direccion2}', '{fech2}', '{altura2}', '{peso2}')"
          cursor.execute(instruccion)
          conn.commit()
          conn.close()
          self.cargadelista()
          self.nuevo.setEnabled(True)
          self.aceptar.setEnabled(False)
          self.cancelar.setEnabled(False)


          

        elif self.key == 2:
           nombre2 = self.nombre.text()
           apellido2 = self.apellido.text()
           email2=self.email.text()
           telefono2=self.telefono.text()
           direccion2=self.direccion.text()
           fech2=self.fechnac.text()
           altura2=self.alt.text()
           peso2=self.peso.text()
        
           item = self.lista.currentItem().text()
           id = split('\D+', item)
           conn = sql.connect('agendanew.db')
           cursor = conn.cursor()
           instruccion = f"""UPDATE contactos SET nombre ='{nombre2}', apellido ='{apellido2}', 
           email ='{email2}, telefono ={telefono2}, direccion ='{direccion2}', fecha_nacimiento ='{fech2}', 
           altura ={altura2}, peso ={peso2} WHERE id ='{id[0]}'"""

           cursor.execute(instruccion)
           conn.commit()
           conn.close()
           self.cargadelista()
           self.nuevo.setEnabled(True)
           self.aceptar.setEnabled(False)
           self.cancelar.setEnabled(False)
        
        #se habilita cancelar
    def on_cancelar(self):
        
        self.nombre.clear()
        self.apellido.clear()
        self.email.clear()
        self.telefono.clear()
        self.direccion.clear()
        self.fechnac.clear()
        self.alt.clear()
        self.peso.clear()

        self.nuevo.setEnabled(True)
        self.aceptar.setEnabled(False)
        self.cancelar.setEnabled(False)
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)


   
     
    #se define editar y habilita las opciones de aceptar y cancelar
    def on_editar(self):   
        self.nombre.text()
        self.apellido.text()
        self.email.text()
        self.telefono.text()
        self.direccion.text()
        self.fechnac.text()
        self.alt.text()
        self.peso.text()

        self.editar.setEnabled(False)
        self.aceptar.setEnabled(True)
        self.cancelar.setEnabled(True)
        self.eliminar.setEnabled(False)
        self.nuevo.setEnabled(False)

        self.nombre.setFocus()
        self.key=1
        
 # se define la opcion de seleccionar en la lista para editar o eliminar
    def on_seleccionlista(self):
    
        self.editar.setEnabled(True)
        self.eliminar.setEnabled(True)
        vista = self.lista.currentItem().text()
        id = split('\D+', vista)
        conn = sql.connect('agendanew.db')
        cursor = conn.cursor()
        instruccion = f'SELECT * FROM contactos WHERE id = {id[0]}'
        carga = cursor.execute(instruccion)
        for fila in carga:
            self.nombre.setText(f'{fila[1]}')
            self.apellido.setText(f'{fila[2]}')
            self.email.setText(f'{fila[3]}')
            self.telefono.setText(f'{fila[4]}')
            self.direccion.setText(f'{fila[5]}')
            self.fechnac.setText(f'{fila[6]}')
            self.alt.setText(f'{fila[7]}')
            self.peso.setText(f'{fila[8]}')
        conn.commit()
        conn.close() 
    

    #carga la lista de la izquierda con el id, nombre y apellido
    def cargadelista(self):
        self.lista.clear()
        conn = sql.connect('agendanew.db')
        cursor = conn.cursor()
        instruccion = f'SELECT * FROM contactos'
        carga = cursor.execute(instruccion)
        for fila in carga:
            self.lista.addItem(f'{fila[0]}.  {fila[1]} {fila[2]}')
        conn.commit()
        conn.close() 
    
    #se define la opcion eliminar despues de seleccionar un contacto
    def on_eliminar(self):
        msg = QMessageBox()
        msg.setWindowTitle('ELIMINAR UN CONTACTO')
        msg.setText('ESTAS SEGURO DE ELIMINAR EL CONTACTO')
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes | QMessageBox.Cancel) 
        resultado = msg.exec_()
        if resultado == QMessageBox.Yes:
         v = self.lista.currentItem().text()
         id = split('\D+', v)
         conn = sql.connect('agendanew.db')
         cursor = conn.cursor()
         instruccion = f'DELETE FROM contactos WHERE id = {id[0]}'
         carga = cursor.execute(instruccion)
         conn.commit()
         conn.close()
         self.cargadelista()
         if resultado == QMessageBox.No:
            print('el usuario eligio No')
         if resultado == QMessageBox.Cancel:
            print('el usuario eligio Cancelar')


app = QApplication([])

win = MiVentana()
win.show()

app.exec_()
