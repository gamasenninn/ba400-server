conf={
  "device": {
    "ip": "192.168.11.205",
    "port": "9100",
    "isPrintOut": "False",
    "isImage": "True"
  },
  "setLabel": {
    "pitch": "0830",
    "width": "1057",
    "height": "0750"
  },
  "setFormat": {
    "bufferClear": "True",
    "PC": [
      {
        "number": "001",
        "x": "0035",
        "y": "0090",
        "xR": "15",
        "yR": "15",
        "fontType": "K",
        "fontSpace": "00",
        "fontDeco": "B"
      },
      {
        "number": "002",
        "x": "0500",
        "y": "0070",
        "xR": "1",
        "yR": "1",
        "fontType": "i",
        "fontSpace": "00",
        "fontDeco": "B"
      },
      {
        "number": "003",
        "x": "0035",
        "y": "0150",
        "xR": "1",
        "yR": "1",
        "fontType": "j",
        "fontSpace": "00",
        "fontDeco": "B",
        "autoLineFeed": {
          "width": "0430",
          "pitch": "045",
          "rowMax": "02"
        }
      }
    ],
    "XB_QR": [
      {
        "number": "01",
        "x": "0510",
        "y": "0100",
        "errorLevel": "M",
        "cellSize": "07",
        "mode": "A",
        "rotation": "0",
        "model": "M2"
      }
    ],
    "XB_BAR": [
      {
        "number": "02",
        "x": "0035",
        "y": "0200",
        "type": "9",
        "digit": "3",
        "width": "05",
        "rotation": "0",
        "height": "0100",
        "outNumber": "1",
        "zeroSup": "00"
      }
    ]
  },
  "fields": [
    {
      "command": "RC",
      "number": "001",
      "bind": "scode",
      "default": "14687-1"
    },
    {
      "command": "RC",
      "number": "002",
      "bind": "datePerson",
      "default": "2020/12/22 田中"
    },
    {
      "command": "RC",
      "number": "003",
      "bind": "title",
      "default": "コンバインAA580 58馬力 クボタ 3条刈 自動水平"
    },
    {
      "command": "RB",
      "number": "01",
      "bind": "qrData",
      "default": "https://www.google.com/search?q=%E9%A3%9B%E8%A1%8C%E8%88%B9"
    },
    {
      "command": "RB",
      "number": "02",
      "bind": "scode",
      "default": "12345-1"
    },
    {
      "command": "XS",
      "copies": "0001",
      "cutInterval": "000",
      "censorType": "2",
      "mode": "C",
      "speed": "2",
      "ribbon": "2",
      "tagRotation": "0",
      "statusResponse": "0"
    }
  ],
  "data": [
    {
      "scode": "14687-1",
      "datePerson": "2020/12/22 田中",
      "title": "コンバインAA580 58馬力 クボタ 3条刈 自動水平",
      "qrData": "https://www.google.com/search?q=%E9%A3%9B%E8%A1%8C%E8%88%B9"
    },
    {
      "scode": "14687-2",
      "datePerson": "2020/12/22 佐藤",
      "title": "トラクターBB999 30馬力 ヤンマー 自動水平",
      "qrData": "https://www.google.com/search?q=%E9%A3%9B%E8%A1%8C%E8%88%B9"
    }
  ],
  "final": [
    {
      "command": "IB"
    }
  ]
};