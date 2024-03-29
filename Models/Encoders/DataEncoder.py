__author__ = 'Daniyar'

class DataEncoder:
	name_to_code = {
	"Balance Sheet": "BalanceSheet",
	"Income Statement": "IncomeStatement",
	"Cash Flow": "CashFlow",
	"ASSETS": "assets",
	"Cash And Short Term Investments": "cashInv",
	"Total Receivables, Net": "ttlRec",
	"Total Inventory": "ttlInv",
	"Prepaid expenses": "prepaidExp",
	"Other current assets, total": "otherAss",
	"Total current assets": "totalCurAss",
	"Property, plant & equipment, net": "propNet",
	"Goodwill, net": "goodwill",
	"Intangibles, net": "intangibles",
	"Long term investments": "longInv",
	"Note receivable - long term": "noteRec",
	"Other long term assets": "otherLong",
	"Total assets": "totalAss",
	"LIABILITIES": "liab",
	"Accounts payable": "accPay",
	"Accrued expenses": "accrued",
	"Notes payable/short-term debt": "notesDebt",
	"Current portion long-term debt/capital leases": "portion",
	"Other current liabilities, total": "currLiab",
	"Total current liabilities": "totalCurLiab",
	"Total long term debt": "debtLiab",
	"Total debt": "totalLiabDebt",
	"Deferred income tax": "defferedTax",
	"Minority interest": "minorInt",
	"Other liabilities, total": "otherLiab",
	"Total liabilities": "totalLiab",
	"SHAREHOLDERS EQUITY": "shareEqu",
	"Common stock": "comStock",
	"Additional paid-in capital": "addCap",
	"Retained earnings (accumulated deficit)": "retEarn",
	"Treasury stock - common": "treasury",
	"Unrealized gain (loss)": "gainLoss",
	"Other equity, total": "otherEq",
	"Total equity": "totalEq",
	"Total liabilities & shareholders' equity": "totalLiabEq",
	"Total common shares outstanding": "totalShares",
	"Treasury shares - common primary issue": "treasShares",
	"OPERATIONS": "operations",
	"Net income": "netInc",
	"Depreciation/depletion": "depr",
	"Non-Cash items": "nonCash",
	"Cash taxes paid, supplemental": "cashTax",
	"Cash interest paid, supplemental": "cashPaid",
	"Changes in working capital": "changes",
	"Total cash from operations": "cashOper",
	"INVESTING": "investing",
	"Capital expenditures": "capExp",
	"Other investing and cash flow items, total": "otherInv",
	"Total cash from investing": "totalInv",
	"FINANCING": "financing",
	"Financing cash flow items": "finCash",
	"Total cash dividends paid": "totalDiv",
	"Issuance (retirement) of stock, net": "issuanceStock",
	"Issuance (retirement) of debt, net": "issuanceDebt",
	"Total cash from financing": "totalFinCash",
	"NET CHANGE IN CASH": "netChangeTitle",
	"Foreign exchange effects": "forExc",
	"Net change in cash": "netChange",
	"Net cash-begin balance/reserved for future use": "netCashBegin",
	"Net cash-end balance/reserved for future use": "netCashEnd",
	"SUPPLEMENTAL INCOME": "suplInc",
	"Depreciation, supplemental": "depSupl",
	"REVENUE AND GROSS PROFIT": "revenueGross",
	"Total revenue": "totalRev",
	"OPERATING EXPENSES": "operExp",
	"Cost of revenue total": "revTotalCost",
	"Selling, general and admin. expenses, total": "sellingTotal",
	"Depreciation/amortization": "deprAmor",
	"Unusual expense(income)": "unusualExp",
	"Other operating expenses, total": "otherOperExp",
	"Total operating expense": "totalOperExp",
	"Operating income": "operInc",
	"Other, net": "otherNet",
	"INCOME TAXES, MINORITY INTEREST AND EXTRA ITEMS": "incTaxes",
	"Net income before taxes": "netIncBeforeTax",
	"Provision for income taxes": "incTaxProv",
	"Net income after taxes": "netIncAfterTax",
	"Net income before extra. Items": "netIncBeforeExt",
	"Total extraordinary items": "totalExtror",
	"Inc.avail. to common excl. extra. Items": "inclToComIncl",
	"Inc.avail. to common incl. extra. Items": "inclToComExcl",
	"EPS RECONCILIATION": "epsRecon",
	"Basic/primary weighted average shares": "basicWeigh",
	"Basic/primary eps excl. extra items": "epsExcl",
	"Basic/primary eps incl. extra items": "epsIncl",
	"Dilution adjustment": "dilutionAdj",
	"Diluted weighted average shares": "dilutedWeigh",
	"Diluted eps excl. extra items": "dilutedExcl",
	"Diluted eps incl. extra items": "dilutedIncl",
	"COMMON STOCK DIVIDENDS": "commonStDiv",
	"DPS - common stock primary issue": "DPS",
	"Gross dividend - common stock": "grossDiv",
	"PRO FORMA INCOME": "proForma",
	"Pro forma net income": "proFormaIncNet",
	"Interest expense, supplemental": "interExp",
	"Total special items": "totalSpecItems",
	"NORMALIZED INCOME":"normInc",
	"Normalized income before taxes": "normIncBeforeTax",
	"Effect of special items on income taxes": "specItemEff",
	"Income tax excluding impact of special items": "incTaxExcl",
	"Normalized income after tax": "normIncAfterTax",
	"Normalized income avail. to common": "normIncAvail",
	"Basic normalized EPS": "basicNormEps",
	"Diluted normalized EPS": "dilutedNormEps"
	}

	@classmethod
	def Decode(data, codes):
		newData = {}
		for key, value in data.iteritems():
			if isinstance(value, dict) and key in codes.keys():
				value = Decode(value, codes)
			if key in codes.keys():
				newData[codes[key]] = value
		return newData