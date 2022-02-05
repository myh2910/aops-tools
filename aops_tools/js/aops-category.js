// Keys
const categoryKeys = [
	'category_id',
	'category_name',
	'category_type',
	'short_description'
];
const folderKeys = [
	'item_id',
	'item_subtitle',
	'item_text',
	'item_type',
];
const viewPostsKeys = [
	'category_id',
	'category_name',
	'post_canonical',
	'post_format',
	'post_id',
	'post_number',
	'post_rendered',
	'post_type',
	'poster_id',
	'topic_id',
	'username'
];

// Get category data from AoPS
const focusCategory = await scrollDown();
const categoryLink = 'https://artofproblemsolving.com/community/c';

// Write and return category data
let categoryData = {category_url: `${categoryLink}${focusCategory.category_id}`};
categoryKeys.forEach(key => categoryData[key] = focusCategory[key]);

switch (focusCategory.category_type) {
	case 'folder':
		categoryData.items = focusCategory.items.map(data => {
			let itemData = {item_url: `${categoryLink}${data.item_id}`};
			folderKeys.forEach(key => itemData[key] = data[key]);
			return itemData;
		});
		break;
	case 'view_posts':
		categoryData.items = focusCategory.items.map(data => {
			let postData = data.post_data;
			let itemData = {
				item_text: data.item_text,
				item_type: data.item_type,
				post_data: {}
			};
			viewPostsKeys.forEach(key => itemData.post_data[key] = postData[key]);
			if (postData.post_type === 'forum') {
				itemData.post_data.post_url = `${categoryLink}${postData.category_id}h${postData.topic_id}p${postData.post_id}`;
			}
			return itemData;
		});
		break;
}

return categoryData;

// Functions
async function scrollDown() {
	while (!getFocusCategory()) {
		await new Promise(resolve => setTimeout(resolve, 10));
	}
	if (!getFocusCategory().attributes.is_forum) {
		while (!getFocusCategory().attributes.no_more_items) {
			window.scrollTo(0, document.body.scrollHeight);
			await new Promise(resolve => requestAnimationFrame(resolve));
		}
	}
	return getFocusCategory().attributes;
}

function getFocusCategory() {
	return AoPS.Community.MasterModel.attributes.focus_category;
}
