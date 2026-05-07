#!/usr/bin/env python3
import sys
import os
import subprocess
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QFileDialog, QMessageBox, QProgressBar)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class ConvertWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, model_path, output_path):
        super().__init__()
        self.model_path = model_path
        self.output_path = output_path
        self.process = None
        
    def run(self):
        try:
            self.progress.emit(10)
            
            script_content = f'''
import sys
import os
import json
import shutil

sys.path.insert(0, "{os.path.dirname(__file__)}")

from ultralytics import YOLO

model = YOLO("{self.model_path}")
print(json.dumps({{"status": "loading", "progress": 30}}))

model.export(format="onnx", opset=13, simplify=True)
print(json.dumps({{"status": "exporting", "progress": 70}}))

pt_path = "{self.model_path}".replace(".pt", ".onnx")
if os.path.exists(pt_path):
    shutil.move(pt_path, "{self.output_path}")
    print(json.dumps({{"status": "done", "progress": 100, "output": "{self.output_path}"}}))
else:
    print(json.dumps({{"status": "error", "message": "输出文件未生成"}}))
'''
            
            self.progress.emit(30)
            
            self.process = subprocess.Popen(
                [sys.executable, '-c', script_content],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(__file__)
            )
            
            self.progress.emit(40)
            
            while True:
                line = self.process.stdout.readline()
                if not line and self.process.poll() is not None:
                    break
                
                if line:
                    try:
                        data = json.loads(line.strip())
                        if 'progress' in data:
                            self.progress.emit(data['progress'])
                        if data.get('status') == 'done':
                            self.progress.emit(100)
                            self.finished.emit(True, f"模型转换成功!\n\n输出文件:\n{self.output_path}")
                            return
                        if data.get('status') == 'error':
                            self.finished.emit(False, f"转换失败: {data.get('message', '未知错误')}")
                            return
                    except:
                        pass
            
            stdout, stderr = self.process.communicate()
            
            if self.process.returncode == 0:
                if os.path.exists(self.output_path):
                    self.progress.emit(100)
                    self.finished.emit(True, f"模型转换成功!\n\n输出文件:\n{self.output_path}")
                else:
                    pt_path = self.model_path.replace('.pt', '.onnx')
                    if os.path.exists(pt_path):
                        shutil.move(pt_path, self.output_path)
                        self.progress.emit(100)
                        self.finished.emit(True, f"模型转换成功!\n\n输出文件:\n{self.output_path}")
                    else:
                        self.finished.emit(False, f"转换完成但输出文件未找到")
            else:
                error_msg = stderr if stderr else stdout
                self.finished.emit(False, f"转换失败:\n{error_msg[:1000]}")
                    
        except Exception as e:
            self.finished.emit(False, f"转换失败:\n{str(e)}")

    def stop(self):
        if self.process:
            try:
                self.process.terminate()
                self.process.wait()
            except:
                pass

class ModelConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLO 模型转 ONNX 工具")
        self.setGeometry(100, 100, 500, 350)
        self.setFixedSize(500, 350)
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title_label = QLabel("YOLO 模型转 ONNX 工具")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("输入模型文件 (.pt):"))
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("选择 YOLO 模型文件")
        input_btn = QPushButton("浏览...")
        input_btn.clicked.connect(self.select_input)
        
        input_row = QHBoxLayout()
        input_row.addWidget(self.input_edit)
        input_row.addWidget(input_btn)
        input_layout.addLayout(input_row)
        layout.addLayout(input_layout)
        
        output_layout = QVBoxLayout()
        output_layout.addWidget(QLabel("输出文件路径 (.onnx):"))
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("输出 ONNX 文件路径")
        output_btn = QPushButton("浏览...")
        output_btn.clicked.connect(self.select_output)
        
        output_row = QHBoxLayout()
        output_row.addWidget(self.output_edit)
        output_row.addWidget(output_btn)
        output_layout.addLayout(output_row)
        layout.addLayout(output_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4CAF50;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("状态: 就绪")
        self.status_label.setStyleSheet("color: #666;")
        layout.addWidget(self.status_label)
        
        button_layout = QHBoxLayout()
        self.convert_btn = QPushButton("开始转换")
        self.convert_btn.clicked.connect(self.start_convert)
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 30px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.cancel_convert)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px 30px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(self.convert_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.worker = None
        
    def select_input(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择模型文件", "", "YOLO Models (*.pt)")
        if path:
            self.input_edit.setText(path)
            auto_output = path.replace('.pt', '.onnx')
            self.output_edit.setText(auto_output)
            
    def select_output(self):
        path, _ = QFileDialog.getSaveFileName(self, "保存 ONNX 文件", "", "ONNX Files (*.onnx)")
        if path:
            if not path.endswith('.onnx'):
                path += '.onnx'
            self.output_edit.setText(path)
            
    def start_convert(self):
        model_path = self.input_edit.text().strip()
        output_path = self.output_edit.text().strip()
        
        if not model_path:
            QMessageBox.warning(self, "警告", "请选择输入模型文件")
            return
            
        if not output_path:
            QMessageBox.warning(self, "警告", "请选择输出文件路径")
            return
            
        if not os.path.exists(model_path):
            QMessageBox.warning(self, "错误", f"输入文件不存在:\n{model_path}")
            return
            
        try:
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法创建输出目录:\n{str(e)}")
            return
            
        self.convert_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("状态: 正在转换...")
        
        self.worker = ConvertWorker(model_path, output_path)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.convert_finished)
        self.worker.start()
        
    def update_progress(self, value):
        if self.progress_bar:
            self.progress_bar.setValue(value)
        
    def convert_finished(self, success, message):
        self.convert_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        if success:
            self.status_label.setText("状态: 转换完成")
            QMessageBox.information(self, "成功", message)
        else:
            self.status_label.setText("状态: 转换失败")
            QMessageBox.critical(self, "错误", message)
            
    def cancel_convert(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.convert_btn.setEnabled(True)
            self.cancel_btn.setEnabled(False)
            self.progress_bar.setVisible(False)
            self.status_label.setText("状态: 已取消")

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModelConverterGUI()
    window.show()
    sys.exit(app.exec_())