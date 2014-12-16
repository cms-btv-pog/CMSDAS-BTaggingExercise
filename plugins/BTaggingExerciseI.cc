// -*- C++ -*-
//
// Package:    CMSDAS2015/BTaggingExercise
// Class:      BTaggingExerciseI
// 
/**\class BTaggingExerciseI BTaggingExerciseI.cc CMSDAS2015/BTaggingExercise/plugins/BTaggingExerciseI.cc

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

#include "TH1F.h"

//
// class declaration
//

class BTaggingExerciseI : public edm::EDAnalyzer {
   public:
      explicit BTaggingExerciseI(const edm::ParameterSet&);
      ~BTaggingExerciseI();

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
      std::map<std::string, TH1F *> bDiscriminatorsMap;
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
BTaggingExerciseI::BTaggingExerciseI(const edm::ParameterSet& iConfig) :

  jets_(iConfig.getParameter<edm::InputTag>("jets")),
  bDiscriminators_(iConfig.getParameter<std::vector<std::string> >("bDiscriminators"))

{
   // initialize b-tag discriminator histograms
   for( const std::string &bDiscr : bDiscriminators_ )
   {
     if( bDiscr.find("Counting") != std::string::npos ) // track counting discriminator can be both positive and negative and covers a wider range then other discriminators
       bDiscriminatorsMap[bDiscr] = fs->make<TH1F>(bDiscr.c_str(), (bDiscr + ";b-tag discriminator").c_str(), 1100, -15, 40);
     else
       bDiscriminatorsMap[bDiscr] = fs->make<TH1F>(bDiscr.c_str(), (bDiscr + ";b-tag discriminator").c_str(), 440, -11, 11);
   }
}


BTaggingExerciseI::~BTaggingExerciseI()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
BTaggingExerciseI::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

}


// ------------ method called once each job just before starting event loop  ------------
void 
BTaggingExerciseI::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
BTaggingExerciseI::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
BTaggingExerciseI::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
BTaggingExerciseI::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
BTaggingExerciseI::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
BTaggingExerciseI::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
BTaggingExerciseI::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(BTaggingExerciseI);
