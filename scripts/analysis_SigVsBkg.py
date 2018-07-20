import ROOT
from ROOT import gStyle, TLegend, TFile, TChain, TLine
#Last Built July 2018

#f1 = Bkg
#f2 = Sig
f1 = "/home/jhall/SUSY/MasterShefWD/LocalAnalysis/samples/reco_Matts/processed/mctTTkt8/ttbar_processed_kt8.txt"
f2 = "/home/jhall/SUSY/MasterShefWD/LocalAnalysis/samples/reco_Matts/processed/mctTTkt8/stop0L_processed_kt8.txt"

class Files:
  def __init__(self,master_file):
    self.master_file = master_file

  def Get_Files(self):
    subfile = open(self.master_file,"r")
    arr = []
    for line in subfile:
      l = list(line)
      n = len(line)
      l[n-1:n] = []
      x = "".join(l)
      arr.append(x)
    return arr      

file1 = Files(f1)
file1_arr = file1.Get_Files()

i = 0
for i in range(len(file1_arr)):
  if i == 0:
    print"bkg_1 = ", file1_arr[i]
    bkg_1 = TChain("NominalFixed")
    bkg_1.AddFile(file1_arr[i])
  if i == 1:
    print"bkg_2 = ", file1_arr[i]
    bkg_2 = TChain("NominalFixed")
    bkg_2.AddFile(file1_arr[i])
  i = i + 1

file2 = Files(f2)
file2_arr = file2.Get_Files()

i = 0
for i in range(len(file2_arr)):
  if i == 0:
    print"sig_1 = ", file2_arr[i]
    sig_1 = TChain("NominalFixed")
    sig_1.AddFile(file2_arr[i])
  if i == 1:
    print"sig_2 = ", file2_arr[i]
    sig_2 = TChain("NominalFixed")
    sig_2.AddFile(file2_arr[i])
  if i == 2:
    print"sig_3 = ", file2_arr[i]
    sig_3 = TChain("NominalFixed")
    sig_3.AddFile(file2_arr[i])
  i = i + 1

noSC='(1)*'
PS='(eT_miss_orig>200)*(nEl+nMu==0)*(nj_good>=4)*(pT_1jet>80)*(pT_2jet>80)*(pT_4jet>40)*(dphimin4>0.4)*'
SRA=PS+'*(num_bjets>=2)*(MTbmin>200 )*( m_1fatjet_kt8>60)*( m_1fatjet_kt12>120)*(eT_miss>400)*(MT2Chi2>400)*'
SRB=PS+'*(num_bjets>=2)*(MTbmin_orig>200)*(m_1fatjet_kt12>120)*(dRb1b2>1.2)*'
ISR='(eT_miss_orig>200)*(pT_1jet>300)*'
Selection_Cuts = [noSC,PS,SRA,SRB]

luminosity="36100"
weights="AnalysisWeight*pileupweight*"#btagweight*"
#weights="AnalysisWeight*LumiWeight*pileupweight*btagweight*"
total=weights+Selection_Cuts[0]+luminosity

fat_jet_vars = ["m_1fatjet_kt12","m_2fatjet_kt12","m_1fatjet_kt8","m_2fatjet_kt8"]
fat_jet_vars2 = ["pT_1fatjet_kt8", "pT_2fatjet_kt8", "pT_1fatjet_kt12", "pT_1fatjet_kt12"]
list_of_vars = ["mctTT"]

for var in fat_jet_vars2:
  hist1 = ROOT.TCanvas("c", "NewVsOldMadGraph",800,600)
  #c.Divide(1,2)
  #hist1 = c.c(1)
  hist1.SetLogy()
  gStyle.SetOptStat(0)

  sig_1.Draw(var+">>h_sig1(20,0,1100)",total,"")
  h_sig1=hist1.GetPrimitive("h_sig1")
  h_sig1.SetLineColor(63)
  h_sig1.SetLineWidth(4)

  sig_2.Draw(var+">>h_sig2(20,0,1100)",total,"")
  h_sig2=hist1.GetPrimitive("h_sig2")
  h_sig2.SetLineColor(59)
  h_sig2.SetLineWidth(4)

  sig_3.Draw(var+">>h_sig3(20,0,1100)",total,"")
  h_sig3=hist1.GetPrimitive("h_sig3")
  h_sig3.SetLineColor(213)
  h_sig3.SetLineWidth(4)

  bkg_1.Draw(var+">>h_bkg1(20,0,1100)",total,"")
  h_bkg1=hist1.GetPrimitive("h_bkg1")
  h_bkg1.SetLineColor(206)
  h_bkg1.SetLineWidth(4)

#  bkg_2.Draw(var+">>h_bkg2(20,0,700)",total,"")
#  h_bkg2=hist1.GetPrimitive("h_bkg2")
#  h_bkg2.SetLineColor(205)
#  h_bkg2.SetLineWidth(4)

                                        #COLOURS:
#224,223,222,221 purples
#3,8,210,209 greens
#46,207,2,205 reds
#66,63,59,213 blues
#12,1 blacks
#pairs PURPLES 222(l),221(d), BLUES 63L,213D, REDS 2L,205D, GREENS 211L, 209D

  norm = 1.0
  h_sig1.Draw("hist e")
  h_sig1.Scale(norm/h_sig1.Integral())
  h_sig2.Draw("hist e same")
  h_sig2.Scale(norm/h_sig2.Integral())
  h_sig3.Draw("hist e same")
  h_sig3.Scale(norm/h_sig3.Integral())
  h_bkg1.Draw("hist e same")
  h_bkg1.Scale(norm/h_bkg1.Integral())
#  h_bkg2.Draw("hist e same")
#  h_bkg2.Scale(norm/h_bkg2.Integral())

  h_sig1.GetYaxis().SetTitle("Normalised Events")
  h_sig1.SetTitle(var)
  h_sig1.GetXaxis().SetTitle(var)

  #line = TLine(170,0,170,0.075)
  #line.SetLineStyle(2)
  #line.SetLineWidth(4)
  #line.Draw("same")

  legend = TLegend(0.677945,0.655052,0.883459,0.893728)
#legend.SetHeader("Title Here","C"           )#C centers header
  legend.SetBorderSize(0)
  legend.AddEntry("h_sig1","directTT [600_427]")
  legend.AddEntry("h_sig2","directTT [1300_1]")
  legend.AddEntry("h_sig3","directTT [800_500]")
  legend.AddEntry("h_bkg1","ttbar")
#  legend.AddEntry("h_bkg2","ttbar (semi-lep)")
  legend.SetTextSize(0.025)
  legend.Draw()

  hist1.Update()
  raw_input()
#  save_path = '/home/jhall/SUSY/AnalysisWrapper/LocalAnalysis/plots/reco_fat_jet_study/SigVsBkg_Comp/updated_script_plots/'
#  hist1.SaveAs(save_path+"reco_"+var+"_kt12_noSC.pdf")

#raw_input()
'''

hist2 = c.cd(2)                                                      #Bottom Histo
#hist2.SetLogy()

ratio = hnew.Clone()
ratio.SetLineColor(221)
ratio.SetTitle("Ratio of new/old")
#ratio.SetMinimum(0.8)
ratio.Divide(hold)


ratio.Draw("hist e")

line = TLine(0,1,1500,1)
line.SetLineStyle(2)
line.SetLineWidth(2)
line.Draw("same")

ratio.GetYaxis().SetTitle("Ratio")
ratio.SetTitle("Ratio of new/old")
ratio.GetXaxis().SetTitle(var)

legend2 = TLegend(0.677945,0.655052,0.883459,0.893728)
#legend.SetHeader("Title Here","C"           )#C centers header
legend2.SetBorderSize(0)
legend2.AddEntry(ratio,"directTT [600_427]")
legend2.SetTextSize(0.025)
legend2.Draw()

c.Update()
'''