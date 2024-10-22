%% Initialization
x = [0,0];
epsilon = 10^(-5);
iter = 0;
beta = 0.5;
gamma = 0.1;

% %% Backtracking method
%  while norm(Q3_grad(x)) > epsilon 
%     d = -Q3_grad(x);
%  
%     t = 1;
%     
%     xtemp = x + t * d;
%     while Q3_obj(xtemp) >= Q3_obj(x) + gamma * t * Q3_grad(x)' * d 
%          t = t * beta;
%          xtemp = x + t * d;
%     end
    

%%Doing exact line search
while norm(Q3_grad(x)) > epsilon
    d = -Q3_grad(x);
    phi = (3 - sqrt(5)) / 2; 
    iteration = 0;

    xl = x; 
    xr = x + 2 * d; 
    while norm(xr - xl)> 10^(-6) && iteration <= 100
        iteration = iteration + 1;
        x1 = phi * xr + (1 - phi) * xl;
        x2 = phi * xl + (1 - phi) * xr;
        if  Q3_obj(x1) >  Q3_obj(x2)
            xl = x1;
        else
            xr = x2;
        end
    end

    xtemp = (xr + xl) / 2;


    plot(x(1), x(2), '*r');
    hold on;
    plot([x(1), xtemp(1)], [x(2), xtemp(2)], '-g');
    hold on;
   
   iter = iter + 1
   x = xtemp;

end

     axis([-0.9, 0.1, -0.5, 0.1])
     hold off;

disp(['Final iteration: ', num2str(iter)]);
disp(['Final x values: [', num2str(x(1)), ', ', num2str(x(2)), ']']);
