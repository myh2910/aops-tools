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

// Write posts data
topic_data.posts_data = topic_data.posts_data.map(function (post_data) {
	var res = {"post_url": topic_url + "p" + post_data.post_id};
	post_keys.forEach(key => {
		res[key] = post_data[key];
	})
	return res;
})

// Write topic data
var res = {"topic_url": topic_url};
topic_keys.forEach(key => {
	res[key] = topic_data[key];
})

// Return topic data
return res;
