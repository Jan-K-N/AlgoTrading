"""
Class to print Swedish tickers other than the
ones from the scraper.
"""

from typing import List
# pylint: disable=too-few-public-methods
class TickerCodeProvider:
    """
    A class for providing a list of additional Swedish ticker codes.

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
        ticker_codes_additional = ["INVE-B.ST", "AZN.ST", "SBB-B.ST", "ATCO-A.ST",
                                   "VOLV-B.ST", "HM-B.ST", "EVO.ST", "SHB-A.ST", "NDA-SE.ST",
                                   "ABB.ST", "SWED-A.ST", "NIBE-B.ST", "ESSITY-B.ST", "BOL.ST",
                                   "SSAB-B.ST", "SECU-B.ST", "TELIA.ST", "SKF-B.ST", "SEB-A.ST",
                                   "LOOMIS.ST", "HMS.ST", "TEL2-B.ST", "HEXA-B.ST", "SAND.ST",
                                   "INVE-A.ST", "SAAB-B.ST", "ASSA-B.ST", "ALLEI.ST", "AZA.ST",
                                   "ATCO-B.ST", "ERIC-B.ST", "SINCH.ST", "ALFA.ST", "SCA-B.ST",
                                   "AMBEA.ST", "SKA-B.ST", "LAGR-B.ST", "BILL.ST", "BEIJ-B.ST",
                                   "ELUX-B.ST", "KINV-B.ST", "EQT.ST", "SAVE.ST", "EKTA-B.ST",
                                   "EMBRAC-B.ST", "GETI-B.ST", "CALTX.ST", "BALD-B.ST", "NOLA-B.ST",
                                   "SSAB-A.ST", "CAST.ST", "TRUE-B.ST", "SOBI.ST", "SF.ST",
                                   "ANOD-B.ST", "INTRUM.ST", "ALIV-SDB.ST", "VOLCAR-B.ST",
                                   "TREL-B.ST", "CIBUS.ST", "INDU-C.ST", "HPOL-B.ST", "ADDT-B.ST",
                                   "BONEX.ST", "STOR-B.ST", "AAK.ST", "AFRY.ST", "EPI-A.ST",
                                   "NEPA.ST", "VITR.ST", "VIT-B.ST", "MTRS.ST", "LATO-B.ST",
                                   "HOLM-B.ST", "LIFCO-B.ST", "HUFV-A.ST", "VPLAY-B.ST", "HTRO.ST",
                                   "LUND-B.ST", "FABG.ST", "GRNG.ST", "AOI.ST", "INDU-A.ST",
                                   "BETS-B.ST", "JM.ST", "CINT.ST", "KIND-SDB.ST", "NEWA-B.ST",
                                   "AXFO.ST", "THULE.ST", "TIGO-SDB.ST", "EPI-B.ST", "FNOX.ST",
                                   "HUSQ-B.ST", "IPCO.ST", "INWI.ST", "MIPS.ST", "CAMX.ST",
                                   "STAR-B.ST", "LUMI.ST","LUMI.ST", "SECARE.ST", "WALL-B.ST",
                                   "SAGA-B.ST", "OX2.ST", "MYCR.ST", "PEAB-B.ST", "CLAS-B.ST",
                                   "RAY-B.ST", "LIAB.ST", "PCELL.ST", "XVIVO.ST", "STE-R.ST",
                                   "NCC-B.ST", "KAMBI.ST", "VOLV-A.ST", "AEC.ST", "DIOS.ST",
                                   "INDT.ST", "PDX.ST", "SECT-B.ST", "SBB-D.ST", "SNM.ST",
                                   "KFAST-B.ST", "BURE.ST", "INSTAL.ST", "BIOA-B.ST", "RENEW.ST",
                                   "SWEC-B.ST", "SEYE.ST", "LUG.ST", "SHOT.ST", "HEM.ST", "WIHL.ST",
                                   "ORRON.ST", "COOR.ST", "BRAV.ST", "BILI-A.ST", "PNDX-B.ST",
                                   "YUBICO.ST", "NYF.ST", "SUS.ST", "SHB-B.ST", "8TRA.ST", "DUNI.ST",
                                   "DOM.ST", "ADDV-B.ST", "ATT.ST", "SAS.ST", "SAGA-D.ST",
                                   "VEFAB.ST",
                                   "BUFAB.ST", "BETCO.ST", "ALIF-B.ST", "XBRANE.ST", "TEQ.ST", "RATO-B.ST",
                                   "SVOL-B.ST", "VIMIAN.ST", "BERG-B.ST", "VBG-B.ST", "SDIP-B.ST", "MEKO.ST",
                                   "CATE.ST", "CLA-B.ST", "NOBI.ST", "NETEL.ST", "CORE-B.ST", "BICO.ST",
                                   "NCAB.ST", "HUM.ST", "MANG.ST", "NP3.ST", "NOTE.ST", "MTG-B.ST",
                                   "CRNO-B.ST", "ALLIGO-B.ST", "GARO.ST", "IVSO.ST", "SOLT.ST", "CRED-A.ST",
                                   "NPAPER.ST", "PLAZ-B.ST", "PACT.ST", "SKIS-B.ST",
                                   "TOBII.ST", "ARJO-B.ST",
                                   "ELAN-B.ST", "NWG.ST", "HANZA.ST", "NEOBO.ST", "BONAV-B.ST", "GUARD.ST",
                                   "NETI-B.ST", "STORY-B.ST", "BHG.ST", "GENO.ST",
                                   "CTT.ST", "ACAD.ST", "RESURS.ST","VNV.ST", "OSSD.ST", "SEB-C.ST",
                                   "BIOG-B.ST", "EG7.ST", "HNSA.ST", "SEZI.ST", "TETY.ST",
                                   "FING-B.ST", "CTM.ST", "G5EN.ST", "EOLU-B.ST", "EPRO-B.ST",
                                   "TROAX.ST", "CANTA.ST", "EPEN.ST", "BFG.ST", "KAR.ST",
                                   "STABL.ST", "LIME.ST", "SYNSAM.ST", "AQ.ST", "SES.ST",
                                   "DOXA.ST", "BOOZT.ST", "HUMBLE.ST", "VOLO.ST", "RVRC.ST",
                                   "ENQ.ST", "OEM-B.ST", "B3.ST", "SYNACT.ST", "KNOW.ST",
                                   "ZZ-B.ST", "SIVE.ST", "GIGSEK.ST", "FAG.ST", "BIOT.ST",
                                   "DUST.ST", "NORB-B.ST", "DVYSR.ST", "QLINEA.ST",
                                   "ATRLJ-B.ST", "COIC.ST", "W5.ST", "BULTEN.ST", "MAVEN.ST",
                                   "PREV-B.ST", "RAKE.ST", "MCOV-B.ST", "BEIA-B.ST",
                                   "BAHN-B.ST", "ESSITY-A.ST", "CLS-B.ST", "BMAX.ST", "CS.ST",
                                   "LOGI-B.ST", "SYSR.ST", "ESGR-B.ST", "MAHA-A.ST", "MMGR-B.ST",
                                   "PRIC-B.ST", "HOFI.ST", "VESTUM.ST", "ENEA.ST", "ALIG.ST",
                                   "SEDANA.ST", "COPP-B.ST", "BRAIN.ST", "LYKO-A.ST", "CEVI.ST",
                                   "ENGCON-B.ST", "KABE-B.ST", "ERIC-A.ST", "IMMU.ST",
                                   "LUMITO.ST", "ONCO.ST", "NEXAM.ST", "CORE-D.ST",
                                   "EGTX.ST", "ABSO.ST", "CRAD-B.ST", "IDUN-B.ST", "K2A-PREF.ST",
                                   "FPAR-A.ST", "XANO-B.ST", "IMP-A-SDB.ST", "HEBA-B.ST", "BEGR.ST",
                                   "FG.ST", "STWK.ST", "MCAP.ST", "RROS.ST", "HEIM-PREF.ST",
                                   "ORT-B.ST", "PRO.ST", "LUMEN.ST", "ZAZZ-B.ST", "NMAN.ST", "KAN.ST",
                                   "DEDI.ST", "ARP.ST", "BUSER.ST", "DE.ST", "TDVOX.ST", "ITAB.ST", "SCST.ST", "INT.ST",
                                   "ASTOR.ST", "SCIB.ST", "KINV-A.ST", "ISOFOL.ST", "SALT-B.ST", "CORE-PREF.ST",
                                   "SKF-A.ST", "2,00 BRE.ST", "EAST.ST", "TRIAN-B.ST", "CAG.ST", "TFBANK.ST", "ICO.ST",
                                   "MOB.ST", "VOLO-PREF.ST", "MILDEF.ST", "M8G.ST", "FERRO.ST", "BINV.ST", "LATF-B.ST",
                                   "THUNDR.ST", "SEAF.ST", "HUSQ-A.ST", "EWRK.ST", "PRFO.ST", "QLIRO.ST", "AJA-B.ST",
                                   "CE.ST", "VICO.ST", "ARISE.ST", "FASTAT.ST", "ORES.ST", "SMOL.ST", "GREEN.ST",
                                   "URBIT.ST", "CI.ST", "TRAC-B.ST", "FNM.ST", "K2A-B.ST", "JOMA.ST", "CAT-B.ST",
                                   "XSPRAY.ST", "KDEV.ST", "TRANS.ST", "SLP-B.ST", "MEAB-B.ST", "FNOVA-B.ST", "GENI.ST",
                                   "SCA-A.ST", "DBP-B.ST", "SINT.ST", "PLEJD.ST", "PRLD.ST", "NAVIGO-STAM.ST",
                                   "CLBIO.ST", "NORION.ST", "EMIL-B.ST", "KEBNI-B.ST", "NIVI-B.ST", "LPGO.ST",
                                   "FIRE.ST", "INSP.ST", "KJELL.ST", "PROVIT.ST", "QLIFE.ST", "MESTRO.ST", "STREAM.ST",
                                   "COMBI.ST", "FOI-B.ST", "BIOVIC-B.ST", "NP3-PREF.ST", "SPRINT.ST", "REJL-B.ST",
                                   "LCLEAN.ST", "ELIC.ST", "4C.ST", "TERRNT-B.ST", "SVIK.ST", "BOAT.ST", "MIDS.ST",
                                   "DMYD-B.ST", "SPEC.ST", "MSAB-B.ST", "ACCON.ST", "READ.ST", "ALM-PREF.ST",
                                   "VULTS.ST", "SVED-B.ST", "MINEST.ST", "OPTI.ST", "ANGL.ST", "BIM.ST",
                                   "SFAB.ST", "LOGIST.ST", "INISS-B.ST", "CFISH.ST", "ELTEL.ST", "ONCOZ.ST", "IRIS.ST",
                                   "ACOU.ST", "MOV.ST", "POLY.ST", "AWRD.ST", "ENZY.ST", "MANTEX.ST", "INTEG-B.ST",
                                   "NANOFS.ST", "OXE.ST", "BYGGP.ST", "WYLD.ST", "EMPIR-B.ST", "NIL-B.ST", "ENVI-B.ST",
                                   "SANION.ST", "MSON-B.ST", "HOLM-A.ST", "ISAB.ST", "LUC.ST", "RUG.ST", "DEVP-B.ST",
                                   "NIO.ST", "PSCAND.ST", "CINIS.ST", "CBTT-B.ST", "IMSYS.ST", "MNTC.ST", "FIL.ST",
                                   "ITECH.ST", "BEO-SDB.ST", "IVACC.ST", "CLAV.ST", "AAC.ST", "EQL.ST", "WAYS.ST",
                                   "PURE.ST", "CANDLE-B.ST", "VSSAB-B.ST", "ADVT.ST", "BLUE.ST", "PLUN.ST", "OGUN-B.ST",
                                   "ARCA.ST", "WIG.ST", "CCC.ST", "TRAIN-B.ST", "FLUO.ST", "S2M.ST", "TIETOS.ST",
                                   "ADDV-A.ST", "ABLI.ST", "GRANGX.ST", "ACAST.ST", "ACARIX.ST", "PROB.ST", "QAIR.ST",
                                   "HAYPP.ST", "FLAT-B.ST", "PAX.ST", "BALCO.ST", "OVZON.ST", "EOID.ST", "LINC.ST",
                                   "BIOEX.ST", "META.ST", "VERT-B.ST", "MVIR.ST", "LADYLU.ST", "VPAB-B.ST", "SOF-B.ST",
                                   "ACUVI.ST", "AXIC-A.ST", "NANEXA.ST", "CLIME-B.ST", "AXOLOT.ST", "CDON.ST",
                                   "NELLY.ST", "ZICC.ST", "ARBO-A.ST", "CTEK.ST", "NOSA.ST", "FMM-B.ST", "HIGHCO-B.ST",
                                   "EMIL-PREF.ST", "MAHVIE.ST", "NILAR.ST", "MIR.ST", "CARE.ST", "GHUS-B.ST",
                                   "ANNE-B.ST", "FLEXM.ST", "BELLP.ST", "MAXENT-B.ST"

                                   ]

        return ticker_codes_additional