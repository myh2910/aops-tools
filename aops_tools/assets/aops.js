// JavaScript from https://artofproblemsolving.com/assets/dist/v2148/
AoPS = {
	Community: {
		// community_utils.js
		Utils: {
			// 1473-1477
			clickHide: function (head) {
				head.next().toggle();
				head.toggleClass("cmty-hide-open");
				return false;
			}
		}
	}
}
