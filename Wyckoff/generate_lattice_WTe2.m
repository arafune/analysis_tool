% To generate crystal for WTe2 using Wyckoff Position 
function generate_lattice_WTe2 ()
a = 3.477;
b = 6.249;
c = 14.017;
beta = 90;
n1= [0]; n2= [0]; n3= [0]; % integers
V = [a 0 0; 0 b 0; 0 0 c]; % three lattice vectors (a=1).
basis = getbasis2_w(); % as many basis as needed obtained from Wyckoff table
[nb] = size(basis); atom=1; % atom is just a counter
for k=1:length(n1)
    for l=1:length(n2)
        for m=1:length(n3)
            for b=1:nb
            H = V (1,:)*n1 (k) + V(2,:)*n2 (1) + V(3,:)* n3 (m)...
                +basis (b, 1) * V (1, :) + basis (b, 2) *V (2, :) +...
                 basis (b, 3) *V (3, :);
           X(atom) = H(1); Y(atom) = H(2); Z(atom) = H(3);
           atom=atom+1;
           end
        end
     
    end
end
plot3 (X,Y,Z,'o', 'MarkerFaceColor', 'r', 'MarkerSize', 20);
Name1 = "W"; writexyz2 (Name1, X, Y,Z) 
%Name2 = "Te"; writexyz3 (Name2, X, Y,Z)
