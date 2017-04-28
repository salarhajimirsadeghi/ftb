<?php
// Include the ShoppingCart class.  Since the session contains a
// ShoppingCard object, this must be done before session_start().
//require "C:/xampp/htdocs/cart.php";
include('dbconn.php');

$dbname = "VCs";
$conn = connect_to_db($dbname);
session_start();
$companyName = $_GET["vc"];
echo "Your VC Choice is " . $vcName;

$companyQuery = "SELECT COMPANY_NAME, DESCRIPTION, IMAGE, CID from COMPANIES where VC_NAME = $companyName";
$company = $conn->prepare($companyQuery);

$vcQuery = "SELECT VID from VC_COMPANY where CID = $company['CID']";
$company = $conn->prepare($companyQuery);

$vcNameQuery = "SELECT VC_NAME, IMAGE FROM VCs WHERE VID = $vcQuery";
$vcName = $conn -> prepare($vcNameQuery);


//$gSelect->bind_param("s", $gname);

//if($conn -> connect_error){
  //die("Connection failed: " . $conn->connect_error);
//}
//$sql = $conn->prepare("SELECT Companies WHERE Name");

//print_r($_SESSION);
//echo "<br>after starting a session in viewcart...";
?>


<!DOCTYPE html>
<html>
<head>
<title>VC Website</title>
<link href="companyVC.css" rel = "stylesheet" type = "text/css">
</head>
<body>
  <center>
<div id = "header-content">
  <div id = "VCPic">
    <img src = "" alt = "VCPic" style = "width: 50%; height: 29%;">
  </div>
  <div id = "VCContainer">
    <h1 id = "companyName"> Company Name</h1>
  </div>
</div>
</center>
<center>
<div id = "middle-content">
  <h2>Description</h2>
  <h3><p id = "description"></p></h3>
</div>
</center>
<center>
<div id = "bottom-content">
  <table>
      <tr>
        <th>VC Invested In It</th>
      </tr>

  <p><?php


    while($row = mysql_fetch_array($vcName)){
    echo "<tr>";
    echo "<td>". $row['COMPANY_NAME'] . "<img src = 'data:image/jpeg;base64,'". base64_encode($row['IMAGE']) . " alt = 'companyPic' style = ' width: 30px; height: 30px'></td>";
  }
  echo "</table>";

  ?></p>
</div>
</center>
</body>
</html>
