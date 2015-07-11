#
# Simple script to extract the b-tag discriminators for b and light-flavor jets
#

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


# b-tagger
bTagger = 'pfCombinedInclusiveSecondaryVertexV2BJetTags'

# input file
inputFile = TFile('exerciseII_histos_ttbar.root')

# get 2D b-tag discriminator vs jet pT histograms
discrVsPt_b    = inputFile.Get('bTaggingExerciseII/' + bTagger + '_b')
discrVsPt_c    = inputFile.Get('bTaggingExerciseII/' + bTagger + '_c')
discrVsPt_udsg = inputFile.Get('bTaggingExerciseII/' + bTagger + '_udsg')

# make y-axis projections to get 1D discriminator distributions
discr_b    = discrVsPt_b.ProjectionY()
discr_c    = discrVsPt_c.ProjectionY()
discr_udsg = discrVsPt_udsg.ProjectionY()

# create canvas
c = TCanvas("c", "",1200,800)
c.cd()

# light-flavor jets
discr_udsg.GetXaxis().SetTitle("pfCSVv2IVF discriminator")
discr_udsg.GetXaxis().SetRangeUser(-0.005,1.005)
discr_udsg.SetLineWidth(1)
discr_udsg.SetLineColor(4) # blue
discr_udsg.SetFillColor(4) # blue
discr_udsg.SetFillStyle(3001)

# c jets
discr_c.SetLineWidth(1)
discr_c.SetLineColor(8) # green
discr_c.SetFillColor(8) # green
discr_c.SetFillStyle(3001)


# b jets
discr_b.SetLineWidth(1)
discr_b.SetLineColor(2) # red
discr_b.SetFillColor(2) # red
discr_b.SetFillStyle(3001)

# adjust the y-axis range
discr_udsg.SetMaximum(1.7*discr_b.GetMaximum())

# draw histograms
discr_udsg.DrawNormalized('hist')
discr_c.DrawNormalized('histsame')
discr_b.DrawNormalized('histsame')

# create legend
legend = TLegend(.50,.60,.80,.75)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.04)
legend.AddEntry(discr_b,"b jets","f")
legend.AddEntry(discr_c,"c jets","f")
legend.AddEntry(discr_udsg,"udsg jets","f")
legend.Draw()

gPad.RedrawAxis()

# save the plot
c.SaveAs('pfCSVv2IVF_discriminator.png')

c.SetLogy()
c.SaveAs('pfCSVv2IVF_discriminator_log.png')

# close the input file
inputFile.Close()
