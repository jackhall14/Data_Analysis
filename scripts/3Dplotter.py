import ROOT
from ROOT import gStyle, TChain, TLine

#f1 = Bkg
#f2 = Sig
f1 = "/home/jhall/SUSY/MasterShefWD/LocalAnalysis/samples/reco_Matts/processed/mctTTkt12/ttbar_processed_kt12.txt"
f2 = "/home/jhall/SUSY/MasterShefWD/LocalAnalysis/samples/reco_Matts/processed/mctTTkt12/stop0L_processed_kt12.txt"

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

file_arr = []
i = 0
for i in range(len(file1_arr)):
  if i == 0:
    print"bkg_1 = ", file1_arr[i]
    bkg_1 = TChain("NominalFixed")
    bkg_1.AddFile(file1_arr[i])
    file_arr.append(bkg_1)
  if i == 1:
    print"bkg_2 = ", file1_arr[i]
    bkg_2 = TChain("NominalFixed")
    bkg_2.AddFile(file1_arr[i])
    file_arr.append(bkg_2)
  i = i + 1

file2 = Files(f2)
file2_arr = file2.Get_Files()

i = 0
for i in range(len(file2_arr)):
  if i == 0:
    print"sig_1 = ", file2_arr[i]
    sig_1 = TChain("NominalFixed")
    sig_1.AddFile(file2_arr[i])
    file_arr.append(sig_1)
  if i == 1:
    print"sig_2 = ", file2_arr[i]
    sig_2 = TChain("NominalFixed")
    sig_2.AddFile(file2_arr[i])
    file_arr.append(sig_2)
  if i == 2:
    print"sig_3 = ", file2_arr[i]
    sig_3 = TChain("NominalFixed")
    sig_3.AddFile(file2_arr[i])
    file_arr.append(sig_3)
  i = i + 1

x = 3                                                 #Dont forget when choosing a file, the index begins at 0
file = file_arr[x]
x = x + 1                                            #For naming purposes in Multiple Plots against a single variable Plotter
h3 = ROOT.TH3F("h3", "h3 title", 24, 0, 600, 24, 0, 600, 24, 0, 600)
c = ROOT.TCanvas("c", "",800,600)
gStyle.SetOptStat(0)
c.cd()

                       #Selections Cuts

old = '(num_bjets>=2)*(nj_good>=4)*(nEl+nMu==0)*'
noSC='(1)*'
PS='(eT_miss_orig>200)*(nEl+nMu==0)*(nj_good>=4)*(pT_1jet>80)*(pT_2jet>80)*(pT_4jet>40)*(dphimin4>0.4)*'
SRA=PS+'*(num_bjets>=2)*(MTbmin>200 )*( m_1fatjet_kt8>60)*( m_1fatjet_kt12>120)*(eT_miss>400)*(MT2Chi2>400)*'
SRB=PS+'*(num_bjets>=2)*(MTbmin_orig>200)*(m_1fatjet_kt12>120)*(dRb1b2>1.2)*'
ISR='(eT_miss_orig>200)*(pT_1jet>300)*'
Selection_Cuts = [noSC,PS,SRA,SRB,ISR]

luminosity="36100"
weights="AnalysisWeight*LumiWeight*pileupweight*btagweight*"
total=weights+Selection_Cuts[0]+luminosity

                       #Single Variable Plot

var = 'm_1fatjet_kt12'                                                   #var is on the y axis
var2="pT_1fatjet_kt12"                                                   #var2 is on the x axis
var3="mctTT"                                                   #var2 is on the x axis

a = "sample_{}".format(x)
file.Draw(var+":"+var2+":"+var3+">>h3",total,"")
h3.Draw("surf")
h3.SetTitle(a)
h3.GetXaxis().SetTitle(var2)
h3.GetYaxis().SetTitle(var)
h3.GetZaxis().SetTitle(var3)

'''
line = TLine(120,0,120,600)
line.SetLineWidth(4)
line.Draw("same")

line2 = TLine(0,120,600,120)
line2.SetLineWidth(4)
line2.Draw("same")

line3 = TLine(0,60,600,60)
line3.SetLineWidth(4)
line3.Draw("same")

text = ROOT.TText()
text.SetNDC()
text.SetTextFont(1)
text.SetTextColor(2)
text.SetTextSize(0.05)
text.SetTextAlign(22)
text.DrawText(0.5, 0.4, "TT")

text2 = ROOT.TText()
text2.SetNDC()
text2.SetTextFont(1)
text2.SetTextColor(2)
text2.SetTextSize(0.05)
text2.SetTextAlign(22)
text2.DrawText(0.5, 0.22, "TW")

text3 = ROOT.TText()
text3.SetNDC()
text3.SetTextFont(1)
text3.SetTextColor(2)
text3.SetTextSize(0.05)
text3.SetTextAlign(22)
text3.DrawText(0.5, 0.14, "T0")
'''
raw_input()
#save_path = '/home/jhall/SUSY/AnalysisWrapper/LocalAnalysis/plots/reco_fat_jet_study/SigVsBkg_Comp/updated_script_plots/2D_correlation/'
#c.SaveAs(save_path+a+"_reco_"+var+"_"+var2+"_noSC.pdf")


                      #Multiple Plots against a single variable
'''
var2="mctTT"
list_of_vars = ["m_1fatjet_kt8","m_1fatjet_kt12","m_2fatjet_kt8","m_2fatjet_kt12"]#,"m_3fatjet_kt8","m_3fatjet_kt12"]
a = "sample_{}".format(x)
for var in list_of_vars:
  file.Draw(var+":"+var2+">>h3",total,"")
  h3.Draw("colz")
  h3.SetTitle(a)
  h3.GetXaxis().SetTitle(var2)
  h3.GetYaxis().SetTitle(var)
  raw_input()
  #save_path = '/home/jhall/SUSY/AnalysisWrapper/LocalAnalysis/plots/reco_fat_jet_study/SigVsBkg_Comp/updated_script_plots/2D_correlation/'
  #c.SaveAs(save_path+a+"_reco_"+var+"_"+var2+"_PS.pdf")
'''

                      #Looping over samples
'''
var2="mctTT"
list_of_vars = ["m_1fatjet_kt8","m_1fatjet_kt12","m_2fatjet_kt8","m_2fatjet_kt12"]#,"m_3fatjet_kt8","m_3fatjet_kt12"]
i = 1
for file in file_arr:
  a = "sample_{}".format(i)
  for var in list_of_vars:
      file.Draw(var+":"+var2+">>h3",total,"")
      h3.Draw("colz")
      h3.SetTitle(a)
      h3.GetXaxis().SetTitle(var2)
      h3.GetYaxis().SetTitle(var)
      raw_input()
      save_path = '/home/jhall/SUSY/AnalysisWrapper/LocalAnalysis/plots/reco_fat_jet_study/SigVsBkg_Comp/updated_script_plots/2D_correlation/'
      c.SaveAs(save_path+a+"_reco_"+var+"_"+var2+"_noSC.pdf")
  i = i + 1
'''

                      #Root Code for var against var plotting
'''
Th3* h3 = new Th3F("h3", "h3 title", 100, 0, 1500, 100, 0, 1500)
NominalFixed->Draw("m_1fatjet_kt8:pT_1fatjet_kt8>>h3")
h3->Draw("colz")
'''
