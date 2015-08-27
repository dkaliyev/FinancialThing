__author__ = 'Daniyar'

class DataEncoder:

	name_to_code = {
	"ASSETS": "assets",
	"Cash And Short Term Investments": "cashInv",
	"Total Receivables, Net": "ttlRec",
	"Total Inventory": "ttlInv",
	"Prepaid"
	"LIABILITIES": "liabt",
	""
	}

    @staticmethod
    def Encode(data):
        return {"name": data.name, "value": data.value}