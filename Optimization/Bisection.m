function [x, gx] = Bisection(g, xl, xr, options)
    gr = g(xr); 
    gl = g(xl); 
    sl = sign(gl);
    if gr*gl > 0
        fprintf(1, 'The input is not suitable\n');
        x = []; 
        gx = []; 
        return;
    end
    for i = 1:options.maxit
        xm = (xl + xr) / 2; 
        gm = g(xm);
        if abs(gm) < options.tol || abs(xl - xr) < options.tol
            x = xm; 
            gx = gm; 
            return;
        end
        if gm > 0
            if sl < 0, xr = xm; else, xl = xm; end
        else
            if sl < 0, xl = xm; else, xr = xm; end
        end
    end
end
