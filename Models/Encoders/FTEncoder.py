from Models.Encoders import PerYearEncoder

__author__ = 'Daniyar'

class FTEncoder:
    @staticmethod
    def Encode(ft):
        return {"company_name": ft.company_name, "date_created": str(ft.date_created), "data": PerYearEncoder.PerYearEncoder.Encode(ft.data)}