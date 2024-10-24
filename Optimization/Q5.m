% Initial problem setup
f = [5; 3; 4]; 
A = [43,25,57;
    83,34,63]; 
b = [150;200]; 
lb = zeros(3,1);
ub = [2;2;2];

%Step0: Initialize LP relaxtion problem
[x,z] = linprog(-f, A, b,[],[], lb, ub);
x;
best = (f'*x);

%Step1&2: Branching and Bounding
%for x1 (x1<=0 or x1>=0+1)
lb = zeros(3,1);
ub = [0;2;2];
[x_1,z_1] = linprog(-f, A, b,[],[], lb, ub);
x_1;
z_1;

lb = [1;0;0];
ub = [2;2;2];
[x_2,z_2] = linprog(-f, A, b,[],[], lb, ub);
x_2;
z_2;

%Under x1<=0 for x3 (x3<=1 or x3>=1+1)
lb = zeros(3,1);
ub = [0;2;1];
[x_3,z_3] = linprog(-f, A, b,[],[], lb, ub);
x_3;
z_3;