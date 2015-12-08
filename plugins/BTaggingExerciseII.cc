// -*- C++ -*-
//
// Package:    CMSDAS2015/BTaggingExercise
// Class:      BTaggingExerciseII
// 
/**\class BTaggingExerciseII BTaggingExerciseII.cc CMSDAS2015/BTaggingExercise/plugins/BTaggingExerciseII.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Dinko Ferencek
//         Created:  Tue, 16 Dec 2014 00:09:47 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

#include "TH2F.h"

//
// class declaration
//

class BTaggingExerciseII : public edm::EDAnalyzer {
   public:
      explicit BTaggingExerciseII(const edm::ParameterSet&);
      ~BTaggingExerciseII();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      const edm::InputTag jets_;
      const std::vector<std::string> bDiscriminators_;

      edm::Service<TFileService> fs;

      // declare a map of b-tag discriminator histograms
      std::map<std::string, TH2F *> bDiscriminatorsMap;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
BTaggingExerciseII::BTaggingExerciseII(const edm::ParameterSet& iConfig) :

  jets_(iConfig.getParameter<edm::InputTag>("jets")),
  bDiscriminators_(iConfig.getParameter<std::vector<std::string> >("bDiscriminators"))

{
   std::string bDiscr_flav = "";
   // initialize b-tag discriminator histograms
   for( const std::string &bDiscr : bDiscriminators_ )
   {
     for( const std::string &flav : {"b","c","udsg"} )
     {
       bDiscr_flav = bDiscr + "_" + flav;
       if( bDiscr.find("Counting") != std::string::npos ) // track counting discriminator can be both positive and negative and covers a wider range then other discriminators
         bDiscriminatorsMap[bDiscr_flav] = fs->make<TH2F>(bDiscr_flav.c_str(), (bDiscr_flav + ";Jet p_{T} [GeV];b-tag discriminator").c_str(), 20, 0, 200, 11000, -15, 40);
       else
         bDiscriminatorsMap[bDiscr_flav] = fs->make<TH2F>(bDiscr_flav.c_str(), (bDiscr_flav + ";Jet p_{T} [GeV];b-tag discriminator").c_str(), 20, 0, 200, 4400, -11, 11);
     }
   }
}


BTaggingExerciseII::~BTaggingExerciseII()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
BTaggingExerciseII::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  // define a jet handle
  edm::Handle<std::vector<pat::Jet> > jets;
  // get jets from the event
  iEvent.getByLabel(jets_, jets);

  std::string bDiscr_flav = "";
  // loop over jets
  for( auto jet = jets->begin(); jet != jets->end(); ++jet )
  {
    int flavor = std::abs( jet->hadronFlavour() );
    // fill discriminator histograms
    for( const std::string &bDiscr : bDiscriminators_ )
    {
      if( jet->pt()<30. || std::abs(jet->eta())>2.4 ) continue; // skip jets with low pT or outside the tracker acceptance

      if( flavor==5 ) // b jet
        bDiscr_flav = bDiscr + "_b";
      else if( flavor==4 ) // c jets
        bDiscr_flav = bDiscr + "_c";
      else // light-flavor jet
        bDiscr_flav = bDiscr + "_udsg";

      bDiscriminatorsMap[bDiscr_flav]->Fill( jet->pt(), jet->bDiscriminator(bDiscr) );
    }
  }
}


// ------------ method called once each job just before starting event loop  ------------
void 
BTaggingExerciseII::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
BTaggingExerciseII::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
BTaggingExerciseII::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
BTaggingExerciseII::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
BTaggingExerciseII::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
BTaggingExerciseII::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
BTaggingExerciseII::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(BTaggingExerciseII);
