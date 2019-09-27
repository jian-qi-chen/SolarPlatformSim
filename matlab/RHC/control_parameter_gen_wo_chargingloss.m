T = 10; %minutes, time step
preh = 24*60; %minutes, prediction horizon
N = 6; % number of prediction interval, SHOULD BE 6 OTHERWISE rewrite constraints
L = preh/T/N; % prediction interval (in time steps)
ECMAX_wh = 10; %maximum stored energy in battery in Watt hour
ECMAX = ECMAX_wh * 3600 / 1000; % in KJ (1000 Joules)
alpha_t = 0; %alpha in equation(8)

X = sdpvar(N+1,1); % in KJ, Parameter vector [Ec(t),E~(t,0),E~(t,1),...,E~(t,N-1)]'
U = sdpvar(N,1); % controller's output, in W
lam = sdpvar(1,1); % lambda

obj = -lam; % objective: -lambda
% constraints
cons = [ U(1)>=lam, U(2)>=lam, U(3)>=lam, U(4)>=lam, U(5)>=lam, U(6)>=lam,...
    X(2)>=0, X(3)>=0, X(4)>=0, X(5)>=0, X(6)>=0, X(7)>=0,...
    0 <= X(1) <= ECMAX,...
    0 <= X(1)+X(2)-L*T*60*U(1)/1000 <= ECMAX,...
    0 <= X(1)+X(2)+X(3)-L*T*60*(U(1)+U(2))/1000 <= ECMAX,...
    0 <= X(1)+X(2)+X(3)+X(4)-L*T*60*(U(1)+U(2)+U(3))/1000 <= ECMAX,...
    0 <= X(1)+X(2)+X(3)+X(4)+X(5)-L*T*60*(U(1)+U(2)+U(3)+U(4))/1000 <= ECMAX,...
    0 <= X(1)+X(2)+X(3)+X(4)+X(5)+X(6)-L*T*60*(U(1)+U(2)+U(3)+U(4)+U(5))/1000 <= ECMAX,...
    0 <= X(1)+X(2)+X(3)+X(4)+X(5)+X(6)+X(7)-L*T*60*(U(1)+U(2)+U(3)+U(4)+U(5)+U(6))/1000 <= ECMAX,...
    X(1)+X(2)+X(3)+X(4)+X(5)+X(6)+X(7)-L*T*60*(U(1)+U(2)+U(3)+U(4)+U(5)+U(6))/1000 >= X(1)+alpha_t]

[sol,diagn,Z,hpwf,zpwf] = solvemp(cons,obj,[],X);

ncr = size(sol{1}.Fi,2) %number of critical regions
mkdir results
delete results/*

for i =1:ncr
    B_t = sol{1}.Fi{i};
    C_t = sol{1}.Gi{i};
    [H_t,K_t] = double( sol{1}.Pn(i) );
    %disp(length(K))
    
    B = zero_filter(B_t);
    C = zero_filter(C_t);
    H = zero_filter(H_t);
    K = zero_filter(K_t);
    
    writematrix(B_t,strcat('results/B',string(i),'.txt'))
    writematrix(C_t,strcat('results/C',string(i),'.txt'))
    writematrix(H_t,strcat('results/H',string(i),'.txt'))
    writematrix(K_t,strcat('results/K',string(i),'.txt'))
end

function out = zero_filter(A)
    for i = 1:size(A,1)
        for j = 1:size(A,2)
            if abs( A(i,j) ) < 1e-8
                out(i,j) = 0;
            else
                out(i,j) = A(i,j);
            end
        end
    end
end
