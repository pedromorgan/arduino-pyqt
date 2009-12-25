# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui


from gui.icons import Ico 
from gui.icons import Icon 

"""
Displays the directories for sketches
Currently two modes, broswse USER sketches, or Examples

TODO - maybe these need to be split up
"""
class SketchListWidget(QtGui.QDockWidget):

	MODE_USER = 0
	MODE_EXAMPES = 1
	
	def __init__(self, main, display_mode):
		QtGui.QDockWidget.__init__(self)

		self.main = main
		
		if display_mode == self.MODE_USER:
			self.dir_to_browse = self.main.settings.sketchbooks_path()
			self.title = "Sketches"
		else:
			self.dir_to_browse = self.main.settings.examples_path()
			self.title = "Examples"

		containerWidget = QtGui.QWidget()
		self.setWidget(containerWidget)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		containerWidget.setLayout(mainLayout)

		label   = QtGui.QLabel(self.title)
		label.setStyleSheet("background-color: black; color: white; font-size: 18pt;")

		mainLayout.addWidget(label)

		#######################################
		## Tree
		#######################################
		self.tree = QtGui.QTreeWidget()
		mainLayout.addWidget(self.tree)
		
		self.tree.setRootIsDecorated(True)
		self.tree.setAlternatingRowColors(False)
		self.tree.headerItem().setText(0, "#")
		self.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_tree_double_clicked)
		self.connect(self.tree, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.on_tree_clicked)

		self.load_files()

	#################################################################
	## Tree Events
	#################################################################
	def on_tree_clicked(self, item, col):
		return
		print "on_tree_clicked", item, col
		data = item.data(0, QtCore.Qt.UserRole)
		print data
		if not data.isNull():
			#if data.toString() == "pde":
			print "YES", data.toString()
		

	def on_tree_double_clicked(self, item, col):
		print "on_tree_double_clicked", item, col
		#print "on_tree_clicked", item, col
		data = item.data(0, QtCore.Qt.UserRole)
		print data
		if not data.isNull():
			#if data.toString() == "pde":
			print "YES", data.toString()
			pdeFile = QtCore.QFile(data.toString())
			if not pdeFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
				print "oops"
				return
			all_file = pdeFile.readAll()
			all_file_string = QtCore.QString(all_file)
			self.emit(QtCore.SIGNAL("open_sketch"), data.toString(), all_file_string)

		#progFile = QtCore.QFile(prog_file)
		#if not progFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			#print "oops"
			#return
		
		#while not progFile.atEnd():
			#line = progFile.readLine();
	#################################################################
	## Load Files
	#################################################################
	def load_files(self):
		dirr = QtCore.QDir(self.dir_to_browse)
		#print self.dir_to_browse
		if not dirr.exists():
			QtGui.QMessageBox.information(self, "OOps", " the examples dir %s was not found" % pathStr)
			return

		infoList = dirr.entryInfoList(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
		for fileInfo in infoList:
			
			#print fileInfo.filePath()
			treeItem = QtGui.QTreeWidgetItem()
			treeItem.setText(0, fileInfo.fileName() ) ## hack to remove .html
			treeItem.setIcon(0, Icon(Ico.Folder))
			self.tree.addTopLevelItem(treeItem)
			self.tree.setItemExpanded(treeItem, True)

			subDir = QtCore.QDir(fileInfo.filePath())
			for sItem in subDir.entryInfoList(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot):
				print sItem.fileName()
				if sItem.fileName() == "applet":
					pass ## igonore TODO - maybe option to hide/show all files
				else:
					subItem = QtGui.QTreeWidgetItem()
					treeItem.addChild(subItem)
					subItem.setText(0, sItem.fileName() ) ## hack to remove .html
					if sItem.isDir():
						subItem.setIcon(0, Icon(Ico.Folder))
						## TODO - walk node
					else:
						subItem.setIcon(0, Icon(Ico.Sketch))
						subItem.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(sItem.filePath()))

