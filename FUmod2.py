# -*- coding: utf-8 -*-
import os
import nuke
import glob
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtUiTools import QUiLoader

def list_make(self):

    self.target_nodes = [] #Fileが含まれているノード
    self.node_num = 0#対象のノード数
    self.list = []
    self.item = []
    self.name = []
    self.fname = []
    self.name_value = []
    self.checklist = [] #置換対象確認用
    self.cancelnum = [] #変換したか確認用
    self.cancellist = [] #ひとつ前のリスト保管用

    self.sorttable = [] #二次元table

    self.firstlist = []
    self.selectedrow = []

    a = 0
    self.filenum = 0
    self.cancelnum.append(0)

    for n in nuke.allNodes():
        try:
            g = n['name'].value()
            f = n['file'].value()
            try:
                f = f.replace('%04d','####')
            except:
                pass
            h = os.path.basename(f)
            if len(f) == 0:
                continue

            self.UI.dstlist.insertRow(a)

            self.UI.dstlist.setItem(a,4,QTableWidgetItem(f))

            self.UI.dstlist.setItem(a,3,QTableWidgetItem(f))

            self.UI.dstlist.setItem(a,2,QTableWidgetItem(h))

            self.UI.dstlist.setItem(a,1,QTableWidgetItem(g))

            self.UI.dstlist.setItem(a,0,QTableWidgetItem('✔'))

            self.cancelnum.append(0)
            self.checklist.append(1)

            self.filenum = self.filenum + 1

            self.sorttable.append([g,n,h,f])#ファイルタイプ、ファイルノード、ファイル名、パス

            if os.path.exists(os.path.dirname(f)):
                pass
            else:
                self.UI.dstlist.item(a,0).setBackground(QColor('#dc143c'))
                self.UI.dstlist.item(a,1).setBackground(QColor('#dc143c'))
                self.UI.dstlist.item(a,2).setBackground(QColor('#dc143c'))
                self.UI.dstlist.item(a,3).setBackground(QColor('#dc143c'))
                self.UI.dstlist.item(a,4).setBackground(QColor('#dc143c'))
            a = a+1
        except:
            a = a

    self.sorttable.sort()
    self.node_num = a

    for n in range(self.node_num):
        self.name.append(self.sorttable[n][0])
        self.target_nodes.append(self.sorttable[n][1])
        self.fname.append(self.sorttable[n][2])
        self.name_value.append(self.sorttable[n][3])
        self.firstlist.append(self.sorttable[n][3])

    self.UI.dstlist.setColumnWidth(0,50)
    self.UI.dstlist.setColumnWidth(1,85)
    self.UI.dstlist.setColumnWidth(2,300)
    self.UI.dstlist.setColumnWidth(3,700)

    self.UI.dstlist.setWordWrap(True)
    self.UI.dstlist.sortItems(1)

def delete_table(self):
    for n in range(self.filenum+1):
        self.UI.dstlist.removeRow(self.filenum-n-1)

def apply_do(self):
    a = 0
    self.cancellist = []
    for n in self.target_nodes:
        self.cancellist.append(self.name_value[a])
        if self.checklist[a] == 0:
            self.cancelnum[a] = 0
            a = a + 1
        else:
            x = self.name_value[a]
            y = x.replace(self.UI.ref_word.text(), self.UI.dst_word.text())
            z = y.replace('####','%04d')
            self.UI.dstlist.setItem(a,4,QTableWidgetItem(y))
            if x == y:

                self.cancelnum[a]=1
            else:
                self.UI.dstlist.item(a,0).setBackground(QColor('#006400'))
                self.UI.dstlist.item(a,1).setBackground(QColor('#006400'))
                self.UI.dstlist.item(a,2).setBackground(QColor('#006400'))
                self.UI.dstlist.item(a,3).setBackground(QColor('#006400'))
                self.UI.dstlist.item(a,4).setBackground(QColor('#006400'))
                self.cancelnum[a]=0
                print 'change path : '+ self.name_value[a]
            n['file'].setValue(z)
            a=a+1

def cancel_do(self):
    a = 0
    for n in self.target_nodes:
        if self.cancelnum[a] == 0:
            self.UI.dstlist.setItem(a,4,QTableWidgetItem(self.cancellist[a]))
            
            self.UI.dstlist.item(a,0).setBackground(QColor('#383838'))
            self.UI.dstlist.item(a,1).setBackground(QColor('#383838'))
            self.UI.dstlist.item(a,2).setBackground(QColor('#383838'))
            self.UI.dstlist.item(a,3).setBackground(QColor('#383838'))
            self.UI.dstlist.item(a,4).setBackground(QColor('#383838'))

            n['file'].setValue(self.cancellist[a])

            self.cancelnum[a] = 0

        a=a+1

def reset_do(self):
    a = 0
    for n in self.target_nodes:
        self.UI.dstlist.setItem(a,4,QTableWidgetItem(self.firstlist[a]))
        n['file'].setValue(self.firstlist[a])
        self.UI.dstlist.item(a,0).setBackground(QColor('#383838'))
        self.UI.dstlist.item(a,1).setBackground(QColor('#383838'))
        self.UI.dstlist.item(a,2).setBackground(QColor('#383838'))
        self.UI.dstlist.item(a,3).setBackground(QColor('#383838'))
        self.UI.dstlist.item(a,4).setBackground(QColor('#383838'))
        a = a + 1

def check_do(self):
    for i in self.UI.dstlist.selectedItems():
        self.checklist[self.UI.dstlist.row(i)] = 1
        self.UI.dstlist.setItem(self.UI.dstlist.row(i),0,QTableWidgetItem('✔'))

def uncheck_do(self):
    for i in self.UI.dstlist.selectedItems():
        self.checklist[self.UI.dstlist.row(i)] = 0
        self.UI.dstlist.setItem(self.UI.dstlist.row(i),0,QTableWidgetItem('　'))

def allcheck_do(self):
    for i in range(self.filenum):
        self.checklist[i] = 1
        self.UI.dstlist.setItem(i,0,QTableWidgetItem('✔'))

def alluncheck_do(self):
    for i in range(self.filenum):
        self.checklist[i] = 0
        self.UI.dstlist.setItem(i,0,QTableWidgetItem(' '))

def move_to(self):
    node = self.target_nodes[self.UI.dstlist.currentRow()]
    nx = node.xpos()+ node.screenWidth()/ 2
    ny = node.ypos()+ node.screenHeight()/ 2
    nuke.zoom(1,[nx,ny])
