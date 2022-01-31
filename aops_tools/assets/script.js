// Keys
const topic_keys = [
	"category_id",
	"category_name",
	"num_deleted",
	"num_posts",
	"num_views",
	"posts_data",
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
var topic_data = AoPS.bootstrap_data.preload_cmty_data.topic_data;
const topic_url = "https://artofproblemsolving.com/community/"
	+ "c" + topic_data.category_id + "h" + topic_data.topic_id;
const posts_data = topic_data.posts_data;
const num_posts = topic_data.num_posts;

// Write posts data
if (posts_data.length === num_posts) {
	topic_data.posts_data = posts_data.map(attrs => {
		let res = {"post_url": topic_url + "p" + attrs.post_id};
		post_keys.forEach(key => res[key] = attrs[key]);
		return res;
	});
} else {
	const models = await scrollDown();
	topic_data.posts_data = models.map(model => {
		let attrs = model.attributes;
		let res = {"post_url": topic_url + "p" + attrs.post_id};
		post_keys.forEach(key => res[key] = attrs[key]);
		return res;
	});
}

// Write and return topic data
let res = {"topic_url": topic_url};
topic_keys.forEach(key => res[key] = topic_data[key]);
return res;

// Scroll down until all posts are loaded
async function scrollDown() {
	const scrollbar = await scrollBar(".cmty-postbox-inner-box");
	let models = getModels();
	while (models.length < num_posts) {
		scrollbar.scrollTo(0, scrollbar.scrollHeight);
		await sleep(100);
		models = getModels();
	}
	return models;
}

// Get scrollbar
// https://stackoverflow.com/questions/16149431/make-function-wait-until-element-exists
async function scrollBar(selector) {
	while (document.querySelector(selector) === null) {
		await new Promise(resolve => requestAnimationFrame(resolve));
	}
	return document.querySelector(selector).parentElement;
}

// Get models object, possibly located at
// ...master.attributes.focus_topic.attributes.posts.models
function getModels() {
	return AoPS.Community.MasterModel.attributes.focus_topic.attributes.posts.models;
}

// Time sleep
// https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}
