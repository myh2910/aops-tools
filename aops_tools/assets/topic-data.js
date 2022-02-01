// Keys
const topic_keys = [
	"category_id",
	"category_name",
	"num_deleted",
	"num_posts",
	"num_views",
	"source",
	"tags",
	"topic_id",
	"topic_title"
]

const post_keys = [
	"last_edit_reason",
	"last_edit_time",
	"last_editor_username",
	"num_edits",
	"post_canonical",
	"post_format",
	"post_id",
	"post_number",
	"post_rendered",
	"post_time",
	"poster_id",
	"thankers",
	"thanks_received",
	"username"
]

// Get data from AoPS
const focus = await scrollDown();
const topic_url = "https://artofproblemsolving.com/community/"
	+ "c" + focus.category_id + "h" + focus.topic_id;

// Write and return data
var data = {
	posts_data: focus.posts.models.map(model => {
		let res = {post_url: topic_url + "p" + model.attributes.post_id};
		post_keys.forEach(key => res[key] = model.attributes[key]);
		return res;
	}),
	topic_url: topic_url
}
topic_keys.forEach(key => data[key] = focus[key]);
return data;

// Scroll down until all posts are loaded
async function scrollDown() {
	let focus_topic = focusTopic();
	while (!focus_topic) {
		await sleep(50);
		focus_topic = focusTopic();
	}
	if (!focus_topic.attributes.all_posts_fetched) {
		const scrollbar = await scrollBar(".cmty-postbox-inner-box");
		do {
			scrollbar.scrollTo(0, scrollbar.scrollHeight);
			await sleep(100);
			focus_topic = focusTopic();
		} while (!focus_topic.attributes.all_posts_fetched)
	}
	return focus_topic.attributes;
}

// https://stackoverflow.com/questions/16149431/make-function-wait-until-element-exists
async function scrollBar(selector) {
	while (document.querySelector(selector) === null) {
		await sleep(100);
	}
	return document.querySelector(selector).parentElement;
}

function focusTopic() {
	return AoPS.Community.MasterModel.attributes.focus_topic;
}

// https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}
