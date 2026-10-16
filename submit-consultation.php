<?php
// Enable error reporting for development (remove in production)
error_reporting(E_ALL);
ini_set('display_errors', 0);

// Start session for flash messages
session_start();

// Configuration
$to_email = "info@terraconsulting.co.tz"; // Your email address
$subject = "New Consultation Request - Terra Consulting";
$success_redirect = "index.html#contact";
$error_redirect = "index.html#contact";

// Function to sanitize input
function sanitize_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

// Function to validate email
function validate_email($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL);
}

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // Initialize error array
    $errors = array();
    
    // Get and sanitize form data
    $name = isset($_POST['name']) ? sanitize_input($_POST['name']) : '';
    $email = isset($_POST['email']) ? sanitize_input($_POST['email']) : '';
    $company = isset($_POST['company']) ? sanitize_input($_POST['company']) : '';
    $industry = isset($_POST['industry']) ? sanitize_input($_POST['industry']) : '';
    $service = isset($_POST['service']) ? sanitize_input($_POST['service']) : '';
    $message = isset($_POST['message']) ? sanitize_input($_POST['message']) : '';
    
    // Validate required fields
    if (empty($name)) {
        $errors[] = "Name is required";
    }
    
    if (empty($email)) {
        $errors[] = "Email is required";
    } elseif (!validate_email($email)) {
        $errors[] = "Invalid email format";
    }
    
    if (empty($company)) {
        $errors[] = "Company name is required";
    }
    
    if (empty($industry)) {
        $errors[] = "Industry selection is required";
    }
    
    if (empty($service)) {
        $errors[] = "Service interest is required";
    }
    
    // Honeypot field for spam protection (add this hidden field in your HTML form)
    if (!empty($_POST['website'])) {
        // This is likely spam
        die("Spam detected");
    }
    
    // If no errors, proceed with sending email
    if (empty($errors)) {
        
        // Prepare email content
        $email_content = "New Consultation Request\n\n";
        $email_content .= "Name: " . $name . "\n";
        $email_content .= "Email: " . $email . "\n";
        $email_content .= "Company: " . $company . "\n";
        $email_content .= "Industry: " . ucfirst($industry) . "\n";
        $email_content .= "Service Interest: " . ucfirst($service) . "\n";
        $email_content .= "Message: " . $message . "\n\n";
        $email_content .= "Submitted on: " . date('Y-m-d H:i:s') . "\n";
        $email_content .= "IP Address: " . $_SERVER['REMOTE_ADDR'] . "\n";
        
        // Email headers
        $headers = "From: " . $email . "\r\n";
        $headers .= "Reply-To: " . $email . "\r\n";
        $headers .= "X-Mailer: PHP/" . phpversion();
        
        // Send email
        if (mail($to_email, $subject, $email_content, $headers)) {
            // Success - redirect with success message
            $_SESSION['form_success'] = "Thank you! Your consultation request has been submitted successfully. We'll get back to you within 24 hours.";
            
            // Optional: Save to database
            // save_to_database($name, $email, $company, $industry, $service, $message);
            
            header("Location: " . $success_redirect . "?status=success");
            exit();
        } else {
            // Email failed
            $_SESSION['form_error'] = "Sorry, there was an error sending your message. Please try again or contact us directly at info@terraconsulting.co.tz";
            header("Location: " . $error_redirect . "?status=error");
            exit();
        }
        
    } else {
        // Validation errors
        $_SESSION['form_error'] = "Please fix the following errors: " . implode(", ", $errors);
        header("Location: " . $error_redirect . "?status=error");
        exit();
    }
    
} else {
    // Not a POST request
    header("Location: index.html");
    exit();
}

// Optional: Function to save to database
/*
function save_to_database($name, $email, $company, $industry, $service, $message) {
    $servername = "localhost";
    $username = "your_db_username";
    $password = "your_db_password";
    $dbname = "your_db_name";
    
    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    
    // Check connection
    if ($conn->connect_error) {
        return false;
    }
    
    // Prepare and bind
    $stmt = $conn->prepare("INSERT INTO consultation_requests (name, email, company, industry, service, message, created_at) VALUES (?, ?, ?, ?, ?, ?, NOW())");
    $stmt->bind_param("ssssss", $name, $email, $company, $industry, $service, $message);
    
    // Execute
    $result = $stmt->execute();
    
    $stmt->close();
    $conn->close();
    
    return $result;
}
*/
?>