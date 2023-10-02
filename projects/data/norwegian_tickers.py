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
        ticker_codes_additional = ["EQNR.OL", "AKRBP.OL", "FRO.OL", "DNB.OL", "PGS.OL",
                                   "NHY.OL", "DNO.OL", "DOFG.OL", "TGS.OL", "SOFF.OL", "MOWI.OL", "KOG.OL", "YAR.OL",
                                   "ZAP.OL", "SALM.OL", "TOM.OL", "TEL.OL", "AKSO.OL", "MPCC.OL", "HAFNI.OL", "SDRL.OL",
                                   "VAR.OL", "NAS.OL", "NEL.OL", "SHLF.OL", "SNI.OL", "ORK.OL", "SUBC.OL", "NOD.OL",
                                   "NSKOG.OL", "HKY.OL", "BAKKA.OL", "KAHOT.OL",
                                   "ELMRA.OL", "GOGL.OL", "ARGEO.OL",
                                   "RECSI.OL", "CRAYN.OL", "AKH.OL", "GJF.OL",
                                   "GCC.OL", "STB.OL", "ELK.OL", "EPR.OL",
                                   "BORR.OL", "KIT.OL", "ULTI.OL", "LINK.OL",
                                   "ADE.OL", "LSG.OL", "OKEA.OL", "SCHA.OL",
                                   "SALME.OL", "SRBNK.OL", "BWLPG.OL", "BWO.OL", "AMSC.OL", "CLCO.OL", "AKER.OL",
                                   "NORAM.OL", "PHO.OL", "ODL.OL", "BONHR.OL", "KCC.OL", "HPUR.OL", "NOM.OL", "VOW.OL",
                                   "2020.OL", "HAUTO.OL", "PNOR.OL", "OTL.OL", "HEX.OL", "AGAS.OL", "SCATC.OL",
                                   "OET.OL", "PEN.OL", "PROT.OL", "NODL.OL", "NONG.OL", "WAWI.OL", "LIFE.OL",
                                   "NORSE.OL", "SBX.OL", "STSU.OL", "SIOFF.OL", "AUSS.OL", "DDRIL.OL", "BRG.OL",
                                   "SCHB.OL", "SDNS.OL", "ENTRA.OL", "GSF.OL", "SVEG.OL", "MING.OL", "IDEX.OL",
                                   "VEI.OL", "NYKD.OL", "PRS.OL", "ENSU.OL", "HYPRO.OL","ARCH.OL", "ACC.OL", "KOA.OL",
                                   "CLOUD.OL", "SEAPT.OL", "TRMED.OL", "PARB.OL", "NEXT.OL",
                                   "AGLX.OL", "EIOF.OL", "WEST.OL",
                                   "CADLR.OL", "BELCO.OL", "AFK.OL", "AUTO.OL", "GIG.OL", "AKAST.OL", "PLT.OL",
                                   "BGBIO.OL", "SSG.OL", "FLNG.OL", "SDSD.OL", "ODF.OL", "WPU.OL", "VGM.OL", "MGN.OL",
                                   "ALT.OL", "BNOR.OL", "SASNO.OL", "HSHP.OL", "HAVI.OL", "MVE.OL", "DVD.OL",
                                   "TECH.OL", "TIETO.OL", "SBO.OL", "WWI.OL", "BWE.OL", "DSRT.OL", "5PG.OL",
                                   "ODFB.OL", "EWIND.OL", "ATEA.OL", "AZT.OL", "ITERA.OL", "AFG.OL", "BOUV.OL",
                                   "VOLUE.OL", "RANA.OL", "GEOS.OL", "ASA.OL", "NAVA.OL", "OTOVO.OL",
                                   "ALNG.OL", "SATS.OL", "BOR.OL", "REACH.OL", "MNTR.OL", "BCS.OL", "QFR.OL",
                                   "WSTEP.OL", "NKR.OL", "ASTK.OL", "NTI.OL", "ENDUR.OL", "RCR.OL", "MOBA.OL",
                                   "PEXIP.OL", "PCIB.OL", "XXL.OL", "SIKRI.OL", "OLT.OL", "BMA.OL", "LYTIX.OL",
                                   "CAMBI.OL", "CODE.OL", "NORBT.OL", "EMGS.OL", "BWIDL.OL", "BEWI.OL", "MAS.OL",
                                   "ELIMP.OL", "KID.OL", "KMCP.OL", "ELABS.OL", "SPOL.OL", "VISTN.OL", "EFUEL.OL",
                                   "CARA.OL", "CONTX.OL", "ZAL.OL", "GOD.OL", "ARR.OL", "ASTRO.OL", "CRNA.OL",
                                   "HMONY.OL", "MORG.OL", "ANDF.OL", "MVW.OL", "STRO.OL"]




        return ticker_codes_additional