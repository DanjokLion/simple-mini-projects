import pyqrcode

qr = pyqrcode.create('https://github.com/DanjokLion')

qr.svg('qrcode.svg', scale=8)