<?php
    session_start();

    $errorMsg = "";
    if(isset($_POST["sub"])) {
        $validUser = $_POST["password"] == "520Clara!";
        if(!$validUser) $errorMsg = "Nope!";
        else $_SESSION["login"] = true;
    }

    if($_SESSION["login"]) {
        header("Location: /hellobabyclara/index.html"); die();
    }

?>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Hello Baby Clara!</title>
    <link href="css/style-login.css" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
    <script type="text/javascript" src="js/plugin/jquery-3.3.1.min.js"></script>
    <script src="vendor/animsition/js/animsition.min.js"></script>
</head>
<body>
    <!--
    <form name="input" action="" method="post">
        <label for="password">Password:</label>
        <input type="password" value="" id="password" name="password" />
        <input type="submit" value="login" name="sub" />
    </form>
    -->

    <div class="container-login100">
        <form name="input" action="" method="post">
            <span class="error"><?= $errorMsg ?></span>
            <!--
            <input class="input100-user" type="text" name="username" placeholder="Username">
            -->
            <input class="input100" type="password" name="password" placeholder="Password" onfocus="this.placeholder = ''"
onblur="this.placeholder = 'Password'" />
            <div class="container-login100-form-btn">
                <button class="login100-form-btn" type="submit" name="sub" >Login</button>
            </div>
        </form>
    </div>
</body>
</html>