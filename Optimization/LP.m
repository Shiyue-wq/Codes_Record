[x1, x2] = meshgrid(-3:.1:3, -3:.1:3);
F = x1.* exp(-0.5 * (x1.^2 + x2.^2));
surf(x1, x2, F, 'FaceAlpha',0.5);
colormap('winter');
hold on;
value = exp(-5/8);
plot3(-1, 0.5, -value, 'ro', 'MarkerSize', 10, 'LineWidth', 2); 
[t1, t2] = meshgrid(-1.5:.1:-0.5, -1:.1:1); 
T = -value + 0.5*value*(t2-0.5) + value*(t1+1).^2 + 3/8*value*(t2-0.5).^2;
surf(t1, t2, T, 'FaceColor', 'flat', 'FaceAlpha', 1);
hold off;
