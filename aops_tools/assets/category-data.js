// Keys
const category_keys = [
	"category_id",
	"category_name",
	"category_type",
	"short_description"
]

const post_keys = [
	"category_id",
	"category_name",
	"post_canonical",
	"post_format",
	"post_id",
	"post_number",
	"post_rendered",
	"post_type",
	"poster_id",
	"topic_id",
	"username"
]

// Get data from AoPS
const category_url = "https://artofproblemsolving.com/community/c";
const focus = await scrollDown();

// Write and return data
var data = {category_url: category_url + focus.category_id};
category_keys.forEach(key => data[key] = focus[key]);

if (!focus.is_forum) {
	data.items = focus.items.map(item_data => {
		let res = {item_text: item_data.item_text, item_type: item_data.item_type};
		if (item_data.item_type.startsWith("post")) {
			let post_data = item_data.post_data;
			res.post_data = {};
			post_keys.forEach(key => res.post_data[key] = post_data[key]);
			if (post_data.post_type == "forum") {
				res.post_data.post_url = category_url + post_data.category_id
					+ "h" + post_data.topic_id + "p" + post_data.post_id;
			}
		} else {
			res.item_id = item_data.item_id;
			res.item_subtitle = item_data.item_subtitle;
			res.item_url = category_url + item_data.item_id;
		}
		return res;
	});
}

return data;

// Scroll down until all posts are loaded
async function scrollDown() {
	let focus_category = focusCategory();
	while (!focus_category) {
		await sleep(50);
		focus_category = focusCategory();
	}
	if (!focus_category.attributes.is_forum) {
		while (!focus_category.attributes.no_more_items) {
			window.scrollTo(0, document.body.scrollHeight);
			await sleep(100);
			focus_category = focusCategory();
		}
	}
	return focus_category.attributes;
}

function focusCategory() {
	return AoPS.Community.MasterModel.attributes.focus_category;
}

// https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}
