#
# Simple script to produce the performance plots
#

from array import array
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

# adjust margins
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)

# set grid color to gray
gStyle.SetGridColor(kGray)

gStyle.SetPadTickX(1)  # to get the tick marks on the opposite side of the frame
gStyle.SetPadTickY(1)  # to get the tick marks on the opposite side of the frame

# set nicer fonts
gStyle.SetTitleFont(42, "XYZ")
gStyle.SetLabelFont(42, "XYZ")
#---------------------------------------------------------------------

def makeEffVsMistagTGraph(histo_b,histo_nonb,allowNegative):

    b_eff = array('f')
    nonb_eff = array('f')
    tot_b= histo_b.GetEntries()
    tot_nonb= histo_nonb.GetEntries()

    #print "Total number of jets:"
    #print tot_b,"b jets"
    #print tot_nonb,"non-b jets"

    b_abovecut = 0
    nonb_abovecut = 0

    firstbin = histo_b.GetXaxis().FindBin(0.) - 1
    if allowNegative: firstbin = -1
    lastbin = histo_b.GetXaxis().GetNbins() + 1 # '+ 1' to also include any entries in the overflow bin

    for i in xrange(lastbin,firstbin,-1) : # from 'overflow' bin to 0, in steps of "-1"
        b_abovecut += histo_b.GetBinContent(i)
        nonb_abovecut += histo_nonb.GetBinContent(i)
        b_eff.append(b_abovecut/tot_b)
        nonb_eff.append(nonb_abovecut/tot_nonb)

    return TGraph(len(b_eff), b_eff, nonb_eff)


def main():

    # input file
    inputFile = TFile.Open('exerciseII_histos_ttbar.root')

    # b-taggers
    bTaggers = [
        'pfTrackCountingHighEffBJetTags',
        'pfTrackCountingHighPurBJetTags',
        'pfSimpleSecondaryVertexHighEffBJetTags',
        'pfSimpleSecondaryVertexHighPurBJetTags',
        'pfJetProbabilityBJetTags',
        'pfJetBProbabilityBJetTags',
        'pfCombinedInclusiveSecondaryVertexV2BJetTags'
    ]
    color = [kOrange, kRed, kCyan, kGreen, kMagenta, kBlue, kBlack]
    legend = ['pfTCHE', 'pfTCHP', 'pfSSVHE', 'pfSSVHP', 'pfJP', 'pfJBP', 'pfCSVv2IVF']

    # non-b flavors
    nonbs = ['c','udsg']

    # loop over non-b flavors
    for nonb in nonbs:
        # create canvas
        c = TCanvas("c", "",800,800)
        c.cd()
        c.SetGridx()
        c.SetGridy()
        c.SetLogy()

        # empty 2D background historgram to simplify defining axis ranges to display
        bkg = TH2F('bkg',';b jet tagging efficiency;' + nonb + ' jet mistag rate',100,0.,1.,100,((1e-3 if nonb=='c' else 1e-4)),1.)
        bkg.GetYaxis().SetTitleOffset(1.2)
        bkg.Draw()

        # create legend
        leg = TLegend(.20,.80-(0.04*len(bTaggers)),.40,.80)
        leg.SetBorderSize(0)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(42)
        leg.SetTextSize(0.03)

        # dictionary to store eff vs mistag rate graphs
        g = {}

        # loop over b-taggers
        for t, bTagger in enumerate(bTaggers):
            # get 2D b-tag discriminator vs jet pT histograms
            discrVsPt_b    = inputFile.Get('bTaggingExerciseII/' + bTagger + '_b')
            discrVsPt_nonb = inputFile.Get('bTaggingExerciseII/' + bTagger + '_' + nonb)

            # make y-axis projections to get 1D discriminator distributions
            discr_b    = discrVsPt_b.ProjectionY()
            discr_nonb = discrVsPt_nonb.ProjectionY()

            allowNegative = False
            if( 'Counting' in bTagger ): allowNegative = True
            # get eff vs mistag rate graph
            g[t] = makeEffVsMistagTGraph(discr_b,discr_nonb,allowNegative)
            g[t].SetLineWidth(2)
            g[t].SetLineColor(color[t])
            g[t].Draw('l')
            leg.AddEntry(g[t],legend[t],"l")

        leg.Draw()

        gPad.RedrawAxis()

        # save the plot
        c.SaveAs('bTagEffVsMistagRate_' + nonb + '.png')

        c.Close()
        bkg.Delete()

    # close the input file
    inputFile.Close()


if __name__ == '__main__':
    main()
