<!DOCTYPE html>
<html lang="en">
<head>
  <title>{{title}}</title>
<meta charset="utf-8">
<meta name="language" content="english">
<meta name="viewport" content="width=device-width">

<link rel="stylesheet" href="/static/semantic/semantic.min.css" />

<style>
.mce-tinymce.mce-container.mce-panel {
    border: none;
}
.mce-edit-area.mce-container.mce-panel.mce-stack-layout-item
{
    border: none;
}
</style>

</head>
<body style="background-color:Gainsboro;">

<div id="app" class="ui container" style="background-color:Gainsboro;">

  <div class="ui center aligned basic segment">
	<div class="ui text">
		<h1 class="ui header"> [[ story_title ]] </h>
	</div>
  </div>

  <div class="ui horizontal menu">
    <div class="ui simple dropdown item">
	  Select story
	  <i class="dropdown icon"></i>
	  <div class="menu" style="overflow:auto; max-height: 50vh; max-width: 50vw;">
	    <a v-for="title in sortedTitles" v-on:click="click_select_story_item" class="item">[[title]]</a>
	    <a v-if="titles.length === 0" class="red item">Empty</a>
	  </div>
    </div>
    <a id="new_story_button" v-on:click="click_new_story_root" class="item">New story</a>
    <a v-if="story_selected" id="new_chapter_button" v-on:click="click_add_chapter_root" class="item">Add chapter</a>
    <a v-if="story_selected" id="delete_story_button" v-on:click="click_delete_story_root" class="right item">Delete story</a>
  </div>

  <!-- Modals-->
  <div v-on-clickaway="click_outside_new_story_modal" class="ui modal" v-bind:class="{ active: new_story_modal_is_active }" >
  
	<div class="header">Create a new story</div>
	<div class="ui content form">
		<p v-if="errors.length">
			<b> Please correct the following error(s):</b>
			<ul>
				<li v-for="error in errors">[[ error ]]</li>
			</ul>
		</p>
		<div class="field"> 
			<label>Enter story title:</label>
			<input type="text" name="story_name" v-model="story_name" placeholder="Title of the story">
		</div>
	</div>
	<div class="actions">
		<div v-on:click="click_new_story_modal_approve" class="ui approve button">Approve</div>
		<div v-on:click="click_new_story_modal_cancel" class="ui cancel button">Cancel</div>
	</div>

  </div>

  <div v-on-clickaway="click_outside_delete_story_modal" class="ui modal" v-bind:class="{ active: delete_story_modal_is_active }" >
  
	<div class="header">Are you sure you want to delete: [[this.story_title]]</div>
	<div class="actions">
		<div v-on:click="click_delete_story_modal_approve" class="ui approve button">Delete</div>
		<div v-on:click="click_delete_story_modal_cancel" class="ui cancel button">Cancel</div>
	</div>

  </div>

  <div v-on-clickaway="click_outside_new_chapter_modal" class="ui modal" v-bind:class="{ active: new_chapter_modal_is_active }" >
  
	<div class="header">Create a new chapter</div>
	<div class="ui content form">
		<p v-if="errors.length">
			<b> Please correct the following error(s):</b>
			<ul>
				<li v-for="error in errors">[[ error ]]</li>
			</ul>
		</p>
		<div class="field"> 
			<label>Enter chapter name:</label>
			<input type="text" name="chapter_name" v-model="chapter_name" placeholder="chapter name">
		</div>
	</div>
	<div class="actions">
		<div v-on:click="click_new_chapter_modal_approve" class="ui approve button">Create chapter</div>
		<div v-on:click="click_new_chapter_modal_cancel" class="ui cancel button">Cancel</div>
	</div>

  </div>


  <!-- Items -->

  <div class="ui divided selection list">
    <div v-for="chapter in chapters" class="item">
	  <div class="content">
	    <div v-on:click="click_select_chapter_item" class="header">[[chapter]]</div>
	  </div>
	</div>
  </div>

  <!-- Editors -->

  <div v-for="(e, index) in editors" class="ui container">
    <div class="ui top attached menu">
      <a class="item">[[e]]</a>
    </div>
    <form class="ui container">
		<input type="hidden" name="editor_name" :value="[[e]]"> 
		<editor v-model="content[index]" api-key="API_KEY" :init=
		"{
		menubar: false,
		plugins: ['wordcount','save'],
		toolbar: 'save',
		save_onsavecallback: save_editor_content,
		height : '50vh',
		resize: true,
		}"
		>
		</editor>
    </form>
	<div class="ui divider"></div>
  </div>

  <div v-if="editors.length" class="ui center aligned container">
	<button class="ui icon button" style="padding: 0; border: none; background: none;">
	  <i class="plus square outline massive icon"></i>
	</button>
  </div>


<!-- close container -->
</div> 

<!-- javascript -->


<script src="/static/vue.js"></script>
<script src="/static/vue-clickaway/dist/vue-clickaway.js"></script>
<script src="/static/axios/dist/axios.min.js"></script>
<script src="https://cloud.tinymce.com/stable/tinymce.min.js"></script>
<script src="/static/tinymce-vue.min.js"></script>

<script type = "text/javascript">

function reverse_escape_html(str) 
{
    var textArea = document.createElement('textarea');
	textArea.innerHTML = str;
	return textArea.value;
}

var app = new Vue({
  el: '#app',
  mixins: [VueClickaway.mixin],
  components: {
    'editor': Editor
  },
  data: {
    titles : [ 
	% for title in titles: 
		"{{title}}",
	% end	
	],
	chapters : [],
	story_selected : false,
	editors: [],
    story_title : "Name of the story",
	new_story_modal_is_active : false,
	new_chapter_modal_is_active : false,
	delete_story_modal_is_active : false,
	errors : [],
	story_name : null,
	chapter_name : null,
	content: [],
  },

  methods: {
	save_editor_content: function(event)
	{
		console.log(event.formElement[0].value)
		content_index = this.editors.indexOf(event.formElement[0].value)

		console.log(this.content[content_index])
		axios.post('/save', 
		{
			story_name: title,
			category: 'chapters',
			item_name: event.formElement[0].value,
			content: this.content[content_index],
		})
		.then(response => 
		{
			console.log("save succesful")
		})
		.catch(error => 
		{
			alert(error.response.data)
		})
	},

	click_new_story_root : function(event)
	{
		this.new_story_modal_is_active = !this.new_story_modal_is_active
		this.errors = []
	},
	click_delete_story_root : function(event)
	{
		this.delete_story_modal_is_active = !this.delete_story_modal_is_active
	},
	
	click_select_story_item : function(event)
	{
		title = reverse_escape_html(event.srcElement.innerHTML)
		axios.post('get_items', 
		{
			story_name: title,
			category: 'chapters',
		})
		.then(response => 
		{
			this.story_title = title
			this.editors = []
			this. content = []
			this.story_selected = true
			this.chapters = response.data
		})
		.catch(error => 
		{
			console.log(error.response.data)
		})
	},
	click_select_chapter_item : function(event)
	{
		chapter_name = reverse_escape_html(event.srcElement.innerHTML)
		axios.post('get_item', 
		{
			story_name: this.story_title,
			category: 'chapters',
			item_name: chapter_name
		})
		.then(response => 
		{
			if(this.editors.includes(chapter_name) == false)
			{	

				this.editors.push(chapter_name)
				this.content.push(response.data)
			}
		})
		.catch(error => 
		{
			console.log(error.response.data)
		})
	},
	click_add_chapter_root : function(event)
	{
		this.new_chapter_modal_is_active = !this.new_chapter_modal_is_active
		this.errors = []
	},

	click_new_story_modal_approve : function(event)
	{
		axios.post('/new_story', 
		{
			story_name: this.story_name
		})
		.then(response => 
		{
			this.new_story_modal_is_active = false
			this.story_title = this.story_name
			this.errors = []
			this.titles.push(this.story_name)
			this.story_selected = true
			this.story_name = null
			this.chapters = []

			this.editors = []
			this.content = []
		})
		.catch(error => 
		{
			this.errors = error.response.data
		})
	},
	click_new_chapter_modal_approve : function(event)
	{
		axios.post('/new_item', 
		{
			story_name: this.story_title,
			category: 'chapters',
			item_name: this.chapter_name
		})
		.then(response => 
		{
			this.new_chapter_modal_is_active = false
			this.errors = []
			this.chapters.push(this.chapter_name)

			this.editors.push(this.chapter_name)
			this.content.push("")

			this.chapter_name = null

			
		})
		.catch(error => 
		{
			this.errors = error.response.data
		})
	},
	click_delete_story_modal_approve : function(event)
	{
		axios.post('/delete', 
		{
			story_name: this.story_title
		})
		.then(response => 
		{
			this.delete_story_modal_is_active = false
			escaped_titles = this.titles.map(reverse_escape_html)
			Vue.delete(this.titles, escaped_titles.indexOf(this.story_title))
			this.story_title = "Name of the story"
			this.story_selected = false
			this.chapters = []

			this.editors = []
			this.content = []
		})
	},

	click_new_story_modal_cancel : function(event)
	{
		this.new_story_modal_is_active = false
	},
	click_new_chapter_modal_cancel : function(event)
	{
		this.new_chapter_modal_is_active = false
	},
	click_delete_story_modal_cancel : function(event)
	{
		this.delete_story_modal_is_active = false
	},

	click_outside_new_story_modal : function(event)
	{
		if(event.srcElement.id !== "new_story_button" && this.new_story_modal_is_active)
		{
			this.new_story_modal_is_active = false
			this.errors = []
		}
	},
	click_outside_new_chapter_modal : function(event)
	{
		if(event.srcElement.id !== "new_chapter_button" && this.new_chapter_modal_is_active)
		{
			this.new_chapter_modal_is_active = false
			this.errors = []
		}
	},
	click_outside_delete_story_modal : function(event)
	{
		if(event.srcElement.id !== "delete_story_button" && this.delete_story_modal_is_active)
		{
			this.delete_story_modal_is_active = false
		}
	},
  },
  computed: 
  {
	sortedTitles: function() 
	{
		function compare(a, b) 
		{
			au = a.toUpperCase()
			bu = b.toUpperCase()
			if (au < bu)
				return -1;
			if (au > bu)
				return 1;
			return 0;
		}
	var tmp = this.titles.map(reverse_escape_html)

    return tmp.sort(compare);
	}
  },
  delimiters: ['[[',']]']
})

</script>

</body>
</html>
