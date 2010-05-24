<?php get_header(); ?>
<!-- Container -->
<div class="CON">
<!-- Start SC -->
<div class="SCS">
<?php if ( function_exists('yoast_breadcrumb') ) {
	yoast_breadcrumb('<p id="breadcrumbs">','</p>');
} ?>
<?php if (have_posts()) : ?>
<?php while (have_posts()) : the_post(); ?>
<h1><?php the_title(); ?></a></h1>
<?php the_content("<p>__('Leer el resto de esta nota &raquo;')</p>"); ?>
<?php edit_post_link(__('Editar'), '<p>', '</p>'); ?>
<?php endwhile; endif; ?>
</div> 
<!-- End SC -->
<?php get_sidebar(); ?>


<!-- Container -->
</div>

<?php get_footer(); ?>