<?php get_header(); ?>
<!-- start content items -->
<div class="CON">

<!-- start center -->
<div class="SC">
<?php if ( function_exists('yoast_breadcrumb') ) {
	yoast_breadcrumb('<p id="breadcrumbs">','</p>');
} ?>
<?php if (have_posts()) : ?>
<?php while (have_posts()) : the_post(); ?>

<div class="Post" id="post-<?php the_ID(); ?>">
<div class="PostHead">
<h1><?php the_title(); ?></h1>
<small class="PostAuthor">Autor: <?php the_author() ?> <?php edit_post_link('Edit'); ?></small>
<p class="PostDate">
<small class="day"><?php the_time('j') ?></small>
<small class="month"><?php the_time('M') ?></small>
<small class="year"><? // php the_time('Y') ?></small>
</p>
</div>

<div class="PostContent">
 <?php the_content("<p>Leer el resto de la nota &raquo;</p>"); ?>
</div>
<div class="PostDet">
 <li class="PostCateg">Guardado en: <?php the_category(', ') ?></li>
</div>
</div>
<br clear="all" />


<?php comments_template(); ?>
<?php endwhile; else : ?>

<h2><?php _e('Not Found'); ?></h2>
<p><?php _e('Sorry, but the page you requested cannot be found.'); ?></p>
<?php endif; ?>
</div> 
<!-- end center -->
<!-- start content left -->
<div class="SR">
<?php get_sidebar(); ?>
</div> 
<!-- end content left -->
</div> 
<?php get_footer(); ?>
