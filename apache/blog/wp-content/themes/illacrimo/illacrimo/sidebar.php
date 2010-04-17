<div class="SR"><div class="SRL">

<div class="Search">
<form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">
<input type="text" name="s" class="keyword" />
<div id="buttonsearch"><input name="submit" type="image" class="search" title="Search" src="<?php bloginfo('template_url'); ?>/images/ButtonTransparent.png" alt="Search" />
</div>
</form>
</div>

<div class="Syn"><div class="SynTop"></div>
 <ul>
  <li><a href="<?php bloginfo('rss2_url'); ?>">Entries</a> (RSS)</li>
  <li><a href="<?php bloginfo('comments_rss2_url'); ?>">Comments</a> (RSS)</li>
 </ul>
</div>

<!-- Start Flickr Photostream -->
<?php if (function_exists('get_flickrrss')) { ?>
<div class="Flickr">
  <h2>PhotoStream</h2>
  <ul>
   <?php get_flickrrss(); ?> 
  </ul>
</div>
<?php } ?>
<!-- End Flickr Photostream -->

<?php if ( function_exists('dynamic_sidebar') && dynamic_sidebar('Sidebar_left') ) : else : ?>

<div class="widget widget_categories">
<h2>Categories</h2>
 <ul>
  <?php wp_list_cats(); ?>
 </ul>
</div>
    
<!-- Start Recent Comments -->
<?php if (function_exists('mdv_recent_comments')) { ?>
<div class="widget widget_recent_entries">
<h2>Recent Comments</h2>
 <ul>
  <?php mdv_recent_comments('10'); ?>
 </ul>
</div>
<?php } ?>
<!-- End Recent Comments -->

<?php endif; ?>
</div>
</div>

