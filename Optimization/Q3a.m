syms x1 x2
obj = (3 + x1 + ((1 - x2) * x2 - 2) * x2)^2 + (3 + x1 + (x2 - 3) * x2)^2;
g1 = diff(obj, x1);
g2 = diff(obj, x2);
stationary_points = solve([g1 == 0, g2 == 0], [x1, x2]);
H = hessian(obj, [x1, x2]);

disp('Stationary points:');
disp([stationary_points.x1, stationary_points.x2]);

if length(stationary_points.x1) > 1
    for i = 1:length(stationary_points.x1)
        stationary_value = subs(obj, [x1, x2], [stationary_points.x1(i), stationary_points.x2(i)]);
        fprintf('Value at stationary point %d: %f\n', i, double(stationary_value));
        H_eval = double(subs(H, [x1, x2], [stationary_points.x1(i), stationary_points.x2(i)]));
        eigenvalues = eig(H_eval);
    if all(eigenvalues > 0)
        disp('It is a local minimum.');
    elseif all(eigenvalues < 0)
        disp('It is a local maximum.');
    else
        disp('It is a saddle point.');
    end
    end
else
    stationary_value = subs(obj, [x1, x2], [stationary_points.x1, stationary_points.x2]);
    disp('Value at stationary point:');
    disp(double(stationary_value));
end
