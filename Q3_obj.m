function y = Q3_obj(x)
    x1 = x(1);
    x2 = x(2);
    y = (3 + x1 + ((1 - x2) * x2 - 2) * x2)^2 + (3 + x1 + (x2 - 3) * x2)^2;
end