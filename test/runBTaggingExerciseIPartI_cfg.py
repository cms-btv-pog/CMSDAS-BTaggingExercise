import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('reportEvery', 10,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "Report every N events (default is N=10)"
)
options.register('outputFilename', 'exerciseIPartI_histos.root',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Output file name"
)
options.register('wantSummary', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Print out trigger and timing summary"
)

## 'maxEvents' is already registered by the Framework, changing default value
options.setDefault('maxEvents', 100)

options.parseArguments()

process = cms.Process("USER")

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # /TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM
        #'/store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/00C90EFC-3074-E411-A845-002590DB9262.root'
        'file:/data/shared/Short_Exercise_BTag/MINIAOD_Phys14DR_TTJets_PU20bx25/00C90EFC-3074-E411-A845-002590DB9262.root'
    )
)

## Output file
process.TFileService = cms.Service("TFileService",
   fileName = cms.string(options.outputFilename)
)

## Options and Output Report
process.options   = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(options.wantSummary),
    allowUnscheduled = cms.untracked.bool(True)
)

## Initialize analyzer
process.bTaggingExerciseIPartI = cms.EDAnalyzer('BTaggingExerciseI',
    jets = cms.InputTag('slimmedJets'), # input jet collection name
    bDiscriminators = cms.vstring(      # list of b-tag discriminators to access
        'trackCountingHighEffBJetTags',
        'trackCountingHighPurBJetTags',
        'jetProbabilityBJetTags',
        'jetBProbabilityBJetTags',
        'simpleSecondaryVertexHighEffBJetTags',
        'simpleSecondaryVertexHighPurBJetTags',
        'combinedSecondaryVertexBJetTags',
        'combinedInclusiveSecondaryVertexV2BJetTags'
    )
)

## Let it run
process.p = cms.Path(process.bTaggingExerciseIPartI)
