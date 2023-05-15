import sys
import json
import yaml
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog


def load_json(file_path):
    """Funkcja wczytująca dane z pliku JSON."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def save_json(file_path, data):
    """Funkcja zapisująca dane do pliku JSON."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def load_yaml(file_path):
    """Funkcja wczytująca dane z pliku YAML."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


def save_yaml(file_path, data):
    """Funkcja zapisująca dane do pliku YAML."""
    with open(file_path, 'w') as file:
        yaml.dump(data, file)


def load_xml(file_path):
    """Funkcja wczytująca dane z pliku XML."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = element_to_dict(root)
    return data


def element_to_dict(element):
    """Funkcja pomocnicza przekształcająca obiekt typu Element na słownik."""
    if len(element) == 0:
        return element.text

    result = {}
    for child in element:
        child_data = element_to_dict(child)
        if child.tag not in result:
            result[child.tag] = child_data
        elif type(result[child.tag]) is list:
            result[child.tag].append(child_data)
        else:
            result[child.tag] = [result[child.tag], child_data]
    return result


def save_xml(file_path, data):
    """Funkcja zapisująca dane do pliku XML."""
    root_element = dict_to_element(data)
    tree = ET.ElementTree(root_element)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


def dict_to_element(data):
    """Funkcja pomocnicza przekształcająca słownik na obiekt typu Element."""
    if isinstance(data, dict):
        element = ET.Element('root')
        for key, value in data.items():
            sub_element = dict_to_element(value)
            sub_element.tag = key
            element.append(sub_element)
        return element
    else:
        element = ET.Element('item')
        element.text = str(data)
        return element


class ConverterWindow(QMainWindow):
    """Klasa reprezentująca okno główne programu."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Konwerter danych')
        self.setMinimumWidth(400)

        self.input_path = None
        self.output_path = None

        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.input_label = QLabel('Ścieżka pliku wejściowego:')
        self.input_line_edit = QLineEdit()
        self.input_line_edit.setReadOnly(True)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_line_edit)

        self.browse_input_button = QPushButton('Przeglądaj')
        self.browse_input_button.clicked.connect(self.browse_input_file)
        self.layout.addWidget(self.browse_input_button)

        self.output_label = QLabel('Ścieżka pliku wyjściowego:')
        self.output_line_edit = QLineEdit()
        self.output_line_edit.setReadOnly(True)
        self.layout.addWidget(self.output_label)
        self.layout.addWidget(self.output_line_edit)

        self.browse_output_button = QPushButton('Przeglądaj')
        self.browse_output_button.clicked.connect(self.browse_output_file)
        self.layout.addWidget(self.browse_output_button)

        self.convert_button = QPushButton('Konwertuj')
        self.convert_button.clicked.connect(self.convert_data)
        self.layout.addWidget(self.convert_button)

    def browse_input_file(self):
        """Funkcja obsługująca przeglądanie pliku wejściowego."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Wybierz plik')
        if file_path:
            self.input_path = file_path
            self.input_line_edit.setText(file_path)

    def browse_output_file(self):
        """Funkcja obsługująca przeglądanie pliku wyjściowego."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'Wybierz plik')
        if file_path:
            self.output_path = file_path
            self.output_line_edit.setText(file_path)

    def convert_data(self):
        """Funkcja obsługująca konwersję danych."""
        if not self.input_path or not self.output_path:
            return

        input_file_extension = self.input_path.split('.')[-1].lower()
        output_file_extension = self.output_path.split('.')[-1].lower()

        if input_file_extension == 'json':
            data = load_json(self.input_path)
        elif input_file_extension == 'yaml' or input_file_extension == 'yml':
            data = load_yaml(self.input_path)
        elif input_file_extension == 'xml':
            data = load_xml(self.input_path)
        else:
            print('Nieobsługiwany format pliku wejściowego')
            return

        if output_file_extension == 'json':
            save_json(self.output_path, data)
        elif output_file_extension == 'yaml' or output_file_extension == 'yml':
            save_yaml(self.output_path, data)
        elif output_file_extension == 'xml':
            save_xml(self.output_path, data)
        else:
            print('Nieobsługiwany format pliku wyjściowego')
            return

        print('Konwersja zakończona sukcesem')
