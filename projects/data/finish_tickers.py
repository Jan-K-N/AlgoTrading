"""
Class to print Finish tickers other than the
ones from the scraper.
"""

from typing import List
# pylint: disable=too-few-public-methods
class TickerCodeProvider:
    """
    A class for providing a list of additional Finish ticker codes.

    Attributes:
        None

    Methods:
        get_ticker_codes(): Get a list of additional Finish ticker codes.

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
        ticker_codes_additional = ["MANTA.HE", "NDA-FI.HE", "SAMPO.HE", "FORTUM.HE",
                                   "NOKIA.HE", "NESTE.HE", "STERV.HE", "UPM.HE",
                                   "KNEBV.HE", "TYRES.HE", "WRT1V.HE", "METSO.HE",
                                   "KESKOB.HE", "VALMT.HE", "OUT1V.HE", "ORNBV.HE",
                                   "QTCOM.HE", "KEMPOWR.HE", "ELISA.HE", "KCR.HE",
                                   "TIETO.HE", "HUH1V.HE", "TELIA1.HE", "METSB.HE",
                                   "UPONOR.HE", "KOJAMO.HE", "CGCBV.HE", "SSABBH.HE",
                                   "PUUILO.HE", "CTY1S.HE", "UNITED.HE", "KEMIRA.HE",
                                   "YIT.HE", "STOCKA.HE", "REG1V.HE", "MUSTI.HE",
                                   "ORNAV.HE", "TOKMAN.HE", "KESKOA.HE", "ICP1V.HE",
                                   "HARVIA.HE", "AKTIA.HE", "TNOM.HE", "ADMCM.HE",
                                   "OMASP.HE", "ANORA.HE", "FSECURE.HE", "FIA1S.HE",
                                   "SANOMA.HE", "TTALO.HE", "OKDBV.HE", "CAPMAN.HE",
                                   "ENENTO.HE", "CAV1V.HE", "OPTOMED.HE", "KAMUX.HE",
                                   "VAIAS.HE", "FARON.HE", "MEKKO.HE", "HEALTH.HE",
                                   "EXL1V.HE", "ROVIO.HE", "STEAV.HE", "FSKRS.HE",
                                   "OLVAS.HE", "WITH.HE", "KHG.HE", "SPINN.HE",
                                   "GOFORE.HE", "REKA.HE", "TAALA.HE", "REMEDY.HE",
                                   "VINCIT.HE", "SCANFL.HE", "SOSI1.HE", "BRETEC.HE",
                                   "RAIVV.HE", "ASPO.HE", "LAT1V.HE", "CTH1V.HE",
                                   "ESENSE.HE", "DUELL.HE", "EFECTE.HE", "TITAN.HE",
                                   "SSABAH.HE", "TEM1V.HE", "EQV1V.HE", "PON1V.HE",
                                   "MODU.HE", "ALMA.HE", "KSLAV.HE", "MERUS.HE",
                                   "METSA.HE", "NXTMH.HE", "NYAB.HE", "SUY1V.HE",
                                   "AIFORIA.HE", "ATRAV.HE", "LEMON.HE", "ALBAV.HE",
                                   "WITTED.HE",
                                   "DIGIA.HE", "OVARO.HE", "VERK.HE", "NOHO.HE",
                                   "OKDAV.HE", "BITTI.HE", "SSH1V.HE", "ALBBV.HE",
                                   "EEZY.HE", "TALLINK.HE", "BONEH.HE", "NIXU.HE",
                                   "ALEX.HE", "LIFA.HE", "LOIHDE.HE", "MERIH.HE",
                                   "AFAGR.HE", "HRTIS.HE", "SIILI.HE", "SOLTEQ.HE",
                                   "VALOE.HE", "RAUTE.HE", "DOV1V.HE", "IFA1V.HE",
                                   "PIHLIS.HE", "ACG1V.HE", "EVLI.HE", "PAMPALO.HE",
                                   "WETTERI.HE", "ORTHEX.HE", "TOIVO.HE", "KOSKI.HE",
                                   "DETEC.HE", "ROBIT.HE", "NETUM.HE", "PURMO.HE",
                                   "AALLON.HE", "WUF1V.HE", "FONDIA.HE", "TULAV.HE",
                                   "ALISA.HE", "LEHTO.HE", "BETOLAR.HE", "FODELIA.HE",
                                   "TLT1V.HE", "KREATE.HE", "GLA1V.HE", "ADMIN.HE",
                                   "VIK1V.HE", "TAMTRON.HE", "HKSAV.HE", "DWF.HE",
                                   "ECOUP.HE", "INDERES.HE", "ETTE.HE", "HONBS.HE",
                                   "NLG1V.HE", "ILKKA2.HE", "PNA1V.HE", "RUSH.HE",
                                   "PARTNE1.HE", "APETIT.HE", "NORRH.HE", "RAP1V.HE",
                                   "LEADD.HE", "ELEAV.HE", "KELAS.HE", "MARAS.HE",
                                   "LAPWALL.HE", "QPR1V.HE", "BIOBV.HE", "FIFAX.HE",
                                   "SRV1V.HE", "SPRING.HE", "SITOWS.HE", "ASUNTO.HE",
                                   "BOREO.HE", "CONSTI.HE", "EAGLE.HE", "INVEST.HE",
                                   "SOLWERS.HE", "DIGIGR.HE", "PUMU.HE", "RELAIS.HE",
                                   "SAGCV.HE", "PIIPPO.HE", "TRH1V.HE",
                                   "HEEROS.HE", "NORDLIG.HE", "VIAFIN.HE"
                                   ]

        return ticker_codes_additional