<form id="searchform" method="get" action="<?php echo home_url(); ?>/">
<input type="text" value="<?php _e('Buscar', 'zbench'); ?>" onfocus="if (this.value == '<?php _e('Buscar', 'zbench'); ?>') {this.value = '';}" onblur="if (this.value == '') {this.value = '<?php _e('Buscar', 'zbench'); ?>';}" size="35" maxlength="50" name="s" id="s" />
<input type="submit" id="searchsubmit" value="<?php _e('Buscar','zbench'); ?>" />
</form>
