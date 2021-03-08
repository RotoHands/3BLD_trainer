<!DOCTYPE html>
<html lang="en">
<head>






    <meta charset="UTF-8">
    <title>3BLDRoto	</title>
</head>
<style>

div.a {
	position: absolute;
	top:0;
	bottom: 250px;
	left: 0;
	right: 0;

	margin: auto;
  border-radius: 25px;
  border: 10px solid LightBlue;

  width: 450px;
  height: 300px;

 max-width: 500px;

  text-align: center;
  font-family: "Rubik", "Rubik";
  font-weight: 600;
  font-size: 15rem;
  letter-spacing: 2px;

}
.c {
  border-radius: 25px;
  border: 0px solid dodgerBlue;
  position: absolute;
	top:450px;
	bottom: 0;
	left: 0;
	right: 0;

  width: 700x;
  height: 80px;
  margin: auto;
  text-align: center;
  font-family: "Rubik", "Rubik";
  font-weight: 600;
  font-size: 4rem;
  letter-spacing: 2px;
}

.b {
  border-radius: 25px;
  border: 0px solid dodgerBlue;
  position: absolute;
	top:180px;
	bottom: 0;
	left: 0;
	right: 0;

  width: 500px;
  height: 80px;
  margin: auto;
  text-align: center;
  font-family: "Rubik", "Rubik";
  font-weight: 600;
  font-size: 4rem;
  letter-spacing: 2px;
}


</style>
<body>
<?php



$lastTimeFileOpened =  filemtime("C:\\Users\\rotem\\PycharmProjects\\pythonProject\\BLD\currentLetterPair.txt");

sleep(1);
$letterpair = "";
$res="";
$stringAlg="";
$currentLetterPair = fopen("C:\\Users\\rotem\\PycharmProjects\\pythonProject\\BLD\currentLetterPair.txt", "r") or die("Unable to open file!");
while(!feof($currentLetterPair)) {
	$letterpair .= fgetc($currentLetterPair);
}
fclose($currentLetterPair);

$currentResult = fopen("C:\\Users\\rotem\\PycharmProjects\\pythonProject\\BLD\‏‏currentLetterPairResults.txt", "r") or die("Unable to open file!");
while(!feof($currentResult)) {
	$res .= fgetc($currentResult);
}
fclose($currentResult);

$currentAlg = fopen("C:\\Users\\rotem\\PycharmProjects\\pythonProject\\BLD\algString.txt", "r") or die("Unable to open file!");
while(!feof($currentAlg)) {
	$stringAlg .= fgetc($currentAlg);
}
fclose($currentAlg);


header("Refresh:0");
?>

<div class = "a"><?php echo $letterpair ?></div>
<div class = "b"><?php echo $res ?></div>
<div class = "c"><?php echo $stringAlg ?></div>
</body>
</html>