cvx_begin
    variables x y
    minimize -7.8*x-7.1*y
    subject to 
        x/4+ y/3 <= 90
        x/8 + y/3 <= 80
        x >= 0
        y >= 0
cvx_end
cvx