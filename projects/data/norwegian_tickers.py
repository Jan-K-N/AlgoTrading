"""
Class to print Norwegian tickers other than the
ones from the scraper.
"""

from typing import List
# pylint: disable=too-few-public-methods
class TickerCodeProvider:
    """
    A class for providing a list of additional Norwegian ticker codes.

    Attributes:
        None

    Methods:
        get_ticker_codes(): Get a list of additional Norwegian ticker codes.

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
        ticker_codes_additional = ["PGS.OL","ADE.OL","HAFNI.OL","KAHOT.OL",
                                   "VAR.OL","SOFF.OL","MPCC.OL","GOGL.OL",
                                   "KOG.OL","NOD.OL","AKSO.OL","NAS.OL",
                                   "SHLF.OL","CRAYN.OL","BORR.OL","BWLPG.OL",
                                   "ELK.OL","DOFG.OL","SRBNK.OL","SCHB.OL",
                                   "OET.OL","SNI.OL","SDRL.OL","NYKD.OL",
                                   "OKEA.OL","FLNG.OL","AKH.OL","SCATC.OL",
                                   "NSKOG.OL","ELMRA.OL","HEX.OL","HAUTO.OL",
                                   "HAUTO.OL","AUSS.OL","EPR.OL","ODL.OL",
                                   "AUTO.OL","QFR.OL","BRG.OL","LINK.OL",
                                   "AGAS.OL","ULTI.OL","GSF.OL","PEN.OL",
                                   "PROT.OL","MING.OL","RECSI.OL","VEI.OL",
                                   "NEXT.OL","WAWI.OL","PHO.OL","KIT.CO"
        ]
        return ticker_codes_additional