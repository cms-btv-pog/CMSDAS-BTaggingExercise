import FWCore.ParameterSet.Config as cms

process = cms.Process("USER")

## Load some standard configuration files
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("RecoBTag.Configuration.RecoBTag_cff") # this loads all available b-taggers

## Load the necessary conditions 
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')

## Load the MessageLogger
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

## Events to process
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(50)
)

## Options and Output Report
process.options   = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # /TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM
        '/store/mc/RunIISpring15DR74/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/Asympt25ns_MCRUN2_74_V9-v2/00000/1041602E-9508-E511-8094-003048FFD7BE.root'
    )
)

## Clone the existing TagInfo configurations
process.MyImpactParameterTagInfos = process.pfImpactParameterTagInfos.clone(
    jets = cms.InputTag("ak4PFJetsCHS") # use ak4PFJetsCHS stored in AOD as input
)
process.MySecondaryVertexTagInfos = process.pfSecondaryVertexTagInfos.clone(
    trackIPTagInfos = cms.InputTag("MyImpactParameterTagInfos") # use the above IP TagInfos as input
)

## Clone the existing b-tagger configurations and use the above TagInfos as input
process.MyTrackCountingHighEffBJetTags = process.pfTrackCountingHighEffBJetTags.clone(
    tagInfos = cms.VInputTag(cms.InputTag("MyImpactParameterTagInfos"))
)
process.MySimpleSecondaryVertexHighEffBJetTags = process.pfSimpleSecondaryVertexHighEffBJetTags.clone(
    tagInfos = cms.VInputTag(cms.InputTag("MySecondaryVertexTagInfos"))
)

## Output file
process.out = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('keep *'), 
    fileName = cms.untracked.string('outfile.root')
)

## Define a Path
process.p = cms.Path(
    process.MyImpactParameterTagInfos
    * process.MyTrackCountingHighEffBJetTags
    * process.MySecondaryVertexTagInfos
    * process.MySimpleSecondaryVertexHighEffBJetTags
)

## Define the EndPath
process.output = cms.EndPath(
    process.out
)
