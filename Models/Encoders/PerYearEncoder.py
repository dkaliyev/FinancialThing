from Models.Encoders import ReportEncoder

__author__ = 'Daniyar'

class PerYearEncoder:
    @staticmethod
    def Encode(peryear):
        return {"year": peryear.year, "data": ReportEncoder.ReportEncoder.Encode(peryear.data)}