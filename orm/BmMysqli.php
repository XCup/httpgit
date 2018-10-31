<?php
/**
 * @desc mysqli类
 * @copyright Copyright 2010-2020 黑室计算机技术研究团队(www.000room.net)
 */
namespace bm;

class BmMysqli
{
    //数据
    public $data = array();
    // 数据库连接
    private $_conn = null;
    // 需要添加的字段
    private $_column = array();

    private $_signEnum = [
        'eq'   => '=',
        'neq'  => '!=', 
        'gt'   => '>', 
        'lt'   => '<', 
        'gteq' => '>=', 
        'lteq' => '<=', 
        'like' => 'LIKE', 
        'in'   => 'IN', 
        'notIn'=> 'NOT IN'
    ];

    private $_sql = [];

    /**
     * @desc 调用run
     * 
     */
    public static function run($data)
    {
        $obj = new BmMysqli();
        $obj->data = json_decode($data , true);

        switch ($obj->data['OPER']) {
            case 'SELECT':
                return $obj->select();
            case 'INSERT':
                return $obj->add();
            case 'UPDATE':
                return $obj->mod();
            case 'DELETE':
                return $obj->delete();
            case 'COUNT':
                return $obj->count();
            default:
                return null;
        }
    }

    /**
     * @desc count 数据
     * 
     */
    public function count()
    {
        // 查询字段
        $whereString = '';
        $order = [];
        $group = [];
        foreach($this->data['FILED'] as $fieldName => $info)
        {
            //where处理
            if(!empty($info['where']))
            {
                foreach($info['where'] as $sign => $where)
                {
                    $whereString .= $this->_getWhereString($fieldName, $where, $sign);
                }
            }

            //order处理
            if ($info['order']) {
                $order[] = "{$fieldName} {$info['order']}";
            }

            //group处理
            if ($info['group']) {
                $group[] = "{$fieldName}";
            }

        }

        $orderString = '';
        if (!empty($order)) {
            $orderString = ' ORDER BY ' . implode(", ", $order);
        }

        $groupString = '';
        if (!empty($group)) {
            $groupString = ' GROUP BY' . implode(", ", $group);
        }

        $table = $this->data['TABLE'];
        $sql = "SELECT count(*) as number FROM {$table} WHERE 1{$whereString}{$groupString}{$orderString}";
        $res = self::_sesql($sql);
        return $res[0]['number'];
    }

    /**
     * @desc select查询数据
     * 
     */
    public function select()
    {
        // 查询字段
        $selectFields = [];
        $whereString = '';
        $order = [];
        $group = [];
        foreach($this->data['FILED'] as $fieldName => $info)
        {
            //查询字段处理
            if ($info['selectField']) $selectFields[] = $fieldName;

            //where处理
            if(!empty($info['where']))
            {
                foreach($info['where'] as $sign => $where)
                {
                    $whereString .= $this->_getWhereString($fieldName, $where, $sign);
                }
            }

            //order处理
            if ($info['order']) {
                $order[] = "{$fieldName} {$info['order']}";
            }

            //group处理
            if ($info['group']) {
                $group[] = "{$fieldName}";
            }

        }

        $selectString = "`" . implode("`, `", $selectFields) . "`";


        $orderString = '';
        if (!empty($order)) {
            $orderString = ' ORDER BY ' . implode(", ", $order);
        }

        $groupString = '';
        if (!empty($group)) {
            $groupString = ' GROUP BY' . implode(", ", $group);
        }

        $limitString = '';
        if (!empty($this->data['LIMIT'])) {
            $limitString = ' LIMIT '.$this->data['LIMIT'];
        }

        $table = $this->data['TABLE'];
        $sql = "SELECT {$selectString} FROM {$table} WHERE 1{$whereString}{$groupString}{$orderString}{$limitString}";
        $res = self::_sesql($sql);
        return json_encode($res);
    }

    private function _getWhereString($fieldName, $arr, $sign)
    {
        $logic = $arr[1];
        $value = $arr[0];

        if ($sign == 'in' || $sign == 'notIn') {
            $value = "('" . implode("', '", $value) . "')";
        } else {
            $value = "'{$value}'";
        }

        $sign = $this->_signEnum[$sign] ?? $sign;
        return " {$logic} `{$fieldName}` {$sign} {$value}";
    }

     /**
     * @desc 添加数据
     * 
     */
    public function add()
    {
        $field = '';
        $values = '';
        $data = $this->data['FILED'];
        $into = [];

        foreach($data as $name => $object)
        {
            $value = $object['value'];
            $into[] = "{$name} = '{$value}'";
        }
        $sql = "INSERT INTO {$this->data['TABLE']} SET " . implode(", ", $into);
        $res = self::_query($sql);
        return $res;
    }

     /**
     * @desc 修改数据
     * 
     */
    public function mod()
    {
        $ret = self::testColumn();
        if ($ret != 'success') return $msg = '字段与数据库不符'; 

        $fields = '';
        $whereString = '';
        $data = $this->data['FILED'];
         // 拼接sql
        foreach ($data as $key => $value) {
            //where处理
            if(!empty($info['where']))
            {
                foreach($info['where'] as $sign => $where)
                {
                    $whereString .= $this->_getWhereString($fieldName, $where, $sign);
                }
            }
            if(empty($value['value'])) continue;
            $fields .= $key."='{$value['value']}',";
        }

        $fields = substr($fields, 0, -1);
        $sql = 'UPDATE '.$this->data['TABLE']." SET {$fields} WHERE 1".$whereString;
        $res = self::_query($sql);
        return $res;
    }

     /**
     * @desc 删除数据
     * 
     */
    public function delete()
    {
        $whereString = '';
        foreach($this->data['FILED'] as $fieldName => $info)
        {
            //where处理
            if(!empty($info['where']))
            {
                foreach($info['where'] as $sign => $where)
                {
                    $whereString .= $this->_getWhereString($fieldName, $where, $sign);
                }
            }
        }
        $sql = 'DELETE FROM '.$this->data['TABLE'].' WHERE 1'.$whereString;
        $res = self::_query($sql);
        return $res;
    }

    /**
     * @desc sqli执行(增，删，改)
     * 
     */
    private function _query($sql)
    {
        self::_conn();
        if (!mysqli_query($this->_conn, $sql)) {
            trigger_error("Error: " . $sql . "<br>" . mysqli_error($this->_conn));
        }
        self::_close();
        return 'success';
    }

    /**
     * @desc select执行sql
     * 
     */
    private function _sesql($sql)
    {
        self::_conn();
        $retval = mysqli_query($this->_conn, $sql);
        if (!$retval) {
            trigger_error("Error: " . $sql . "<br>" . mysqli_error($this->_conn));
        }
        $arr = array();
        while ($row = mysqli_fetch_array($retval,MYSQLI_ASSOC))
        {
            $arr[] = $row;
        }

        self::_close();
        return $arr;
    }

    /**
     * @desc 判断是否存在该表
     */
    private function isexist()
    {
        // return "success";
        $data  = array();
        self::_conn();
        $msg = "error";
        $result = mysqli_query($this->_conn , "SHOW TABLES");
        $key = 'Tables_in_'.$this->data['PROTOCOL']['user'];
        While($row = mysqli_fetch_assoc($result)){
          $data[] = $row[$key];
        }
        self::_close();

        if (in_array(strtolower($this->data['TABLE']), $data)){
            $msg = 'success';
        }

        return $msg;
    }

    /**
     * @desc 创建数据库表
     */
    private function _createTable()
    {

        $sql = 'CREATE TABLE '.$this->data['TABLE'].' (';
        $data = $this->data['FILED'];

        foreach ($data as $key => $value) {
            $sql .= $key.' '.$value['type'];
            // 默认值
            if (!empty($value['defValue'])) {
                $sql .= ' DEFAULT'.$value['defValue'];
            }
            // 是否主键
            if ($value['key'] == 'primaryKey') {
                $sql .= ' PRIMARY KEY';
            }
            // 是否自增
            // if ($value['auto'] == 1) {
            //     $sql .= ' AUTO_INCREMENT';
            // }
            // 有无符号
            if ($value['symbol'] === false) {
                $sql .= ' UNSIGNED';
            }
            // 注释
            $sql .= " COMMENT '{$value["desc"]}',";
        }
        $sql = substr($sql, 0, -1);
        $sql .= ')';
        // 表备注 COMMENT='表注释'

   //      $sql = "CREATE TABLE user1 (
            // id int(20) PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
            // name char(255)  COMMENT '姓名',
            // age int(20) UNSIGNED COMMENT '年龄',
            // introduction text  COMMENT '自我介绍',
            // career int(1) UNSIGNED COMMENT '0：学生，1：教师，2：员工，3：经理'
            // )";

        $res = self::_query($sql);
        return $res;

    }

    /**
     * @desc 检测数据库的栏位和对应数据是否匹配
     */
    private function testColumn()
    {    
        $msg = 'success';
        $data = $this->data['FILED'];
        $tablename = $this->data['TABLE'];

        $sql = "select column_name from information_schema.COLUMNS where table_name='{$tablename}'";

        $res = self::_sesql($sql);
        $array = array();
        foreach ($res as $k => $v) {
            $array[] = $v['column_name'];
        }

        // 判断和数据库是否匹配
        foreach ($data as $key => $value) {
            if (!in_array($key,$array)) {
                $this->_column[$key] = $value;
                $msg = 'error';
            }
        }

        return $msg;
    }

    /**
     * @desc 在已有表中加字段
     * 
     */
    private function addColumn()
    {    
        $data = $this->_column;
        $arr = array();
        foreach ($this->data['FILED'] as $key => $value) {
            if (in_array($key,$data)) {
                $arr[$key] = $value;
            }
        }

        $sql = "ALTER TABLE {$this->data['TABLE']} ADD";
        foreach ($arr as $key => $value) {
            $sql .= $key.' '.$value['type'];
            // 默认值
            if (!empty($value['defValue'])) {
                $sql .= ' DEFAULT'.$value['defValue'];
            }
            // // 是否主键
            // if ($value['key'] == 'primaryKey') {
            //     $sql .= ' PRIMARY KEY';
            // }
            // 是否自增
            // if ($value['auto'] == 1) {
            //     $sql .= ' AUTO_INCREMENT';
            // }
            // 有无符号
            if ($value['symbol'] == false) {
                $sql .= ' UNSIGNED';
            }
            // 注释
            $sql .= " COMMENT '{$value["desc"]}',";
        }
        $sql = substr($sql, 0, -1);
        print_r($sql);die;
        self::_query($sql);
        // "ALTER TABLE TABLE_USER ADD 
        // DEPARTMENT_ID INT NOT NULL,
        // COMPANY_ID INT NOT NULL,
        // TEMP_COL NVARCHAR(10)"
    }

    /**
     * @desc sqli连接
     */
    private function _conn()
    {
        $conn = mysqli_connect($this->data['PROTOCOL']['host'], $this->data['PROTOCOL']['user'], $this->data['PROTOCOL']['password']);
        if(! $conn )
        {
            die('Could not connect: ' . mysqli_error());
        }else{
            mysqli_query($conn , "set names utf8");
            mysqli_select_db($conn, $this->data['PROTOCOL']['database']);
            $this->_conn = $conn;
        }
    }

    /**
     * @desc sqli关闭
     */
    private function _close()
    {
        mysqli_close($this->_conn);
    }

    /**
     * @desc 标准输出
     * $msg 消息
     * $s_data 数据 
     */
    private function _output($msg='success',$s_data='')
    {  
        $seeSql = '';
        if (1) {
           $seeSql = $this->_sql; 
        }
        $arr = array('msg'=>$msg,'data'=>$s_data,'sql'=>$seeSql);
        return json_encode($arr);
        
    }


}

?>