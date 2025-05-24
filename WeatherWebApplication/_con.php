<?php
// Set the content type to JSON for the response
header('Content-Type: application/json');
// Allow cross-origin requests from any domain (CORS)
header("Access-Control-Allow-Origin: *");
// Allow specific HTTP methods (GET, POST, PUT, DELETE, OPTIONS) in cross-origin requests
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');

// Making connection to database
$serverName = "sql308.infinityfree.com";
$userName = "if0_38740847";
$password = "B5QQtBj5o4iNr";
$databaseName = "if0_38740847_appweather";
$conn = mysqli_connect($serverName, $userName, $password, $databaseName);

if (!$conn) {
    die("Failed to connect: " . mysqli_connect_error());
}

// Function to create database
function createDatabase($conn) {
    $createDatabase = "CREATE DATABASE IF NOT EXISTS `$databaseName`";
    mysqli_query($conn, $createDatabase);
    if (!mysqli_query($conn, $createDatabase)) {
        die("Error creating database: " . mysqli_error($conn));
    }
}

// Function to create table
function createWeatherTable($conn) {
    $createTable = "CREATE TABLE IF NOT EXISTS weather (
        city_name VARCHAR(255) NOT NULL,
        temperature FLOAT NOT NULL,
        weather_condition TEXT NOT NULL,
        weather_description TEXT NOT NULL,
        pressure FLOAT NOT NULL,
        humidity FLOAT NOT NULL,
        wind_speed FLOAT NOT NULL,
        wind_direction FLOAT NOT NULL,
        icon TEXT NOT NULL,
        dt INT NOT NULL,
        timezone INT NOT NULL,
        lastfetched INT NOT NULL,
        PRIMARY KEY (city_name)
    );";

    mysqli_query($conn, $createTable);
}

// Function to extract data in associative array
function extractWeatherData($data) {
    return [
        'temperature' => $data['main']['temp'],
        'condition' => $data['weather'][0]['main'],
        'descriptions' => $data['weather'][0]['description'],
        'pressure' => $data['main']['pressure'],
        'humidity' => $data['main']['humidity'],
        'wind_speed' => $data['wind']['speed'],
        'wind_direction' => $data['wind']['deg'],
        'icon' => $data['weather'][0]['icon'],
        'dt' => $data['dt'],
        'timezone' => $data['timezone'],
    ];
}

// Function to insert or update data as required
function insertOrUpdateWeatherData($conn, $cityName, $data, $isNewData) {
    $weatherData = extractWeatherData($data);
    $currentTimestamp = time();

    if ($isNewData) {
        $insertData = "INSERT INTO weather (city_name, temperature, weather_condition, weather_description, pressure, humidity, wind_speed, wind_direction, icon, dt, timezone, lastfetched)
        VALUES ('$cityName', {$weatherData['temperature']}, '{$weatherData['condition']}', '{$weatherData['descriptions']}', {$weatherData['pressure']}, {$weatherData['humidity']}, {$weatherData['wind_speed']}, {$weatherData['wind_direction']}, '{$weatherData['icon']}', {$weatherData['dt']}, {$weatherData['timezone']}, $currentTimestamp)";
        mysqli_query($conn, $insertData);
    } else {
        $updateData = "UPDATE weather SET 
            temperature = {$weatherData['temperature']}, 
            weather_condition = '{$weatherData['condition']}', 
            weather_description = '{$weatherData['descriptions']}', 
            pressure = {$weatherData['pressure']}, 
            humidity = {$weatherData['humidity']}, 
            wind_speed = {$weatherData['wind_speed']}, 
            wind_direction = {$weatherData['wind_direction']}, 
            icon = '{$weatherData['icon']}', 
            dt = {$weatherData['dt']}, 
            timezone = {$weatherData['timezone']}, 
            lastfetched = $currentTimestamp
        WHERE city_name = '$cityName'";
        mysqli_query($conn, $updateData);
    }
}

// Function to retrieve and return the timestamp of the last weather data fetch for a specific city
function getLastFetchedTime($conn, $cityName) {
    $selectLastFetched = "SELECT lastfetched FROM weather WHERE city_name = '$cityName'";
    $resultLastFetched = mysqli_query($conn, $selectLastFetched);
    $lastFetchedRow = mysqli_fetch_assoc($resultLastFetched);
    return $lastFetchedRow['lastfetched'];
}

// Function to fetch data in the database
function fetchWeatherData($conn, $cityName) {
    $selectAllData = "SELECT * FROM weather WHERE city_name = '$cityName'";
    $result = mysqli_query($conn, $selectAllData);

    if (mysqli_num_rows($result) == 0) {
        $data = getWeatherDataFromAPI($cityName);
        if (isset($data['main'])) {
            insertOrUpdateWeatherData($conn, $cityName, $data, true);
        }

    } else {
        $lastFetched = getLastFetchedTime($conn, $cityName);

        $currentTimestamp = time();

        if (($currentTimestamp - $lastFetched) > 7200) {

            $data = getWeatherDataFromAPI($cityName);
            if (isset($data['main'])) {
                insertOrUpdateWeatherData($conn, $cityName, $data, false);
            }
        }
    }

    $rows = [];
    $result = mysqli_query($conn, $selectAllData);
    while ($row = mysqli_fetch_assoc($result)) {
        $rows[] = $row;
    }
    return json_encode($rows);
}

// Function to return the data fetched from the API
function getWeatherDataFromAPI($cityName) {
    $apiURL = "https://api.openweathermap.org/data/2.5/weather?units=metric&q=";
    $apiKey = "402fedade5914e983b66bf4e5e208f90";
    $url = $apiURL . $cityName . "&appid=" . $apiKey;

    $response = file_get_contents($url);
    return json_decode($response, true);
}

createWeatherTable($conn);

// Declaring city as global variable
$cityName = isset($_GET['city']) ? urlencode($_GET['city']) : "Gadsden";
// Retrieving the data
$json_data = fetchWeatherData($conn, $cityName);
// Displaying the data
echo $json_data;

// Closing mysqli connection
mysqli_close($conn);
?>