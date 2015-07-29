from Models.Encoders import DataTypeEncoder

__author__ = 'Daniyar'

class ReportEncoder:
    @staticmethod
    def Encode(report):
        return {"name": report.name, "data": DataTypeEncoder.DataTypeEncoder.Encode(report.data)}