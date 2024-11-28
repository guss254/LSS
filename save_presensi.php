<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "test";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$nama = $_POST['nama'];
$unit_kerja = $_POST['unit_kerja'];
$waktu = $_POST['waktu'];
$alamat = $_POST['alamat'];
$foto = $_POST['foto'];

$foto_data = explode(',', $foto)[1];

$foto_name = uniqid() . '.png';
$foto_path = 'uploads/' . $foto_name;

file_put_contents($foto_path, base64_decode($foto_data));

$sql = "INSERT INTO absen (nama, unit, tanggal, alamat, foto) 
        VALUES ('$nama', '$unit_kerja', '$waktu', '$alamat', '$foto_name')";

if ($conn->query($sql) === TRUE) {
    echo "Presensi berhasil disimpan!";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
