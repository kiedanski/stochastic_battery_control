from pyomo.core import *

model = AbstractModel()

model.first_stage = Set()
model.second_stage = Set()
model.periods = Set()

model.e_ch      = Param(within = PositiveReals)
model.e_dis     = Param(within = PositiveReals)
model.ramp_up   = Param(within = PositiveReals)
model.ramp_down = Param(within = PositiveReals)
model.b_max = Param(within = NonNegativeReals)
model.b_min = Param(within = NonNegativeReals)
model.b_ini = Param(within = NonNegativeReals)

model.max_t = Param(within = Reals)
model.min_t = Param(within = Reals)

model.zs = Param(model.periods, within = Reals)
model.pb = Param(model.periods, within = PositiveReals)
model.ps = Param(model.periods, within = PositiveReals)


model.xcf = Var(model.first_stage, within = NonNegativeReals, bounds=(0, model.ramp_up))
model.xdf = Var(model.first_stage, within = NonNegativeReals, bounds=(0,
                                                                      model.ramp_down))
model.tsf = Var(model.first_stage, within = Reals,
                bounds=(model.min_t, model.max_t))

model.xcs = Var(model.second_stage, within = NonNegativeReals, bounds=(0, model.ramp_up))
model.xds = Var(model.second_stage, within = NonNegativeReals, bounds=(0,
                                                                      model.ramp_down))
model.tss = Var(model.second_stage, within = Reals,
                bounds=(model.min_t, model.max_t))

## Model constraints

def tfirststage_ps(model, i):
    cons = model.ps[i] * (model.xcf[i] / model.e_ch - model.xdf[i] *
                          model.e_dis + model.zs[i]) <= model.tsf[i]
    return cons
model.t_firststage_ps = Constraint(model.first_stage, rule=tfirststage_ps)

def tfirststage_pb(model, i):
    cons = model.pb[i] * (model.xcf[i] / model.e_ch - model.xdf[i] *
                          model.e_dis + model.zs[i]) <= model.tsf[i]
    return cons
model.t_firststage_pb = Constraint(model.first_stage, rule=tfirststage_pb)

def tsecondstage_ps(model, i):
    cons = model.ps[i] * (model.xcs[i] / model.e_ch - model.xds[i] *
                          model.e_dis + model.zs[i]) <= model.tss[i]
    return cons
model.t_secondstage_ps = Constraint(model.second_stage, rule=tsecondstage_ps)

def tsecondstage_pb(model, i):
    cons = model.pb[i] * (model.xcs[i] / model.e_ch - model.xds[i] *
                          model.e_dis + model.zs[i]) <= model.tss[i]
    return cons
model.t_secondstage_pb = Constraint(model.second_stage, rule=tsecondstage_pb)


## Battery charging/discharging constraints

def first_stage_range_up(model, i):
    cons = sum(model.xcf[j] - model.xdf[j] for j in range(i + 1)) <= model.b_max - model.b_ini
    return cons
model.first_stage_range_up = Constraint(model.first_stage,
                                        rule=first_stage_range_up)
def first_stage_range_low(model, i):
    cons = sum(model.xcf[j] - model.xdf[j] for j in range(i + 1)) >= model.b_min - model.b_ini
    return cons
model.first_stage_range_low = Constraint(model.first_stage,
                                        rule=first_stage_range_low)

def second_stage_range_up(model, i):
    min_r = min(model.second_stage)
    cons1 = sum([model.xcf[j] - model.xdf[j] for j in range(min_r)])
    cons2 = sum([model.xcs[j] - model.xds[j] for j in range(min_r, i + 1)])
    cons = cons1 + cons2 <= model.b_max - model.b_ini
    return cons
model.second_stage_range_up = Constraint(model.second_stage,
                                         rule=second_stage_range_up)
def second_stage_range_low(model, i):
    min_r = min(model.second_stage)
    cons1 = [model.xcf[j] - model.xdf[j] for j in range(min_r)]
    cons2 = [model.xcs[j] - model.xds[j] for j in range(min_r, i + 1)]
    cons = sum(cons1 + cons2) >= model.b_min - model.b_ini
    return cons
model.second_stage_range_low = Constraint(model.second_stage,
                                         rule=second_stage_range_low)


#### Objective function

def first_stage_cost(model):
    return 0
model.FirstStageCost = Expression(rule=first_stage_cost)

def second_stage_cost(model):
    return summation(model.tss) + summation(model.tsf)
model.SecondStageCost = Expression(rule=second_stage_cost)

def total_cost(model):
    return model.FirstStageCost + model.SecondStageCost

model.obj = Objective(rule=total_cost, sense=minimize)
