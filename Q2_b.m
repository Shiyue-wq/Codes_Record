cvx_begin
    variables y1 y2 y3
    maximize 25*y1 + 40*y2 + 400*y3
    subject to
        4*y1 + 8*y2 + 130*y3 <= 2
        6*y1 + 12*y2 + 120*y3 <= 3.5
       20*y1 + 150*y3 <= 8
       y1 + 30*y2 + 70*y3 <= 1.5
        y1 >= 0
        y2 >= 0
        y3 >= 0
cvx_end