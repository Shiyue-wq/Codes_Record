cvx_begin
    variables x1 x2 x3 x4
    minimize 2*x1 + 3.5*x2 + 8*x3 +1.5*x4
    subject to
        4*x1 + 6*x2 + 20*x3 + x4 >= 25
        8*x1 + 12*x2 + 30*x4 >= 40
        130*x1 + 120*x2 + 150*x3 + 70*x4 >= 400
        x1 >= 0
        x2 >= 0
        x3 >= 0
        x4 >= 0
cvx_end
