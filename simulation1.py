from compare_mpcs import compare

def show(j, res):
    s = f'Points: {j}, True {res[0]["obj"]:0.02f}, MPC {res[3]:0.02f}, SMPC {res[4]:0.02f}'
    print(s)

print('User 1, 2012 - 10 - 22 - No true present')
for i in range(5, 20):
    r0 = compare(1, 2012, 10, 22, i)
    if r0 is not None:
        show(i, r0)

print('User 1, 2012 - 10 - 22 - True present')
for i in range(5, 20):
    r0 = compare(1, 2012, 10, 22, i, True)
    if r0 is not None:
        show(i, r0)

print('User 1, 2013 - 05 - 22 - No true present')
for i in range(5, 20):
    r0 = compare(1, 2013, 5, 22, i)
    if r0 is not None:
        show(i, r0)

print('User 1, 2013 - 05 - 22 - True present')
for i in range(5, 20):
    r0 = compare(1, 2013, 5, 22, i, True)
    if r0 is not None:
        show(i, r0)

print('User 300, 2012 - 10 - 22 - No true present')
for i in range(5, 20):
    r0 = compare(300, 2012, 10, 22, i)
    if r0 is not None:
        show(i, r0)

print('User 300, 2012 - 10 - 22 - True present')
for i in range(5, 20):
    r0 = compare(300, 2012, 10, 22, i, True)
    if r0 is not None:
        show(i, r0)
