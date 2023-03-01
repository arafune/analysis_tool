function writexyz2 (Name1, X, Y, Z)
fp = fopen('WTe2.xyz', "W");
fprintf(fp, '%10d\n', length (X));
fprintf (fp, '%s\n', "WTe2 lattice");
for j=1:length (X)
fprintf (fp, '%1s\t%12.5f\t%12.5f\t%12.5f\n',Name1, X (j), Y(j),Z(j));
end
fclose(fp);
end
