<?php
// Enable error reporting for development (remove in production)
error_reporting(E_ALL);
ini_set('display_errors', 0);

// Start session for flash messages
session_start();

// Configuration
$to_email = "info@terraconsulting.co.tz"; // Your email address
$subject = "New Newsletter Subscription - Terra Consulting";
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
    $interest = isset($_POST['interest']) ? sanitize_input($_POST['interest']) : 'all';
    
    // Validate required fields
    if (empty($name)) {
        $errors[] = "Name is required";
    }
    
    if (empty($email)) {
        $errors[] = "Email is required";
    } elseif (!validate_email($email)) {
        $errors[] = "Invalid email format";
    }
    
    // Honeypot field for spam protection
    if (!empty($_POST['website'])) {
        die("Spam detected");
    }
    
    // If no errors, proceed
    if (empty($errors)) {
        
        // Prepare email content
        $email_content = "New Newsletter Subscription\n\n";
        $email_content .= "Name: " . $name . "\n";
        $email_content .= "Email: " . $email . "\n";
        $email_content .= "Interest: " . ucfirst($interest) . "\n\n";
        $email_content .= "Subscribed on: " . date('Y-m-d H:i:s') . "\n";
        $email_content .= "IP Address: " . $_SERVER['REMOTE_ADDR'] . "\n";
        
        // Email headers
        $headers = "From: noreply@terraconsulting.co.tz\r\n";
        $headers .= "Reply-To: info@terraconsulting.co.tz\r\n";
        $headers .= "X-Mailer: PHP/" . phpversion();
        
        // Send notification email
        if (mail($to_email, $subject, $email_content, $headers)) {
            
            // Send confirmation email to subscriber
            send_confirmation_email($email, $name);
            
            // Success - redirect with success message
            $_SESSION['form_success'] = "Thank you for subscribing! You'll receive our latest ESG insights and updates.";
            
            // Optional: Save to database or mailing list service
            // save_to_mailing_list($name, $email, $interest);
            
            header("Location: " . $success_redirect . "?status=success");
            exit();
        } else {
            // Email failed
            $_SESSION['form_error'] = "Sorry, there was an error processing your subscription. Please try again.";
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

// Function to send confirmation email to subscriber
function send_confirmation_email($email, $name) {
    $subject = "Welcome to Terra Consulting Newsletter";
    
    $message = "Dear " . $name . ",\n\n";
    $message .= "Thank you for subscribing to Terra Consulting's newsletter!\n\n";
    $message .= "You'll now receive regular updates on:\n";
    $message .= "- Latest ESG trends and best practices\n";
    $message .= "- Regulatory updates and compliance news\n";
    $message .= "- Success stories and case studies\n";
    $message .= "- Expert insights and industry analysis\n\n";
    $message .= "We're committed to helping you stay informed about sustainability and ESG excellence.\n\n";
    $message .= "If you have any questions, feel free to reach out to us at info@terraconsulting.co.tz\n\n";
    $message .= "Best regards,\n";
    $message .= "Terra Consulting Team\n";
    $message .= "Kibo Complex Tegeta, Floor 1, Near TRA\n";
    $message .= "Dar es Salaam, Tanzania\n";
    $message .= "+255 762 395 632\n";
    $message .= "www.terraconsulting.co.tz\n";
    
    $headers = "From: info@terraconsulting.co.tz\r\n";
    $headers .= "Reply-To: info@terraconsulting.co.tz\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();
    
    return mail($email, $subject, $message, $headers);
}

// Optional: Function to save to database or integrate with mailing list service
/*
function save_to_mailing_list($name, $email, $interest) {
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
    $stmt = $conn->prepare("INSERT INTO newsletter_subscribers (name, email, interest, subscribed_at) VALUES (?, ?, ?, NOW())");
    $stmt->bind_param("sss", $name, $email, $interest);
    
    // Execute
    $result = $stmt->execute();
    
    $stmt->close();
    $conn->close();
    
    return $result;
}
*/

// Optional: Integrate with Mailchimp, SendGrid, or other email service
/*
function add_to_mailchimp($email, $name) {
    $api_key = 'your_mailchimp_api_key';
    $list_id = 'your_list_id';
    
    $data = array(
        'email_address' => $email,
        'status' => 'subscribed',
        'merge_fields' => array(
            'FNAME' => $name
        )
    );
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "https://us1.api.mailchimp.com/3.0/lists/" . $list_id . "/members/");
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json', 'Authorization: Basic ' . base64_encode('user:' . $api_key)));
    curl_setopt($ch, CURLOPT_USERAGENT, 'PHP-MCAPI/2.0');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    
    $result = curl_exec($ch);
    curl_close($ch);
    
    return $result;
}
*/
?>