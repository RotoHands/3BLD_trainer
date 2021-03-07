<!DOCTYPE html>
<html lang="en">
<head>





    <p>hello</p>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<?php
echo "hello"
echo filectime("currentLetterPair.txt");
echo "Last changed: ".date("F d Y H:i:s.", filectime("webdictionary.txt"));
?>
</body>
</html>