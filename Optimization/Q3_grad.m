function y = Q3_grad(x)
    x1 = x(1);
    x2 = x(2);
    y1 = 2 * (3 + x1 + ((1 - x2) * x2 - 2) * x2) + 2 * (3 + x1 + (x2 - 3) * x2);
    y2 = 2*(2*x2 - 3)*(x1 + x2*(x2 - 3) + 3) - 2*(x2*(2*x2 - 1) + x2*(x2 - 1) + 2)*(x1 - x2*(x2*(x2 - 1) + 2) + 3);
    y = [y1; y2];
end