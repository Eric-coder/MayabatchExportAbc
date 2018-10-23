# -*- coding:utf-8 -*-
import subprocess
import sys
from CgtwQss.qss import styleData
try:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore
    from PySide import QtGui
except ImportError:
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui


#转换正常路径
def _getFilePath(urls):
    if '///' in urls.toString():
        filePath = urls.toString().split('///')[-1]
        return filePath
    elif '///' not in urls.toString():
        filePath = urls.toString()[1:]
        return filePath


def _assemblePath(path):
    assemblePaths = ''
    for string in path:
        assemblePaths+=string
        assemblePaths+='#'
    return assemblePaths

class QTextEdit(QtGui.QTextEdit):
    def __init__(self,parent = None):
        super(QTextEdit,self).__init__(parent)
        self._parent = parent
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        self.information=[]
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
            event.acceptProposedAction()

    def dragMoveEvent(self,event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
            urls[0].setScheme("")
            for uu in urls:
                uu=_getFilePath(uu)
                self.information.append(uu)
        self._parent.Run(_assemblePath(self.information))

class MainView(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setWindowTitle('Export Abc')
        self._mainUI()
    def _mainUI(self):
        filterLabel = QtGui.QLabel(u'过滤字段:')
        self.filterLine = QtGui.QLineEdit()

        resultLabel = QtGui.QLabel(u'输出路径')
        self.resultLine = QtGui.QLineEdit()
        resultLButton = QtGui.QPushButton(u'浏览')


        FileLabel = QtGui.QLabel(u'拖入导出的文件:')
        self.FileText =QTextEdit(self)

        Hlayout1 = QtGui.QHBoxLayout()
        Hlayout1.addWidget(filterLabel)
        Hlayout1.addWidget(self.filterLine)

        Hlayout2 = QtGui.QHBoxLayout()
        Hlayout2.addWidget(resultLabel)
        Hlayout2.addWidget(self.resultLine)
        Hlayout2.addWidget(resultLButton)

        Hlayout3 = QtGui.QHBoxLayout()
        Hlayout3.addWidget(FileLabel)
        Hlayout3.addWidget(self.FileText)

        VLayout = QtGui.QVBoxLayout()
        VLayout.addLayout(Hlayout1)
        VLayout.addLayout(Hlayout2)
        VLayout.addWidget(FileLabel)
        VLayout.addWidget(self.FileText)

        self.setLayout(VLayout)
        resultLButton.clicked.connect(self.openFile)
    def openFile(self):
        filename=QtGui.QFileDialog.getExistingDirectory(self,"choose directory",r"C:\Users\Administrator\Desktop")
        self.resultLine.setText(str(filename))


    def Run(self,maFilePath):
        mayaBatchPath = 'I:/Program Files/Autodesk/Maya2017/bin/mayabatch.exe'
        currentFolder = 'C:/Users/Mr.Wang/Desktop/BATCH'
        melFile = 'C:/Users/Mr.Wang/Desktop/BATCH/exportAbc.mel'
        filters = self.filterLine.text()
        publishPath = self.resultLine.text()
        cmd = '"{mayaBatchPath}" -script "{melFile}" "{publishPath}" "{filters}" "{maPath}" "{currentFolder}"'.format(
            mayaBatchPath = mayaBatchPath,
            melFile = melFile,
            publishPath = publishPath,
            filters = filters,
            maPath = maFilePath,
            currentFolder = currentFolder,
            )

        subprocess.call(cmd,shell=True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    ex = MainView()
    ex.setStyleSheet(styleData)
    ex.show()
    sys.exit(app.exec_())



# mayaBatchPath = 'I:/Program Files/Autodesk/Maya2017/bin/mayabatch.exe'
# currentFolder = 'C:/Users/Mr.Wang/Desktop/BATCH'
# melFile = 'C:/Users/Mr.Wang/Desktop/BATCH/exportGpu.mel'
# filters = 'Wang'
#
# maFilePath = str(['C:/Users/Mr.Wang/Desktop/code.ma','C:/Users/Mr.Wang/Desktop/code2.ma'])
# publishPath = 'C:/Users/Mr.Wang/Desktop/code.abc'
#
#
# cmd = '"{mayaBatchPath}" -script "{melFile}" "{publishPath}" "{filters}" "{maPath}" "{currentFolder}"'.format(
#     mayaBatchPath = mayaBatchPath,
#     melFile = melFile,
#     publishPath = publishPath,
#     filters = filters,
#     maPath = maFilePath,
#     currentFolder = currentFolder,
#     )
#
# subprocess.call(cmd,shell=True)
