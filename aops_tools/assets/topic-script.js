// Keys
const topicKeys = [
	'category_id',
	'category_name',
	'num_deleted',
	'num_posts',
	'num_views',
	'source',
	'tags',
	'topic_id',
	'topic_title'
];
const postKeys = [
	'last_edit_reason',
	'last_edit_time',
	'last_editor_username',
	'num_edits',
	'post_canonical',
	'post_format',
	'post_id',
	'post_number',
	'post_rendered',
	'post_time',
	'poster_id',
	'thankers',
	'thanks_received',
	'username'
];

// Get topic data from AoPS
const focusTopic = await scrollDown();
const topicLink = `https://artofproblemsolving.com/community/c${focusTopic.category_id}h${focusTopic.topic_id}`;

// Write and return topic data
let topicData = {
	posts_data: focusTopic.posts.models.map(model => {
		let postData = {post_url: `${topicLink}p${model.attributes.post_id}`};
		postKeys.forEach(key => postData[key] = model.attributes[key]);
		return postData;
	}),
	topic_url: topicLink
};
topicKeys.forEach(key => topicData[key] = focusTopic[key]);
return topicData;

// Functions
async function scrollDown() {
	while (!getFocusTopic()) {
		await new Promise(resolve => setTimeout(resolve, 10));
	}
	if (!getFocusTopic().attributes.all_posts_fetched) {
		const selector = '.cmty-postbox-inner-box';
		while (document.querySelector(selector) === null) {
			await new Promise(resolve => setTimeout(resolve, 10));
		}
		const scrollBar = document.querySelector(selector).parentElement;
		do {
			scrollBar.scrollTo(0, scrollBar.scrollHeight);
			await new Promise(resolve => requestAnimationFrame(resolve));
		} while (!getFocusTopic().attributes.all_posts_fetched)
	}
	return getFocusTopic().attributes;
}

function getFocusTopic() {
	return AoPS.Community.MasterModel.attributes.focus_topic;
}
