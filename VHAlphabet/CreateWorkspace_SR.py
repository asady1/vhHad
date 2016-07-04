import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy, copy


import Alphabet_Header
from Alphabet_Header import *
import Plotting_Header
from Plotting_Header import *

#gSystem.Load("PU_C.so")
'''
gInterpreter.ProcessLine( 'TFile *f = TFile::Open("trigger_objects.root")')
gInterpreter.ProcessLine( 'TH1F *histo_efficiency = (TH1F*)f->Get("histo_efficiency")')
gInterpreter.ProcessLine( 'TH1F *histo_efficiency_lower = (TH1F*)f->Get("histo_efficiency_lower")')
gInterpreter.ProcessLine( 'TH1F *histo_efficiency_upper = (TH1F*)f->Get("histo_efficiency_upper")')
gInterpreter.ProcessLine(".x trigger_function.cxx")
'''

mass=[600,800,1000,1200,1400,1600,1800,2000,2500, 3000, 3500, 4000]
VAR = "dijetmass_corr"
binBoundaries = [800, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687,
        1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509]
vartitle = "m_{X} (GeV)"

presel = "(dijetmass_corr>800&jetVID>0.&&jetHID>0&jetVpmass<105&jetVpmass>65&(jetVtau21+(0.063*log(jetVpmass*jetVpmass/jetVpt)))<0.55)"
sigregcutNoTrig = "jetHpmass>105&jetHpmass<135&jetHbbtag>0.6&"+presel
sigregcut = "jetHpmass>105&jetHpmass<135&jetHbbtag>0.6&triggerpassbb>0.&"+presel
lumi =2691.
SF_tau21 =1.
background = TFile("outputs/SR_output.root")
UD = ['Up','Down']


for m in mass:

	output_file = TFile("outputs/datacards/VH_mX_%s_13TeV.root"%(m),"RECREATE")
	vh=output_file.mkdir("vh")
	vh.cd()

	Signal_mX = TH1F("Signal_mX_%s"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
	Signal_mX_trig_up = TH1F("Signal_mX_%s_CMS_eff_trigUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
	Signal_mX_trig_down = TH1F("Signal_mX_%s_CMS_eff_trigDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
	Signal_mX_btag_up = TH1F("Signal_mX_%s_CMS_eff_btagUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
        Signal_mX_btag_down = TH1F("Signal_mX_%s_CMS_eff_btagDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
        Signal_mX_pu_up = TH1F("Signal_mX_%s_CMS_eff_puUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
 	Signal_mX_pu_down = TH1F("Signal_mX_%s_CMS_eff_puDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
	Signal_mX_FJEC_Up = TH1F("Signal_mX_%s_CMS_eff_JECUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
	Signal_mX_FJEC_Down = TH1F("Signal_mX_%s_CMS_eff_JECDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
	Signal_mX_FJER_Up = TH1F("Signal_mX_%s_CMS_eff_JERUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
        Signal_mX_FJER_Down = TH1F("Signal_mX_%s_CMS_eff_JERDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
	Signal_mX_MJEC_Up = TH1F("Signal_mX_%s_CMS_eff_massJECUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
        Signal_mX_MJEC_Down = TH1F("Signal_mX_%s_CMS_eff_massJECDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))

	print(m)

	signal_file= TFile("tree_WP_%s_VH_alph.root"%(m))
	tree = signal_file.Get("mynewTree") 
	bbj = signal_file.Get("bbj")
	generatedEvents =bbj.GetEntries()
	writeplot(tree, Signal_mX, VAR, sigregcut, "puWeights*SF")#(trigger_function(int(round(htJet40eta3)))*weight2(nTrueInt))")
        writeplot(tree, Signal_mX_btag_up, VAR, sigregcut, "puWeights*SFup")
	writeplot(tree, Signal_mX_btag_down, VAR, sigregcut, "puWeights*SFdown")
        writeplot(tree, Signal_mX_trig_up, VAR, sigregcutNoTrig, "trigWeightUp*puWeights*SF")
	writeplot(tree, Signal_mX_trig_down, VAR, sigregcutNoTrig, "trigWeightDown*puWeights*SF")
	writeplot(tree, Signal_mX_pu_up, VAR, sigregcut, "puWeightsUp*SF")
	writeplot(tree, Signal_mX_pu_down, VAR, sigregcut, "puWeightsDown*SF")
	###missing here the pu variation

	print(Signal_mX.Integral())

	btaglnN= 1.+ abs(Signal_mX_btag_up.GetSumOfWeights()-Signal_mX_btag_down.GetSumOfWeights())/(2.*Signal_mX_btag_up.GetSumOfWeights())
	PUlnN= 1.+ abs(Signal_mX_pu_up.GetSumOfWeights()-Signal_mX_pu_down.GetSumOfWeights())/(2.*Signal_mX.GetSumOfWeights())
	Signal_mX.Scale(lumi*0.01)
	
 	Signal_mX_btag_up.Scale(SF_tau21*lumi*0.01/generatedEvents)
	Signal_mX_btag_down.Scale(SF_tau21*lumi*0.01/generatedEvents)
	Signal_mX_trig_up.Scale(SF_tau21*0.01*lumi/generatedEvents)
	Signal_mX_trig_down.Scale(SF_tau21*0.01*lumi/generatedEvents)
	Signal_mX_pu_up.Scale(lumi*SF_tau21*0.01/generatedEvents)
        Signal_mX_pu_down.Scale(lumi*SF_tau21*0.01/generatedEvents)

	MJEClnN= 1.02 ## add variation from ntuples
	FJEClnN= 1.02
	FJERlnN= 1.02


        signal_integral = Signal_mX.Integral()
	print(signal_integral) 
        background.cd() 	
	qcd_integral = EST.Integral()

	qcd = background.Get("EST")
	qcd_antitag = background.Get("EST_Antitag")
	qcd_up = background.Get("EST_CMS_scale_13TeVUp")
	qcd_down = background.Get("EST_CMS_scale_13TeVDown")
	data_obs = background.Get("data_obs")
        data_integral = data_obs.Integral() 
	output_file.cd()
        vh.cd()
	qcd_stat_up =TH1F("qcd_stat_up","",len(binBoundaries)-1, array('d',binBoundaries))
        qcd_stat_down =TH1F("qcd_stat_down","",len(binBoundaries)-1, array('d',binBoundaries))
	
	for bin in range(0,len(binBoundaries)-1):
            for Q in UD:
                qcd_syst =TH1F("%s_bin%s%s"%("EST_CMS_stat_13TeV",bin,Q),"",len(binBoundaries)-1, array('d',binBoundaries))
 		bin_stat = qcd.GetBinContent(bin+1)
		for bin1 in range(0,len(binBoundaries)-1):
			bin_stat1 = qcd.GetBinContent(bin1+1)
			qcd_syst.SetBinContent(bin1+1,bin_stat1)
		#if bin_stat==0 :	
		#	bin_stat = 1.5
		bin_at = qcd_antitag.GetBinContent(bin+1)
		if bin_at < 1 and bin_at >0:  
			bin_at=1.
                if Q == 'Up':
			if bin_at >0 :
			       qcd_stat_up.SetBinContent(bin+1,bin_stat+qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)	
                               qcd_syst.SetBinContent(bin+1,bin_stat+qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)
			else : 
				qcd_syst.SetBinContent(bin+1,bin_stat)
				qcd_stat_up.SetBinContent(bin+1,bin_stat)
				
                if Q == 'Down':
			if bin_at >0 :
				if ( bin_stat-qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat >0 ):
                        		qcd_syst.SetBinContent(bin+1,bin_stat-qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)
					qcd_stat_down.SetBinContent(bin+1,bin_stat-qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)
				else :
					qcd_syst.SetBinContent(bin+1, 0.1)
					qcd_stat_down.SetBinContent(bin+1, 0.1)
			else : 	
				qcd_syst.SetBinContent(bin+1,bin_stat)
				qcd_stat_down.SetBinContent(bin+1,bin_stat)
		qcd_syst.Write()
		

	#qcd_trigger_up.Write()
	#qcd_trigger_low.Write()
	qcd.Write()
	qcd_up.Write()
	qcd_down.Write()
	qcd_stat_up.Write()
	qcd_stat_down.Write()
	Signal_mX.Write()
	Signal_mX_btag_up.Write()
	Signal_mX_btag_down.Write()
	Signal_mX_trig_up.Write()
	Signal_mX_trig_down.Write()
	data_obs.Write()
	vh.Write()
	output_file.Write()
	#output_file.Close()

	

	text_file = open("outputs/datacards/VH_mX_%s_13TeV.txt"%(m), "w")


	text_file.write("max    1     number of categories\n")
        text_file.write("jmax   1     number of samples minus one\n")
        text_file.write("kmax    *     number of nuisance parameters\n")
        text_file.write("-------------------------------------------------------------------------------\n")
        text_file.write("shapes * * VH_mX_%s_13TeV.root vh/$PROCESS vh/$PROCESS_$SYSTEMATIC\n"%(m))
        text_file.write("-------------------------------------------------------------------------------\n")
        text_file.write("bin                                            vh4b\n")
        text_file.write("observation                                    %f\n"%(data_integral))
        text_file.write("-------------------------------------------------------------------------------\n")
        text_file.write("bin                                             vh4b            vh4b\n")
        text_file.write("process                                          0      1\n")
        text_file.write("process                                         Signal_mX_%s  EST\n"%(m))
        text_file.write("rate                                            %f  %f\n"%(signal_integral,qcd_integral))
        text_file.write("-------------------------------------------------------------------------------\n")
	text_file.write("lumi_13TeV lnN                          1.027       -\n")	
        text_file.write("CMS_eff_tau21_sf lnN                    1.027       -\n") #(0.028/0.979)
        #text_file.write("CMS_eff_Htag_sf lnN                    1.1       -\n")   
        text_file.write("CMS_JEC lnN 		     %f        -\n"%(FJEClnN)) 	
	text_file.write("CMS_massJEC lnN                 %f        -\n"%(MJEClnN))
	text_file.write("CMS_eff_bbtag_sf lnN                    %f       -\n"%(btaglnN))
        text_file.write("CMS_JER lnN                    %f        -\n"%(FJERlnN))
        text_file.write("CMS_PU lnN                    %f        -\n"%(PUlnN))
	text_file.write("CMS_eff_trig shapeN2           1.0   -\n")
        text_file.write("CMS_scale_13TeV shapeN2                           -       1.000\n")
	text_file.write("CMS_PDF_Scales lnN   1.02 -       \n")

	for bin in range(0,len(binBoundaries)-1):
		text_file.write("CMS_stat_13TeV_bin%s shapeN2                           -       1.000\n"%(bin))


	text_file.close()
