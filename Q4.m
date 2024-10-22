f = [16;14;15];
A1 = [-1,-1,0;
    0,-1,-1;
    -1,0,-1];
b1 = [-1;-1;-1];
A2 = [-1,-1,-1];
b2 = [-2];
cvx_begin
    variables x(3)
    minimize (f'*x)
    subject to
        A1 * x <= b1
cvx_end
cvx_begin
    variables x(3)
    minimize (f'*x)
    subject to
        A2 * x <= b2
cvx_end