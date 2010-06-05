<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head profile="http://gmpg.org/xfn/11">
<?
$theTitle=wp_title(" - ", false);
if($theTitle != "") {
?>
<title><?php echo wp_title('',false); ?></title>
<?
}
else{
?>
<title><?php bloginfo('name'); ?></title>
<?
}
?>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<meta http-equiv="pragma" content="no-cache" />
<meta http-equiv="cache-control" content="no-cache" />
<link rel="stylesheet" type="text/css" href="/media/css/style.css" />
<script type="text/javascript" src="<?php bloginfo('template_url'); ?>/javascript/imghover.js"> </script>
<link rel="alternate" type="application/rss+xml" title="RSS 2.0" href="<?php bloginfo('rss2_url'); ?>" />
<link rel="alternate" type="text/xml" title="RSS .92" href="<?php bloginfo('rss_url'); ?>" />
<link rel="alternate" type="application/atom+xml" title="Atom 0.3" href="<?php bloginfo('atom_url'); ?>" />
<link rel="shortcut icon" href="/media/icons/favicon.ico" type="image/x-icon" />
<link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />
<?php wp_head(); ?>
<meta name="google-site-verification" content="_LS4YqLaSpHUPBM7dg2oRWgl0lvlF3ZZrU3UT2tA2C0" />
</head>

<body>
<div class="BGC">
<!-- start header -->


 <div class="Header"><div class="LS"></div>
  </div>
  
 <div class="Menu">
  <div class="MTL"></div><div class="MTR"></div>
   <ul>
   <li><a href="/"><span>Catálogo</span></a></li>
<?php
$pages = wp_list_pages('sort_column=menu_order&title_li=&echo=0');
$pages = preg_replace('%<a ([^>]+)>%U','<a $1><span>', $pages);
$pages = str_replace('</a>','</span></a>', $pages);
echo $pages;
?>
  </ul> 
 </div>
