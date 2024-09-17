<?php
$servername = "localhost"; 
$username = "root";        
$password = "Muxe@2001";            
$dbname = "my_online_library"; 

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

