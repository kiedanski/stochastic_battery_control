def generate(ss, T, e_ch, e_dis, ramp_up, ramp_down, b_max, b_min, b_ini, zs,
            pb, ps):
    if b_ini > b_max:
        b_ini = b_max
    elif b_ini < b_min:
        b_ini = b_min
    max_t = max(pb) * (max(max(zs), 0) + ramp_up)
    min_t = max(ps) * (min(min(zs), 0) + ramp_down)

    first_stage = '\n'.join([str(j) for j in range(ss)])
    second_stage = '\n'.join([str(j) for j in range(ss, T)])
    periods = '\n'.join([str(j) for j in range(T)])
    zs = '\n'.join([f'{k} {zs[k]}' for k in range(T)])
    ps = '\n'.join([f'{k} {ps[k]}' for k in range(T)])
    pb = '\n'.join([f'{k} {pb[k]}' for k in range(T)])

    output = f"""

set first_stage :=
{first_stage};

set second_stage :=
{second_stage};

set periods :=
{periods};

param e_ch      := {e_ch};
param e_dis     := {e_dis};
param ramp_up   := {ramp_up};
param ramp_down := {-ramp_down};
param b_max     := {b_max};
param b_min     := {b_min};
param b_ini     := {b_ini};
param max_t     := {max_t};
param min_t     := {min_t};
param zs        := {zs};
param pb        := {pb};
param ps        := {ps};

"""
    return output
