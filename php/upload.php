<?php
    error_reporting(0);
    //$dir=md5("icq" . $_SERVER['REMOTE_ADDR']);
    //$dir=md5("icq");
    //$sandbox = '/sandbox/' . $dir;
    //@mkdir($sandbox);
    //@chdir($sandbox);

    if($_FILES['file']['name']){
        $filename = !empty($_POST['file']) ? $_POST['file'] : $_FILES['file']['name'];
        if (!is_array($filename)) {
            $filename = explode('.', $filename);
        }
        $ext = end($filename);
        var_dump($ext);
        if($ext==$filename[count($filename) - 1]){
            die("emmmm...");
        }
        var_dump($filename);
        $new_name = (string)rand(100,999).".".$ext;
        move_uploaded_file($_FILES['file']['tmp_name'],$new_name);
        $_ = $_POST['hehe'];
        if(@substr(file($_)[0],0,6)==='@<?php' && strpos($_,$new_name)===false){
            include($_);
        }
        unlink($new_name);
    }
    else{
        highlight_file(__FILE__);
    }
?>

<form action="" method="post" enctype="multipart/form-data">
    <input type="file" name="file" id="file" />
    <input type="submit" name="submit" value="Submit" />
</form>