<?php
function my_wp_link_page( $i ) {
	global $post, $wp_rewrite;

	if ( 1 == $i ) {
		$url = get_permalink();
	} else {
		if ( '' == get_option('permalink_structure') || in_array($post->post_status, array('draft', 'pending')) )
			$url = add_query_arg( 'page', $i, get_permalink() );
		elseif ( 'page' == get_option('show_on_front') && get_option('page_on_front') == $post->ID )
			$url = trailingslashit(get_permalink()) . user_trailingslashit("$wp_rewrite->pagination_base/" . $i, 'single_paged');
		else
			$url = trailingslashit(get_permalink()) . user_trailingslashit($i, 'single_paged');
	}

	return esc_url( $url );
}
?>

<?php get_header(); ?>
<div id="content">
	<?php the_post(); ?>
	<div <?php post_class('post-single'); ?> id="post-<?php the_ID(); ?>"><!-- post div -->
		<h2 class="title"><?php the_title(); ?></h2>
		<div class="post-info-top">
			<span class="post-info-date">
				<?php _e('Posted by', 'zbench'); ?> <a href="<?php echo get_author_posts_url( get_the_author_meta( 'ID' ) ); ?>" title="<?php printf( __( 'View all posts by %s', 'zbench' ), get_the_author() ) ?>" rel="author"><?php the_author(); ?></a>
				<?php _e('on', 'zbench'); ?>
				<?php the_time(get_option( 'date_format' )); ?>
				<?php edit_post_link(__('Edit','zbench'), '[', ']'); ?>
			</span>
			<?php if (comments_open()) : ?>
			<span class="addcomment"><a href="#respond"  rel="nofollow" title="<?php _e('Leave a comment ?', 'zbench'); ?>"><?php _e('Leave a comment', 'zbench'); ?></a><?php comments_number(' (0)', ' (1)', ' (%)'); ?></span>
			<span class="gotocomments"><a href="#comments"  rel="nofollow" title="<?php _e('Go to comments ?', 'zbench'); ?>"><?php _e('Go to comments', 'zbench'); ?></a></span>
			<?php endif; ?>
		</div>
		<div class="clear"></div>
		<div class="entry">
			<?php the_content(); ?>
			
			<?php
    			$subject = $post->post_content;
                $pattern = '/<h1>(?P<name>.*)<\/h1>/';
                $num_matches = preg_match_all($pattern, $subject, $matches, PREG_OFFSET_CAPTURE, 3);
                $matches = $matches['name'];
            ?>
			
			<br />
			<div style="font-size: 18px;">
			<?php
			    if ($page > 1) {
			        echo '<a style="width: 290px; float:left;" href="' . my_wp_link_page($page - 1) .'">« ' . $matches[$page - 2][0] . '</a>';
			    }
			    
			    if ($page < $numpages && $numpages > 1) {
			        echo '<a style="width: 290px; float:right; text-align: right;" href="' . my_wp_link_page($page + 1) . '">' . $matches[$page][0] . ' »</a>';
			    }
			    
			?>
			</div>

            <?php            
                if ($num_matches > 1) {
                    echo '<select class="custom_paginator" style="width: 400px; margin-top: 30px; margin-bottom: 30px;">';
                    foreach ($matches as $i => $value) {
                        echo '<option value="' . my_wp_link_page($i + 1) . '"';
                        if ($i == $page - 1) {
                            echo ' selected="selected"';
                        }
                        echo '>' . ($i + 1) . ' - ' . $value[0] . '</option>';
                    }
                    echo '</select>';
                }
            ?>
            
			
		</div><!-- END entry -->
		<div class="add-info">
			<?php if(function_exists('st_related_posts')) { st_related_posts('title=<h3>'._e('Related Posts','zbench').'</h3>'); } ?>
		</div>
		<div class="post-info-bottom">
			<span class="post-info-category"><?php the_category(', '); ?></span><span class="post-info-tags"><?php the_tags('', ', ', ''); ?></span>
		</div>
		<div id="nav-below">
			<div class="nav-previous"><?php previous_post_link( '%link', '<span class="meta-nav">&larr;</span> %title' ); ?></div>
			<div class="nav-next"><?php next_post_link( '%link', '%title <span class="meta-nav">&rarr;</span>' ); ?></div>
		</div><!-- #nav-below -->					
	</div><!-- END post -->
	<?php comments_template( '', true ); ?>
</div><!--content-->
<?php get_sidebar(); ?>
<?php get_footer(); ?>
