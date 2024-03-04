from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import requests
import pandas as pd

class MainView(QDialog):
    def __init__(self):
        super().__init__()

        # MEMBER
        self.btcPriceLabel = QLabel(self)
        self.fluctuationLabel = QLabel(self)
        self.fluctuationLabel.setAlignment(Qt.AlignRight)
        self.entryPriceEdit = QLineEdit(self)
        self.timer = QTimer(self)

        # INIT
        self.initUI()

        # CONNECT
        self.timer.timeout.connect(self.updateBtcPrice)
        self.timer.start(1000)
        self.updateBtcPrice()

    def updateBtcPrice(self):
        url = "https://www.binance.com/api/v3/uiKlines?limit=1000&symbol=BTCUSDT&interval=1s"
        headers = {"User-Agent": 
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
        res = requests.get(url, headers=headers)
        # res.raise_for_status()

        value = res.json()
        df = pd.DataFrame(value)
        indexPrice = float(df.iloc[999][1])

        self.btcPriceLabel.setText(str(round(indexPrice, 2)))

        entryPrice = self.entryPriceEdit.text()
        if entryPrice == "":
            self.fluctuationLabel.setText("")
            return
        else:
            entryPrice = float(entryPrice)
        fluctuation = indexPrice / entryPrice * 100.0 - 100.0
        self.fluctuationLabel.setText(str(round(fluctuation, 2)) + "%")

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.btcPriceLabel,      0, 0, 1, 1)
        grid.addWidget(self.fluctuationLabel,   0, 1, 1, 1)
        grid.addWidget(self.entryPriceEdit,     1, 0, 1, 2)

        self.setLayout(grid)

        self.setWindowTitle("Bit")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
