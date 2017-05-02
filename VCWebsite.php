<?php
// Include the ShoppingCart class.  Since the session contains a
// ShoppingCard object, this must be done before session_start().
//require "C:/xampp/htdocs/cart.php";
//include('dbconn.php');
$dbc = mysqli_connect( "localhost", "root", "", "vcs");
//mysql_select_db("vcs", $dbc);
// $dbname = "VCs";
// $conn = connect_to_db($dbname);
session_start();
$vcName = $_GET["vc"];
echo "Your VC Choice is " . $vcName;

//$vcQuery = [];
$vcQuery = "SELECT VID from VCs where VC_NAME = $vcName";
//VC_NAME, DESCRIPTION, IMAGE,
//$vcQuery = "SELECT VID from VCs where VC_NAME = $vcName";
$vc = mysqli_query($dbc, $vcQuery);

$vcDescriptionQuery = "SELECT DESCRIPTION from VCs where VC_NAME = $vcName";
$vcDescription = mysqli_query($dbc, $vcDescriptionQuery);

$vcImageQuery = "SELECT IMAGE from VCs where VC_NAME = $vcName";
$vcImage = mysqli_query($dbc, $vcImageQuery);

echo("*******************" . $vc);
//run a for loop over result
//store each element into a different variable
//pass that into the companyQuery VID
//$companyQuery =[];
$companyIDQuery = "";
$companyArr = array();
//foreach($vc as $res){
  //$theVID = $res['VID'];
  $companyIDQuery = "SELECT CID from VC_COMPANY where VID = $vc";
  $companyID = mysqli_query($dbc, $companyIDQuery);
  foreach ($companyID as $comp) {// for each compqny put that in an array.....
    array_push($companyArr, $comp);
//store that result in an array ** TODO **
   }


//}

// $companyQuery = "SELECT CID from VC_COMPANY where VID = $vc['VID']";
// $company = $conn->prepare($companyQuery);
//search how to iterate over a query select result
//$companyName = [];
//$companyNameQuery = [];
$companyNameQuery = "";
$companyNameArr = array();
foreach($companyArr as $cRes){
  //$theCID = $cRes['CID'];
  $companyNameQuery = "SELECT COMPANY_NAME, IMAGE FROM COMPANIES WHERE CID = $cRes";
  $row = mysqli_query($dbc, $companyNameQuery);
  $companyNameArr[$row['COMPANY_NAME']]= $row['IMAGE'];

  //store that result in an array -** TODO **

}



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
    <<?php
    echo "<img src = 'data:image/jpeg;base64'". base64_encode($vcImage) . "alt = 'VCPic' style = 'width: 50%; height: 29%;'";
    ?>>
  </div>
  <div id = "VCContainer">
    <h1 id = "vcCompanyName"> <<?php echo" ". $vcName . " " ?>></h1>
  </div>
</div>
</center>
<center>
<div id = "middle-content">
  <h2>Description</h2>
  <h3><p id = "description"><<?php echo " " . $vcDescription . " " ?>></p></h3>
</div>
</center>
<center>
<div id = "bottom-content">
  <table>
      <tr>
        <th>Companies Invested In</th>
      </tr>

  <p><?php


    foreach($companyNameArr as $name => $image){
    echo "<tr>";
    echo "<td>". $name . "<img src = 'data:image/jpeg;base64,'". base64_encode($image) . " alt = 'companyPic' style = ' width: 30px; height: 30px'></td>";
  }
  echo "</table>";

  ?></p>
</div>
</center>
</body>
</html>
