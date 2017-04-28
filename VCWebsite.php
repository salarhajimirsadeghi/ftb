<?php
// Include the ShoppingCart class.  Since the session contains a
// ShoppingCard object, this must be done before session_start().
//require "C:/xampp/htdocs/cart.php";
include('dbconn.php');

$dbname = "VCs";
$conn = connect_to_db($dbname);
session_start();
$vcName = $_GET["vc"];
echo "Your VC Choice is " . $vcName;

$vcQuery = "SELECT VC_NAME, DESCRIPTION, IMAGE from VCs where VC_Name = $vcName";
$vc = $conn->prepare($vcQuery);

$companyQuery = "SELECT CID from VC_COMPANY where VID = $vcName";
$company = $conn->prepare($companyQuery);

$companyNameQuery = "SELECT COMPANY_NAME, IMAGE FROM COMPANIES WHERE CID = $company";
$companyName = $conn -> prepare($companyNameQuery);


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
    <h1 id = "companyName"> VC Name</h1>
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
        <th>Companies Invested In</th>
      </tr>

  <p><?php


    while($row = mysql_fetch_array($companyName)){
    echo "<tr>";
    echo "<td>". $row['COMPANY_NAME'] . "<img src = 'data:image/jpeg;base64,'". base64_encode($row['IMAGE']) . " alt = 'companyPic' style = ' width: 30px; height: 30px'></td>";
  }
  echo "</table>"



  //  echo"<table>
    //<thead>
  //   <tr>
  //     <th>Companies Invested In</th>
  //   </tr>
  //   </thead>";
  //
  //
  // echo "</table>";
  // echo "<input type ='submit' value = 'Update' name = 'submitButton'>" . "</input>" ;


  ?></p>
</div>
</center>
</body>
</html>
