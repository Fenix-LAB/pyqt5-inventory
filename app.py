#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
# import os
# Add the parent directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QApplication

from controller.windowPrincipal import Principal
from controller.windowIniciar import WindowIniciar
from PyQt5.QtWidgets import QMessageBox, QDialog

class windowMain():

    def __init__(self):
        #self.Principal = Principal()

        self.iniciar = WindowIniciar()
        self.iniciar.winIniciar.btnIniciar.clicked.connect(self.comprobarUsuario)


    def comprobarUsuario(self):
        usuario = self.iniciar.onClickValidarUsuario()
        print(f'Usuario: {usuario}')
        if usuario != None:
            self.principal = Principal(usuario=usuario)
            self.iniciar.winIniciar.close()
            # self.principal.winPrincipal.lblNombreUsuario.setText(usuario.getUsuario())
            self.principal.winPrincipal.actionCerrarSesion.triggered.connect(self.cerrarSesion)
            self.principal.winPrincipal.actionSalir.triggered.connect(self.salir)


    def cerrarSesion(self):
        alert = QDialog()
        confirm  = QMessageBox.question(alert, "Mensaje", "¿ Desea cerrar sesion ?", QMessageBox.Yes,
             QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.iniciar.winIniciar.show()
            self.principal.winPrincipal.close()


    def salir(self):
        alert = QDialog()
        confirm = QMessageBox.question(alert, "Mensaje", "¿ Desea salir ?", QMessageBox.Yes, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.principal.winPrincipal.close()


app = QApplication(sys.argv)
windowMain = windowMain()
sys.exit(app.exec_())