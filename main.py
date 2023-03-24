import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QPushButton
import PyQt5.QtCore

from decode import get_data
from RSpinBox import RangedSpinBox


class Decoder(QWidget):

    def __init__(self, data_file, n_samples, max_n, space_thres):
        super().__init__()
        self.data = get_data(data_file, n_samples, max_n, space_thres)
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        # creating row of sliders
        key = self.data['key']
        probable_key = self.data['probable_key']
        self.key = key
        for i in range(len(key)):
            sb = RangedSpinBox(probable_key[i])

            sb.setMaximum(255)
            sb.setMaximumWidth(40)
            sb.setValue(key[i])
            sb.newValueChanged.connect(
                lambda value, idx=i: self.update_samples(idx, value))
            grid.addWidget(sb, 0, i)

        # create rows of decoded samples
        samples = self.data['samples']
        self.samples = samples
        self.labels = [[] for _x in range(len(samples))]
        for r in range(len(samples)):
            for i in range(len(samples[0])):
                ch = chr(self.key[i] ^ self.samples[r][i])
                label = QLabel(ch)
                label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
                self.labels[r].append(label)
                grid.addWidget(label, 1 + r, i)

        # add decoded cipher row
        label = QLabel("Cipher")
        grid.addWidget(label, len(samples) + 1, 0, 1, 3)

        # add cipher letters
        self.cipher_labels = []
        cipher = self.data['cipher']
        self.cipher = cipher
        for i in range(len(cipher)):
            ch = chr(self.key[i] ^ self.cipher[i])
            label = QLabel(ch)
            label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
            self.cipher_labels.append(label)
            grid.addWidget(label, 2 + len(samples), i)

        # add copy button
        button = QPushButton("Copy result to clipboard")
        button.clicked.connect(self.copy_result)
        grid.addWidget(button, 3 + len(samples), 0, 1, 4)

        self.setWindowTitle('Decoder')
        self.show()

    def update_samples(self, i, value):
        # update column i when slider value changed
        self.key[i] = value
        for r in range(len(self.samples)):
            self.labels[r][i].setText(chr(self.samples[r][i] ^ self.key[i]))

        if i < len(self.cipher_labels):
            self.cipher_labels[i].setText(chr(self.cipher[i] ^ self.key[i]))

    def copy_result(self):
        # copy result to clipboard
        decoded = "".join([chr(self.cipher[i] ^ self.key[i])
                          for i in range(len(self.cipher))])
        QApplication.clipboard().setText(decoded)


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 5:
        data_file = sys.argv[1]
        n_samples = int(sys.argv[2])
        max_n = int(sys.argv[3])
        space_thres = int(sys.argv[4])
        # launch decoder
        app = QApplication(sys.argv)
        ex = Decoder(data_file, n_samples, max_n, space_thres)
        sys.exit(app.exec_())
    else:
        print("Wrong syntax!")
        print("Usage:")
        print("$ python main.py DATA_FILE N_SAMPLES MAX_N SPACE_THRES")
        print("\tDATA_FILE: STR - path to data file")
        print("\tN_SAMPLES: INT - number of cipher texts encoded with the same key")
        print("\tMAX_N: INT - limit of guessing iterations. Recomended: 5000")
        print("\tSPACE_THRES: INT - minimal score to determine if char is a space. Recomended: 8")

