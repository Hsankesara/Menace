num_iter = 1000;
Q = zeros(num_iter,10);
N = zeros(1,10);
R = zeros(1, num_iter);
epsilon = 0.1;
for t=1:num_iter
    if rand > epsilon
        [m, id] = max(Q(t, :));
        A = id;
    else
        temp = randperm(10);
        A = temp(1);
    end 
    r = bandit(A);
    if t>1
        R(t) = ((R(t-1)*(t-1)) + r) / t;
    end
    N(A) = N(A) + 1;
    Q(t + 1, A) = Q(t, A) + (r - Q(t, A)) / N(A);
end
plot([1:num_iter], R)