def generate_structure(datafiles):

    N = len(datafiles)
    nodes = '\n'.join([f'Node{i}' for i in range(N)])
    nodestage = '\n'.join([f'Node{i} SecondStage' for i in range(N)])
    nodesprob = '\n'.join([f'Node{i} {1 / N}' for i in range(N)])
    scenarios = '\n'.join([x[:-4] for x in datafiles])
    scenarionodes = '\n'.join([x[:-4] + f' Node{i}' for i, x in enumerate(datafiles)])
    



    output = f"""
set Stages := FirstStage SecondStage;

set Nodes :=
RootNode
{nodes}
;

param NodeStage :=
RootNode FirstStage
{nodestage}
;

set Children[RootNode] :=
{nodes}
;

param ConditionalProbability :=
RootNode 1.0
{nodesprob}
;

set Scenarios :=
{scenarios}
;

param ScenarioLeafNode :=
{scenarionodes}
;

set StageVariables[FirstStage] :=
xcf[*]
xdf[*]
;

set StageVariables[SecondStage] :=
xcs[*]
xds[*]
tsf[*]
tss[*]
;

param StageCost :=
FirstStage FirstStageCost
SecondStage SecondStageCost
;"""

    return output
