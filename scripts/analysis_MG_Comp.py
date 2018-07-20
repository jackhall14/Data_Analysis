import ROOT
from ROOT import *
#Last Updated June 2018 - v. similar to analysis_SigVsBkg.py but uses older system and takes more samples
                                          #Old Sample

o_file = open("/home/jhall/SUSY/MasterShefWD/LocalAnalysis/samples/v_2_2_3/stop/processed/stop0L_processed_v_2_2_33.txt","r")

#num_lines = sum(1 for line in open('/home/jhall/SUSY/AnalysisWrapper/LocalAnalysis/samples/06FebProcessed/processedSig/stopSignalProcessed.txt'))                          #Number of lines in sample
#print num_lines

old_file = TChain("NominalFixed")
old_file2 = TChain("NominalFixed")
old_file3 = TChain("NominalFixed")
print("\nOld Files:")
i = 1
for line in o_file:
    l = list(line)
    n = len(line)
    l[n-1:n] = []
    x = "".join(l)
    if i == 1:
        print"old = ", x
        old_file.AddFile(x)
        #old_file.ls()
    if i == 2:
        print"old2 = ", x
        old_file2.AddFile(x)
        #old_file2.ls()
    if i == 3:
        print"old3 = ", x
        old_file3.AddFile(x)
        #old_file3.ls()
    i = i +1


old = old_file
old2 = old_file2
old3 = old_file3
#print old, old.GetEntries()
#print old2, old2.GetEntries()
#print old3, old3.GetEntries()

                                          #New Sample

n_file = open("/home/jhall/SUSY/MasterShefWD/LocalAnalysis/samples/v_2_6_1/stop/processed/stop0L_processed_v_2_6_13.txt","r")

new_file = TChain("NominalFixed")
new_file2 = TChain("NominalFixed")
new_file3 = TChain("NominalFixed")
print("\nNew Files:")
i = 1
for line in n_file:
    l = list(line)
    n = len(line)
    l[n-1:n] = []
    x = "".join(l)
    if i == 1:
       print"new = ", x
       new_file.AddFile(x)
       #new_file.ls()
    if i == 2:
       print"new2 = ", x
       new_file2.AddFile(x)
       #new_file2.ls()
    if i == 3:
       print"new3 = ", x
       new_file3.AddFile(x)
       #new_file3.ls()
    i = i +1


new = new_file
new2 = new_file2
new3 = new_file3
#print new, new.GetEntries()
#print new2, new2.GetEntries()
#print new3, new3.GetEntries()

                                        #Selection Criteria

none="(1)*"
PS="(eT_miss_orig>200)*(nEl+nMu==0)*(nj_good>=4)*(pT_1jet>80)*(pT_2jet>80)*(pT_4jet>40)*(dphimin4>0.4)*"
SRA=PS+"*(num_bjets>=2)*(MTbmin>200 )*( m_1fatjet_kt8>60)*( m_1fatjet_kt12>120)*(eT_miss>400)*(MT2Chi2>400)*"
#SRB=PS+"*(passtauveto==1)*(num_bjets>=2)*(MTbmin_orig>200)*(m_1fatjet_kt12>120)*(dRb1b2>1.2)"
SRB=PS+"*(num_bjets>=2)*(MTbmin_orig>200)*(m_1fatjet_kt12>120)*(dRb1b2>1.2)*"
ISR="(eT_miss_orig>200)*(pT_1jet>300)*"

luminosity="36100"
#weights="AnalysisWeight*LumiWeight*pileupweight*btagweight*"
weights="1*"
total=weights+SRB+luminosity

#var="mctTT"                                                          #choose variable
list_of_vars = ["eT_miss"]

for var in list_of_vars:
    c = ROOT.TCanvas("c", "NewVsOldMadGraph",700,900)
    c.Divide(1,2)
    hist1 = c.cd(1)                                                            #Top Histo
    hist1.SetLogy()
    gStyle.SetOptStat(0)

                                      #New Plots

    new.Draw(var+">>hnew(20,0,1500)",total,"")
    hnew=hist1.GetPrimitive("hnew")
    hnew.SetLineColor(221)                                            #new,
    hnew.SetLineWidth(4)

    new2.Draw(var+">>hnew2(20,0,1500)",total,"")
    hnew2=hist1.GetPrimitive("hnew2")
    hnew2.SetLineColor(209)                                           #new4, 
    hnew2.SetLineWidth(4)

    new3.Draw(var+">>hnew3(20,0,1500)",total,"")
    hnew3=hist1.GetPrimitive("hnew3")
    hnew3.SetLineColor(213)                                           #new3,
    hnew3.SetLineWidth(4)

                                      #Old Plots

    old.Draw(var+">>hold(20,0,1500)",total,"")
    hold=hist1.GetPrimitive("hold")
    hold.SetLineColor(222)                                           #old,
    hold.SetLineWidth(4)

    old2.Draw(var+">>hold2(20,0,1500)",total,"")
    hold2=hist1.GetPrimitive("hold2")
    hold2.SetLineColor(211)                                           #old4, 
    hold2.SetLineWidth(4)

    old3.Draw(var+">>hold3(20,0,1500)",total,"")
    hold3=hist1.GetPrimitive("hold3")
    hold3.SetLineColor(63)                                           #old3, 
    hold3.SetLineWidth(4)


#224,223,222,221 purples
#3,8,210,209 greens
#46,207,2,205 reds
#66,63,59,213 blues
#12,1 blacks

#pairs PURPLES 222(l),221(d), BLUES 63L,213D, REDS 2L,205D, GREENS 211L, 209D

    norm = 1
    scale = norm/hnew.Integral()
    hnew.Scale(scale)
    hnew.Draw("hist e")

    scale = norm/hnew2.Integral()
    hnew2.Scale(scale)
    hnew2.Draw("hist e same")

    scale = norm/hnew3.Integral()
    hnew3.Scale(scale)
    hnew3.Draw("hist e same")

    scale = norm/hold.Integral()
    hold.Scale(scale)
    hold.Draw("hist e same")

    scale = norm/hold2.Integral()
    hold2.Scale(scale)
    hold2.Draw("hist e same")

    scale = norm/hold3.Integral()
    hold3.Scale(scale)
    hold3.Draw("hist e same")

    hnew.GetYaxis().SetTitle("Normalised Events")

    hnew.SetTitle("MadGraph v2.2.3 vs v2.6.1")              #Removes Title of histo
#hnew.SetTitle("")
    hnew.GetXaxis().SetTitle(var)

    legend = TLegend(0.677945,0.655052,0.883459,0.893728)
#legend.SetHeader("Title Here","C"           )#C centers header
    legend.SetBorderSize(0)
    legend.AddEntry("hnew","v2.6.1 directTT [600_427]")
    legend.AddEntry("hold","v2.2.3 directTT [600_427]")
    legend.AddEntry("hnew2","v2.6.1 directTT [1300_1]")
    legend.AddEntry("hold2","v2.2.3 directTT [1300_1]")
    legend.AddEntry("hnew3","v2.6.1 directTT [800_500]")
    legend.AddEntry("hold3","v2.2.3 directTT [800 500]")
    legend.SetTextSize(0.025)
    legend.Draw()

    c.Update()



    hist2 = c.cd(2)                                                      #Bottom Histo
#hist2.SetLogy()

    ratio = hnew.Clone()
    ratio.SetLineColor(221)
    ratio.SetTitle("Ratio of new/old")
    ratio.SetMaximum(2.0)
    ratio.SetMinimum(0.0)
    ratio.Divide(hold)

    ratio2 = hnew2.Clone()
    ratio2.SetLineColor(209)
    ratio2.SetMaximum(2.0)
    ratio2.SetMinimum(0.0)
    ratio2.Divide(hold2)

    ratio3 = hnew3.Clone()
    ratio3.SetLineColor(213)
    ratio3.SetMaximum(2.0)
    ratio3.SetMinimum(0.)
    ratio3.Divide(hold3)

    ratio.Draw("hist e")
    ratio2.Draw("hist e same")
    ratio3.Draw("hist e same")

    ratio.GetYaxis().SetTitle("Ratio")
    ratio.SetTitle("Ratio of new/old")
    ratio.GetXaxis().SetTitle(var)

    line = TLine(0,1,1500,1)
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw("same")

    legend2 = TLegend(0.677945,0.655052,0.883459,0.893728)
#legend.SetHeader("Title Here","C"           )#C centers header
    legend2.SetBorderSize(0)
    legend2.AddEntry(ratio,"directTT [600_427]")
    legend2.AddEntry(ratio2,"directTT [1300_1]")
    legend2.AddEntry(ratio3,"directTT [800_500]")
    legend2.SetTextSize(0.025)
    legend2.Draw()

    c.Update()
    save_path = '/home/jhall/SUSY/AnalysisWrapper/LocalAnalysis/plots/reco_fat_jet_study/SigVsBkg_Comp/'
    c.SaveAs(save_path+var+"_truth_MG_Comp_SRB.pdf")

#raw_input()

'''
                                                                  #2D Plot
c2 = ROOT.TCanvas("c2", "c2",700,900)
signal.Draw("num_bjets:mct2b>>h2D(100,0,500,100,0,500)",total,"colz")
h2D=c2.GetPrimitive("h2D")
c2.SetLogy(False)
#print h2D.GetEntries()
h2D.Draw("colz")
'''

'''
                                                #MET selection cuts
var="mct2b"
for i in range(250,550,100):

    met_selection="*(eT_miss>%d)"%(i)
    
    c=ROOT.TCanvas("c","c",800,600)
    c.SetLogy()

    signal.Draw(var+">>hsignal(11,0,1000)",total+met_selection,"")
    hsignal=c.GetPrimitive("hsignal")
    hsignal.SetLineColor(225)                                            #Signal is green
    hsignal.SetLineWidth(3)

    background.Draw(var+">>hbkg(11,0,1000)",total+met_selection,"")
    hbkg=c.GetPrimitive("hbkg")
    hbkg.SetLineColor(221)                                               #bkg is purple
    hbkg.SetLineWidth(3)

    signal2.Draw(var+">>hsignal2(11,0,1000)",total+met_selection,"")
    hsignal2=c.GetPrimitive("hsignal2")
    hsignal2.SetLineColor(50)                                           #Signal is Yellow
    hsignal2.SetLineWidth(3)

    signal3.Draw(var+">>hsignal3(11,0,1000)",total+met_selection,"")
    hsignal3=c.GetPrimitive("hsignal3")
    hsignal3.SetLineColor(59)                                            #Signal is Blue
    hsignal3.SetLineWidth(3)

    hbkg.Draw("hist e")
    hsignal.Draw("hist e same")
    hsignal2.Draw("hist e same")
    hsignal3.Draw("hist e same")

    hbkg.GetYaxis().SetTitle("Events")

    hbkg.SetTitle(met_selection)                                            #Removes Title of histo
    hbkg.GetXaxis().SetTitle(var)

    legend = TLegend(0.677945,0.655052,0.883459,0.893728)
#legend.SetHeader("Title Here","C"           )#C centers header
    legend.SetBorderSize(0)
    legend.AddEntry("hbkg","TTBar")
    legend.AddEntry("hsignal","Signal [700,400]")
    legend.AddEntry("hsignal2","Signal [1000,1]")
    legend.AddEntry("hsignal3","Signal [900,150]")
    legend.SetTextSize(0.025)
    legend.Draw()    

    print "Drawn met selection=",met_selection
    raw_input()

'''



