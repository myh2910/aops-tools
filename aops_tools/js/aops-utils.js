const AoPS = {Community: {}};

// From community_utils.js
AoPS.Community.Utils = {
	mouseOverTip: function(head) {
		var shape = head.next();
		var txt = shape.next();
		shape.toggle();
		txt.toggle();
		head.toggleClass('cmty-tip-open');
		head.addClass('first-time');
		var top = head.offset().top + head.height();
		shape.offset({
			top: top,
			left: head.offset().left + head.outerWidth() / 2 - 6,
		});
		var left;
		var head_left = head.offset().left - head.parent().offset().left;
		var head_right = head.parent().outerWidth() - head_left - head.outerWidth();
		var no_fit_right = txt.outerWidth() > head.outerWidth() + 2 * head_right;
		var no_fit_left = txt.outerWidth() > head.outerWidth() + 2 * head_left;
		if (no_fit_right === no_fit_left) {
			left = head.offset().left + head.outerWidth() / 2 - txt.outerWidth() / 2;
		} else if (no_fit_right) {
			left =
				head.offset().left + head.outerWidth() + head_right - txt.outerWidth();
		} else {
			left = head.offset().left - head_left;
		}
		txt.offset({top: top + 7.5, left: left});
	},

	mouseOutTip: function(head) {
		head.next().toggle();
		head.next().next().toggle();
		head.toggleClass('cmty-tip-open');
	},

	clickMidlineHide: function(head) {
		head.next().next().toggle();
		head.toggleClass('cmty-hide-open');
		return false;
	},

	clickHide: function(head) {
		head.next().toggle();
		head.toggleClass('cmty-hide-open');
		return false;
	}
};

// From community_views.js
AoPS.Community.Views = {
	onClickHiddenBar: function() {
		$(this).parent().toggleClass('cmty-view-posts-item-reveal');
		return false;
	}
};

// Change image source links
$('img').each(function() {
	let src = $(this).attr('src');
	if (src.startsWith('//')) {
		$(this).attr('src', `https:${src}`);
	} else if (src.startsWith('/')) {
		$(this).attr('src', `https://artofproblemsolving.com${src}`);
	}
});

// Change document width properties
$('.cmty-tip-header').each(function() {
	AoPS.Community.Utils.mouseOverTip($(this));
});
let maxHeight = $(document).height();

$('.cmty-tip-header').each(function() {
	AoPS.Community.Utils.mouseOutTip($(this));
});
$('.cmty-post-wrapper').css('marginBottom', maxHeight - $(document).height());

// Toggle hidden content on click
$('.cmty-post-item-hidden-bar').click(AoPS.Community.Views.onClickHiddenBar);
