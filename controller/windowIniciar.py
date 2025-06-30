#!/usr/bin/env python
# -*- coding: utf-8 -*-



from PyQt5 import uic
# from Conexion.conexionUsuario import conexionUsuario
# from Modelo.usuario import Usuario
from PyQt5.QtWidgets import QMessageBox, QDialog
import os


class WindowIniciar():

    def __init__(self):

        # Get the absolute path to the UI file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, '..', 'views', 'iniciar.ui')
        self.winIniciar = uic.loadUi(ui_path)
        # self.conexionUsuario = conexionUsuario()
        #self.winIniciar.btnIniciar.clicked.connect(self.onClickValidarUsuario)
        self.winIniciar.btnSalir.clicked.connect(self.onClickSalir)
        # self.usuario = Usuario()

        self.winIniciar.show()


    def onClickValidarUsuario(self):

        # self.usuario = Usuario()
        # self.usuario.setUsuario(self.winIniciar.txtUsuario.text())
        # self.usuario.setPasswd(self.winIniciar.txtPass.text())
        # value = ''
        # if self.usuario.getUsuario() != '' and self.usuario.getPasswd() != '':
        #     value  = self.conexionUsuario.validarUsuario(usuario=self.usuario)
        #     if len(value) != 0:
        #         self.usuario.setUsuario(value[0][0])
        #         self.usuario.setTipoUsuario(value[0][1])
        #         self.winIniciar.txtPass.setText('')
        #         self.winIniciar.txtUsuario.setText('')
        #         return self.usuario
        #     else:
        #         self.winIniciar.lblError.setText('LA CONTRASEÑA O USUARIO NO COINCIDEN')
        #         self.winIniciar.txtPass.setText('')
        #         alert = QDialog()
        #         QMessageBox.information(alert,"ERROR", 'LA CONTRASEÑA O USUARIO NO COINCIDEN')
        # else:
        #     print('Falta completar algun campo')
        #     alert = QDialog()
        #     QMessageBox.information(alert,"ERROR", 'Falta completar algun campo')

        usaer_name = self.winIniciar.txtUsuario.text()
        password = self.winIniciar.txtPass.text()

        if usaer_name and password:
            if usaer_name == "admin" and password == "admin":
                self.winIniciar.txtPass.setText('')
                self.winIniciar.txtUsuario.setText('')
                return True
            else:
                self.winIniciar.lblError.setText('LA CONTRASEÑA O USUARIO NO COINCIDEN')
                self.winIniciar.txtPass.setText('')
                alert = QDialog()
                QMessageBox.information(alert, "ERROR", 'LA CONTRASEÑA O USUARIO NO COINCIDEN')
        else:
            print('Falta completar algun campo')
            alert = QDialog()
            QMessageBox.information(alert, "ERROR", 'Falta completar algun campo')


    def onClickSalir(self):
        self.winIniciar.close()


