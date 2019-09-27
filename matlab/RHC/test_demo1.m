A = [eye(2);-eye(2)];
b = [1;1;-0.5;-0.5];
u = 2;
c = [1; 1];
D = [1; 1];

% optimization variables
nx = size(A, 2);
x = sdpvar(nx, 1);

% parameter
theta = sdpvar(1, 1);

% objective function
J = (c+D*theta)'*x;

% constraints
C = [ A*x+[theta;0;-theta;0] <= b, x>=0, 0<=theta<=u];

plp = Opt( C, J, theta, x);
solution = plp.solve();

for i = 1:nx
    figure;
    solution.xopt.fplot('primal','position',i);
    xlabel('theta');
    ylabel(sprintf('x_%d(t)',i));
end

figure;
solution.xopt.fplot('obj');
xlabel('theta');
ylabel('J(t)');

% plot critical regions
figure;
solution.xopt.plot();
xlabel('theta (critical regions)')

% for theta = 0.5
t0=0.5;
x_t0=solution.xopt.feval(t0,'primal')
J_t0=solution.xopt.feval(t0,'obj')
