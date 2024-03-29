"""
Class to print Swedish tickers other than the
ones from the scraper.
"""

from typing import List
# pylint: disable=too-few-public-methods
# pylint: disable=line-too-long
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
                                   "VOLV-B.ST", "HM-B.ST", "EVO.ST", "SHB-A.ST",
                                   "NDA-SE.ST","ABB.ST", "SWED-A.ST", "NIBE-B.ST",
                                   "ESSITY-B.ST", "BOL.ST", "SSAB-B.ST", "SECU-B.ST",
                                   "TELIA.ST", "SKF-B.ST", "SEB-A.ST", "LOOMIS.ST",
                                   "HMS.ST", "TEL2-B.ST", "HEXA-B.ST", "SAND.ST",
                                   "INVE-A.ST", "SAAB-B.ST", "ASSA-B.ST", "ALLEI.ST",
                                   "AZA.ST","ATCO-B.ST", "ERIC-B.ST", "SINCH.ST",
                                   "ALFA.ST", "SCA-B.ST","AMBEA.ST", "SKA-B.ST",
                                   "LAGR-B.ST", "BILL.ST", "BEIJ-B.ST","ELUX-B.ST",
                                   "KINV-B.ST", "EQT.ST", "SAVE.ST", "EKTA-B.ST",
                                   "EMBRAC-B.ST", "GETI-B.ST", "CALTX.ST",
                                   "BALD-B.ST", "NOLA-B.ST","SSAB-A.ST", "CAST.ST",
                                   "TRUE-B.ST", "SOBI.ST", "SF.ST",
                                   "ANOD-B.ST", "INTRUM.ST", "ALIV-SDB.ST", "VOLCAR-B.ST",
                                   "TREL-B.ST", "CIBUS.ST", "INDU-C.ST", "HPOL-B.ST",
                                   "ADDT-B.ST","BONEX.ST", "STOR-B.ST", "AAK.ST",
                                   "AFRY.ST", "EPI-A.ST",
                                   "NEPA.ST", "VITR.ST", "VIT-B.ST", "MTRS.ST",
                                   "LATO-B.ST",
                                   "HOLM-B.ST", "LIFCO-B.ST", "HUFV-A.ST",
                                   "VPLAY-B.ST", "HTRO.ST",
                                   "LUND-B.ST", "FABG.ST", "GRNG.ST", "AOI.ST",
                                   "INDU-A.ST",
                                   "BETS-B.ST", "JM.ST", "CINT.ST", "KIND-SDB.ST",
                                   "NEWA-B.ST",
                                   "AXFO.ST", "THULE.ST", "TIGO-SDB.ST", "EPI-B.ST",
                                   "FNOX.ST",
                                   "HUSQ-B.ST", "IPCO.ST", "INWI.ST", "MIPS.ST",
                                   "CAMX.ST",
                                   "STAR-B.ST", "LUMI.ST","LUMI.ST", "SECARE.ST", "WALL-B.ST",
                                   "SAGA-B.ST", "OX2.ST", "MYCR.ST", "PEAB-B.ST", "CLAS-B.ST",
                                   "RAY-B.ST", "LIAB.ST", "PCELL.ST", "XVIVO.ST", "STE-R.ST",
                                   "NCC-B.ST", "KAMBI.ST", "VOLV-A.ST", "AEC.ST", "DIOS.ST",
                                   "INDT.ST", "PDX.ST", "SECT-B.ST", "SBB-D.ST", "SNM.ST",
                                   "KFAST-B.ST", "BURE.ST", "INSTAL.ST",
                                   "BIOA-B.ST", "RENEW.ST",
                                   "SWEC-B.ST", "SEYE.ST", "LUG.ST", "SHOT.ST", "HEM.ST", "WIHL.ST",
                                   "ORRON.ST", "COOR.ST", "BRAV.ST", "BILI-A.ST", "PNDX-B.ST",
                                   "YUBICO.ST", "NYF.ST", "SUS.ST", "SHB-B.ST", "8TRA.ST", "DUNI.ST",
                                   "DOM.ST", "ADDV-B.ST", "ATT.ST", "SAS.ST", "SAGA-D.ST",
                                   "VEFAB.ST",
                                   "BUFAB.ST", "BETCO.ST", "ALIF-B.ST",
                                   "XBRANE.ST", "TEQ.ST", "RATO-B.ST",
                                   "SVOL-B.ST", "VIMIAN.ST", "BERG-B.ST",
                                   "VBG-B.ST", "SDIP-B.ST", "MEKO.ST",
                                   "CATE.ST", "CLA-B.ST", "NOBI.ST",
                                   "NETEL.ST", "CORE-B.ST", "BICO.ST",
                                   "NCAB.ST", "HUM.ST", "MANG.ST",
                                   "NP3.ST", "NOTE.ST", "MTG-B.ST",
                                   "CRNO-B.ST", "ALLIGO-B.ST", "GARO.ST",
                                   "IVSO.ST", "SOLT.ST", "CRED-A.ST",
                                   "NPAPER.ST", "PLAZ-B.ST", "PACT.ST", "SKIS-B.ST",
                                   "TOBII.ST", "ARJO-B.ST",
                                   "ELAN-B.ST", "NWG.ST", "HANZA.ST",
                                   "NEOBO.ST", "BONAV-B.ST", "GUARD.ST",
                                   "NETI-B.ST", "STORY-B.ST", "BHG.ST", "GENO.ST",
                                   "CTT.ST", "ACAD.ST", "RESURS.ST",
                                   "VNV.ST", "OSSD.ST", "SEB-C.ST",
                                   "BIOG-B.ST", "EG7.ST", "HNSA.ST",
                                   "SEZI.ST", "TETY.ST","FING-B.ST", "CTM.ST",
                                   "G5EN.ST", "EOLU-B.ST", "EPRO-B.ST",
                                   "TROAX.ST", "CANTA.ST", "EPEN.ST",
                                   "BFG.ST", "KAR.ST","STABL.ST", "LIME.ST",
                                   "SYNSAM.ST", "AQ.ST", "SES.ST",
                                   "DOXA.ST", "BOOZT.ST", "HUMBLE.ST", "VOLO.ST", "RVRC.ST",
                                   "ENQ.ST", "OEM-B.ST", "B3.ST", "SYNACT.ST", "KNOW.ST",
                                   "ZZ-B.ST", "SIVE.ST", "GIGSEK.ST", "FAG.ST", "BIOT.ST",
                                   "DUST.ST", "NORB-B.ST", "DVYSR.ST", "QLINEA.ST",
                                   "ATRLJ-B.ST", "COIC.ST", "W5.ST",
                                   "BULTEN.ST", "MAVEN.ST",
                                   "PREV-B.ST", "RAKE.ST", "MCOV-B.ST", "BEIA-B.ST",
                                   "BAHN-B.ST", "ESSITY-A.ST", "CLS-B.ST",
                                   "BMAX.ST", "CS.ST",
                                   "LOGI-B.ST", "SYSR.ST", "ESGR-B.ST",
                                   "MAHA-A.ST", "MMGR-B.ST",
                                   "PRIC-B.ST", "HOFI.ST", "VESTUM.ST", "ENEA.ST", "ALIG.ST",
                                   "SEDANA.ST", "COPP-B.ST", "BRAIN.ST",
                                   "LYKO-A.ST", "CEVI.ST",
                                   "ENGCON-B.ST", "KABE-B.ST", "ERIC-A.ST", "IMMU.ST",
                                   "LUMITO.ST", "ONCO.ST", "NEXAM.ST", "CORE-D.ST",
                                   "EGTX.ST", "ABSO.ST", "CRAD-B.ST",
                                   "IDUN-B.ST", "K2A-PREF.ST",
                                   "FPAR-A.ST", "XANO-B.ST", "IMP-A-SDB.ST",
                                   "HEBA-B.ST", "BEGR.ST",
                                   "FG.ST", "STWK.ST", "MCAP.ST", "RROS.ST", "HEIM-PREF.ST",
                                   "ORT-B.ST", "PRO.ST", "LUMEN.ST",
                                   "ZAZZ-B.ST", "NMAN.ST", "KAN.ST",
                                   "DEDI.ST", "ARP.ST", "BUSER.ST", "DE.ST",
                                   "TDVOX.ST", "ITAB.ST", "SCST.ST", "INT.ST",
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
                                   "ANNE-B.ST", "FLEXM.ST", "BELLP.ST", "MAXENT-B.ST",
                                   "KLARA-B.ST", "ABSL-B.ST", "CLEM.ST", "LIPUM.ST", "ORGC.ST", "SUST.ST", "BTS-B.ST",
                                   "INFRA.ST", "GOMX.ST", "AROS-PREF-B.ST", "FRACTL.ST", "FOOT-B.ST", "NORVA.ST",
                                   "OPTER.ST", "OP.ST", "FPAR-D.ST", "TIRO.ST", "ORX.ST", "KOBR-B.ST", "SERT.ST",
                                   "OBSE.ST", "FREJA.ST", "DEAR.ST", "REFINE.ST", "SPEQT.ST", "MODEL-B.ST", "INIT.ST",
                                   "CX.ST", "SFTR.ST", "WNT.ST", "SLEEP.ST", "FLUI.ST", "STIL.ST", "KAV.ST",
                                   "PAGERO.ST", "AGTIRA-B.ST", "LAMM-B.ST", "PTRK.ST", "DURC-B.ST", "GPG.ST",
                                   "CCOR-B.ST", "ATORX.ST", "TEL2-A.ST", "KOLL.ST", "MCLR.ST", "VIMAB.ST", "NGENIC.ST",
                                   "SGG.ST", "STVA-B.ST", "SYNT.ST", "ALELIO.ST", "MOMENT.ST", "NNH.ST", "BAT.ST",
                                   "PRESRV.ST", "QIIWI.ST", "TOURN.ST", "247.ST", "EXPRS2.ST", "WISE.ST", "CISH.ST",
                                   "VIVE.ST", "AVT-B.ST", "MPOS.ST", "DSNO.ST", "GGEO.ST", "PHI.ST", "NEOD.ST",
                                   "STEF-B.ST", "ALZCUR.ST", "ACE.ST", "GAPW-B.ST", "DIST.ST", "BORG.ST", "IRLAB-A.ST",
                                   "INCOAX.ST", "REALFI.ST", "NTEK-B.ST", "HDW-B.ST", "OBAB.ST", "IBT-B.ST", "HEART.ST",
                                   "NXTCL.ST", "BIOGAS.ST", "SODER.ST", "IAR-B.ST", "HEXI.ST", "TAGM-B.ST", "BEYOND.ST",
                                   "BRIN-B.ST", "CHECK.ST", "GBK.ST", "ALZ.ST", "LITI.ST", "GREAT.ST", "RATO-A.ST",
                                   "CYXO.ST", "WPTG-B.ST", "NAIG-B.ST", "DICOT.ST",
                                   "TRIBO-B.ST", "SUSG.ST", "ENERS.ST", "AERO.ST", "LEMSE.ST", "FREEM.ST", "NYTTO.ST",
                                   "KAPIAB.ST", "AMH2-B.ST", "LOHILO.ST", "QBNK.ST", "BIOS.ST", "SDIP-PREF.ST",
                                   "OBDU-B.ST", "QUIA.ST", "MNDRK.ST", "NITRO.ST", "STE-A.ST", "BOMILL.ST", "ALCA.ST",
                                   "SIMRIS-B.ST", "ZAPLOX.ST", "KILI.ST", "HMPLY.ST", "VOLAB.ST", "INFREA.ST",
                                   "ELON.ST", "REDW.ST", "ENRO.ST", "AGES-B.ST", "AGROUP.ST", "AEGIR.ST",
                                   "TINGS-PREF.ST", "ECC-B.ST", "ARCEDE.ST", "BIOSGN.ST", "EPIS-B.ST", "ADVE.ST",
                                   "DIABIO.ST", "BRG-B.ST", "ASAI.ST", "MAGI.ST", "CHEF.ST", "ZENI.ST", "GCOR.ST",
                                   "KOPY.ST", "IMINT.ST", "SUN4.ST", "NORDIG.ST", "PMED.ST", "CMOTEC-B.ST", "NETM-B.ST",
                                   "BIOF.ST", "SDOS.ST", "PROGEN.ST", "VSD-B.ST", "SWEC-A.ST", "EMBELL.ST", "NAXS.ST",
                                   "IZAFE-B.ST", "MAV.ST", "BRIX.ST", "ZIGN.ST", "PION-B.ST", "GATE.ST", "PLEX.ST",
                                   "TANGI.ST", "BOUL.ST", "PENG-B.ST", "NANOC-B.ST", "AMIDO.ST", "FIRST-B.ST",
                                   "SLOTT-B.ST", "YIELD.ST", "AMNI.ST", "NGS.ST", "TSEC.ST", "COEGIN.ST", "GABA.ST",
                                   "NOTEK.ST", "NAVIGO-PREF.ST", "ASAB.ST", "DIGN.ST", "RAYTL.ST", "EMPLI.ST",
                                   "SCOL.ST", "ARION-SDB.ST", "SBOK.ST", "HUBSO.ST", "ZWIPE.ST", "CIRCHE.ST",
                                   "UMIDA-B.ST", "BAWAT.ST", "ORTI-B.ST", "HAMLET-B.ST", "ALLT.ST", "NCC-A.ST",
                                   "MERIS.ST", "JDT.ST", "STUDBO.ST",
                                   "BRILL.ST", "VAXXA.ST", "RAIL.ST", "LIDDS.ST", "SFAST.ST", "GTAB-B.ST", "AERW-B.ST",
                                   "UNIBAP.ST", "REATO.ST", "FAGA.ST", "FLOWS.ST", "PCAT.ST", "BTCX.ST", "STAR-A.ST",
                                   "IMMNOV.ST", "EEVIA.ST", "AIXIA-B.ST", "CLEMO.ST", "STW.ST", "TESSIN.ST", "XINT.ST",
                                   "NOHARM.ST", "QBIT.ST", "NOSIUM-B.ST", "FRAG.ST", "HILB-B.ST", "SFL.ST", "CRET.ST",
                                   "KLAR.ST", "SAGA-A.ST", "CRBX.ST", "PREBON.ST", "TOPR.ST", "EPTI.ST", "AVEN.ST",
                                   "DLAB.ST", "SECI.ST", "EVERY.ST", "AIK-B.ST", "ELOS-B.ST", "NATTA.ST", "ACUC.ST",
                                   "GOMERO.ST", "TCC-A.ST", "HAV-B.ST", "EFFH.ST", "IMPC.ST", "SYNC-B.ST", "FGG.ST",
                                   "SAXG.ST", "PCOM-B.ST", "CMH.ST", "EKOBOT.ST", "POLYG.ST", "BOKUS.ST", "SPERM.ST",
                                   "RO.ST", "PREC.ST", "SWEM-B.ST", "RESP.ST", "ECOM.ST", "ATANA.ST", "SDET.ST",
                                   "BBROOM.ST", "MODTX.ST", "ACTI.ST", "ZESEC.ST", "SHT-B.ST", "BIBB.ST", "SKMO.ST",
                                   "PHLOG-B.ST", "FLEXQ.ST", "TRAN-A.ST", "MFA.ST", "LAIR.ST", "FPIP.ST", "SCC-B.ST",
                                   "IMSOL-B.ST", "QBRICK.ST", "EASY-B.ST", "JSSEC.ST", "WEG.ST", "EATG.ST", "BLICK.ST",
                                   "AROC.ST", "BESQ.ST", "SPEONE.ST", "ECO-B.ST", "ABIG.ST", "SOSI.ST", "APTA.ST",
                                   "CSEC.ST", "VO2.ST", "MIDW-B.ST", "CRWN.ST", "CAPS.ST", "ALPH.ST", "XAVI-B.ST",
                                   "MEDIMI.ST", "EUCI.ST",
                                   "UPSALE.ST", "ASAP.ST", "KONT.ST", "STRLNG.ST", "RVN.ST", "OMNI.ST", "LINKFI.ST",
                                   "SONE.ST", "ANNX.ST", "2CUREX.ST", "DIV-B.ST", "GTG.ST", "TOL.ST", "SOLNA.ST",
                                   "SPIFF.ST", "BODY.ST", "TEBEDE-A.ST", "XMR.ST", "BPCINS.ST", "QUART-PREF.ST",
                                   "SKOLON.ST", "HEMC.ST", "MACK-B.ST", "JLT.ST", "SOCIAL.ST", "RIGHTB.ST", "PILA.ST",
                                   "BOTX.ST", "ALPCOT-B.ST", "NJOB.ST", "TRML.ST", "CHOSA.ST", "DIVIO-B.ST",
                                   "CORE-A.ST", "MODI.ST", "SCOUT.ST", "EXALT.ST", "RESQ.ST", "RECY-B.ST", "MISE.ST",
                                   "ONEF.ST", "VPLAY-A.ST", "RIZZO-B.ST", "AINO.ST", "EASY-BTA-B.ST", "QLOSR-B.ST",
                                   "OP-PREF.ST", "CHARGE.ST", "MONI.ST", "CALMA-B.ST", "FINE.ST", "COMPDM.ST",
                                   "BONZUN.ST", "DEX.ST", "BIOWKS.ST", "BONAV-A.ST", "NICA.ST", "LINKAB.ST",
                                   "ALBERT.ST", "WIL.ST", "ADVBOX.ST", "DORO.ST", "BUILD.ST", "TITA-B.ST", "PROF-B.ST",
                                   "QUART.ST", "ANTCO-B.ST",
                                   "NOVU.ST", "NOWO.ST", "NIS.ST", "TURA.ST", "FOOT-PREF.ST", "FSPORT.ST", "AROS.ST",
                                   "F2M.ST", "ACRI-B.ST", "ODI.ST", "DRIL.ST", "BEAMMW-B.ST", "ATIC.ST", "LYGRD.ST",
                                   "NXAR.ST", "TOUCH.ST", "CARDEO.ST", "GPX.ST", "TENDO.ST", "NICO.ST", "NFO.ST",
                                   "CAT-A.ST", "SPAGO.ST", "L2S.ST", "ANIMA-B.ST", "JETPAK.ST", "RLOS-B.ST", "JOBS.ST",
                                   "MBBAB.ST", "IS.ST", "CAM-B.ST", "GOTL-B.ST", "GIAB.ST", "PROMO.ST", "IRRAS.ST",
                                   "MEGR.ST", "ARCT.ST", "CHRO.ST", "CDMIL.ST", "UTG.ST", "ORTI-A.ST", "BINERO.ST",
                                   "OURLIV.ST", "RLS.ST", "PEXA-B.ST", "NILS.ST", "STRAX.ST", "SAFE.ST", "FOUT.ST",
                                   "FLMNG.ST", "ELN.ST", "SOUND.ST", "SAMT-B.ST", "LOYAL.ST", "ABERA.ST", "ARCOMA.ST",
                                   "HYCO.ST", "SOLIDX.ST", "BACTI-B.ST", "IMS.ST", "HELIO.ST", "HOI-B.ST", "ELLWEE.ST",
                                   "FXI.ST", "TAUR-B.ST", "KLIMAT.ST", "XPC.ST", "NBZ.ST", "ECTIN-B.ST", "EURA.ST",
                                   "AQUAT.ST", "RMDX.ST", "GAMEC.ST", "BUY.ST", "AYIMA-B.ST", "LXB.ST", "ZENZIP-B.ST",
                                   "ALONNR-B.ST", "WPAY.ST", "NFGAB.ST", "BACKA.ST", "ALM.ST", "PHYR-B.ST", "THINC.ST",
                                   "REAL.ST", "MTI.ST", "SDS.ST", "TRAD.ST", "ERMA.ST", "SMART-SDB.ST", "HOODIN.ST",
                                   "MOFAST.ST", "HUBS.ST", "ENRAD.ST", "HEGR.ST", "SNX.ST", "APTR.ST", "BRANDB.ST",
                                   "AVENT-B.ST", "CLINE-B.ST",
                                   "RPLAN.ST", "APRNDR.ST", "DIAH.ST", "SMG.ST", "AUR.ST", "SLG-B.ST", "PHARM.ST",
                                   "ACROUD.ST", "MEDHLP.ST", "ACRI-A.ST", "AMNO.ST", "UPGRAD.ST", "SARS.ST",
                                   "PIERCE.ST", "EBLITZ.ST", "MEDF.ST", "ADTR.ST", "AFRI.ST", "ALTE.ST", "ARCTIC.ST",
                                   "ATIN.ST", "BONAS.ST", "CASE.ST", "CEDER.ST", "COMINT.ST", "ECORE.ST", "ELUX-A.ST",
                                   "EOS.ST", "EURI-B.ST", "FRAM-B.ST", "FRILAN.ST", "GENE.ST", "HIFA-B.ST", "HOME-B.ST",
                                   "HOYLU.ST", "LOVE-B.ST", "IMSOL-BTB.ST", "IMS-BTA.ST", "SPLTN.ST", "JOJK.ST",
                                   "KAKEL.ST", "KENH.ST", "KRONA.ST", "KVIX.ST", "LCT.ST", "MOBA.ST", "MBRS.ST",
                                   "MSON-A.ST", "MIDW-A.ST", "MTG-A.ST", "MYBEAT.ST", "N55.ST", "NODE.ST", "LEVEL.ST",
                                   "CAPS-PREF.ST", "OBDU-PREF-B.ST", "ODIN.ST", "OP-PREFB.ST", "PHAL.ST", "POLYMER.ST",
                                   "PHOL-PREF.ST", "PHYR-PREF.ST", "GOTL-A.ST", "SELARM.ST", "SOZAP.ST", "SPGR.ST",
                                   "NYTTO-PREF.ST", "SVOL-A.ST", "SYDSV.ST", "TELLUS.ST", "TPGR.ST", "TINGS-A.ST",
                                   "TINGS-B.ST", "TRIONA.ST", "TWIIK.ST", "USWE.ST", "VADS.ST", "VH.ST", "WTG.ST"

                                   ]

        return ticker_codes_additional
