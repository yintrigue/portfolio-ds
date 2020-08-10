<?php
    session_start();
    unset($_SESSION["login"]);
    header("Location: /hellobabyclara/index.html"); die();
?>