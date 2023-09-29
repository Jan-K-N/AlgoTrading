"""
Class to print Danish tickers other than the
ones from the scraper.
"""

from typing import List
# pylint: disable=too-few-public-methods
class TickerCodeProvider:
    """
    A class for providing a list of additional Danish ticker codes.

    Attributes:
        None

    Methods:
        get_ticker_codes(): Get a list of additional Danish ticker codes.

    Example:
        To get the list of ticker codes, create an instance of this class
        and call the get_ticker_codes() method:

        >>> ticker_provider = TickerCodeProvider()
        >>> ticker_codes = ticker_provider.get_ticker_codes()
        >>> print(ticker_codes)
    """
    @staticmethod
    def get_ticker_codes() -> List[str]:
        """
        Get a list of additional ticker codes.

        Returns:
            List[str]: A list of ticker codes.
        """
        ticker_codes_additional = [
            "AAB.CO", "AGAT.CO", "AGF-B.CO", "AGILC.CO", "ALEFRM.CO",
            "AQP.CO", "ASTK.CO", "ASTRLS.CO", "ATLA-DKK.CO", "AUDNTS.CO",
            "BACTIQ.CO", "BO.CO", "BNORDIK-CSE.CO", "BIOPOR.CO", "BRAINP.CO",
            "KLEE-B.CO", "AOJ-B.CO", "HART.CO", "BIF.CO", "CBRAIN.CO",
            "CEMAT.CO", "CESSA.CO", "COLUM.CO", "CONFRZ.CO",
            "CPHCAP-PREF32.CO", "CPHCAP-PREF.CO", "CPHCAP-ST.CO", "CSMED.CO",
            "CURAS.CO", "DANCAN.CO", "DAC.CO", "DAB.CO", "DANT.CO",
            "DATA.CO", "ACT.CO", "DJUR.CO", "DONKEY.CO", "EAC.CO",
            "EGNETY.CO", "ESG.CO", "ERRIA.CO", "FED.CO", "FASTPC.CO",
            "FFARMS.CO", "FLUG-B.CO", "FOM.CO", "FREETR.CO", "FYNBK.CO",
            "GABR.CO", "GERHSP.CO", "GJ.CO", "GREENH.CO", "GREENM.CO",
            "GRLA.CO", "GUBRA.CO", "GYLD-A.CO", "GYLD-B.CO", "HH.CO",
            "HARB-B.CO", "HOVE.CO", "HRC.CO", "HUSCO.CO", "HVID.CO",
            "HYDRCT.CO", "HYPE.CO", "IMPERO.CO", "IMAIL.CO",
            "KONSOL.CO", "KRE.CO", "LEDIBOND.CO", "LOLB.CO",
            "LUXOR-B", "LASP.CO", "MAPS.CO", "MATAS.CO", "MDUNDO.CO",
            "MONSO.CO", "MOVINN.CO", "MTHH.CO", "MNBA.CO", "NEWCAP.CO",
            "NEXCOM.CO", "NLFSK.CO", "NNIT.CO", "NORD.CO", "NRDF.CO",
            "NORDIC.CO", "NORTHM.CO", "NTR-B.CO", "ODICO.CO", "YOYO.CO",
            "ORPHA.CO", "PARKST-A.CO", "PARKEN.CO", "PENNEO.CO",
            "PAAL-B.CO", "PEG.CO", "PRIMOF.CO", "QINTER.CO", "RELE.CO"
        ]
        return ticker_codes_additional
