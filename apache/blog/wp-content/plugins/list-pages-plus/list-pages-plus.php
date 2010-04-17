<?php
/*
Plugin Name: List Pages Plus
Plugin URI: http://skullbit.com/wordpress-plugin/list-pages-plus/
Description: Alter the output of the wp_list_pages() function with ease
Author: devbits
Version: 1.5
*/

load_plugin_textdomain( 'lpplus', '/wp-content/plugins/list-pages-plus' );
if( !class_exists( 'ListPagesPlus' ) ):
	class ListPagesPlus {
		function ListPagesPlus(){
			add_filter( 'wp_list_pages', array($this, 'ApplyEnhancements') );
			add_action( 'admin_menu', array($this, 'AddPanel') );
			if( $_POST['action'] == 'lpplus_update' )
				add_action( 'init', array($this,'SaveSettings') );
		}
		
		function AddPanel(){
			add_pages_page( __('List Pages Plus', 'lpplus'), __('List Pages Plus', 'lpplus'), 7, 'list-pages-plus', array($this, 'Panel'));
		}
		
		function SaveSettings(){
			check_admin_referer('lpplus-update-options');
			$update = get_option( 'list_pages_plus' );
			$update['sort_column'] = $_POST['sort_column'];
			$update['sort_order'] = $_POST['sort_order'];
			$update['excinc'] = $_POST['excinc'];
			$update['exclude'] = $_POST['exclude'];
			$update['depth'] = $_POST['depth'];
			if( !isset($_POST['null_parent']) ) $_POST['null_parent'] = 0;
			$update['null_parent'] = $_POST['null_parent'];
			if( !isset($_POST['null_subparent']) ) $_POST['null_subparent'] = 0;
			$update['null_subparent'] = $_POST['null_subparent'];
			$update["class"] = $_POST['class'];
			$update["aclass"] = $_POST['aclass'];
			$update["title_li"] = $_POST['title_li'];
			$update["pre"] = $_POST['pre'];
			$update["post"] = $_POST['post'];
			$update["subclass"] = $_POST['subclass'];
			$update["subaclass"] = $_POST['subaclass'];
			$update["subtitle"] = $_POST['subtitle'];
			$update["subpre"] = $_POST['subpre'];
			$update["subpost"] = $_POST['subpost'];
			update_option( 'list_pages_plus', $update );
			$_POST['notice'] = __('Settings Saved', 'lpplus');
		}
		
		function Panel(){
			$enhanced = get_option('list_pages_plus');
			$sort_column = $enhanced['sort_column'];
			$sort_order = $enhanced['sort_order'];
			$excinc = $enhanced['excinc'];
			$exclude = $enhanced['exclude'];
			$depth = $enhanced['depth'];
			$null_parent = $enhanced['null_parent'];
			$null_subparent = $enhanced['null_subparent'];
			$title_li = $enhanced['title_li'];
			$ac = $enhanced['class'];
			$aac = $enhanced['aclass'];
			$at = $enhanced['title'];
			$pre = $enhanced['pre'];
			$post = $enhanced['post'];
			$sac = $enhanced['subclass'];
			$saac = $enhanced['subaclass'];
			$sat = $enhanced['subtitle'];
			$spre = $enhanced['subpre'];
			$spost = $enhanced['subpost'];
			if( $_POST['notice'] )
				echo '<div id="message" class="updated fade"><p><strong>' . $_POST['notice'] . '.</strong></p></div>';
			?>
            <div class="wrap">
            	<h2><?php _e('List Pages Plus', 'lpplus');?></h2>
                <p><?php _e('Enhance your Page List menu by making additions to the default classes, title, and tags surrounding the Page Title for both Parent and Child pages.', 'lpplus');?></p>
             <form method="post" action=""> 
             <?php if( function_exists( 'wp_nonce_field' )) wp_nonce_field( 'lpplus-update-options'); ?>
             	<p><code>&lt;li class="&hellip;<input type="text" name="class" value="<?php echo $ac;?>" style="width:50px;font-size:0.8em;" />">&lt;a class="<input type="text" name="aclass" value="<?php echo $aac;?>" style="width:50px;font-size:0.8em;" />" href="&hellip;" title="<?php _e('Page Title', 'lpplus');?><input type="text" name="title" value="<?php echo $at;?>" style="width:50px;font-size:0.8em;" />"><input type="text" name="pre" value="<?php echo $pre;?>" style="width:50px;font-size:0.8em;" /><?php _e('Parent Page Title', 'lpplus');?><input type="text" name="post" value="<?php echo $post;?>" style="width:50px;font-size:0.8em;" />&lt;/a>&lt;/li></code></p>
                <p><code>&lt;li class="&hellip;<input type="text" name="subclass" value="<?php echo $sac;?>" style="width:50px;font-size:0.8em;" />">&lt;a class="<input type="text" name="subaclass" value="<?php echo $saac;?>" style="width:50px;font-size:0.8em;" />" href="&hellip;" title="<?php _e('Page Title', 'lpplus');?><input type="text" name="subtitle" value="<?php echo $sat;?>" style="width:50px;font-size:0.8em;" />"><input type="text" name="subpre" value="<?php echo $spre;?>" style="width:50px;font-size:0.8em;" /><?php _e('Child Page Title', 'lpplus');?><input type="text" name="subpost" value="<?php echo $spost;?>" style="width:50px;font-size:0.8em;" />&lt;/a>&lt;/li></code></p>
                <h3><?php _e('Override Arguments', 'lpplus');?></h3>
                <p><?php _e('You can replace your <code>wp_list_pages();</code> function with <code>wp_list_pages_plus();</code> and set the default arguments here.  You can also override these arguments using the same inline arguments as', 'lpplus');?> <a href="http://codex.wordpress.org/Template_Tags/wp_list_pages">wp_list_pages()</a> <?php _e('in your template files', 'lpplus');?>.
                <table class="form-table"> 
                	
                    <tr> 
                		<th scope="row"><label for="title_li"><?php _e('Title', 'lpplus');?></label></th> 
                		<td><input type="text" name="title_li" id="title_li" value="<?php echo $title_li;?>" /></td> 
                	</tr> 
                    <tr> 
                		<th scope="row"><label for="sort_column"><?php _e('Sort Column', 'lpplus');?></label></th> 
                		<td><?php $this->SelectList( array('post_title', 'menu_order', 'post_date', 'post_modified', 'ID', 'post_author', 'post_name'), 'sort_column', $sort_column);?></td> 
                	</tr> 
                    <tr> 
                		<th scope="row"><label for="sort_order"><?php _e('Sort Order', 'lpplus');?></label></th> 
                		<td><?php $this->SelectList( array('asc', 'desc'), 'sort_order', $sort_order);?></td> 
                	</tr> 
                    <tr> 
                		<th scope="row"><label for="exclude"><select name="excinc"><option value="exclude" <?php if($excinc == 'exclude') echo 'selected="selected"';?>><?php _e('Exclude', 'lpplus');?></option><option value="include" <?php if($excinc == 'include') echo 'selected="selected"';?>><?php _e('Include', 'lpplus');?></option></select></label></th> 
                		<td><?php $this->SelectPage( 'exclude', $exclude);?><br /><small><?php _e('Exclude will hide selected pages from your menu.  Include will only show selected pages on your menu','lpplus');?></small></td> 
                	</tr> 
                   
                    <tr> 
                		<th scope="row"><label for="depth"><?php _e('Depth', 'lpplus');?></label></th> 
                		<td><?php $this->SelectList( array('0|Pages & sub-pages displayed in a hierarchical (indented) form', '-1|Pages & sub-pages displayed in flat (no indent) form', '1|Show only top level Pages', '2|Decend to 2nd level of Pages only', '3|Decend to 3rd level of Pages only'), 'depth', $include);?></td> 
                	</tr> 
                    <tr> 
                		<th scope="row"><label for="null_parent"><?php _e('No Parent Links', 'lpplus');?></label></th> 
                		<td><input type="checkbox" name="null_parent" id="null_parent" value="1" <?php if ($null_parent == 1) echo 'checked="checked"';?> /> <small><?php _e('If checked top-level parent pages will not have a link - pages without children will still link', 'lpplus');?></small></td> 
                	</tr>
                    <tr> 
                		<th scope="row"><label for="null_subparent"><?php _e('No Sub-Parent Links', 'lpplus');?></label></th> 
                		<td><input type="checkbox" name="null_subparent" id="null_subparent" value="1" <?php if ($null_subparent == 1) echo 'checked="checked"';?> /> <small><?php _e('If checked all levels of parent pages will not have a link - pages without children will still link', 'lpplus');?></small></td> 
                	</tr>
                 </table>
             
                
                <p class="submit"><input type="submit" value="<?php _e('Save Settings', 'lpplus');?>" /></p>
                <input name="action" value="lpplus_update" type="hidden" />
             </form> 
            </div>
            <?php
		}
		
		function SelectPage( $id, $select=false ){
			global $wpdb;
			$all = $wpdb->get_results( "SELECT ID FROM $wpdb->posts WHERE post_type='page'" );
			$total = count( $all );
			$ht = $total*18;
			$pages = $wpdb->get_results( "SELECT ID, post_title FROM $wpdb->posts WHERE post_type='page' AND post_parent = 0 ORDER BY post_parent, menu_order, post_title ASC" );
			$out = "<select name='".$id."[]' id='$id' multiple='multiple' size='8' style='height:".$ht."px;'>\n";
			if( !is_array($select) ) $select = array($select);
			foreach( $pages as $pg ):
				$out .= "\t<option value='".$pg->ID."'";
				if( in_array($pg->ID, $select) ) $out .= " selected='selected'";
				$out .= ">".$pg->post_title."</option>\n";
				$kids = $wpdb->get_results( "SELECT ID, post_title FROM $wpdb->posts WHERE post_type='page' AND post_parent = $pg->ID ORDER BY menu_order, post_title ASC" );
				if( $kids ):
				foreach( $kids as $kid ):
					$out .= "\t<option value='".$kid->ID."'";
					if( in_array($kid->ID, $select) ) $out .= " selected='selected'";
					$out .= "> - ".$kid->post_title."</option>\n";
					$subkids = $wpdb->get_results( "SELECT ID, post_title FROM $wpdb->posts WHERE post_type='page' AND post_parent = $kid->ID ORDER BY menu_order, post_title ASC" );
					if( $subkids ):
					foreach( $subkids as $sk ):
						$out .= "\t<option value='".$sk->ID."'";
						if( in_array($sk->ID, $select) ) $out .= " selected='selected'";
						$out .= "> -- ".$sk->post_title."</option>\n";
					endforeach;
					endif;
				endforeach;
				endif;
			endforeach;
			$out .= "</select>";
			echo $out;
		}
		
		function SelectList( $array, $id, $select=false ){
			$out = "<select name='$id' id='$id'>\n";
			foreach( $array as $opt ):
				$op = explode( '|', $opt);
				$opt = $op[0];
				if( $op[1] ) $nm = $op[1]; else $nm = $op[0];
				$out .= "\t<option value='$opt'";
				if( $opt == $select ) $out .= " selected='selected'";
				$out .= ">$nm</option>\n";
			endforeach;
			$out .= "</select>";
			echo $out;
		}
		
		function ApplyEnhancements($pages){
			$enhanced = get_option('list_pages_plus');
			$ac = ' '.$enhanced['class'];
			$aac = ' class="'.$enhanced['aclass'].'"';
			$at = $enhanced['title'];
			$pre = $enhanced['pre'];
			$post = $enhanced['post'];
			$sac = ' '.$enhanced['subclass'];
			$saac = ' class="'.$enhanced['subaclass'].'"';
			$sat = $enhanced['subtitle'];
			$spre = $enhanced['subpre'];
			$spost = $enhanced['subpost'];
			
			$null_parent = $enhanced['null_parent'];
			$null_subparent = $enhanced['null_subparent'];
			
			//put each li in an array
			$litem = explode('</li>', $pages);
			//echo '<pre>'; print_r($litem);echo '</pre>';
			//print_r($litem);
			
			foreach( $litem as $k=>$li ):
				//check for ul and seperate
				
				if( strpos( $li, '<ul>' ) ): //PARENT PAGE
					$lis = explode( '<ul>', $li );
					$class1 = $this->GetValue( 'class="', '"', $lis[0] );
					$href1 = $this->GetValue( 'href="', '"', $lis[0] );
					$title1 = $this->GetValue( 'title="', '"', $lis[0] );
					$text1 = $this->GetValue( $title1.'">', '</a>', $lis[0] );
					$li2 = false;
					$li3 = false;
					$li4 = false;
					if( $lis[1] ){
						$class2 = $this->GetValue( 'class="', '"', $lis[1] );
						$href2 = $this->GetValue( 'href="', '"', $lis[1] );
						$title2 = $this->GetValue( 'title="', '"', $lis[1] );
						$text2 = $this->GetValue( $title2.'">', '</a>', $lis[1] );
						if( $lis[2] && $null_subparent ){ $subnull2 =  'onclick="return false;"';}
						$li2 = "\n\t <ul> \n\t" .'<li class="'.$class2.$sac.' p2"><a href="'.$href2.$sah.'"'.$subnull2.' title="'.$title2.$sat.'">'.$spre.$text2.$spost.'</a>';
						$issub = 1;
					}
					if( $lis[2] ){
						$class3 = $this->GetValue( 'class="', '"', $lis[2] );
						$href3 = $this->GetValue( 'href="', '"', $lis[2] );
						$title3 = $this->GetValue( 'title="', '"', $lis[2] );
						$text3 = $this->GetValue( $title3.'">', '</a>', $lis[2] );
						if( $lis[3] && $null_subparent ){ $subnull3 =  'onclick="return false;"';}
						$li3 = "\n\t <ul> \n\t" .'<li class="'.$class3.$sac.' p3"><a href="'.$href3.$sah.'"'.$subnull3.' title="'.$title3.$sat.'">'.$spre.$text3.$spost.'</a>';
						$issub = 1;
					}
					if( $lis[3] ){
						$class4 = $this->GetValue( 'class="', '"', $lis[3] );
						$href4 = $this->GetValue( 'href="', '"', $lis[3] );
						$title4 = $this->GetValue( 'title="', '"', $lis[3] );
						$text4 = $this->GetValue( $title4.'">', '</a>', $lis[3] );
						$li4 = "\n\t <ul> \n\t" .'<li class="'.$class4.$sac.' p4"><a href="'.$href4.$sah.'" title="'.$title4.$sat.'">'.$spre.$text4.$spost.'</a>';
					}
					
					if( $null_parent ){ $null =  'onclick="return false;"';}
					$litem[$k] = "\n\t" . '<li class="'.$class1.$ac.' p1"><a href="'.$href1.'"'.$null.' title="'.$title1.$at.'">'.$pre.$text1.$post.'</a>'.$li2.$li3.$li4;
					
					 
				elseif( strpos( $li, '</ul>' ) ): //END OF LIST
					$issub = false;
					
				elseif( strpos( $li, 'li') ): //CHILD PAGE
					$class = $this->GetValue( 'class="', '"', $li );
					$href = $this->GetValue( 'href="', '"', $li );
					$title = $this->GetValue( 'title="', '"', $li );
					$text = $this->GetValue( $title.'">', '</a>', $li );

					//NEED MORE LEVELS!
					
					if( $issub ):		
						$litem[$k] = "\n\t" . '<li class="'.$class.$sac.' sub"><a '.$saac.' href="'.$href.'" title="'.$title.$sat.'">'.$spre.$text.$spost.'</a>'.$end;
					else:
						$litem[$k] = "\n\t" . '<li class="'.$class.$ac.' other"><a '.$aac.' href="'.$href.'" title="'.$title.$at.'">'.$pre.$text.$post.'</a>';	
					endif;
										
				endif;
				
			endforeach;
			
			$pages = implode('</li>', $litem);
			
			return $pages;
		}
		
		function GetValue($start, $end, $item){
			$output = explode( $start, $item );
			$output = explode( $end, $output[1]);
			$output = $output[0];
			return $output;
		}
		
	}
endif;

if( class_exists( 'ListPagesPlus' ) )
	$lpe = new ListPagesPlus();
	
function wp_list_pages_plus($args=''){
	global $lpe;
	$enhanced = get_option('list_pages_plus');
 	if( $enhanced['excinc'] == 'exclude' ) $ex = implode(',',$enhanced['exclude']); else $in = implode(',',$enhanced['exclude']);
	$defaults = array(
		'depth' => $enhanced['depth'], 
		'show_date' => '',
		'date_format' => get_option('date_format'),
		'child_of' => 0, 
		'exclude' => $ex,
		'include' => $in,
		'title_li' => $enhanced['title_li'], 
		'echo' => 1,
		'authors' => '', 
		'sort_column' => $enhanced['sort_column'], 
		'sort_order' => $enhanced['sort_order']
	);
	$r = wp_parse_args( $args, $defaults );
	extract( $r, EXTR_SKIP );
	
	if( $r['exclude'] ) 
		$exclude = '&exclude='.$r['exclude'].$hide;

	if( $r['include'] )
		$include = '&include='.$r['include'];
	
	if( $r['echo'] == 1 )
		wp_list_pages('title_li='.$r['title_li'].'&sort_column='.$r['sort_column'].'&sort_order='.$r['sort_order'].$exclude.'&include='.$r['include'].'&depth='.$r['depth'].'&echo='.$r['echo'].'&show_date='.$r['show_date'].'&date_format='.$r['date_format'].'&authors='.$r['authors'].$include);	
	else 
		return wp_list_pages('title_li='.$r['title_li'].'&sort_column='.$r['sort_column'].'&sort_order='.$r['sort_order'].$exclude.'&depth='.$r['depth'].'&echo='.$r['echo'].'&show_date='.$r['show_date'].'&date_format='.$r['date_format'].'&authors='.$r['authors'].$include);
}
?>