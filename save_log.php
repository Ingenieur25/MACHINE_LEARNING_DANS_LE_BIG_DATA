<?php
// Set the timezone to GMT+1
date_default_timezone_set('Etc/GMT-1'); // GMT+1 is written as GMT-1 in PHP's timezone settings

// Get the incoming log data
$data = json_decode(file_get_contents("php://input"), true);

// Check if the log entry exists
if (isset($data['log'])) {
    // Use the log message as provided
    $logMessage = $data['log'];
    $timestamp = $data['timestamp'] ?? date('Y-m-d H:i:s'); // Use provided timestamp or current time

    // Convert the timestamp to DateTime and apply the GMT+1 timezone
    $datetime = new DateTime($timestamp);
    $datetime->setTimezone(new DateTimeZone(date_default_timezone_get())); // Adjust the timezone to GMT+1

    // Define the base directory for logs
    $baseLogDir = 'Logs'; // Directory where all logs are stored

    // Ensure the base directory exists
    if (!is_dir($baseLogDir)) {
        mkdir($baseLogDir, 0777, true);
    }

    // Format the directory name and file name based on the adjusted time
    $directory = $baseLogDir . DIRECTORY_SEPARATOR . $datetime->format('YmdH'); // Full path to directory: Logs/YearMonthDayHour
    $filename = $directory . DIRECTORY_SEPARATOR . $datetime->format('YmdHis') . '.txt'; // Full path to file: Logs/YearMonthDayHour/YearMonthDayHourMinuteSecond.txt

    // Create the subdirectory if it doesn't exist
    if (!is_dir($directory)) {
        mkdir($directory, 0777, true);
    }

    // Write the log message directly to the corresponding file
    file_put_contents($filename, $logMessage . PHP_EOL, FILE_APPEND);

    // Return a success response
    echo json_encode(['status' => 'success', 'message' => 'Log saved successfully']);
} else {
    // Return an error response
    echo json_encode(['status' => 'error', 'message' => 'No log entry provided']);
}
?>

