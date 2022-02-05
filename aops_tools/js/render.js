const AoPSUrl = 'https://artofproblemsolving.com';

// Change image source links
$('img').each(function() {
	let src = $(this).attr('src');
	if (src.startsWith('//')) {
		$(this).attr('src', `https:${src}`);
	}
	else if (src.startsWith('/')) {
		$(this).attr('src', `${AoPSUrl}${src}`);
	}
});

const cssUrl = `${AoPSUrl}/assets/dist/v2160/css/`;
const cssFiles = [
	`${cssUrl}main-head.css`,
	`${cssUrl}sharedsite.css`,
	`${AoPSUrl}/assets/pythonbook/_static/codemirrorEdited.css`,
	`${cssUrl}community_common.css`
];

// Load AoPS CSS files
cssFiles.forEach(file => $('head').append(`<link rel="stylesheet" href="${file}">`));

// From community_utils.js
const AoPS = {Community: {}};

AoPS.Community.Utils = {
	mouseOverTip: function(head) {
		const shape = head.next();
		const txt = shape.next();
		shape.toggle();
		txt.toggle();
		head.toggleClass('cmty-tip-open');
		head.addClass('first-time');
		const headTop = head.offset().top + head.height();
		shape.offset({
			top: headTop,
			left: head.offset().left + head.outerWidth() / 2 - 6,
		});
		let headLeft;
		const head_left = head.offset().left - head.parent().offset().left;
		const head_right = head.parent().outerWidth() - head_left - head.outerWidth();
		const no_fit_right = txt.outerWidth() > head.outerWidth() + 2 * head_right;
		const no_fit_left = txt.outerWidth() > head.outerWidth() + 2 * head_left;
		if (no_fit_right === no_fit_left) {
			headLeft = head.offset().left + head.outerWidth() / 2 - txt.outerWidth() / 2;
		} else if (no_fit_right) {
			headLeft = head.offset().left + head.outerWidth() + head_right - txt.outerWidth();
		} else {
			headLeft = head.offset().left - head_left;
		}
		txt.offset({top: headTop + 7.5, left: headLeft});
	},

	mouseOutTip: function(head) {
		head.next().toggle();
		head.next().next().toggle();
		head.toggleClass('cmty-tip-open');
	},

	clickHide: function(head) {
		head.next().toggle();
		head.toggleClass('cmty-hide-open');
		return false;
	}
};
