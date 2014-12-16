#
# Simple script to extract the MC b-tagging efficiencies and mistag rates
#

import copy, optparse
from ROOT import *

#---------------------------------------------------------------------
# to run in the batch mode (to prevent canvases from popping up)
gROOT.SetBatch()

# set plot style
gROOT.SetStyle("Plain")

# suppress the statistics box
gStyle.SetOptStat(0)

# suppress the histogram title
gStyle.SetOptTitle(0)

gStyle.SetPadTickX(1)  # to get the tick marks on the opposite side of the frame
gStyle.SetPadTickY(1)  # to get the tick marks on the opposite side of the frame

# set nicer fonts
gStyle.SetTitleFont(42, "XYZ")
gStyle.SetLabelFont(42, "XYZ")
#---------------------------------------------------------------------

parser = optparse.OptionParser(usage="")

parser.add_option('-o', '--operating_point', metavar='OPERATING_POINT', action='store', dest='operating_point', default='medium', help='Operating point to use')

(options, args) = parser.parse_args(args=None)


# b-tagger
bTagger = 'combinedInclusiveSecondaryVertexV2BJetTags'

# medium operating point
operatingPoint = 0.814 # CSVv2IVFM
if options.operating_point == 'loose': operatingPoint = 0.423 # CSVv2IVFL
if options.operating_point == 'tight': operatingPoint = 0.941 # CSVv2IVFT

# input files
inputFile_ttbar = TFile('exerciseII_histos_ttbar.root')
inputFile_QCD   = TFile('exerciseII_histos_QCD.root')

# get 2D b-tag discriminator vs jet pT histograms
discrVsPt_b_ttbar    = inputFile_ttbar.Get('bTaggingExerciseII/' + bTagger + '_b')
discrVsPt_udsg_ttbar = inputFile_ttbar.Get('bTaggingExerciseII/' + bTagger + '_udsg')
discrVsPt_b_QCD      = inputFile_QCD.Get('bTaggingExerciseII/' + bTagger + '_b')
discrVsPt_udsg_QCD   = inputFile_QCD.Get('bTaggingExerciseII/' + bTagger + '_udsg')

# make x-axis projections to get 1D distributions of the total number of b and light-flavor (udsg) jets
total_b_ttbar    = copy.deepcopy(discrVsPt_b_ttbar.ProjectionX("_px1"))
total_udsg_ttbar = copy.deepcopy(discrVsPt_udsg_ttbar.ProjectionX("_px1"))
total_b_QCD      = copy.deepcopy(discrVsPt_b_QCD.ProjectionX("_px1"))
total_udsg_QCD   = copy.deepcopy(discrVsPt_udsg_QCD.ProjectionX("_px1"))

# here we are finding the bin containing the operationg point discriminator threshold
firstbin = discrVsPt_b_ttbar.GetYaxis().FindBin(operatingPoint)
lastbin = discrVsPt_b_ttbar.GetYaxis().GetNbins() + 1 # '+ 1' to also include any entries in the overflow bin

# make x-axis projections to get 1D distributions of the number of tagged b and light-flavor (udsg) jets
# note that here we are integrating from the bin containing the operating point discriminator threshold.
# hence, the definition of the operationg point is only approximate since the bin boundary will not necessarily
# coincide with the operating point discriminator threshold
tagged_b_ttbar    = copy.deepcopy(discrVsPt_b_ttbar.ProjectionX("_px2",firstbin,lastbin))
tagged_udsg_ttbar = copy.deepcopy(discrVsPt_udsg_ttbar.ProjectionX("_px2",firstbin,lastbin))
tagged_b_QCD      = copy.deepcopy(discrVsPt_b_QCD.ProjectionX("_px2",firstbin,lastbin))
tagged_udsg_QCD   = copy.deepcopy(discrVsPt_udsg_QCD.ProjectionX("_px2",firstbin,lastbin))

# create canvas
c = TCanvas("c", "",1200,800)
c.cd()

# b jets
eff_b_ttbar = TGraphAsymmErrors(tagged_b_ttbar, total_b_ttbar, "cp")
eff_b_ttbar.GetXaxis().SetTitle("Jet p_{T} [GeV]")
eff_b_ttbar.GetYaxis().SetTitle("b-tagging efficiency")
eff_b_ttbar.GetXaxis().SetRangeUser(0.,200.)
eff_b_ttbar.GetYaxis().SetRangeUser(0.,1.)
eff_b_ttbar.SetLineWidth(2)
eff_b_ttbar.SetLineColor(kRed)
eff_b_ttbar.SetMarkerColor(kRed)
eff_b_ttbar.SetMarkerStyle(20)
eff_b_ttbar.Draw('ap')

eff_b_QCD = TGraphAsymmErrors(tagged_b_QCD, total_b_QCD, "cp")
eff_b_QCD.SetLineWidth(2)
eff_b_QCD.SetLineColor(kBlack)
eff_b_QCD.SetMarkerColor(kBlack)
eff_b_QCD.SetMarkerStyle(21)
eff_b_QCD.Draw('p')

legend = TLegend(.70,.30,.90,.40)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.04)
legend.AddEntry(eff_b_ttbar,"t#bar{t}","lp")
legend.AddEntry(eff_b_QCD,"QCD","lp")
legend.Draw()

# save the plot
c.SaveAs('bTaggingEfficiency_CSVv2IVFM.png')

# light-flavor jets
mistag_udsg_ttbar = TGraphAsymmErrors(tagged_udsg_ttbar, total_udsg_ttbar, "cp")
mistag_udsg_ttbar.GetXaxis().SetTitle("Jet p_{T} [GeV]")
mistag_udsg_ttbar.GetYaxis().SetTitle("Mistag rate")
mistag_udsg_ttbar.GetXaxis().SetRangeUser(0.,200.)
mistag_udsg_ttbar.GetYaxis().SetRangeUser(1e-4,1e+0)
mistag_udsg_ttbar.SetLineWidth(2)
mistag_udsg_ttbar.SetLineColor(kRed)
mistag_udsg_ttbar.SetMarkerColor(kRed)
mistag_udsg_ttbar.SetMarkerStyle(20)
mistag_udsg_ttbar.Draw('ap')

mistag_udsg_QCD = TGraphAsymmErrors(tagged_udsg_QCD, total_udsg_QCD, "cp")
mistag_udsg_QCD.SetLineWidth(2)
mistag_udsg_QCD.SetLineColor(kBlack)
mistag_udsg_QCD.SetMarkerColor(kBlack)
mistag_udsg_QCD.SetMarkerStyle(21)
mistag_udsg_QCD.Draw('p')

# create legend
legend = TLegend(.70,.30,.90,.40)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.04)
legend.AddEntry(mistag_udsg_ttbar,"t#bar{t}","lp")
legend.AddEntry(mistag_udsg_QCD,"QCD","lp")
legend.Draw()

# show y-axis in log scale
c.SetLogy()

# save the plot
c.SaveAs('MistagRate_CSVv2IVFM.png')

# close the input files
inputFile_ttbar.Close()
inputFile_QCD.Close()
