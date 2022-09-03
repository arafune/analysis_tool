function [b]= getbasis2_w()
% Given pmn2/1 and that the basis atoms are present at 
%WP d, c and a  
ba_W1 = [0 0.60 0.5; 0.5 1-0.60 0.5+0.5]; 
ba_W2 = [0 0.03 0.015; 0.5 1-0.03 0.015+0.5]; 
ba_Te1 = [0 0.85 0.655; 0.5 1-0.85 0.655+0.5]; 
ba_Te2 = [0 0.646  0.11; 0.5 1-0.646  0.11+0.5]; 
ba_Te3 = [0 0.298 0.859; 0.5 1-0.298 0.859+0.5];
ba_Te4 = [0 0.207 0.403; 0.5 1-0.207 0.403+0.5]; 
b=[ba_W1;ba_W2;ba_Te1;ba_Te2;ba_Te3;ba_Te4];
end