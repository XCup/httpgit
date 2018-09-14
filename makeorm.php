<?php
use \entity\EntityModel;
spl_autoload_register(function($class){
    $arr = explode("\\", $class);
    while($arr) {
        $file = dirname(__FILE__) . "/" . implode("/", $arr) . ".php";
        if (file_exists($file)) break;
        array_pop($arr);
    }
    include $file;
});

$format = array(
    'name'   => '',
    'length' => '',
    'type'   => '',
    'desc'   => '',
);
if (!empty($_POST['isSubmit']))
{
    $fields = [];
    foreach($_POST as $key => $arr) {
        if ($key == 'isSubmit') continue;
        if ($key == 'table') continue;
        foreach((array)$arr as $index => $value) {
            $info = $fields[$index] ?? $format;
            $info[$key] = $value;
            $fields[$index] = $info;
        }
    }

    $data = [
        'table'  => $_POST['table'],
        'fields' => $fields
    ];
    
    $entity = new EntityModel();
    $entity->data = json_encode($data);
    $entity->id = md5(time());
    $entity->insert();
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>测试orm</title>
</head>
<style>.inputdiv{display: inline-block; margin-right: 40px;}</style>
<script type='text/javascript' src='http://s.dev.000room.com/js/jquery-2.1.1.min.js'></script>
<script type="text/javascript">
function addFieldInfo()
{
    str = '<div>' + 
    '<div class="inputdiv">字段名:<input type="text" name="name[]"></div>' +
    '<div class="inputdiv">长度:<input type="text" name="length[]"></div>'+
    '<div class="inputdiv">类型:<input type="text" name="type[]"></div>' +
    '<div class="inputdiv">注释<input type="text" name="desc[]"></div>' +
    '<br /><br />';

    $("p").append(str);
}

function submitForm()
{
    $("#ormForm").submit();
}
</script>
<body>
    <center>
        <form action="" method="post" id="ormForm">
            <input type="hidden" name="isSubmit" value="1" />
            请输入表名<input type="text" name="table">
            <a href="javascript:submitForm();">提交</a><br /><br />
            <p></p>
            <a href="javascript:addFieldInfo();">添加字段</a>
        </form>
    </center>
</body>
</html>