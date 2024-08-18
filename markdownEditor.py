from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QAction, QFileDialog, QMessageBox, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown
import sys

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Markdown Editor")
        self.setGeometry(100, 100, 800, 600)

        self.editor = QTextEdit()
        self.preview = QWebEngineView()

        self.is_modified = False
        self.current_file = None

        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        layout.addWidget(self.preview)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.editor.textChanged.connect(self.update_preview)
        self.editor.textChanged.connect(self.set_modified)

        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("File")

        self.save_action = QAction("Save", self)
        self.open_action = QAction("Open", self)
        self.exit_action = QAction("Exit", self)

        self.save_action.triggered.connect(self.save_file)
        self.open_action.triggered.connect(self.open_file)
        self.exit_action.triggered.connect(self.close)

        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(self.save_file)

    def update_preview(self):
        markdown_text = self.editor.toPlainText()

        html_text = markdown.markdown(markdown_text)

        self.preview.setHtml(html_text)

    def set_modified(self):
        self.is_modified = True

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                file.write(self.editor.toPlainText())
            self.is_modified = False
        else:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Markdown Files (*.md);;All Files (*)", options=options)
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(self.editor.toPlainText())
                self.is_modified = False
                self.current_file = file_name

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Markdown Files (*.md);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.editor.setText(file.read())
            self.is_modified = False
            self.current_file = file_name

    def closeEvent(self, event):
        if self.is_modified:
            reply = QMessageBox.question(self, 'Unsaved Changes',
                                         'You have unsaved changes. Do you want to save them before exiting?',
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                         QMessageBox.Save)
            if reply == QMessageBox.Save:
                self.save_file()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec_())
