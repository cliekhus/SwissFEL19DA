energy = linspace(2,4,1000);
finalSpectra_ACN = zeros(size(energy));
finalSpectra_Cl = zeros(size(energy));

width = 1/30;

for ii = 1:length(ACN_Energy)
    if ACN_Energy(ii) < 4
    finalSpectra_ACN = finalSpectra_ACN + ACN_Prob(ii)./((energy-ACN_Energy(ii)).^2+width);
    end
end
   

for ii = 1:length(Cl_Energy)
    if Cl_Energy(ii) < 4
    finalSpectra_Cl = finalSpectra_Cl + Cl_Prob(ii)./((energy-Cl_Energy(ii)).^2+width);
    end
end

figure();
plot(energy, finalSpectra_ACN/6.5659)
hold on;
stem(ACN_Energy, ACN_Prob/max(ACN_Prob))
plot([3.391, 3.391],[0,1], 'k', 'linewidth', 2)
xlim([2,4])
title('ACN')

figure();
plot(energy, finalSpectra_Cl/6.1258)
hold on;
stem(Cl_Energy, Cl_Prob/max(Cl_Prob))
plot([3.391, 3.391],[0,1], 'k', 'linewidth', 2)
xlim([2,4])
title('Cl')