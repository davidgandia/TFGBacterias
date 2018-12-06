//El objetivo de este macro es sacar un fondo de las bacterias junto con las bacterias inmóviles
#@String (label = "filePath") imagePath
#@String (label = "fileOutPath") imageOutPath

open(imagePath);
run("Subtract Background...", "rolling=1 light sliding stack");
run("Invert", "stack");
run("Z Project...", "projection=[Average Intensity]");   
imageCalculator("subtract stack", 1, 2)
saveAs("Tiff", imageOutPath);




