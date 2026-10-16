<?php
/**
 * Simple Admin Page to View Form Submissions
 * Password protect this file!
 */

// Simple password protection
session_start();

if (!isset($_SESSION['admin_logged_in'])) {
    if (isset($_POST['password'])) {
            $_SESSION['admin_logged_in'] = true;
        } else {
            $error = "Wrong password!";
        }
    }

    if (!isset($_SESSION['admin_logged_in'])) {
        ?>
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Login - Terra Consult</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .login-box {
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                    text-align: center;
                }
                h2 { color: #2D5A27; }
                input[type="password"] {
                    padding: 10px;
                    width: 250px;
                    border: 2px solid #ddd;
                    border-radius: 5px;
                    font-size: 16px;
                }
                button {
                    padding: 10px 30px;
                    background: #2D5A27;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    margin-top: 10px;
                }
                button:hover { background: #1f3d1a; }
                .error { color: red; margin-top: 10px; }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h2>🔐 Admin Login</h2>
                <form method="POST">
                    <input type="password" name="password" placeholder="Enter password" required>
                    <br>
                    <button type="submit">Login</button>
                </form>
                <?php if (isset($error)) echo "<p class='error'>$error</p>"; ?>
            </div>
        </body>
        </html>
        <?php
        exit();
    }
}

// Logout functionality
if (isset($_GET['logout'])) {
    session_destroy();
    header("Location: admin-view.php");
    exit();
}

// Database connection

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get data
$consultations = $conn->query("SELECT * FROM consultation_requests ORDER BY created_at DESC");
$newsletters = $conn->query("SELECT * FROM newsletter_subscribers ORDER BY subscribed_at DESC");
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - Terra Consult</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }

        .header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .header h1 {
            color: #2D5A27;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logout-btn {
            padding: 10px 20px;
            background: #dc3545;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 500;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .stat-card h3 {
            color: #666;
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 10px;
        }

        .stat-card .number {
            font-size: 36px;
            font-weight: bold;
            color: #2D5A27;
        }

        .section {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .section h2 {
            color: #2D5A27;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #2D5A27;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }

        .badge-primary {
            background: #e7f3ff;
            color: #0066cc;
        }

        .no-data {
            text-align: center;
            padding: 40px;
            color: #999;
        }

        .export-btn {
            padding: 8px 16px;
            background: #2D5A27;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 14px;
            display: inline-block;
            margin-bottom: 15px;
        }

        @media (max-width: 768px) {
            table {
                font-size: 14px;
            }

            th, td {
                padding: 8px;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>
            <span>🍃</span>
            Terra Consult - Admin Dashboard
        </h1>
        <a href="?logout=1" class="logout-btn">Logout</a>
    </div>

    <div class="stats">
        <div class="stat-card">
            <h3>Total Consultations</h3>
            <div class="number"><?= $consultations->num_rows ?></div>
        </div>
        <div class="stat-card">
            <h3>Newsletter Subscribers</h3>
            <div class="number"><?= $newsletters->num_rows ?></div>
        </div>
        <div class="stat-card">
            <h3>Total Submissions</h3>
            <div class="number"><?= $consultations->num_rows + $newsletters->num_rows ?></div>
        </div>
    </div>

    <!-- Consultation Requests -->
    <div class="section">
        <h2>📋 Consultation Requests</h2>

        <?php if ($consultations->num_rows > 0): ?>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Date</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Company</th>
                        <th>Industry</th>
                        <th>Service</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
                    <?php while ($row = $consultations->fetch_assoc()): ?>
                    <tr>
                        <td><?= $row['id'] ?></td>
                        <td><?= date('M d, Y', strtotime($row['created_at'])) ?></td>
                        <td><?= htmlspecialchars($row['name']) ?></td>
                        <td><a href="mailto:<?= $row['email'] ?>"><?= htmlspecialchars($row['email']) ?></a></td>
                        <td><?= htmlspecialchars($row['company']) ?></td>
                        <td><span class="badge badge-primary"><?= ucfirst($row['industry']) ?></span></td>
                        <td><?= ucfirst($row['service']) ?></td>
                        <td><?= htmlspecialchars(substr($row['message'], 0, 50)) ?>...</td>
                    </tr>
                    <?php endwhile; ?>
                </tbody>
            </table>
        <?php else: ?>
            <div class="no-data">No consultation requests yet.</div>
        <?php endif; ?>
    </div>

    <!-- Newsletter Subscribers -->
    <div class="section">
        <h2>📧 Newsletter Subscribers</h2>

        <?php if ($newsletters->num_rows > 0): ?>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Date</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Interest</th>
                    </tr>
                </thead>
                <tbody>
                    <?php while ($row = $newsletters->fetch_assoc()): ?>
                    <tr>
                        <td><?= $row['id'] ?></td>
                        <td><?= date('M d, Y', strtotime($row['subscribed_at'])) ?></td>
                        <td><?= htmlspecialchars($row['name']) ?></td>
                        <td><a href="mailto:<?= $row['email'] ?>"><?= htmlspecialchars($row['email']) ?></a></td>
                        <td><span class="badge badge-primary"><?= ucfirst($row['interest']) ?></span></td>
                    </tr>
                    <?php endwhile; ?>
                </tbody>
            </table>
        <?php else: ?>
            <div class="no-data">No newsletter subscribers yet.</div>
        <?php endif; ?>
    </div>

    <p style="text-align: center; color: #999; margin-top: 30px;">
        Terra Consulting © 2025 | Admin Dashboard
    </p>
</body>
</html>
<?php $conn->close(); ?>
