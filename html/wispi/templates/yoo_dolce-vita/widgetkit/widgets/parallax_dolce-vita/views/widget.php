<?php
/**
* @package   yoo_dolce-vita
* @author    YOOtheme http://www.yootheme.com
* @copyright Copyright (C) YOOtheme GmbH
* @license   http://www.gnu.org/licenses/gpl.html GNU/GPL
*/

// JS Options
$options = array();
$options[] = ($settings['viewport'] !== '') ? 'viewport: ' . $settings['viewport'] : '';
$options[] = ($settings['velocity'] !== '') ? 'velocity: ' . $settings['velocity'] : '';

$options_bg = array();
$options_bg[] = ($settings['background_translatey'] !== '') ? 'bg: ' . $settings['background_translatey'] : '';
$options_bg[] = ($settings['background_color_start'] && $settings['background_color_end']) ? '\'background-color\': \'' . $settings['background_color_start'] . ',' . $settings['background_color_end'] . '\'' : '';

$options_title = array();
$options_title[] = ($settings['title_opacity_start'] !== '' && $settings['title_opacity_end'] !== '') ? 'opacity: \'' . $settings['title_opacity_start'] . ',' . $settings['title_opacity_end'] . '\'' : '';
$options_title[] = ($settings['title_translatex_start'] !== '' && $settings['title_translatex_end'] !== '') ? 'x: \'' . $settings['title_translatex_start'] . ',' . $settings['title_translatex_end'] . '\'' : '';
$options_title[] = ($settings['title_translatey_start'] !== '' && $settings['title_translatey_end'] !== '') ? 'y: \'' . $settings['title_translatey_start'] . ',' . $settings['title_translatey_end'] . '\'' : '';
$options_title[] = ($settings['title_scale_start'] !== '' && $settings['title_scale_end'] !== '') ? 'scale: \'' . $settings['title_scale_start'] . ',' . $settings['title_scale_end'] . '\'' : '';
$options_title[] = ($settings['title_blur_start'] !== '' && $settings['title_blur_end'] !== '') ? 'blur: \'' . $settings['title_blur_start'] . ',' . $settings['title_blur_end'] . '\'' : '';

$options_content = array();
$options_content[] = ($settings['content_opacity_start'] !== '' && $settings['content_opacity_end'] !== '') ? 'opacity: \'' . $settings['content_opacity_start'] . ',' . $settings['content_opacity_end'] . '\'' : '';
$options_content[] = ($settings['content_translatex_start'] !== '' && $settings['content_translatex_end'] !== '') ? 'x: \'' . $settings['content_translatex_start'] . ',' . $settings['content_translatex_end'] . '\'' : '';
$options_content[] = ($settings['content_translatey_start'] !== '' && $settings['content_translatey_end'] !== '') ? 'y: \'' . $settings['content_translatey_start'] . ',' . $settings['content_translatey_end'] . '\'' : '';
$options_content[] = ($settings['content_scale_start'] !== '' && $settings['content_scale_end'] !== '') ? 'scale: \'' . $settings['content_scale_start'] . ',' . $settings['content_scale_end'] . '\'' : '';
$options_content[] = ($settings['content_blur_start'] !== '' && $settings['content_blur_end'] !== '') ? 'blur: \'' . $settings['content_blur_start'] . ',' . $settings['content_blur_end'] . '\'' : '';

// Container
$container  = 'uk-flex uk-flex-center uk-flex-middle uk-overflow-hidden uk-position-relative';
$container .= ' uk-text-'.$settings['text_align'];
$container .= $settings['fullscreen'] ? ' uk-height-viewport' : '';

// Contrast
switch ($settings['contrast']) {
    case 'secondary':
        $container .= ' uk-contrast';
        break;
    case 'primary':
        $container .= ' uk-contrast-primary';
        break;
    default:
        break;
}

// Width
$width = 'uk-width-'.$settings['width'];
$width .= $settings['width_small'] ? ' uk-width-small-'.$settings['width_small'] : '';
$width .= $settings['width_medium'] ? ' uk-width-medium-'.$settings['width_medium'] : '';
$width .= $settings['width_large'] ? ' uk-width-large-'.$settings['width_large'] : '';

// Title Size
switch ($settings['title_size']) {
    case 'large':
        $title_size = 'uk-heading-large uk-margin-top-remove';
        break;
    default:
        $title_size = 'uk-' . $settings['title_size'] . ' uk-margin-top-remove';
}

// Content Size
switch ($settings['content_size']) {
    case 'large':
        $content_size = 'uk-text-large';
        break;
    case 'h2':
    case 'h3':
    case 'h4':
        $content_size = 'uk-' . $settings['content_size'];
        break;
    default:
        $content_size = '';
}

// Link Style
switch ($settings['link_style']) {
    case 'button':
        $link_style = 'uk-button';
        break;
    case 'primary':
        $link_style = 'uk-button uk-button-primary';
        break;
    case 'button-large':
        $link_style = 'uk-button uk-button-large';
        break;
    case 'primary-large':
        $link_style = 'uk-button uk-button-large uk-button-primary';
        break;
    case 'button-link':
        $link_style = 'uk-button uk-button-link';
        break;
    default:
        $link_style = '';
}

// Link Target
$link_target = ($settings['link_target']) ? ' target="_blank"' : '';

// Image Options
$image_blend_mode = ($settings['image_blend_mode']) ? 'background-blend-mode:' . $settings['image_blend_mode'] :  '' . ';';
$image_opacity = ($settings['image_opacity']) ? 'opacity:' . $settings['image_opacity'] . ';' :  'display: none;';

foreach ($items as $i => $item) :

    // Media Type
    if ($item->type('media') == 'image' && $settings['media']) {
        if ($settings['image_width'] != 'auto' || $settings['image_height'] != 'auto') {

            $width  = ($settings['image_width'] != 'auto') ? $settings['image_width'] : '';
            $height = ($settings['image_height'] != 'auto') ? $settings['image_height'] : '';

            $media = 'background-image: url(' . $item->thumbnail('media', $width, $height, array(), true) . ');' . $image_blend_mode;

        } else {
            $media = 'background-image: url(' . $item['media'] . ');' . $image_blend_mode;
        }
    } else {
        $media = '';
    }

    // `min-height` doesn't work in IE11 and IE10 if flex items are centered vertically
    $media = 'style="height: ' . $settings['min_height'] . 'px; ' . $media . '"';

    // Id
    $id = substr(uniqid(), -3);
    $target = ($settings['target']) ? 'target: \'#wk-' . $id . '\', ': '';

    $parallax_bg      = '{' . implode(',', $options_bg) . '}';
    $parallax_title   = '{' . $target . implode(',', array_filter(array_merge($options, $options_title))) . '}';
    $parallax_content = '{' . $target . implode(',', array_filter(array_merge($options, $options_content))) . '}';

?>

    <div id="wk-<?php echo $id; ?>" class="tm-parallax-dolce-vita <?php echo $container; ?> <?php echo $settings['class']; ?>" <?php echo $media; ?> data-uk-parallax="<?php echo $parallax_bg; ?>">
        <div class="uk-position-cover uk-position-z-index" style="<?php echo $image_opacity; ?>" data-uk-parallax="<?php echo $parallax_bg; ?>"></div>

        <?php if ($item['badge']) : ?>
        <div class="tm-badge-vertical uk-hidden-small">
            <div class="uk-flex uk-flex-middle uk-flex-center uk-height-1-1">
                <div class="tm-text-vertical tm-font-alt-2"><div><?php echo $item['badge']; ?></div></div>
            </div>
        </div>
        <?php endif; ?>

        <div class="<?php echo $width; ?> uk-panel" style="z-index: 2;">

            <?php if ($item['title'] && $settings['title']) : ?>
            <h3 class="<?php echo $title_size; ?>" data-uk-parallax="<?php echo $parallax_title; ?>">

                <?php if ($item['link']) : ?>
                    <a class="uk-link-reset" href="<?php echo $item->escape('link') ?>"<?php echo $link_target; ?>><?php echo $item['title']; ?></a>
                <?php else : ?>
                    <?php echo $item['title']; ?>
                <?php endif; ?>

            </h3>
            <?php endif; ?>

            <?php if (($item['content'] && $settings['content']) || ($item['link'] && $settings['link'])) : ?>
            <div data-uk-parallax="<?php echo $parallax_content; ?>">

                <?php if ($item['content'] && $settings['content']) : ?>
                <div class="<?php echo $content_size; ?>"><?php echo $item['content']; ?></div>
                <?php endif; ?>

                <?php if ($item['link'] && $settings['link']) : ?>
                <p class="uk-margin-bottom-remove"><a<?php if($link_style) echo ' class="' . $link_style . '"'; ?> href="<?php echo $item->escape('link'); ?>"<?php echo $link_target; ?>><?php echo $app['translator']->trans($settings['link_text']); ?></a></p>
                <?php endif; ?>

            </div>
            <?php endif; ?>

        </div>
    </div>

<?php endforeach; ?>
