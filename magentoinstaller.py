#!/usr/bin/python
# -*- encoding: utf-8 -*-
from gi.repository import Gtk, Gdk, GObject, GLib
import os, sys
import commands


class AppWindow(Gtk.Window):

  def __init__(self):
		Gtk.Window.__init__(self, title="Instalador de Magento - Rafael Ortega Bueno")
		self.set_size_request(400,200)
		self.timeout_id = None

		hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
		hbox.set_homogeneous(False)

		titulo = Gtk.Label()
		titulo.set_markup('<span font_desc="Helvetica bold 16">%s</span>' % 'Instalador de Magento')
		
		version_box = Gtk.Box(spacing=0)
		version_box.set_homogeneous(False)
		version_label = Gtk.Label('Versão Desejada: ')
		
		version_entry = Gtk.Entry()
		self.version_entry = version_entry
		version_entry.set_text('1.7.0.2')		
		version_box.pack_start(version_label, True, True, 40)
		version_box.pack_start(version_entry,True, True, 40)

		path_box = Gtk.Box(spacing=0)
		path_box.set_homogeneous(False)
		path_label = Gtk.Label('Path de instalação: ')
		self.path_entry = Gtk.Entry()
		self.path_entry.set_text('/var/www/magento')
		path_box.pack_start(path_label, True, True, 40)
		path_box.pack_start(self.path_entry,True,True,40)

		button = Gtk.Button(label="Instalar")
		button.connect('clicked',self.install)

		terminal = Gtk.Box()
		
		terminal_text = Gtk.Label()
		self.terminal = terminal_text
		terminal_text.set_markup('<span font_desc="Helvetica" color="green" background="black">%s</span>' % ' Instalador de Magento ')
		terminal.pack_start(terminal_text,True,True,0)


		hbox.pack_start(titulo, True, True, 0)
		hbox.pack_start(version_box,True,True,0)
		hbox.pack_start(path_box,True,True,0)
		hbox.pack_start(button, True, True, 0)
		hbox.pack_start(terminal,True,True,0)

				
		self.add(hbox)


	def install(self, widget):
		
		if os.path.isfile('magento-'+self.version_entry.get_text()+'.tar.gz'):
			self.installpath()
		else:
			self.sh(str('wget http://www.magentocommerce.com/downloads/assets/'+self.version_entry.get_text()+'/magento-'+self.version_entry.get_text()+'.tar.gz'))
			self.installpath()

	def installpath(self):
		project_path = self.path_entry.get_text()
		if os.path.exists(self.path_entry.get_text()):
			self.setinfo('Já existe um projeto com este nome.')
		else:
			self.sh(str('mkdir '+self.path_entry.get_text()))
			self.sh(str('tar -C '+self.path_entry.get_text()+' -zxvf magento-'+self.version_entry.get_text()+'.tar.gz'))
			self.sh(str('mv '+self.path_entry.get_text()+'/magento/* '+self.path_entry.get_text()+'/magento/.htaccess '+self.path_entry.get_text()))
			self.sh(str('rm '+self.path_entry.get_text()+'/magento -Rf'))
			self.sh(str('chmod -R o+w '+project_path+'/media '+project_path+'/var'))
			self.sh(str('chmod o+w '+project_path+'/app/etc'))
			self.setinfo('Instalação Concluida!')


	def executa(self, comando):
		output = commands.getoutput(comando)
		#self.setinfo(output)


	def sh(self,script):
		os.system("bash -c '%s'" % script)

	def setinfo(self,info):
		self.terminal.set_markup('<span font_desc="Helvetica" color="green" background="black">%s</span>' %  info)

win = AppWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
