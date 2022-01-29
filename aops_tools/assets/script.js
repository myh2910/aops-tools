// Keys
const topic_keys = [
	"category_id",
	"num_posts",
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
var topic_url = "https://artofproblemsolving.com/community/";
topic_url += "c" + topic_data.category_id + "h" + topic_data.topic_id;
const num_posts = topic_data.num_posts;

// Write posts data
if (num_posts > 30) {
	const scrollbar = await scrollBar(".cmty-postbox-inner-box");
	const models = await scrollDown(scrollbar);
	topic_data.posts_data = models.map(model => {
		let attributes = model.attributes;
		let res = {"post_url": topic_url + "p" + attributes.post_id};
		post_keys.forEach(key => res[key] = attributes[key]);
		return res;
	});
} else {
	topic_data.posts_data = topic_data.posts_data.map(post_data => {
		let res = {"post_url": topic_url + "p" + post_data.post_id};
		post_keys.forEach(key => res[key] = post_data[key]);
		return res;
	});
}

// Write and return topic data
let res = {"topic_url": topic_url};
topic_keys.forEach(key => res[key] = topic_data[key]);
return res;

// Get scrollbar
// https://stackoverflow.com/questions/16149431/make-function-wait-until-element-exists/47776379/
async function scrollBar(selector) {
	while (document.querySelector(selector) === null) {
		await new Promise(resolve => requestAnimationFrame(resolve));
	}
	return document.querySelector(selector).parentElement;
}

// Scroll down until all posts are loaded
async function scrollDown(scrollbar) {
	let models = getModels();
	while (true) {
		if (models.length === num_posts) {
			return models;
		}
		scrollbar.scrollTo(0, scrollbar.scrollHeight);
		await sleep(1000);
		models = getModels();
	}
}

// Get models object
function getModels() {
	let byId = AoPS.bootstrap_data.preload_cmty_data.topic_data.master.attributes.focus_topic.attributes.posts._byId;
	return byId[Object.keys(byId)[0]].collection.models;
}

// Time sleep
// https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}
