import ROOT
from ROOT import gStyle, TLegend, TFile, TChain, TLine
#Last Built July 2018
#Things to improve: Make a method for normalisation, make a method for cols for histos (cols:reds,blues,etc)
#(continued) make a class method for x axis labelling, change lists to list comphrensions

#f1 = Bkg
#f2 = Sig
f1 = "/home/jhall/SUSY/MasterShefWD/LocalAnalysis/samples/reco_Matts/processed/mctTTkt8/ttbar_processed_kt8.txt"
f2 = "/home/jhall/SUSY/MasterShefWD/LocalAnalysis/samples/reco_Matts/processed/mctTTkt8/stop0L_processed_kt8.txt"

'''
class Colours:
  def __init__(self, cols):
    self.cols = cols

standard = Colours([63,206, 59, 205, 213,1, 2, 3])

print standard.cols()
print Colours.cols(standard)
'''

class Files:
  def __init__(self,master_file):
    self.master_file = master_file

  def Get_OG_Files(self):
    subfile = open(self.master_file,"r")
    arr = []
    for line in subfile:
      l = list(line)
      n = len(line)
      l[n-1:n] = []
      x = "".join(l)
      arr.append(x)
    return arr                                                #Returns an array of strings of the files

  @staticmethod
  def Process_Files(file_arr):
    emp_arr = []
    i = 0
    for i in range (len(file_arr)):
      print"Sample_"+str(i)+" = "+file_arr[i]
      a = TChain("NominalFixed")
      a.AddFile(file_arr[i])
      emp_arr.append(a)
      i = i + 1
    return emp_arr                                            #Returns an array of TChain Root Objects

  @staticmethod
  def create_total_file_arr(file_arr1, file_arr2):
    final_file_arr = []
    for x in file_arr1:
      final_file_arr.append(x)
    for x in file_arr2:
      final_file_arr.append(x)
    return final_file_arr

  @staticmethod
  def Multi_Var(file_arr, list_of_vars):
    c = ROOT.TCanvas("c", "",800,600)
    c.SetLogy()
    gStyle.SetOptStat(0)

    cols = [63,206, 59, 205, 213,1, 2, 3]
    norm = 1

    hists = []
    legend_names = []
    i = 0
    y = i + 1
    for var in list_of_vars:
      x = var
      legend_names.append(x)

      h = "h_var{}".format(y)      
      file_arr.Draw(var+">>"+h+"(14,0,1400)",total,"")
      h = c.GetPrimitive(h)

      h.SetLineColor(cols[i])
      h.SetLineWidth(5)
      scale = norm/h.Integral()
      h.Scale(scale)
      h.Draw("hist e")
      h.GetYaxis().SetTitle("Normalised Events")
      h.SetTitle(title)
      if 'pT' in x:
        h.GetXaxis().SetTitle("pT [GeV]")

      hist = h.Clone()
      hists.append(hist)
      h.Delete()
      i = i + 1
      y = y + 1

    legend = TLegend(0.677945,0.655052,0.883459,0.893728)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.025)
    i = 0
    for hist in hists:
      if i == 0:
        hist.Draw("hist e")
        legend.AddEntry(hist,legend_names[i])
      else:
        hist.Draw("hist e same")
        legend.AddEntry(hist,legend_names[i])
      i = i + 1
    legend.Draw()
    #save_path = '/home/jhall/SUSY/AnalysisWrapper/LocalAnalysis/plots/reco_fat_jet_study/pT_dists/'
    #c.SaveAs(save_path+title+"_reco_MultiVarPlot_"+x+".pdf")
    raw_input()



master_file1 = Files(f1)
master_file1_arr = Files.Get_OG_Files(master_file1)
master_file2 = Files(f2)
master_file2_arr = Files.Get_OG_Files(master_file2)

                                  #Gather Arrays for Data Analysis

subfile1_arr = Files.Process_Files(master_file1_arr)
subfile2_arr = Files.Process_Files(master_file2_arr)
total_file_arr = Files.create_total_file_arr(subfile1_arr, subfile2_arr)

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
total=weights+Selection_Cuts[1]+luminosity

                                        #Variable arrays listings

fat_jet_m_vars = ["m_1fatjet_kt12","m_2fatjet_kt12","m_1fatjet_kt8","m_2fatjet_kt8"]
fat_jet_pT_vars = ["pT_1fatjet_kt8", "pT_2fatjet_kt8", "pT_1fatjet_kt12", "pT_2fatjet_kt12", 'eT_miss']
mct_vars = ["mctTT"]

sample_no = 3
sample_title = sample_no + 1
title = "Sample_{}".format(sample_title)
Files.Multi_Var(total_file_arr[sample_no],fat_jet_pT_vars)
