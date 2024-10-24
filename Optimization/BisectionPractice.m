options.maxit = 1000;
options.tol = 1e-5;
xl = 1.5; xr = 4.5;
gl = g(xl);
gr = g(xr);

[x,gx] = Bisection(@g,xl,xr,options);
fprintf('Root found at x = %.5f, g(x) = %.5f\n', x, gx);
