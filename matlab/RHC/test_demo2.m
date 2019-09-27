A = randn(15,3);
b = rand(15,1);
E = randn(15,2);

z = sdpvar(3,1);
obj = (z-1)'*(z-1)

x = sdpvar(2,1);
F = [A*z <= b+E*x, -1 <= x <= 1];

[sol,diagn,z,hpwf,zpwf] = solvemp(F,obj,[],x);